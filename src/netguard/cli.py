import argparse
import socket
import sys
import time

from netguard import __version__
from netguard.host_info import HostInfo, get_host_info
from netguard.port_scanner import (
    DEFAULT_PORTS,
    DEFAULT_TIMEOUT,
    DEFAULT_WORKERS,
    PortResult,
    PortState,
    parse_ports,
    scan_ports,
)


def print_host_info(info: HostInfo) -> None:
    print("=== NETWORK INFORMATION ===")
    print(f"Computer name: {info.hostname}")
    if info.local_ip:
        print(f"Local IP address: {info.local_ip}")
    else:
        print("Unable to detect local IP address.")


def print_port_results(results: list[PortResult], show_all: bool) -> None:
    shown = results if show_all else [r for r in results if r.state == PortState.OPEN]
    if not shown:
        print("No open ports found.")
        return

    print(f"{'PORT':<8}{'STATE':<10}SERVICE")
    for result in shown:
        print(f"{result.port:<8}{result.state.value:<10}{result.service or 'unknown'}")


def print_scan_summary(results: list[PortResult], elapsed: float) -> None:
    counts = {state: 0 for state in PortState}
    for result in results:
        counts[result.state] += 1
    summary = ", ".join(f"{counts[state]} {state.value}" for state in PortState)
    print(f"\nScanned {len(results)} ports in {elapsed:.2f}s: {summary}")


def port_list(value: str) -> list[int]:
    """argparse type for --ports, so bad input becomes a clean usage error."""
    try:
        return parse_ports(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return number


def cmd_info(args: argparse.Namespace) -> int:
    print_host_info(get_host_info())
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    try:
        # Resolve once up front instead of once per port.
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Error: could not resolve host {args.host!r}", file=sys.stderr)
        return 2

    target = args.host if ip == args.host else f"{args.host} ({ip})"
    print(f"Scanning {target}: {len(args.ports)} ports\n")

    start = time.perf_counter()
    results = scan_ports(ip, args.ports, timeout=args.timeout, workers=args.workers)
    elapsed = time.perf_counter() - start

    print_port_results(results, show_all=args.all)
    print_scan_summary(results, elapsed)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="netguard",
        description="Lightweight network monitoring and security tool.",
        epilog="Only scan networks you own or have permission to test.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    info = subparsers.add_parser("info", help="show this computer's hostname and local IP")
    info.set_defaults(func=cmd_info)

    scan = subparsers.add_parser("scan", help="scan TCP ports on a host")
    scan.add_argument(
        "--host", default="127.0.0.1", help="host name or IP to scan (default: %(default)s)"
    )
    scan.add_argument(
        "-p",
        "--ports",
        type=port_list,
        default=DEFAULT_PORTS,
        help='ports to scan, e.g. "22,80,443" or "1-1024" (default: a few common ports)',
    )
    scan.add_argument(
        "--timeout",
        type=positive_float,
        default=DEFAULT_TIMEOUT,
        help="seconds to wait per port (default: %(default)s)",
    )
    scan.add_argument(
        "--workers",
        type=positive_int,
        default=DEFAULT_WORKERS,
        help="number of ports to check at the same time (default: %(default)s)",
    )
    scan.add_argument(
        "-a", "--all", action="store_true", help="also list closed and filtered ports"
    )
    scan.set_defaults(func=cmd_scan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
