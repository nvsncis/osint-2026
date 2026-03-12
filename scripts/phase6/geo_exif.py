#!/usr/bin/env python3
"""
Phase 6 — Geolocation: EXIF Extraction & IP Analysis
Author: @nvsncis | OSINT 2026 Edition

Setup:
    Set SHODAN_API_KEY in .env
"""

import os
import subprocess
import requests
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()
console = Console()

SHODAN_KEY = os.getenv("SHODAN_API_KEY", "")


def exif_extract(filepath: str):
    """Extract GPS and device metadata from image using ExifTool."""
    console.rule(f"[bold cyan]EXIF Extraction: {filepath}")
    try:
        import exiftool
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(filepath)
            if not metadata:
                console.print("[red]No metadata found")
                return

            meta = metadata[0]
            table = Table(title=f"EXIF Data: {filepath}")
            table.add_column("Tag", style="cyan")
            table.add_column("Value", style="green")

            priority_tags = [
                "EXIF:GPSLatitude", "EXIF:GPSLongitude", "EXIF:GPSAltitude",
                "EXIF:GPSImgDirection", "EXIF:DateTimeOriginal",
                "EXIF:Make", "EXIF:Model", "EXIF:Software",
                "EXIF:GPSLatitudeRef", "EXIF:GPSLongitudeRef"
            ]

            for tag in priority_tags:
                val = meta.get(tag)
                if val:
                    table.add_row(tag.replace("EXIF:", ""), str(val))

            console.print(table)

            lat = meta.get("EXIF:GPSLatitude")
            lon = meta.get("EXIF:GPSLongitude")
            if lat and lon:
                console.print(f"\n[bold green][+] Google Maps: https://maps.google.com/?q={lat},{lon}")

    except ImportError:
        console.print("[red]Install: pip install pyexiftool")
        console.print("[yellow]Also ensure ExifTool binary is installed: apt install exiftool")
    except Exception as e:
        console.print(f"[red]Error: {e}")


def batch_exif(folder: str, output_csv: str = "metadata.csv"):
    """Batch extract EXIF from all images in a folder."""
    console.rule(f"[bold cyan]Batch EXIF: {folder}")
    try:
        result = subprocess.run(
            ["exiftool", "-csv", "-r",
             "-GPSLatitude", "-GPSLongitude", "-DateTimeOriginal", "-Make", "-Model",
             folder],
            capture_output=True, text=True
        )
        with open(output_csv, "w") as f:
            f.write(result.stdout)
        lines = result.stdout.strip().split("\n")
        console.print(f"[green][+] Extracted {len(lines)-1} files → {output_csv}")
    except FileNotFoundError:
        console.print("[red]exiftool binary not found. Install: apt install exiftool")


def analyze_ip(ip: str):
    """Full IP geolocation and infrastructure analysis."""
    console.rule(f"[bold cyan]IP Analysis: {ip}")
    table = Table(title=f"IP Intel: {ip}")
    table.add_column("Source", style="cyan")
    table.add_column("Field", style="yellow")
    table.add_column("Value", style="green")

    # ipapi.is - high accuracy
    try:
        r = requests.get(f"https://ipapi.is/json/?ip={ip}", timeout=10)
        data = r.json()
        geo = data.get("location", {})
        asn = data.get("asn", {})
        table.add_row("ipapi.is", "Country", geo.get("country", ""))
        table.add_row("ipapi.is", "City", geo.get("city", ""))
        table.add_row("ipapi.is", "ISP", asn.get("org", ""))
        table.add_row("ipapi.is", "Is Datacenter", str(data.get("is_datacenter", False)))
        table.add_row("ipapi.is", "Is VPN", str(data.get("is_vpn", False)))
        table.add_row("ipapi.is", "Is Proxy", str(data.get("is_proxy", False)))
    except Exception as e:
        table.add_row("ipapi.is", "Error", str(e))

    # ipinfo.io
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = r.json()
        table.add_row("ipinfo.io", "Org", data.get("org", ""))
        table.add_row("ipinfo.io", "Region", data.get("region", ""))
        table.add_row("ipinfo.io", "Hostname", data.get("hostname", ""))
        table.add_row("ipinfo.io", "Timezone", data.get("timezone", ""))
    except Exception as e:
        table.add_row("ipinfo.io", "Error", str(e))

    # Shodan
    if SHODAN_KEY:
        try:
            import shodan
            api = shodan.Shodan(SHODAN_KEY)
            host = api.host(ip)
            ports = ", ".join(str(p) for p in host.get("ports", []))
            table.add_row("Shodan", "Open Ports", ports)
            table.add_row("Shodan", "OS", host.get("os", "unknown") or "unknown")
            table.add_row("Shodan", "Last Update", host.get("last_update", ""))
        except Exception as e:
            table.add_row("Shodan", "Error", str(e))
    else:
        table.add_row("Shodan", "Note", "Set SHODAN_API_KEY in .env")

    console.print(table)


def email_header_ip(raw_headers: str):
    """Extract originating IP from raw email headers."""
    console.rule("[bold cyan]Email Header IP Extraction")
    import re
    patterns = [
        r"X-Originating-IP:\s*([\d.]+)",
        r"X-Sender-IP:\s*([\d.]+)",
        r"Received:.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    ]
    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, raw_headers, re.IGNORECASE)
        found.update(matches)

    private_ranges = ("10.", "192.168.", "172.")
    public_ips = [ip for ip in found if not any(ip.startswith(p) for p in private_ranges)]

    if public_ips:
        console.print(f"[green][+] Found public IPs: {public_ips}")
        for ip in public_ips:
            analyze_ip(ip)
    else:
        console.print("[red]No public originating IPs found in headers")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 6 - Geolocation & EXIF")
    subparsers = parser.add_subparsers(dest="command")

    exif_p = subparsers.add_parser("exif", help="Extract EXIF from image")
    exif_p.add_argument("filepath")

    batch_p = subparsers.add_parser("batch", help="Batch EXIF from folder")
    batch_p.add_argument("folder")
    batch_p.add_argument("--output", default="metadata.csv")

    ip_p = subparsers.add_parser("ip", help="Full IP analysis")
    ip_p.add_argument("ip")

    header_p = subparsers.add_parser("headers", help="Extract IP from email headers")
    header_p.add_argument("file", help="File containing raw email headers")

    args = parser.parse_args()

    if args.command == "exif":
        exif_extract(args.filepath)
    elif args.command == "batch":
        batch_exif(args.folder, args.output)
    elif args.command == "ip":
        analyze_ip(args.ip)
    elif args.command == "headers":
        with open(args.file) as f:
            email_header_ip(f.read())
    else:
        parser.print_help()
