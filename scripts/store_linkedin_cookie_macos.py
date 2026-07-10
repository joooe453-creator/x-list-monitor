#!/usr/bin/env python3
"""Store a LinkedIn session cookie in macOS Keychain without echoing it.

This helper is intended for local use only. It never prints the cookie value.
Service name: x-list-monitor.linkedin-session
Account name: linkedin-monitor
"""
import getpass
import subprocess
import sys

SERVICE = "x-list-monitor.linkedin-session"
ACCOUNT = "linkedin-monitor"


def main() -> int:
    print("LinkedIn cookie/session local storage")
    print("The value will be stored in macOS Keychain and will not be printed.")
    print("Use a dedicated LinkedIn account/session. Do not commit or share this secret.")
    value = getpass.getpass("Paste LinkedIn Cookie header or session value (hidden input): ").strip()
    if not value:
        print("No value entered; nothing stored.", file=sys.stderr)
        return 1
    if len(value) < 20:
        print("Value looks too short to be a session secret; not storing.", file=sys.stderr)
        return 1

    # Delete an existing secret if present, then add the new one. Never print stderr because
    # some systems include contextual details; keep output generic.
    subprocess.run(
        ["security", "delete-generic-password", "-s", SERVICE, "-a", ACCOUNT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    result = subprocess.run(
        ["security", "add-generic-password", "-s", SERVICE, "-a", ACCOUNT, "-w", value, "-U"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        print("Failed to store secret in macOS Keychain.", file=sys.stderr)
        return result.returncode
    print(f"Stored LinkedIn session secret in macOS Keychain: service={SERVICE}, account={ACCOUNT}")
    print("Cookie value was not printed. Next step: run the monitor validation check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
