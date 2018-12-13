Python port scanner.

## Prerequisites

python 3.5.2 or later

## Usage

```bash
python3 main.py --help
```

e.g.

```bash
python3 main.py 192.168.1.100
python3 main.py 192.168.1.100 --timeout 2
python3 main.py 192.168.1.100 --timeout .8 --startport 10 --endport 20
python3 main.py 192.168.1.100 --timeout .8 --startport 10 --endport 20 --udppayload udp_payload.bin
python3 main.py 192.168.1.100 --timeout_udp 2 --timeout .8 --startport 10 --endport 20 --udppayload udp_payload.bin
```
