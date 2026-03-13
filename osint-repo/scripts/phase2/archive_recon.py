#!/usr/bin/env python3
"""
Phase 2 — Wayback Machine & Archive.today Automation
Author: @nvsncis | OSINT 2026 Edition
"""

import requests
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

console = Console()


def cdx_snapshots(domain: str, limit: int = 500, status: str = "200"):
    """Bulk retrieve all CDX snapshots for a domain."""
    console.rule(f"[bold cyan]Wayback CDX: {domain}")
    url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"{domain}/*",
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype",
        "filter": f"statuscode:{status}",
        "limit": str(limit),
        "collapse": "urlkey"
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        if len(data) <= 1:
            console.print("[red]No snapshots found.")
            return []

        snapshots = data[1:]  # skip header row
        table = Table(title=f"CDX Snapshots for {domain} (top {min(20, len(snapshots))})")
        table.add_column("Timestamp", style="cyan")
        table.add_column("URL", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Type", style="white")

        for snap in snapshots[:20]:
            table.add_row(snap[0], snap[1][:80], snap[2], snap[3])

        console.print(table)
        console.print(f"[green][+] Total snapshots found: {len(snapshots)}")
        return snapshots

    except Exception as e:
        console.print(f"[red]Error: {e}")
        return []


def archive_today_save(url: str):
    """Submit a URL to archive.today for archiving."""
    console.rule(f"[bold cyan]archive.today Save: {url}")
    try:
        r = requests.post(
            "https://archive.ph/submit/",
            data={"url": url},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=30,
            allow_redirects=True
        )
        console.print(f"[green][+] Archived at: {r.url}")
        return r.url
    except Exception as e:
        console.print(f"[red]Error: {e}")
        return None


def find_deleted_pages(domain: str):
    """Find pages that existed in archive but return 404 on live site."""
    console.rule(f"[bold cyan]Deleted Page Finder: {domain}")
    snapshots = cdx_snapshots(domain, limit=200)
    if not snapshots:
        return

    console.print("[yellow][*] Checking live status of archived URLs...")
    deleted = []

    for snap in tqdm(snapshots[:50], desc="Checking"):
        live_url = snap[1]
        try:
            r = requests.head(live_url, timeout=5, allow_redirects=True)
            if r.status_code == 404:
                deleted.append(live_url)
        except Exception:
            pass

    if deleted:
        console.print(f"\n[green][+] Found {len(deleted)} potentially deleted pages:")
        for url in deleted:
            wb_url = f"https://web.archive.org/web/*/{url}"
            console.print(f"  [cyan]{url}[/cyan] → [yellow]{wb_url}")
    else:
        console.print("[red]No deleted pages found in sample.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2 - Archive Analysis")
    subparsers = parser.add_subparsers(dest="command")

    cdx_p = subparsers.add_parser("cdx", help="Bulk CDX snapshot retrieval")
    cdx_p.add_argument("domain")
    cdx_p.add_argument("--limit", type=int, default=500)

    save_p = subparsers.add_parser("save", help="Save URL to archive.today")
    save_p.add_argument("url")

    deleted_p = subparsers.add_parser("deleted", help="Find deleted pages")
    deleted_p.add_argument("domain")

    args = parser.parse_args()

    if args.command == "cdx":
        cdx_snapshots(args.domain, args.limit)
    elif args.command == "save":
        archive_today_save(args.url)
    elif args.command == "deleted":
        find_deleted_pages(args.domain)
    else:
        parser.print_help()
