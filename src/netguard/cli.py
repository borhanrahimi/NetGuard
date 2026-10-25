from netguard.host_info import HostInfo, get_host_info
from netguard.port_scanner import DEFAULT_PORTS, PortResult, scan_ports


def print_host_info(info: HostInfo) -> None:
    print("\n=== NETWORK INFORMATION ===")
    print(f"Computer name: {info.hostname}")
    if info.local_ip:
        print(f"Local IP address: {info.local_ip}")
    else:
        print("Unable to detect local IP address.")


def print_port_results(results: list[PortResult]) -> None:
    print("\n=== LOCAL PORT SCANNER ===")
    for result in results:
        print(f"Port {result.port}: {result.state.value.upper()}")


def main() -> None:
    print("Welcome to NetGuard!")

    print_host_info(get_host_info())
    print_port_results(scan_ports("127.0.0.1", DEFAULT_PORTS))

    print("\nNetGuard scan completed!")
