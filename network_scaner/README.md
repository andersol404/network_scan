# `network_scaner` 🛰️

```text
┌──[0xander@kali]─[~/network_scaner]
└─$ python3 main.py <target>

[+] Initializing TCP scanner...
[+] Enumerating ports...
[+] Analyzing responses...
```

> **A lightweight TCP network scanner built with Python for network discovery and security labs.**

`network_scaner` is a simple but practical command-line tool designed to scan TCP ports on a target host, making it useful for **network administration, cybersecurity labs, reconnaissance, and learning network programming with Python.**

---

## ⚡ Features

* 🔎 TCP port scanning
* 🎯 Supports **IP addresses and hostnames**
* 📡 Scan individual ports
* 📋 Comma-separated ports
* 🔢 Port ranges
* ⏱️ Configurable connection timeout
* ⚙️ Configurable number of workers
* 💻 Lightweight CLI interface
* 🐍 Built entirely with Python

### Port formats

```text
80
80,443,8080
20-100
80,443,8000-8100
```

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/0xander/network_scaner.git
cd network_scaner
```

Run the scanner:

```bash
python3 main.py <target>
```

No external dependencies are required.

---

## 🚀 Usage

### Basic scan

```bash
python3 main.py 127.0.0.1
```

### Scan a port range

```bash
python3 main.py 192.168.1.10 -p 20-100
```

### Scan specific ports

```bash
python3 main.py localhost -p 80,443,8080
```

### Custom timeout

```bash
python3 main.py 192.168.1.10 -p 1-1000 -t 0.3
```

### Increase the number of workers

```bash
python3 main.py 192.168.1.10 -p 1-1000 -w 30
```

---

## 🧠 How it works

The scanner attempts to establish a TCP connection with each specified port.

```text
                ┌──────────────┐
                │    TARGET    │
                │ 192.168.1.10 │
                └──────┬───────┘
                       │
              TCP connection attempt
                       │
             ┌─────────┴─────────┐
             │                   │
          ACCEPTED             REFUSED
             │                   │
             ▼                   ▼
         OPEN PORT            CLOSED
```

A successful connection indicates that the port is reachable and accepting TCP connections.

---

## 🔬 Example

```text
$ python3 main.py 127.0.0.1 -p 20-100

[*] Target: 127.0.0.1
[*] Ports: 20-100
[*] Timeout: 1.0s
[*] Workers: 10

[+] Port 22   OPEN
[+] Port 80   OPEN

[*] Scan completed.
```

---

## 📚 What I learned

This project was built as part of my journey into **Python and cybersecurity**, focusing on:

* TCP/IP fundamentals
* Socket programming
* Port scanning
* Network reconnaissance
* Concurrency with workers
* Command-line argument parsing
* Error handling
* Writing practical security tools

---

## 🗂️ Project Structure

```text
network_scaner/
│
├── main.py
├── README.md
└── LICENSE
```

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes, authorized security testing, and systems you own or have permission to test**.

Do not scan networks or systems without authorization.

---

## 👨‍💻 Author

```text
   ___  __  __    _    _   _ ____  _____ ____
  / _ \|  \/  |  / \  | \ | |  _ \| ____|  _ \
 | | | | |\/| | / _ \ |  \| | | | |  _| | |_) |
 | |_| | |  | |/ ___ \| |\  | |_| | |___|  _ <
  \___/|_|  |_/_/   \_\_| \_|____/|_____|_| \_\

                    0xander
```

**Cybersecurity • Python • Networking**

> `Learning systems. Breaking assumptions. Building skills.`

