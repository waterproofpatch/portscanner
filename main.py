#!/usr/bin/env python3
"""
Port scanner
"""
import socket
import argparse

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("host", help="Hostname to scan")

    args = argument_parser.parse_args()

    print("Scanning host {}".format(args.host))

    successful_connections = []
    for port in range(65536):
        print("Connecting to {}:{}".format(args.host, port))
        try:
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            s.settimeout(0.8)
            s.connect((args.host, port))
        except OSError as exc:
            print("Unable to connect: {}".format(exc))
            continue
        successful_connections.append(port)

    for successful_connection in successful_connections:
        print("Port {}: Open".format(successful_connection))
