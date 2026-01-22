# nvitop-kubernetes

Kubernetes integration for [nvitop](https://github.com/XuehaiPan/nvitop) - the interactive NVIDIA-GPU process viewer.

## Installation

```bash
pip install nvitop-kubernetes
```

Or install nvitop with kubernetes extra:

```bash
pip install nvitop[kubernetes]
```

## Usage

### Automatic Patching (Recommended)

The easiest way to enable Kubernetes integration is to patch the Device class before running nvitop:

```python
from nvitop.tui.library import Device
from nvitop_kubernetes import patch_device

# Enable Kubernetes integration
patch_device(Device)

# Now run nvitop as usual
from nvitop.cli import main
main()
```

### Manual Usage

You can also use the `KubernetesGpuProcess` class directly:

```python
from nvitop_kubernetes import KubernetesGpuProcess

# Get Kubernetes info for a process
process = KubernetesGpuProcess(pid=12345, device=my_device)
print(process.pod_name)
print(process.pod_namespace)
print(process.command())  # Will include [pod-name/namespace] prefix
```

## Features

When running in a Kubernetes environment, nvitop-kubernetes will:

- Detect pod information from process cgroups
- Prepend pod name and namespace to process command lines: `[pod-name/namespace] original-command`
- Support both in-cluster and kubeconfig-based authentication

## Requirements

- nvitop >= 1.0.0
- kubernetes >= 28.0.0, < 35.0.0
- Access to Kubernetes API (via kubeconfig or in-cluster service account)

## License

Apache-2.0 AND GPL-3.0-only
