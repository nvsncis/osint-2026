<div align="center">

```
 ██████╗ ███████╗██╗███╗   ██╗████████╗    ██████╗  ██████╗ ██████╗  ██████╗ 
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ╚════██╗██╔═████╗╚════██╗██╔════╝ 
██║   ██║███████╗██║██╔██╗ ██║   ██║         ▄███╔╝██║██╔██║ █████╔╝███████╗ 
██║   ██║╚════██║██║██║╚██╗██║   ██║         ▀▀══╝ ████╔╝██║██╔═══╝ ██╔══██║ 
╚██████╔╝███████║██║██║ ╚████║   ██║         ██████╗╚██████╔╝███████╗╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝         ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ 
```

**The most complete OSINT methodology & toolkit for 2026**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/nvsncis/osint-2026?style=for-the-badge&color=yellow)](https://github.com/nvsncis/osint-2026/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/nvsncis/osint-2026?style=for-the-badge)](https://github.com/nvsncis/osint-2026/commits)
[![Telegram](https://img.shields.io/badge/Author-@nvsncis-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/nvsncis)

> **For B2B & B2C Red Team operations only. Educational purposes.**

</div>

---

## What is this?

A battle-tested, continuously updated OSINT field manual covering **6 operational phases** — from initial digital footprint collection to physical geolocation tracking. Every technique includes working code, real commands, and 2026-relevant tooling.

**No outdated Maltego screenshots. No basic Google dork lists from 2019. This is the real workflow.**

---

## 📚 Full Documentation

> Each phase has a dedicated deep-dive document with complete methodology, all techniques, and working code examples.

| Phase | Topic | Doc |
|-------|-------|-----|
| 🔵 Phase 1 | Primary Data Collection | [→ Read](docs/phase1.md) |
| 🔵 Phase 2 | Archives, Search Engines & Google Dork | [→ Read](docs/phase2.md) |
| 🔵 Phase 3 | Social Networks & Platform Vectors | [→ Read](docs/phase3.md) |
| 🔴 Phase 4 | Data Breaches & Darknet | [→ Read](docs/phase4.md) |
| 🔵 Phase 5 | Cross-Analysis & Link Visualization | [→ Read](docs/phase5.md) |
| 🔵 Phase 6 | Geolocation & Physical Tracking | [→ Read](docs/phase6.md) |
| 🛡️ OPSEC | Operational Security for the Researcher | [→ Read](docs/opsec.md) |

---

## Quick Start

```bash
git clone https://github.com/nvsncis/osint-2026.git
cd osint-2026
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
playwright install chromium
```

---

## Repository Structure

```
osint-2026/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
│
└── scripts/
    ├── phase1/
    │   ├── gaia_lookup.py       ← Google GAIA ID + Apple ID + WiGLE
    │   └── account_warmup.py    ← Synthetic identity warm-up automation
    ├── phase2/
    │   └── archive_recon.py     ← Wayback CDX + archive.today + deleted page finder
    ├── phase3/
    │   └── telegram_recon.py    ← User lookup, channel dump, live leak monitor
    ├── phase4/
    │   └── breach_checker.py    ← HIBP + DeHashed + k-anonymity password check
    ├── phase5/
    │   └── identity_fusion.py   ← Avatar hash matching + stylometry analysis
    └── phase6/
        └── geo_exif.py          ← EXIF extraction + IP geolocation + header analysis
```

---

## Methodology — 6 Phases

<details>
<summary><b>Phase 1 — Primary Data Collection</b></summary>

### Digital Footprints

Standard names and phone numbers change. Collect what stays with the target.

#### Google GAIA ID
A numeric Google account ID. Extracted via `ghunt`. Provides all devices, creation date, and a hidden phone number.

```bash
pip install ghunt
ghunt login
ghunt email target@gmail.com
```

#### Apple ID Probe

```python
import requests
r = requests.post('https://iforgot.apple.com/password/verify/appleid',
                  data={'id': 'target@email.com'})
# 200 = exists, 404 = not found
```

#### BSSID / WiGLE Lookup

```bash
python scripts/phase1/gaia_lookup.py wigle AA:BB:CC:DD:EE:FF \
    --user YOUR_USER --token YOUR_TOKEN
```

#### Browser Automation (Playwright + Stealth)

```bash
pip install playwright playwright-stealth
playwright install chromium
python scripts/phase1/account_warmup.py https://target.com --actions 80
```

#### Toolset

| Tool | Purpose | Link |
|------|---------|-------|
| ghunt | Google GAIA / Gmail OSINT | [GitHub](https://github.com/mxrch/GHunt) |
| SpiderFoot | Automated OSINT framework | [GitHub](https://github.com/smicallef/spiderfoot) |
| Recon-ng | Modular recon framework | [GitHub](https://github.com/lanmaster53/recon-ng) |
| Playwright | Stealth browser automation | [Docs](https://playwright.dev/python/) |

</details>

<details>
<summary><b>Phase 2 — Search Engines, Archives & Google Dork</b></summary>

### Wayback CDX API

```bash
waybackpack target.com -d ./snapshots --from-date 20220101 --to-date 20261231
python scripts/phase2/archive_recon.py deleted target.com
```

```python
params = {'url': 'target.com/*', 'output': 'json', 'fl': 'timestamp,original,statuscode',
          'filter': 'statuscode:200', 'limit': '500'}
r = requests.get('http://web.archive.org/cdx/search/cdx', params=params)
```

### Google Dork Cheatsheet

| Operator | Function | Example |
|----------|----------|---------|
| `site:` | Limit to domain | `site:github.com "password"` |
| `inurl:` | String in URL | `inurl:admin_panel` |
| `intitle:` | String in `<title>` | `intitle:"index of" "backup"` |
| `intext:` | Body text search | `intext:"strictly confidential"` |
| `filetype:` | Exact file extension | `filetype:env "DB_USER"` |
| `-` | Exclude domain | `"target" -site:linkedin.com` |
| `""` | Exact phrase | `"internal use only"` |
| `*` | Wildcard | `"API key * exposed"` |
| `..` | Numeric range | `vulnerable version 1.0..2.5` |
| `before:/after:` | Date range | `site:target.com after:2025-01-01` |

**Critical dorks:**
```
filetype:env "DB_PASSWORD"
filetype:sql "INSERT INTO" "users"
filetype:log "username" "password"
intitle:"index of" "passwords.txt"
inurl:"wp-config.php" filetype:txt
```

#### Anti-ban automation

```bash
python pagodo.py -d target.com -g dorks/all.txt \
    --proxy socks5://user:pass@proxy:1080 --delay 7 --maxresults 100
```

</details>

<details>
<summary><b>Phase 3 — Social Network Vectors</b></summary>

### Telegram

```bash
python scripts/phase3/telegram_recon.py user @target_username
python scripts/phase3/telegram_recon.py members @channelname --limit 500 --csv out.csv
python scripts/phase3/telegram_recon.py monitor @ch1 @ch2 --keywords leak combo logs
```

**Telepathy — full channel archiver:**
```bash
python telepathy.py -t @channelname --comprehensive --media
python telepathy.py -t @channelname --forwards
```

### VK API

```python
params = {
    'user_ids': 'target_username',
    'fields': 'id,first_name,last_name,bdate,city,country,photo_max,contacts',
    'access_token': VK_TOKEN, 'v': '5.199'
}
r = requests.get('https://api.vk.com/method/users.get', params=params)
```

### Instagram — TLS Bypass

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
    'x-ig-app-id': '936619743392459',
    'Cookie': 'sessionid=YOUR_SESSION; csrftoken=TOKEN;'
}
r = requests.get('https://i.instagram.com/api/v1/users/web_profile_info/?username=target',
                 headers=headers)
```

### Snoop — Mass Username Recon (Sherlock 2026 replacement)

```bash
git clone https://github.com/snooppr/snoop
python3 snoop.py username_target
snoop --input targets.txt --output report.json --format json
python3 snoop.py username_target --proxy socks5://127.0.0.1:9050
python3 snoop.py username_target --parse-all
```

</details>

<details>
<summary><b>Phase 4 — Data Breaches & Darknet</b></summary>

> **Strict OPSEC required. Work from VM only. Open all downloaded files in sandbox.**

### Breach Check

```bash
python scripts/phase4/breach_checker.py email target@gmail.com
python scripts/phase4/breach_checker.py password "password123"
python scripts/phase4/breach_checker.py dehashed target@gmail.com --field email
python scripts/phase4/breach_checker.py bulk emails.txt
```

**k-anonymity password check:**
```python
import hashlib, requests
sha1 = hashlib.sha1("password".encode()).hexdigest().upper()
prefix, suffix = sha1[:5], sha1[5:]
r = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
print("PWNED" if suffix in r.text else "CLEAN")
```

### Shadow Forums

| Forum | Specialty |
|-------|-----------|
| XSS | RU elite — RDP/VPN access sales |
| Exploit | Zero-days, malware |
| BreachForums | EN — massive DB dumps |
| Dread | EN — darknet marketplace |

### Onion Crawler

```bash
git clone https://github.com/DedSecInside/TorBot
systemctl start tor
python torbot.py -u http://example.onion --depth 2 --info
python darkdump.py --search "initial access" --count 20
```

</details>

<details>
<summary><b>Phase 5 — Cross-Analysis & Link Visualization</b></summary>

### Identity Selectors

| Type | Examples |
|------|---------|
| **Hard** (definitive) | Reused emails, phones, Apple/GAIA IDs, PGP keys |
| **Soft** (probabilistic) | Same nickname, avatar hash match, stylometry, temporal patterns |

### Avatar Hash Matching

```bash
python scripts/phase5/identity_fusion.py avatars \
    https://vk.com/photo_url https://t.me/avatar_url --threshold 10
```

```python
import imagehash
from PIL import Image
diff = imagehash.phash(Image.open("a.jpg")) - imagehash.phash(Image.open("b.jpg"))
print("SAME" if diff < 10 else "DIFFERENT")
```

### Stylometry

```bash
python scripts/phase5/identity_fusion.py stylometry \
    --files post1.txt post2.txt post3.txt
```

### Maltego Custom Transform

```python
pip install maltego-trx

@registry.register_transform(display_name='Email to Breaches',
                              input_entity='maltego.EmailAddress')
class EmailToBreaches(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request, response):
        for breach in check_email(request.Value):
            entity = response.addEntity('maltego.Phrase', breach['Name'])
            entity.addProperty('breach.date', breach['BreachDate'])
```

</details>

<details>
<summary><b>Phase 6 — Geolocation & Physical Tracking</b></summary>

### EXIF Extraction

```bash
python scripts/phase6/geo_exif.py exif photo.jpg
python scripts/phase6/geo_exif.py batch ./photos/ --output metadata.csv
exiftool -GPSLatitude -GPSLongitude -DateTimeOriginal photo.jpg
```

### IP Analysis

```bash
python scripts/phase6/geo_exif.py ip TARGET_IP
python scripts/phase6/geo_exif.py headers email_headers.txt
```

**Pipeline:** ipapi.is (geo accuracy) → ipinfo.io (VPN/proxy detect) → Shodan (open ports)

If datacenter IP detected → target is behind VPN → check for WebRTC leak

### 2026 Vector — Sec-CH-IP-Geo

Chrome 130+ sends geolocation in HTTP header. Deploy a landing page, send phishing link, collect coordinates passively.

```
Request header: Sec-CH-IP-Geo: <geolocation_data>
```

</details>

<details>
<summary><b>OPSEC — Operational Security</b></summary>

> If you leave footprints during investigation — you've already failed.

### Stack

```
Physical machine
  └── VPN (Mullvad / ProtonVPN — no-logs, paid with Monero)
       └── VM (Whonix or Tails OS)
            └── Tor Browser or hardened Firefox
                 └── Residential proxy (for Tor-blocking sites)
```

### Rules

| Rule | How |
|------|-----|
| Burn accounts | 1 target = 1 account set. Never reuse. |
| Temp email | temp-mail.org, guerrillamail.com |
| Virtual SIM | SMS-activate.org, 5sim.net |
| Payments | Monero (XMR) only |
| Fingerprint | Canvas Blocker + uBlock Origin + Random Agent Spoofer |

### Firefox Hardening

```javascript
user_pref("media.peerconnection.enabled", false);   // Kill WebRTC leak
user_pref("privacy.resistFingerprinting", true);
user_pref("toolkit.telemetry.enabled", false);
```

### Sandbox Untrusted Files

```bash
pip install cuckoo
cuckoo init && cuckoo community && cuckoo -d
cuckoo submit --timeout 120 suspicious.exe
```

Alternatives: [any.run](https://any.run) · [Dangerzone](https://dangerzone.rocks)

### Wipe Before Sharing

```bash
exiftool -all= output.jpg
mat2 document.pdf
shred -vz -n 3 /dev/sdX
```

</details>

---

## API Keys Required

| Service | Purpose | Free? |
|---------|---------|-------|
| [Telegram API](https://my.telegram.org) | Telethon recon | ✅ Free |
| [HaveIBeenPwned](https://haveibeenpwned.com/API/Key) | Breach lookup | ❌ Paid |
| [DeHashed](https://dehashed.com) | Password/leak DB | ❌ Paid |
| [Shodan](https://account.shodan.io) | Port/infra scanning | ✅ Free tier |
| [WiGLE](https://wigle.net/account) | Wi-Fi geolocation | ✅ 200 req/day |
| [Google API](https://console.cloud.google.com) | YouTube Data API | ✅ Free tier |

---

## Legal Disclaimer

This repository is for **authorized red team engagements, penetration testing, and educational research only**. Use only against targets with **explicit written permission**.

The author is not responsible for any misuse.

---

## Support

If this helped — drop a ⭐ It keeps the repo alive and updated.

**Author:** [@nvsncis](https://t.me/nvsncis)
