#!/usr/bin/env python3
"""
Phase 1 — Google GAIA ID & Digital Footprint Collector
Author: @nvsncis | OSINT 2026 Edition
"""

import requests
import subprocess
import sys
from rich.console import Console
from rich.table import Table

console = Console()


def check_ghunt_installed():
    try:
        subprocess.run(["ghunt", "--help"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def gaia_lookup(email: str):
    console.rule(f"[bold cyan]Google GAIA Lookup: {email}")
    if not check_ghunt_installed():
        console.print("[red]ghunt not found. Run: pip install ghunt && ghunt login")
        return
    console.print(f"[yellow]Running ghunt on {email}...")
    result = subprocess.run(
        ["ghunt", "email", email],
        capture_output=False,
        text=True
    )


def iforgot_probe(email: str):
    console.rule(f"[bold cyan]Apple ID Probe: {email}")
    url = "https://iforgot.apple.com/password/verify/appleid"
    try:
        r = requests.post(url, data={"id": email}, timeout=10)
        if r.status_code == 200:
            console.print(f"[green][+] Apple ID EXISTS: {email}")
        elif r.status_code == 404:
            console.print(f"[red][-] Apple ID NOT found: {email}")
        else:
            console.print(f"[yellow][?] Status: {r.status_code}")
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}")


def wigle_lookup(bssid: str, wigle_user: str, wigle_token: str):
    console.rule(f"[bold cyan]WiGLE BSSID Lookup: {bssid}")
    import base64
    creds = base64.b64encode(f"{wigle_user}:{wigle_token}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}
    url = "https://api.wigle.net/api/v2/network/search"
    params = {"netid": bssid, "onlymine": "false"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        results = r.json().get("results", [])
        if not results:
            console.print("[red]No results found.")
            return
        table = Table(title=f"WiGLE Results for {bssid}")
        table.add_column("SSID", style="cyan")
        table.add_column("Latitude", style="green")
        table.add_column("Longitude", style="green")
        table.add_column("Last Seen", style="yellow")
        for net in results[:10]:
            table.add_row(
                str(net.get("ssid", "")),
                str(net.get("trilat", "")),
                str(net.get("trilong", "")),
                str(net.get("lasttime", ""))
            )
        console.print(table)
    except requests.RequestException as e:
        console.print(f"[red]Error: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 1 - Digital Footprint Collector")
    subparsers = parser.add_subparsers(dest="command")

    gaia_parser = subparsers.add_parser("gaia", help="Google GAIA lookup via ghunt")
    gaia_parser.add_argument("email")

    apple_parser = subparsers.add_parser("apple", help="Apple ID probe")
    apple_parser.add_argument("email")

    wigle_parser = subparsers.add_parser("wigle", help="WiGLE BSSID lookup")
    wigle_parser.add_argument("bssid")
    wigle_parser.add_argument("--user", required=True)
    wigle_parser.add_argument("--token", required=True)

    args = parser.parse_args()

    if args.command == "gaia":
        gaia_lookup(args.email)
    elif args.command == "apple":
        iforgot_probe(args.email)
    elif args.command == "wigle":
        wigle_lookup(args.bssid, args.user, args.token)
    else:
        parser.print_help()
