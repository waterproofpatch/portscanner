#!/usr/bin/env python3
"""
Port scanner
"""
import socket
import argparse
import errno

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
    argument_parser.add_argument("--timeout", type=int, default=.8, help="Timeout for each connection attempt in seconds")
    argument_parser.add_argument("--startport", type=int, default=0, help="Starting port to scan (inclusive)")
    argument_parser.add_argument("--endport", type=int, default=65563, help="Ending port to scan (inclusive)")

    args = argument_parser.parse_args()

    print("Scanning host {}".format(args.host))

    successful_connections = []
    closed_ports = []
    # attempt a tcp connection to each port
    for port in range(args.startport, args.endport + 1):
        print("Connecting to {}:{}".format(args.host, port))
        try:
            if connect_tcp(args.timeout, args.host, port):
                successful_connections.append(port)
            else:
                closed_ports.append(port)
        except OSError as exc:
            print("Unable to connect: {}".format(exc))

    # print summary
    for closed_port in closed_ports:
        print("Port {}: Closed".format(closed_port))
    for successful_connection in successful_connections:
        print("Port {}: Open".format(successful_connection))
