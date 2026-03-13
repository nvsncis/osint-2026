# Phase 1 — Primary Data Collection

> **[← Back to README](../README.md)**

Standard names and phone numbers change. Collect what stays with the target.

---

## 1. Digital Footprints

### Google GAIA ID
A numeric Google account ID. Extracted via `ghunt`. Provides a list of all devices, creation date, and a hidden phone number. Excellent for searching through breach logs.

```bash
pip install ghunt
ghunt login
ghunt email target@gmail.com
```

Output includes: GAIA ID, device list, profile photo URL, Maps contributions, creation date.

---

### Apple ID
Checked via "Find My" services (Telegram bots) or iCloudOSINT scripts using the iForgot API.

```python
import requests
url = 'https://iforgot.apple.com/password/verify/appleid'
r = requests.post(url, data={'id': 'target@email.com'})
# 200 = account exists, 404 = not found
```

---

### Android ID / Advertising ID
Searched for in tracking company leaks via Dehashed.

```bash
curl -s -H 'Authorization: Basic BASE64CREDS' \
  'https://api.dehashed.com/search?query=android_id:XXXX&size=10'
```

---

### BSSID and MAC Addresses
If a router with active WiFi is visible in a target's photo, its BSSID is run through WiGLE.net database to find historical locations.

```python
import requests
headers = {'Authorization': 'Basic BASE64(user:apitoken)'}
r = requests.get('https://api.wigle.net/api/v2/network/search?netid=AA:BB:CC:DD:EE:FF', headers=headers)
print(r.json()['results'])
```

---

## 2. Current Toolset (2026)

### Browser Automation
Use Playwright over Selenium — more efficient and harder to fingerprint.

```bash
pip install playwright playwright-stealth
playwright install chromium
```

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    await stealth_async(page)
    await page.goto('https://target.com')
```

### Collection Automation

```bash
# SpiderFoot
git clone https://github.com/smicallef/spiderfoot
cd spiderfoot && pip install -r requirements.txt
python sf.py -l 127.0.0.1:5001
python sf.py -s TARGET_DOMAIN -t INTERNET_NAME -m sfp_whois,sfp_dns,sfp_shodan -o table

# Recon-ng
recon-ng
> workspaces create TARGET
> marketplace install all
> modules load recon/domains-hosts/hackertarget
> options set SOURCE target.com
> run
```

### AI Agents
Commercial Penligent.ai or configured AutoGPT for autonomous parsing of contacts from forums.

---

## 3. Synthetic Identity (Legend Creation / Backstopping)

### Visuals and Voice
Photos purchased on Generated Photos. AI avatars from HeyGen or Synthesia for video calls. Voice cloned via ElevenLabs.

| Tool | Link |
|------|------|
| Generated Photos | https://generated.photos |
| HeyGen | https://heygen.com |
| ElevenLabs | https://elevenlabs.io |

**Account warm-up automation:**

```python
import asyncio, random
from playwright.async_api import async_playwright

async def warmup(page, actions=50):
    for _ in range(actions):
        await page.mouse.move(random.randint(0,1280), random.randint(0,720))
        await asyncio.sleep(random.uniform(1.5, 4.0))
        await page.evaluate(f'window.scrollBy(0, {random.randint(100,400)})')
```

### Physical Sector
If office infiltration is planned, badges and IDs are designed in Photoshop/Canva, uniforms purchased on classified ad boards.

---

> **Scripts:** [`gaia_lookup.py`](../scripts/phase1/gaia_lookup.py) · [`account_warmup.py`](../scripts/phase1/account_warmup.py)
