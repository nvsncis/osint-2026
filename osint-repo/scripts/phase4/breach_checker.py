#!/usr/bin/env python3
"""
Phase 4 — Breach Aggregator & Password Reuse Checker
Author: @nvsncis | OSINT 2026 Edition

Setup:
    Set HIBP_API_KEY and DEHASHED_EMAIL / DEHASHED_API_KEY in .env
"""

import os
import hashlib
import base64
import requests
import time
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()
console = Console()

HIBP_KEY = os.getenv("HIBP_API_KEY", "")
DEHASHED_EMAIL = os.getenv("DEHASHED_EMAIL", "")
DEHASHED_KEY = os.getenv("DEHASHED_API_KEY", "")


def hibp_check_email(email: str):
    """Check email against HaveIBeenPwned breach database."""
    console.rule(f"[bold cyan]HIBP Check: {email}")
    if not HIBP_KEY:
        console.print("[red]Set HIBP_API_KEY in .env")
        return []
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": HIBP_KEY, "User-Agent": "OSINT-2026"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 404:
            console.print(f"[green][+] {email} — NOT found in any breach")
            return []
        elif r.status_code == 200:
            breaches = r.json()
            table = Table(title=f"Breaches for {email}")
            table.add_column("Breach Name", style="red")
            table.add_column("Date", style="yellow")
            table.add_column("Data Classes", style="cyan")
            for b in breaches:
                table.add_row(
                    b.get("Name", ""),
                    b.get("BreachDate", ""),
                    ", ".join(b.get("DataClasses", [])[:4])
                )
            console.print(table)
            console.print(f"[red][!] Found in {len(breaches)} breaches")
            return breaches
        else:
            console.print(f"[yellow]Status: {r.status_code}")
    except Exception as e:
        console.print(f"[red]Error: {e}")
    return []


def hibp_check_password(password: str):
    """Check password via k-anonymity API (safe — never sends full hash)."""
    console.rule("[bold cyan]HIBP Password Check")
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=10)
        found = suffix in r.text
        count_line = [l for l in r.text.splitlines() if l.startswith(suffix)]
        count = int(count_line[0].split(":")[1]) if count_line else 0
        if found:
            console.print(f"[red][!] Password found in {count:,} breach records!")
        else:
            console.print("[green][+] Password NOT found in any breach")
        return found, count
    except Exception as e:
        console.print(f"[red]Error: {e}")
        return False, 0


def dehashed_search(query: str, field: str = "email", size: int = 100):
    """Search DeHashed for target data."""
    console.rule(f"[bold cyan]DeHashed: {field}:{query}")
    if not DEHASHED_EMAIL or not DEHASHED_KEY:
        console.print("[red]Set DEHASHED_EMAIL and DEHASHED_API_KEY in .env")
        return []
    creds = base64.b64encode(f"{DEHASHED_EMAIL}:{DEHASHED_KEY}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Accept": "application/json"}
    url = f"https://api.dehashed.com/search?query={field}:{query}&size={size}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        entries = data.get("entries", [])
        if not entries:
            console.print("[red]No results found")
            return []
        table = Table(title=f"DeHashed Results ({len(entries)} entries)")
        table.add_column("Email", style="cyan")
        table.add_column("Password", style="red")
        table.add_column("IP", style="yellow")
        table.add_column("Source", style="white")
        for e in entries[:20]:
            table.add_row(
                e.get("email", "")[:40],
                e.get("password", "")[:30],
                e.get("ip_address", ""),
                e.get("database_name", "")[:25]
            )
        console.print(table)
        console.print(f"[green][+] Total entries: {len(entries)}")
        return entries
    except Exception as e:
        console.print(f"[red]Error: {e}")
        return []


def bulk_email_check(filepath: str, delay: float = 1.5):
    """Check a list of emails from file against HIBP."""
    console.rule(f"[bold cyan]Bulk Email Check: {filepath}")
    try:
        with open(filepath) as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[red]File not found: {filepath}")
        return

    console.print(f"[yellow]Checking {len(emails)} emails...")
    results = {}
    for email in emails:
        breaches = hibp_check_email(email)
        results[email] = len(breaches)
        time.sleep(delay)  # respect rate limit

    console.rule("[bold green]Summary")
    for email, count in results.items():
        status = f"[red]{count} breaches" if count else "[green]clean"
        console.print(f"  {email}: {status}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 4 - Breach Checker")
    subparsers = parser.add_subparsers(dest="command")

    email_p = subparsers.add_parser("email", help="Check single email in HIBP")
    email_p.add_argument("email")

    pass_p = subparsers.add_parser("password", help="Check password via k-anonymity")
    pass_p.add_argument("password")

    dehashed_p = subparsers.add_parser("dehashed", help="Search DeHashed")
    dehashed_p.add_argument("query")
    dehashed_p.add_argument("--field", default="email", choices=["email", "username", "ip_address", "name", "phone"])

    bulk_p = subparsers.add_parser("bulk", help="Bulk check emails from file")
    bulk_p.add_argument("filepath")
    bulk_p.add_argument("--delay", type=float, default=1.5)

    args = parser.parse_args()

    if args.command == "email":
        hibp_check_email(args.email)
    elif args.command == "password":
        hibp_check_password(args.password)
    elif args.command == "dehashed":
        dehashed_search(args.query, args.field)
    elif args.command == "bulk":
        bulk_email_check(args.filepath, args.delay)
    else:
        parser.print_help()
