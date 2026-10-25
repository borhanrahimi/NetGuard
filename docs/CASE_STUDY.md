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

*TBD, recorded per phase.* Topics to document:

- Telling apart *closed* and *filtered* ports
- Making scans fast with concurrency without overwhelming the network
- Identifying devices reliably when IP addresses change (DHCP)
- Privilege requirements for ARP scanning

## Results

*TBD*: scan performance (e.g. time to scan 1,024 ports before vs. after concurrency), test coverage, screenshots.

## What's next

See [ROADMAP.md](ROADMAP.md).
