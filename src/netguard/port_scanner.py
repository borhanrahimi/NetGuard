import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum

DEFAULT_PORTS = [22, 80, 443, 3000, 5000, 8000, 8080]
DEFAULT_TIMEOUT = 0.5
DEFAULT_WORKERS = 100

MIN_PORT = 1
MAX_PORT = 65535

# Names for common ports, checked before the OS services database so results
# are the same on every platform.
COMMON_SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    445: "smb",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-alt",
    27017: "mongodb",
}


class PortState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"


@dataclass
class PortResult:
    port: int
    state: PortState
    service: str | None = None


def parse_ports(spec: str) -> list[int]:
    """Turn a spec like "22,80,8000-8010" into a sorted list of unique ports."""
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                start_text, end_text = part.split("-", 1)
                start, end = int(start_text), int(end_text)
            else:
                start = end = int(part)
        except ValueError:
            raise ValueError(f"invalid port or range: {part!r}") from None

        if start > end:
            raise ValueError(f"range start is greater than end: {part!r}")
        if start < MIN_PORT or end > MAX_PORT:
            raise ValueError(f"ports must be between {MIN_PORT} and {MAX_PORT}: {part!r}")
        ports.update(range(start, end + 1))

    if not ports:
        raise ValueError("no ports given")
    return sorted(ports)


def lookup_service(port: int) -> str | None:
    """Return the usual service name for a TCP port, if one is known."""
    if port in COMMON_SERVICES:
        return COMMON_SERVICES[port]
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return None


def check_port(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> PortResult:
    """Try a TCP connection to host:port and classify the port's state."""
    service = lookup_service(port)
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortResult(port=port, state=PortState.OPEN, service=service)
    except ConnectionRefusedError:
        # The host actively rejected us: reachable, but nothing listening.
        return PortResult(port=port, state=PortState.CLOSED, service=service)
    except OSError:
        # Timeouts and unreachable errors: something (usually a firewall)
        # is dropping our traffic.
        return PortResult(port=port, state=PortState.FILTERED, service=service)


def scan_ports(
    host: str,
    ports: list[int],
    timeout: float = DEFAULT_TIMEOUT,
    workers: int = DEFAULT_WORKERS,
) -> list[PortResult]:
    """Check many ports at once using a thread pool; results keep port order."""
    if not ports:
        return []
    # Port checks spend almost all their time waiting on the network, so
    # threads give a big speedup despite the GIL.
    with ThreadPoolExecutor(max_workers=min(workers, len(ports))) as pool:
        return list(pool.map(lambda port: check_port(host, port, timeout), ports))
