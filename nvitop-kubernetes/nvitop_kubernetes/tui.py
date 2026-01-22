# This file is part of nvitop-kubernetes, Kubernetes integration for nvitop.
# License: Apache-2.0 AND GPL-3.0-only

"""TUI integration module for Kubernetes support in nvitop."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from nvitop.api import NA, NaType
from nvitop.tui.library.process import GpuProcess as GpuProcessBase

from nvitop_kubernetes.kubernetes import KubernetesInfo, get_kubernetes_info


if TYPE_CHECKING:
    from nvitop.api import Snapshot
    from nvitop.tui.library.device import Device


__all__ = ['KubernetesGpuProcess', 'patch_device']


class KubernetesGpuProcess(GpuProcessBase):
    """GPU Process with Kubernetes integration.

    This class extends the base GpuProcess to include Kubernetes pod information
    in the process command line, as recommended by the nvitop maintainer.

    The pod information is prepended to the command line in the format:
    [pod-name/namespace] original-command
    """

    _kubernetes_info: KubernetesInfo | None

    def __new__(cls, *args: Any, **kwargs: Any) -> KubernetesGpuProcess:
        """Create a new KubernetesGpuProcess instance."""
        instance = super().__new__(cls, *args, **kwargs)
        instance._kubernetes_info = None
        return instance

    def _get_kubernetes_info(self) -> KubernetesInfo:
        """Get cached Kubernetes information for this process."""
        if self._kubernetes_info is None:
            try:
                self._kubernetes_info = get_kubernetes_info(self.pid)
            except (ImportError, OSError, KeyError, ValueError):
                self._kubernetes_info = KubernetesInfo(
                    pod_name=NA,
                    pod_namespace=NA,
                    pod_uid=NA,
                    container_name=NA,
                    container_id=NA,
                    node_name=NA,
                    metadata={},
                )
        return self._kubernetes_info

    @property
    def pod_name(self) -> str | NaType:
        """Get the Kubernetes pod name if running in a pod."""
        return self._get_kubernetes_info().pod_name

    @property
    def pod_namespace(self) -> str | NaType:
        """Get the Kubernetes pod namespace if running in a pod."""
        return self._get_kubernetes_info().pod_namespace

    @property
    def pod_uid(self) -> str | NaType:
        """Get the Kubernetes pod UID if running in a pod."""
        return self._get_kubernetes_info().pod_uid

    @property
    def container_name(self) -> str | NaType:
        """Get the container name if running in a container."""
        return self._get_kubernetes_info().container_name

    @property
    def container_id(self) -> str | NaType:
        """Get the container ID if running in a container."""
        return self._get_kubernetes_info().container_id

    @property
    def node_name(self) -> str | NaType:
        """Get the Kubernetes node name if running in a pod."""
        return self._get_kubernetes_info().node_name

    @property
    def pod_labels(self) -> dict[str, str] | NaType:
        """Get the Kubernetes pod labels if running in a pod."""
        return self._get_kubernetes_info().pod_labels

    @property
    def nvidia_gpu_requests(self) -> int | NaType:
        """Get the number of NVIDIA GPUs requested by this process's container."""
        return self._get_kubernetes_info().nvidia_gpu_requests

    @property
    def nvidia_gpu_limits(self) -> int | NaType:
        """Get the number of NVIDIA GPUs limited to this process's container."""
        return self._get_kubernetes_info().nvidia_gpu_limits

    def command(self) -> str:
        """Return the command with Kubernetes pod info prepended.

        If the process is running in a Kubernetes pod, the command will be
        prefixed with [pod-name/namespace]. Otherwise, returns the original command.
        """
        original_command = super().command()

        pod_name = self.pod_name
        pod_namespace = self.pod_namespace

        if pod_name is not NA and pod_name not in ('N/A', '', None):
            namespace = pod_namespace if pod_namespace is not NA else 'default'
            return f'[{pod_name}/{namespace}] {original_command}'

        return original_command

    def as_snapshot(
        self,
        *,
        host_process_snapshot_cache: dict[int, Snapshot] | None = None,
    ) -> Snapshot:
        """Return a snapshot with Kubernetes info included."""
        snapshot = super().as_snapshot(host_process_snapshot_cache=host_process_snapshot_cache)

        # Add Kubernetes info to snapshot for potential use
        k8s_info = self._get_kubernetes_info()
        snapshot.pod_name = k8s_info.pod_name
        snapshot.pod_namespace = k8s_info.pod_namespace
        snapshot.pod_uid = k8s_info.pod_uid
        snapshot.container_name = k8s_info.container_name
        snapshot.container_id = k8s_info.container_id
        snapshot.node_name = k8s_info.node_name

        return snapshot


def patch_device(device_class: type[Device]) -> None:
    """Patch a Device class to use KubernetesGpuProcess.

    This function sets the GPU_PROCESS_CLASS attribute of the given Device class
    to use KubernetesGpuProcess, enabling Kubernetes integration.

    Args:
        device_class: The Device class to patch (e.g., nvitop.tui.library.Device)

    Example:
        >>> from nvitop.tui.library import Device
        >>> from nvitop_kubernetes import patch_device
        >>> patch_device(Device)
    """
    device_class.GPU_PROCESS_CLASS = KubernetesGpuProcess
