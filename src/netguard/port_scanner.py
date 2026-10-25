import socket
from dataclasses import dataclass
from enum import Enum

DEFAULT_PORTS = [22, 80, 443, 3000, 5000, 8000, 8080]


class PortState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"


@dataclass
class PortResult:
    port: int
    state: PortState


def check_port(host: str, port: int, timeout: float = 0.5) -> PortResult:
    """Try a TCP connection to host:port and classify the port's state."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortResult(port=port, state=PortState.OPEN)
    except ConnectionRefusedError:
        # The host actively rejected us: reachable, but nothing listening.
        return PortResult(port=port, state=PortState.CLOSED)
    except OSError:
        # Timeouts and unreachable errors: something (usually a firewall)
        # is dropping our traffic.
        return PortResult(port=port, state=PortState.FILTERED)


def scan_ports(host: str, ports: list[int], timeout: float = 0.5) -> list[PortResult]:
    return [check_port(host, port, timeout) for port in ports]
