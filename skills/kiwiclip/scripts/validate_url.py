#!/usr/bin/env python3
"""Validate a URL is safe to navigate to before /kiwiclip records it.

Blocks localhost, private IP ranges, and cloud metadata endpoints so a
malicious or mistaken product_url/login_url can't be used to make the
recording browser reach internal infrastructure (SSRF).

Usage: python3 validate_url.py <url>
Exits 0 and prints the URL if safe. Exits 1 with an error message otherwise.
"""
import ipaddress
import socket
import sys
from urllib.parse import urlparse

BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "metadata.google.internal"}
BLOCKED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]


class SecurityError(Exception):
    pass


def validate_url_for_recording(url: str) -> str:
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise SecurityError(f"Scheme '{parsed.scheme}' is not allowed")

    if not parsed.hostname:
        raise SecurityError("URL has no hostname")

    if parsed.hostname in BLOCKED_HOSTS:
        raise SecurityError(f"Host '{parsed.hostname}' is blocked")

    if "@" in parsed.netloc:
        raise SecurityError("Embedded credentials in the URL are not allowed")

    # Check the hostname itself, if it's already an IP literal.
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for r in BLOCKED_RANGES:
            if ip in r:
                raise SecurityError(f"Private/blocked IP range: {parsed.hostname}")
    except ValueError:
        pass  # Not an IP literal — resolve it below instead.

    # Resolve the hostname and check what it actually points to, so a
    # DNS record can't point a normal-looking hostname at an internal IP.
    try:
        resolved_ips = {info[4][0] for info in socket.getaddrinfo(parsed.hostname, None)}
    except socket.gaierror as e:
        raise SecurityError(f"Could not resolve host '{parsed.hostname}': {e}")

    for ip_str in resolved_ips:
        ip = ipaddress.ip_address(ip_str)
        for r in BLOCKED_RANGES:
            if ip in r:
                raise SecurityError(f"'{parsed.hostname}' resolves to blocked range: {ip_str}")

    return url


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_url.py <url>", file=sys.stderr)
        sys.exit(2)

    try:
        safe_url = validate_url_for_recording(sys.argv[1])
        print(safe_url)
        sys.exit(0)
    except SecurityError as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        sys.exit(1)
