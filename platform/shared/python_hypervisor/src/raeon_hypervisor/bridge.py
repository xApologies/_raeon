from .hypervisor import Hypervisor


def open(horizon_adapter, config):
    """Return a local byte bridge. Creates no listener and grants no actor authority."""
    return Hypervisor(horizon_adapter, config)
