#!/usr/bin/env python3
"""
Port scanner
"""
import socket
import argparse
import errno

def connect_udp(timeout_udp, host, port, payload):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.settimeout(timeout_udp)
    s.sendto(payload, (host, port))
    try:
        data = s.recvfrom(1024)
        print("Received data from UDP socket {}".format(data))
    except socket.timeout:
        return 0
    finally:
        s.close()
    return 1

def connect_tcp(timeout, host, port):
    """
    Attempt to connect to the host:port combination

    :param host: the hostname (IP) to connect to
    :param port: the port number to connect to
    :return 1: connection was successful
    :return 0: connection was refused
    """
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((host, port))
    s.close()
    if result == 0:
        return 1
    elif result == errno.ECONNREFUSED:
        return 0


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("host", help="Hostname to scan")
    argument_parser.add_argument("--timeout", type=int, default=.8, help="Timeout for each TCP connection attempt in seconds")
    argument_parser.add_argument("--timeout_udp", type=int, default=1, help="Timeout for each UDP connection attempt in seconds")
    argument_parser.add_argument("--startport", type=int, default=0, help="Starting port to scan (inclusive)")
    argument_parser.add_argument("--endport", type=int, default=65563, help="Ending port to scan (inclusive)")
    argument_parser.add_argument("--udppayload", default=None, help="Payload for UDP scans")

    args = argument_parser.parse_args()

    udp_payload = b'aaaa'
    if args.udppayload:
        print("Reading specified payload from file {}".format(args.udppayload))
        udp_payload = open(args.udppayload, 'rb').read()

    print("Scanning host {}".format(args.host))

    successful_connections_tcp = []
    successful_connections_udp = []
    closed_ports = []
    # attempt a tcp connection to each port
    for port in range(args.startport, args.endport + 1):
        print("Connecting to {}:{}".format(args.host, port))
        try:
            if connect_tcp(args.timeout, args.host, port):
                successful_connections_tcp.append(port)
            if connect_udp(args.timeout_udp, args.host, port, udp_payload):
                successful_connections_udp.append(port)
            else:
                closed_ports.append(port)
        except OSError as exc:
            print("Unable to connect: {}".format(exc))

    # print summary
    for closed_port in closed_ports:
        print("Port {}: Closed".format(closed_port))
    for successful_connection in successful_connections_tcp:
        print("Port {}: Open (TCP)".format(successful_connection))
    for successful_connection in successful_connections_udp:
        print("Port {}: Open (UDP)".format(successful_connection))
