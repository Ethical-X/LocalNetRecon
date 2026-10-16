# Local Network Recon Tool v1

Interactive local network reconnaissance tool for host discovery and targeted nmap scanning.

> **For authorized use only.** Only run this on networks you own or have explicit permission to test.

---

## Features

- Automatic detection of usable network interfaces
- Host discovery on the local subnet (`nmap -sn`)
- Multi-target selection (choose specific hosts or scan all)
- Flexible scanning options:
  - Use the same flags for every host
  - Set custom flags per host
  - Fall back to a basic `nmap <ip>` scan
- Clean, consistent terminal UI

---

## Requirements

- Python 3.8+
- [nmap](https://nmap.org/) installed and available in your `PATH`
- Python packages:
1. psutil

to install psutil you can run:
`python3 -m pip install -r requirements.txt`

Project Structure:
localnetrecon/
├── main.py                 # Main program logic & user interaction\n
├── scan.py                 # nmap wrapper functions\n
└── detect_interfaces.py    # Network interface detection\n

## Usage
Clone or download the project and navigate into the folder:
`cd localnetrecon`
Run the tool:
`python3 main.py`

The tool detects usable interfaces and lets you choose one (or auto-selects if only one is found).
It performs a host discovery scan on the local network.
You can choose to scan individual hosts.
Select one or more hosts by index (e.g. 0,2,3) or just press Enter to scan all discovered hosts.
Optionally provide nmap flags (same flags for all hosts, or different flags per host).

The tool prints nmap results directly to the terminal.

If you want to save results, just include normal nmap output flags, for example:
-oN results.txt
-oX results.xml
-oA scan_output

## Notes & Limitations
- No built-in result saving (by design — use nmap’s own output options).
- Designed for local/lab use. Not intended as a full professional scanner.

## Disclaimer
This tool is intended for educational purposes and authorized security testing only.
Unauthorized scanning of networks is illegal. Always obtain proper permission before use.
