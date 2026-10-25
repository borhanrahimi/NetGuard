import socket
from dataclasses import dataclass


@dataclass
class HostInfo:
    hostname: str
    local_ip: str | None


def get_local_ip() -> str | None:
    """Return the IP address this machine uses for outbound traffic."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # A UDP "connect" sends no packets; it only picks a network route.
            s.connect(("1.1.1.1", 80))
            return s.getsockname()[0]
    except OSError:
        return None


def get_host_info() -> HostInfo:
    return HostInfo(hostname=socket.gethostname(), local_ip=get_local_ip())
