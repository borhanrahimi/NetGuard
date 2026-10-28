# Case Study: NetGuard

> This case study is written alongside development. Sections marked *TBD* are filled in as each phase is completed.

## The problem

Home and small-office networks keep growing: laptops, phones, smart TVs, cameras, IoT devices. Most owners cannot answer basic questions:

- What devices are on my network right now?
- Has an unknown device joined?
- Is any device exposing a risky service, such as Telnet or an open database?

Enterprise tools answer these questions but are complex and expensive. NetGuard aims to answer them with a lightweight tool anyone can run.

## Goals

1. Discover devices on a local network.
2. Establish a baseline of what is "normal".
3. Detect and alert on changes: new devices, newly opened ports, risky services.
4. Present the results clearly in the terminal and in a web dashboard.

## My role

Solo project: design, implementation, testing, and documentation.

## Approach

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design. In short:

- A modular Python package where scanners return structured data instead of printing.
- SQLite stores scan history so scans can be compared over time.
- A change detector compares each scan against the baseline and rates findings by severity.

## Challenges & what I learned

### Phase 1: Solid foundation

- **Closed vs. filtered ports.** A *closed* port answers with a TCP reset, which Python reports as `ConnectionRefusedError`. A *filtered* port gives no answer at all because a firewall drops the packet, so the connection times out. Catching these two cases separately turns one "not open" result into two useful ones.
- **Concurrency for network I/O.** A port check spends nearly all its time waiting for the network, so threads help a lot despite Python's GIL. A `ThreadPoolExecutor` with `pool.map` keeps results in port order, and the `--workers` limit stops the scan from opening thousands of connections at once.
- **Testing network code without the network.** Tests open a real listening socket on `127.0.0.1` (port 0 lets the OS choose a free port) to check the *open* case, and use `monkeypatch` to fake timeouts for the *filtered* case. The suite needs no internet and runs in well under a second.
- **Validating input at the edge.** Port specs are parsed by a pure function (`parse_ports`) and plugged into argparse as a `type`, so bad input such as `--ports 70000` becomes a clean usage error instead of a stack trace.

### Topics for later phases

- Identifying devices reliably when IP addresses change (DHCP)
- Privilege requirements for ARP scanning

## Results

- **Scan speed (Phase 1):** 1,024 ports on localhost took 1.61s with one worker and 0.38s with 100 workers, about 4× faster. The gain is far larger on real networks, where filtered ports each wait for the full timeout: 1,000 filtered ports at 0.5s would take over 8 minutes one at a time and about 5 seconds with 100 workers.
- **Tests:** 33 unit tests with `pytest`; lint and formatting with `ruff`.
- *TBD:* screenshots, coverage numbers.

## What's next

See [ROADMAP.md](ROADMAP.md).
