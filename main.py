
import socket


def get_network_info():
    print("\n=== NETWORK INFORMATION ===")

    hostname = socket.gethostname()
    print(f"Computer name: {hostname}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("1.1.1.1", 80))
            ip_address = s.getsockname()[0]

        print(f"Local IP address: {ip_address}")

    except OSError:
        print("Unable to detect local IP address.")


def check_ports():
    print("\n=== LOCAL PORT SCANNER ===")

    ports = [22, 80, 443, 3000, 5000, 8000, 8080]

    for port in ports:
        try:
            with socket.create_connection(
                ("127.0.0.1", port), timeout=0.5
            ):
                print(f"Port {port}: OPEN")

        except OSError:
            print(f"Port {port}: CLOSED or unavailable")


def main():
    print("Welcome to NetGuard!")

    get_network_info()
    check_ports()

    print("\nNetGuard scan completed!")


if __name__ == "__main__":
    main()
