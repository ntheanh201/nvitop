# This file is part of nvitop-kubernetes, Kubernetes integration for nvitop.
# License: Apache-2.0 AND GPL-3.0-only

"""Kubernetes integration module for nvitop."""

from __future__ import annotations

from nvitop_kubernetes.kubernetes import (
    KUBERNETES_AVAILABLE,
    KubernetesClient,
    KubernetesError,
    KubernetesInfo,
    extract_pod_from_pid,
    get_kubernetes_client,
    get_kubernetes_info,
    is_kubernetes_environment,
)
from nvitop_kubernetes.tui import KubernetesGpuProcess, patch_device
from nvitop_kubernetes.version import __version__


__all__ = [
    '__version__',
    'KUBERNETES_AVAILABLE',
    'KubernetesClient',
    'KubernetesError',
    'KubernetesInfo',
    'KubernetesGpuProcess',
    'extract_pod_from_pid',
    'get_kubernetes_client',
    'get_kubernetes_info',
    'is_kubernetes_environment',
    'patch_device',
]
