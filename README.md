# NetGuard

A lightweight network monitoring and security tool for home and small-office networks, built with Python.

NetGuard's goal is to answer three questions: **What is on my network? What changed? Is anything exposed that shouldn't be?**

> **Status:** early development. See the [roadmap](docs/ROADMAP.md).

## Current Features

- Detect computer hostname
- Identify local IP address
- Check common local TCP ports
- Display scan results in the terminal

## Planned Features

- Discover devices on the local network
- Baseline the network and detect changes (new devices, newly opened ports)
- Flag risky exposed services
- Scan history and continuous monitoring
- Web dashboard (FastAPI + React)

## Run the Project

```bash
python3 main.py
```

## Documentation

- [Roadmap](docs/ROADMAP.md): phases and progress
- [Architecture](docs/ARCHITECTURE.md): design, components, and key decisions
- [Case Study](docs/CASE_STUDY.md): the problem, approach, and lessons learned

## Responsible Use

NetGuard is intended **only for networks you own or have explicit permission to test**. Unauthorized scanning may be illegal in your jurisdiction.
