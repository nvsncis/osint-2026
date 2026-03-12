#!/usr/bin/env python3
"""
Phase 5 — Identity Fusion: Avatar Hash Matching & Cross-Platform Correlation
Author: @nvsncis | OSINT 2026 Edition
"""

import requests
from io import BytesIO
from rich.console import Console
from rich.table import Table

console = Console()


def get_phash(url: str):
    """Download image and compute perceptual hash."""
    try:
        import imagehash
        from PIL import Image
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return imagehash.phash(img)
    except ImportError:
        console.print("[red]Install: pip install imagehash Pillow")
        return None
    except Exception as e:
        console.print(f"[red]Error fetching {url}: {e}")
        return None


def compare_avatars(urls: list, threshold: int = 10):
    """
    Compare avatar images across multiple platforms using perceptual hashing.
    Images with hash difference < threshold are considered the same person.
    """
    console.rule("[bold cyan]Avatar Hash Comparison")
    hashes = {}

    for url in urls:
        console.print(f"[yellow][*] Hashing: {url[:70]}...")
        h = get_phash(url)
        if h:
            hashes[url] = h
            console.print(f"[green]    Hash: {h}")

    if len(hashes) < 2:
        console.print("[red]Need at least 2 valid images to compare")
        return

    console.rule("[bold cyan]Comparison Results")
    table = Table(title="Avatar Cross-Platform Matching")
    table.add_column("URL A", style="cyan")
    table.add_column("URL B", style="cyan")
    table.add_column("Hash Diff", style="yellow")
    table.add_column("Verdict", style="bold")

    url_list = list(hashes.keys())
    for i in range(len(url_list)):
        for j in range(i + 1, len(url_list)):
            a, b = url_list[i], url_list[j]
            diff = hashes[a] - hashes[b]
            verdict = "[green]✓ SAME PERSON" if diff < threshold else "[red]✗ DIFFERENT"
            table.add_row(a[:50], b[:50], str(diff), verdict)

    console.print(table)


def stylometry_patterns(texts: list):
    """
    Basic stylometry analysis: find writing patterns across texts.
    Looks for shared vocabulary, punctuation habits, and common phrases.
    """
    console.rule("[bold cyan]Stylometry Analysis")
    import re
    from collections import Counter

    results = []
    for i, text in enumerate(texts):
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        # punctuation habits
        ellipsis = text.count("...")
        exclaim = text.count("!")
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)

        results.append({
            "idx": i,
            "top_words": word_freq.most_common(5),
            "ellipsis": ellipsis,
            "exclaim": exclaim,
            "caps_ratio": round(caps_ratio, 3),
            "avg_word_len": round(sum(len(w) for w in words) / max(len(words), 1), 2)
        })

    table = Table(title="Stylometry Patterns")
    table.add_column("Text #", style="cyan")
    table.add_column("Top Words", style="green")
    table.add_column("...", style="yellow")
    table.add_column("!", style="yellow")
    table.add_column("CAPS %", style="yellow")
    table.add_column("Avg Word Len", style="white")

    for r in results:
        table.add_row(
            str(r["idx"] + 1),
            str([w for w, _ in r["top_words"]]),
            str(r["ellipsis"]),
            str(r["exclaim"]),
            str(r["caps_ratio"]),
            str(r["avg_word_len"])
        )

    console.print(table)
    console.print("[yellow][*] Similar CAPS%, ellipsis count, and word length → likely same author")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 5 - Identity Fusion")
    subparsers = parser.add_subparsers(dest="command")

    avatar_p = subparsers.add_parser("avatars", help="Compare avatar images across platforms")
    avatar_p.add_argument("urls", nargs="+", help="Image URLs to compare")
    avatar_p.add_argument("--threshold", type=int, default=10, help="Hash diff threshold (default: 10)")

    style_p = subparsers.add_parser("stylometry", help="Basic writing style analysis")
    style_p.add_argument("--texts", nargs="+", help="Text samples to compare")
    style_p.add_argument("--files", nargs="+", help="Text files to compare")

    args = parser.parse_args()

    if args.command == "avatars":
        compare_avatars(args.urls, args.threshold)
    elif args.command == "stylometry":
        texts = []
        if args.texts:
            texts = args.texts
        elif args.files:
            for fp in args.files:
                with open(fp) as f:
                    texts.append(f.read())
        if texts:
            stylometry_patterns(texts)
        else:
            console.print("[red]Provide --texts or --files")
    else:
        parser.print_help()
