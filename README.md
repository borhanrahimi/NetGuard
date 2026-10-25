# NetGuard

A lightweight network monitoring and security tool for home and small-office networks, built with Python.

NetGuard's goal is to answer three questions: **What is on my network? What changed? Is anything exposed that shouldn't be?**

> **Status:** early development. See the [roadmap](docs/ROADMAP.md).

## Current Features

- Detect computer hostname
- Identify local IP address
- Scan TCP ports and classify them as open, closed, or filtered
- Display scan results in the terminal

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
netguard
```

Example output:

```
Welcome to NetGuard!

=== NETWORK INFORMATION ===
Computer name: my-laptop.lan
Local IP address: 192.168.1.43

=== LOCAL PORT SCANNER ===
Port 22: CLOSED
Port 80: CLOSED
Port 5000: OPEN
...

NetGuard scan completed!
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
