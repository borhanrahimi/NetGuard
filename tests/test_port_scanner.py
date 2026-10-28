import socket

import pytest

from netguard.port_scanner import (
    PortState,
    check_port,
    lookup_service,
    parse_ports,
    scan_ports,
)


@pytest.fixture
def listening_port():
    """A real TCP port on localhost that accepts connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))  # port 0 lets the OS pick a free port
        server.listen()
        yield server.getsockname()[1]


@pytest.fixture
def closed_port():
    """A localhost port that was free a moment ago, so nothing is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestParsePorts:
    def test_single_port(self):
        assert parse_ports("22") == [22]

    def test_list(self):
        assert parse_ports("443,22,80") == [22, 80, 443]

    def test_range(self):
        assert parse_ports("8000-8003") == [8000, 8001, 8002, 8003]

    def test_mixed_with_duplicates_and_spaces(self):
        assert parse_ports(" 80, 79-81 ,80 ") == [79, 80, 81]

    def test_full_range(self):
        assert len(parse_ports("1-65535")) == 65535

    @pytest.mark.parametrize(
        "spec", ["", ",", "abc", "80-", "-80", "0", "65536", "100-90", "1-2-3"]
    )
    def test_invalid(self, spec):
        with pytest.raises(ValueError):
            parse_ports(spec)


class TestLookupService:
    def test_common_port(self):
        assert lookup_service(22) == "ssh"
        assert lookup_service(443) == "https"

    def test_unknown_port(self, monkeypatch):
        def not_found(port, proto):
            raise OSError("port/proto not found")

        monkeypatch.setattr(socket, "getservbyport", not_found)
        assert lookup_service(54321) is None


class TestCheckPort:
    def test_open(self, listening_port):
        result = check_port("127.0.0.1", listening_port)
        assert result.port == listening_port
        assert result.state == PortState.OPEN

    def test_closed(self, closed_port):
        assert check_port("127.0.0.1", closed_port).state == PortState.CLOSED

    def test_filtered_on_timeout(self, monkeypatch):
        def time_out(address, timeout):
            raise TimeoutError

        monkeypatch.setattr(socket, "create_connection", time_out)
        assert check_port("127.0.0.1", 80).state == PortState.FILTERED

    def test_includes_service_name(self, monkeypatch):
        def refuse(address, timeout):
            raise ConnectionRefusedError

        monkeypatch.setattr(socket, "create_connection", refuse)
        assert check_port("127.0.0.1", 22).service == "ssh"


class TestScanPorts:
    def test_results_keep_port_order(self, listening_port, closed_port):
        ports = sorted([listening_port, closed_port])
        results = scan_ports("127.0.0.1", ports, workers=4)

        assert [r.port for r in results] == ports
        states = {r.port: r.state for r in results}
        assert states[listening_port] == PortState.OPEN
        assert states[closed_port] == PortState.CLOSED

    def test_empty_port_list(self):
        assert scan_ports("127.0.0.1", []) == []
