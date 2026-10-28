import pytest

from netguard import cli
from netguard.host_info import HostInfo
from netguard.port_scanner import PortResult, PortState


@pytest.fixture
def fake_scan(monkeypatch):
    """Replace the real scanner and record how it was called."""
    calls = []

    def scan_ports(host, ports, timeout, workers):
        calls.append({"host": host, "ports": ports, "timeout": timeout, "workers": workers})
        return [
            PortResult(22, PortState.OPEN, "ssh"),
            PortResult(80, PortState.CLOSED, "http"),
            PortResult(81, PortState.FILTERED, None),
        ]

    monkeypatch.setattr(cli, "scan_ports", scan_ports)
    return calls


def test_no_command_prints_help(capsys):
    assert cli.main([]) == 1
    assert "usage: netguard" in capsys.readouterr().out


def test_info(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_host_info", lambda: HostInfo("my-laptop", "192.168.1.43"))

    assert cli.main(["info"]) == 0
    out = capsys.readouterr().out
    assert "my-laptop" in out
    assert "192.168.1.43" in out


def test_info_without_ip(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_host_info", lambda: HostInfo("my-laptop", None))

    assert cli.main(["info"]) == 0
    assert "Unable to detect local IP address." in capsys.readouterr().out


def test_scan_passes_options_to_scanner(fake_scan):
    cli.main(["scan", "--host", "127.0.0.1", "-p", "20-22,80", "--timeout", "1", "--workers", "5"])

    assert fake_scan == [
        {"host": "127.0.0.1", "ports": [20, 21, 22, 80], "timeout": 1.0, "workers": 5}
    ]


def test_scan_shows_only_open_ports_by_default(fake_scan, capsys):
    assert cli.main(["scan"]) == 0
    out = capsys.readouterr().out
    assert "22      open      ssh" in out
    assert "closed  " not in out
    assert "1 open, 1 closed, 1 filtered" in out


def test_scan_all_shows_every_port(fake_scan, capsys):
    cli.main(["scan", "--all"])
    out = capsys.readouterr().out
    assert "80      closed    http" in out
    assert "81      filtered  unknown" in out


@pytest.mark.parametrize(
    "args",
    [
        ["scan", "--ports", "70000"],
        ["scan", "--ports", "abc"],
        ["scan", "--timeout", "0"],
        ["scan", "--workers", "0"],
    ],
)
def test_scan_rejects_bad_options(args, fake_scan):
    with pytest.raises(SystemExit) as exc:
        cli.main(args)
    assert exc.value.code == 2
    assert fake_scan == []


def test_scan_unresolvable_host(fake_scan, capsys):
    assert cli.main(["scan", "--host", "no-such-host.invalid"]) == 2
    assert "could not resolve host" in capsys.readouterr().err
    assert fake_scan == []
