# Phase 2 — Search Engines, Archives & Google Dork

> **[← Back to README](../README.md)**

---

## 1. Archive Analysis (Wayback Machine and archive.today)

Archives allow you to find deleted admin panels or contacts hidden from live sites.

### Wayback Machine — CDX API Bulk Retrieval

```bash
pip install waybackpy waybackpack

# Download all historical snapshots
waybackpack target.com -d ./snapshots --from-date 20220101 --to-date 20261231
```

```python
import requests
url = 'http://web.archive.org/cdx/search/cdx'
params = {
    'url': 'target.com/*',
    'output': 'json',
    'fl': 'timestamp,original,statuscode',
    'filter': 'statuscode:200',
    'limit': '500'
}
r = requests.get(url, params=params)
for snap in r.json()[1:]:  # skip header
    print(snap)
```

### archive.today
Excellent for saving "witness" pages — saves content without executing JavaScript.

```python
import requests
def archive_page(url):
    r = requests.post('https://archive.ph/submit/',
        data={'url': url},
        headers={'User-Agent': 'Mozilla/5.0'})
    return r.url  # returns redirect to archived URL
```

---

## 2. Open Directories and Clouds

### Directory Dorking

```
-inurl:(htm|html|php) intitle:"index of" "last modified" "parent directory"
intitle:"index of" (backup|dump|db|sql|config)
intitle:"index of" "passwords.txt"
intitle:"index of" ".env"
```

**OpenDirectory Downloader:**
```bash
git clone https://github.com/KoalaBear84/OpenDirectoryDownloader
./OpenDirectoryDownloader --url 'http://target.com/opendir/' --threads 5
```

### Cloud Searching

```
site:drive.google.com "target company"
site:yadi.sk "target name"
site:docs.google.com inurl:/spreadsheets "confidential"
site:onedrive.live.com "target.com"
```

### Large-Scale Analysis (2026)
Index all downloaded files locally (Apache Tika, Recoll) for instant full-text searching.

```bash
# Extract emails, phones, URLs from any dump
bulk_extractor -o output_dir/ -x all -e email -e phone -e url dump.img

# YARA scan for API keys
yara rules/api_keys.yar ./dump_folder/ -r
```

---

## 3. Advanced Google Dorking and Automation

| Operator | Core Function | Example |
|----------|--------------|---------|
| `site:` | Limit to domain/TLD | `site:github.com "password"` |
| `inurl:` | String in URL | `inurl:admin_panel` |
| `intitle:` | String in `<title>` | `intitle:"index of" "backup"` |
| `intext:` | Body text only | `intext:"strictly confidential"` |
| `filetype:` | Exact file extension | `filetype:env "DB_USER"` |
| `-` | Exclude | `"target name" -site:linkedin.com` |
| `""` | Exact phrase | `"internal use only"` |
| `*` | Wildcard | `"API key * exposed"` |
| `..` | Numeric range | `vulnerable version 1.0..2.5` |
| `before:/after:` | Date range (YYYY-MM-DD) | `site:target.com after:2025-01-01` |

**Critical data dorks:**
```
filetype:env "DB_PASSWORD"
inurl:".php?id="
intitle:"index of" "passwords.txt"
filetype:sql "INSERT INTO" "users"
filetype:log "username" "password"
inurl:"wp-config.php" filetype:txt
```

### Bypassing Google IP Bans

```bash
pip install pagodo fake-useragent 2captcha-python

python pagodo.py -d target.com -g dorks/all.txt \
    --proxy socks5://user:pass@proxy_host:1080 \
    --delay 7 --maxresults 100
```

```python
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': ua.random}
```

**2captcha integration:**
```python
from twocaptcha import TwoCaptcha
solver = TwoCaptcha('YOUR_2CAPTCHA_API_KEY')
result = solver.recaptcha(sitekey='SITE_KEY', url='https://target.com')
captcha_token = result['code']
```

---

> **Script:** [`archive_recon.py`](../scripts/phase2/archive_recon.py)
