#!/usr/bin/env python3
"""
Phase 3 — Telegram Deep Recon via Telethon
Author: @nvsncis | OSINT 2026 Edition

Setup:
    1. Get API credentials at https://my.telegram.org
    2. Set TG_API_ID and TG_API_HASH in .env file
"""

import os
import asyncio
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()

console = Console()

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")


def get_client():
    try:
        from telethon.sync import TelegramClient
        return TelegramClient("osint_session", API_ID, API_HASH)
    except ImportError:
        console.print("[red]telethon not installed. Run: pip install telethon")
        raise


def user_lookup(username: str):
    """Get User ID, name, phone, and registration info by username."""
    console.rule(f"[bold cyan]Telegram User Lookup: {username}")
    client = get_client()
    with client:
        try:
            entity = client.get_entity(username)
            table = Table(title=f"User Info: {username}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("User ID", str(entity.id))
            table.add_row("First Name", str(getattr(entity, "first_name", "N/A")))
            table.add_row("Last Name", str(getattr(entity, "last_name", "N/A")))
            table.add_row("Username", str(getattr(entity, "username", "N/A")))
            table.add_row("Phone", str(getattr(entity, "phone", "N/A")))
            table.add_row("Bot", str(getattr(entity, "bot", False)))
            console.print(table)
            return entity
        except Exception as e:
            console.print(f"[red]Error: {e}")


def channel_members(channel: str, limit: int = 200, output_csv: str = None):
    """Export channel members list."""
    console.rule(f"[bold cyan]Channel Members: {channel}")
    client = get_client()
    with client:
        try:
            from telethon.tl.functions.channels import GetParticipantsRequest
            from telethon.tl.types import ChannelParticipantsSearch
            entity = client.get_entity(channel)
            participants = client.get_participants(entity, limit=limit)

            table = Table(title=f"Members of {channel}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Username", style="yellow")

            rows = []
            for user in participants:
                name = f"{getattr(user,'first_name','')} {getattr(user,'last_name','')}".strip()
                uname = getattr(user, "username", "") or ""
                table.add_row(str(user.id), name, uname)
                rows.append({"id": user.id, "name": name, "username": uname})

            console.print(table)
            console.print(f"[green][+] Total: {len(rows)} members")

            if output_csv:
                with open(output_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["id", "name", "username"])
                    writer.writeheader()
                    writer.writerows(rows)
                console.print(f"[green][+] Saved to {output_csv}")

        except Exception as e:
            console.print(f"[red]Error: {e}")


def monitor_leaks(channels: list, keywords: list = None):
    """Monitor channels for leak-related posts in real time."""
    if keywords is None:
        keywords = ["leak", "combo", "logs", "dump", "breach", "сливы", "пробив"]

    console.rule("[bold red]Telegram Leak Monitor — LIVE")
    console.print(f"[yellow]Watching: {channels}")
    console.print(f"[yellow]Keywords: {keywords}")

    from telethon import TelegramClient, events

    client = TelegramClient("monitor_session", API_ID, API_HASH)

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        msg = event.message.message or ""
        if any(kw.lower() in msg.lower() for kw in keywords):
            ts = datetime.now().strftime("%H:%M:%S")
            console.print(f"[red][!] [{ts}] New hit in {event.chat_id}:")
            console.print(f"    {msg[:300]}")
            if event.message.document:
                console.print(f"[yellow]    → File attached, downloading...")
                await event.message.download_media("./leaks/")

    with client:
        console.print("[green][+] Monitoring started. Press Ctrl+C to stop.")
        client.run_until_disconnected()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 3 - Telegram Recon")
    subparsers = parser.add_subparsers(dest="command")

    user_p = subparsers.add_parser("user", help="Lookup user by username")
    user_p.add_argument("username")

    members_p = subparsers.add_parser("members", help="Export channel members")
    members_p.add_argument("channel")
    members_p.add_argument("--limit", type=int, default=200)
    members_p.add_argument("--csv", dest="output_csv", default=None)

    monitor_p = subparsers.add_parser("monitor", help="Monitor channels for leaks")
    monitor_p.add_argument("channels", nargs="+")
    monitor_p.add_argument("--keywords", nargs="+", default=None)

    args = parser.parse_args()

    if not API_ID or not API_HASH:
        console.print("[red]Set TG_API_ID and TG_API_HASH in your .env file")
        exit(1)

    if args.command == "user":
        user_lookup(args.username)
    elif args.command == "members":
        channel_members(args.channel, args.limit, args.output_csv)
    elif args.command == "monitor":
        monitor_leaks(args.channels, args.keywords)
    else:
        parser.print_help()
