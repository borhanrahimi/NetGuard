# Roadmap

NetGuard is built in phases. Each phase ends with something usable, tested, and documented.

**Status legend:** ✅ Done · 🚧 In progress · ⏳ Planned

## Phase 0 — Prototype ✅

- [x] Detect hostname and local IP address
- [x] Check a fixed list of TCP ports on localhost

## Phase 1 — Solid foundation 🚧

Goal: turn the prototype into a well-structured, testable Python package.

- [x] Package layout (`src/netguard/`) with `pyproject.toml` and a `netguard` command
- [x] Scanners return structured data (dataclasses); only the CLI prints
- [ ] CLI with subcommands (`netguard info`, `netguard scan`)
- [ ] Configurable target host and port ranges (`--host`, `--ports 1-1024`)
- [x] Report three port states: **open**, **closed**, **filtered**
- [ ] Concurrent scanning with a thread pool
- [ ] Service name lookup (22 → ssh, 443 → https)
- [ ] Unit tests with `pytest`, linting with `ruff`

## Phase 2 — Device discovery ⏳

Goal: know what is on the local network.

- [ ] Discover devices on the LAN (ARP scan, ping sweep fallback)
- [ ] Record IP, MAC address, hostname, and hardware vendor
- [ ] Persist scans and devices in SQLite

## Phase 3 — Change detection ⏳

Goal: the core security feature. Alert when the network deviates from normal.

- [ ] Save a **baseline** of known devices and their open ports
- [ ] Detect new / unknown devices joining the network
- [ ] Detect newly opened or closed ports
- [ ] Detect devices going offline
- [ ] Flag risky services (Telnet, FTP, SMB, RDP, exposed databases)
- [ ] Severity levels for alerts (info / warning / critical)

## Phase 4 — Continuous monitoring ⏳

- [ ] Scheduled scans (configurable interval)
- [ ] Notifications (desktop, email, or webhook)
- [ ] Scan history and export (JSON / CSV)

## Phase 5 — Dashboard ⏳

- [ ] REST API with FastAPI
- [ ] React dashboard: device list, alert timeline, scan history

## Phase 6 — Production polish ⏳

- [ ] CI with GitHub Actions (tests + lint on every push)
- [ ] Docker image
- [ ] Demo screenshots / GIF in the README
- [ ] Finalize the [case study](CASE_STUDY.md)
