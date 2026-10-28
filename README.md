# NetGuard

A lightweight network monitoring and security tool for home and small-office networks, built with Python.

NetGuard's goal is to answer three questions: **What is on my network? What changed? Is anything exposed that shouldn't be?**

> **Status:** early development. See the [roadmap](docs/ROADMAP.md).

## Current Features

- Show the computer's hostname and local IP address
- Scan any TCP ports or port ranges on a host (`--ports 1-1024`)
- Classify ports as open, closed, or filtered
- Fast concurrent scanning with a thread pool
- Service name lookup (22 → ssh, 443 → https)

## Planned Features

- Discover devices on the local network
- Baseline the network and detect changes (new devices, newly opened ports)
- Flag risky exposed services
- Scan history and continuous monitoring
- Web dashboard (FastAPI + React)

## Getting Started

Requires Python 3.10+.

```bash
git clone https://github.com/borhanrahimi/NetGuard.git
cd NetGuard
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
netguard info                              # hostname and local IP
netguard scan                              # a few common ports on localhost
netguard scan --host 192.168.1.1 -p 1-1024 # a port range on another host
netguard scan -p 22,80,443 --all           # also list closed / filtered ports
netguard scan --help                       # all options
```

Example output:

```
$ netguard info
=== NETWORK INFORMATION ===
Computer name: my-laptop.lan
Local IP address: 192.168.1.43

$ netguard scan -p 1-1024
Scanning 127.0.0.1: 1024 ports

PORT    STATE     SERVICE
22      open      ssh
80      open      http

Scanned 1024 ports in 0.38s: 2 open, 1022 closed, 0 filtered
```

| Option | Default | Description |
|---|---|---|
| `--host` | `127.0.0.1` | Host name or IP address to scan |
| `-p`, `--ports` | a few common ports | Ports to scan, e.g. `22,80,443` or `1-1024` |
| `--timeout` | `0.5` | Seconds to wait for each port |
| `--workers` | `100` | Number of ports checked at the same time |
| `-a`, `--all` | off | Also list closed and filtered ports |

## Development

```bash
pytest          # run the tests
ruff check .    # lint
ruff format .   # format
```

## Project Structure

```
netguard/
├── pyproject.toml          # package metadata and dependencies
├── src/netguard/
│   ├── cli.py              # command-line entry point
│   ├── host_info.py        # hostname and local IP detection
│   └── port_scanner.py     # TCP port scanning
├── tests/                  # unit tests
└── docs/                   # roadmap, architecture, case study
```

## Documentation

- [Roadmap](docs/ROADMAP.md): phases and progress
- [Architecture](docs/ARCHITECTURE.md): design, components, and key decisions
- [Case Study](docs/CASE_STUDY.md): the problem, approach, and lessons learned

## Responsible Use

NetGuard is intended **only for networks you own or have explicit permission to test**. Unauthorized scanning may be illegal in your jurisdiction.
