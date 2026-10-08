# network_scaner

A simple TCP network scanner written in Python.

## Features
- scans ports on a target host
- accepts ranges and comma-separated ports
- works with IPs or hostnames
- configurable timeout and worker count

## Usage
```bash
python3 main.py 127.0.0.1
python3 main.py 192.168.1.10 -p 20-100
python3 main.py localhost -p 80,443,8080-8090 -t 0.3 -w 30
```

## Author
0xander
