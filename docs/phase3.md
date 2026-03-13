# Phase 3 — Vectors Across Social Networks and Platforms

> **[← Back to README](../README.md)**

---

## 1. VKontakte (VK)

The API is partially open, but the best parts are buried deeper.

### Hidden Data
Basic collection includes ID, short name, phone number, email. Through VK User Bookmarklet — extract maiden name and date of birth even if hidden via privacy settings.

```python
import requests
VK_TOKEN = 'YOUR_ACCESS_TOKEN'
params = {
    'user_ids': 'target_username',
    'fields': 'id,first_name,last_name,screen_name,bdate,city,country,photo_max,contacts',
    'access_token': VK_TOKEN,
    'v': '5.199'
}
r = requests.get('https://api.vk.com/method/users.get', params=params)
print(r.json())
```

### Bypassing Limits
For mass comment collection — use Selenium/Playwright combo under an authorized fake account.

---

## 2. Telegram

Primary data source. Username = public marker. User ID = immutable digital footprint.

### Deep Parsing — Telepathy

```bash
git clone https://github.com/jordanwildon/Telepathy
cd Telepathy && pip install -r requirements.txt

# Archive entire channel
python telepathy.py -t @channelname --comprehensive --media

# Export to CSV
python telepathy.py -t @channelname --output csv

# Forward mapping (who forwarded from whom)
python telepathy.py -t @channelname --forwards
```

### Quick Recon — Telethon

```python
pip install telethon

from telethon.sync import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)

with client:
    entity = client.get_entity('@target_username')
    print(f'ID: {entity.id}')
    print(f'Name: {entity.first_name} {entity.last_name}')
    print(f'Phone: {entity.phone}')
```

Bots like `@getuserinfobot` return ID, photo, and account registration date.

---

## 3. Meta's Secured Perimeter (Instagram and Facebook)

In 2026, Meta blocks scrapers at the TLS fingerprint (SSL handshake) level and bans datacenter IPs.

### Instagram
Direct parsing works poorly. Use internal GraphQL API with correct headers.

```python
import requests
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)',
    'x-ig-app-id': '936619743392459',
    'x-asbd-id': '198387',
    'Cookie': 'sessionid=YOUR_SESSION; csrftoken=TOKEN;'
}
url = 'https://i.instagram.com/api/v1/users/web_profile_info/?username=target'
r = session.get(url, headers=headers)
data = r.json()
```

To get exact UTC time of posts instead of "2w" — use **Instagram User Profile Post Date Revealer** bookmarklet.

### Facebook
To obtain account creation date — use modified **Facebook Marketplace Profile Bookmarklet**.

---

## 4. Professional Networks (LinkedIn)

Ideal for understanding career paths and B2B connections.

### linkedin-scraper (Playwright-based)

```python
pip install linkedin-scraper

from linkedin_scraper import Person, actions
from selenium import webdriver

driver = webdriver.Chrome()
actions.login(driver, 'your_email', 'your_pass')
person = Person('https://linkedin.com/in/target', driver=driver)
print(person.name, person.company, person.job_title)
print(person.experiences)
```

**Analysis:** Changing jobs indicates geographic movements. Comments reveal actual business connections.

---

## 5. Video Platforms (YouTube and TikTok)

### YouTube

```python
pip install youtube-transcript-api google-api-python-client

# Get transcript
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript('VIDEO_ID', languages=['en', 'ru'])
text = ' '.join([t['text'] for t in transcript])

# Channel metadata — account creation date
from googleapiclient.discovery import build
yt = build('youtube', 'v3', developerKey='YOUR_API_KEY')
res = yt.channels().list(part='snippet,statistics', forUsername='TARGET').execute()
print(res['items'][0]['snippet']['publishedAt'])
```

### TikTok
API is closed — use browser automation via Playwright. For exact upload dates use **TikTok Date Revealer Bookmarklet**.

---

## Mass Username Reconnaissance (Snoop)

Searching a single nickname is the foundation of Cross-Platform Identity Correlation.

In 2026, Sherlock has been replaced by its tactical fork — **Snoop**.

```bash
git clone https://github.com/snooppr/snoop
cd snoop && pip install -r requirements.txt

# Basic search (5,300+ sites)
python3 snoop.py username_target

# Batch processing
snoop --input targets.txt --output report.json --format json

# With proxy
python3 snoop.py username_target --proxy socks5://127.0.0.1:9050

# Detect hidden emails/phones on discovered pages
python3 snoop.py username_target --parse-all
```

**Integration:** Discovered accounts are clustered, checked for password reuse in leaks (Dehashed), writing style analyzed. Matching avatars or emails across different forums = identity confirmed.

---

> **Script:** [`telegram_recon.py`](../scripts/phase3/telegram_recon.py)
