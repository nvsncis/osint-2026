# Phase 6 — Geolocation Data and Physical Tracking

> **[← Back to README](../README.md)**

---

## 1. Geotags and Metadata (EXIF)

Most social networks strip metadata upon upload, but loopholes remain.

**Where to look:** Telegram (file sent as document), original photos from cloud drives, backups, forums.

**What we extract:** GPS coordinates, altitude, shooting azimuth, exact time, device specs.

```bash
# Install
apt install exiftool

# Extract all metadata
exiftool -a -u -g1 photo.jpg

# Extract GPS only
exiftool -GPSLatitude -GPSLongitude -GPSAltitude photo.jpg

# Batch extract from folder → CSV
exiftool -csv -r ./photos/ > metadata.csv
```

```python
pip install pyexiftool

import exiftool
with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata('photo.jpg')
    lat = metadata[0].get('EXIF:GPSLatitude')
    lon = metadata[0].get('EXIF:GPSLongitude')
    print(f'https://maps.google.com/?q={lat},{lon}')
```

**Bypassing hidden dates:** For Instagram use **Instagram Date Revealer** bookmarklets — show exact UTC time instead of "2 weeks ago".

---

## 2. Wi-Fi Reconnaissance (WiGLE.net)

WiGLE is the largest crowdsourced database with 2+ billion records of Wi-Fi hotspots, Bluetooth devices, and cell towers.

- **Router search:** If you have BSSID of the target's home/work router (from screenshot or leak) — WiGLE provides exact historical coordinates.
- **Bluetooth footprints:** Smartwatches, IoT devices, medical equipment broadcast MAC addresses.
- **Practice:** Free API = 200 requests/day. Integrate with WiFi Pineapple for real-time interception.

```python
import requests, base64

creds = base64.b64encode(f'{WIGLE_USER}:{WIGLE_TOKEN}'.encode()).decode()
headers = {'Authorization': f'Basic {creds}', 'Accept': 'application/json'}

def lookup_bssid(bssid):
    r = requests.get('https://api.wigle.net/api/v2/network/search',
                     headers=headers, params={'netid': bssid, 'onlymine': 'false'})
    for net in r.json().get('results', []):
        print(f"SSID: {net['ssid']} | Location: {net['trilat']}, {net['trilong']} | Last seen: {net['lasttime']}")

lookup_bssid('AA:BB:CC:DD:EE:FF')
```

---

## 3. IP Geolocation and New Methods

Standard IP tracking often lies due to VPNs, CDNs, and mobile networks.

### TSG (Temporal-Spatial Correlation)
New algorithms reduced error margin by 72% (median ~1.68 km). Top databases (MaxMind, ipapi) now bind IP to a specific neighborhood.

### Triangulation (Active Probing)
By measuring RTT (ping time) from different servers to the target, calculate the radius of its location.
> Rough calculation over fiber optics: **1 ms ping ≈ 100 km distance**

### HTTP Headers — 2026 Vector
The new **Sec-CH-IP-Geo** standard (Chrome 130+) allows the browser to send geolocation to the server in the header. Deploy your own site, send link to target, extract coordinates without additional requests.

### Combat IP Analysis

```python
import requests

def analyze_ip(ip):
    # ipapi.is — high accuracy geolocation
    r1 = requests.get(f'https://ipapi.is/json/?ip={ip}')
    geo = r1.json()

    # ipinfo.io — VPN/proxy/datacenter detection
    r2 = requests.get(f'https://ipinfo.io/{ip}/json')
    info = r2.json()

    # Shodan — open ports
    import shodan
    api = shodan.Shodan('YOUR_SHODAN_KEY')
    try:
        host = api.host(ip)
        print(f"Open ports: {host.get('ports')}")
    except shodan.APIError as e:
        print(e)

    if geo.get('is_datacenter'):
        print('[!] Datacenter IP — target is behind VPN. Check for WebRTC leak.')
    else:
        print(f"[+] ISP: {info.get('org')}")
        print(f"[+] Location: {info.get('city')}, {info.get('region')}")
```

**Pipeline:**
1. Collect IPs from email headers (`X-Originating-IP`) or server logs
2. Run through ipapi.is (accuracy) + ipinfo.io (VPN detection) + Shodan (ports)
3. If datacenter → look for real IP via WebRTC leaks
4. If mobile IP → run through cell tower databases (OpenCellID)
5. Cross-reference with WiGLE for final confirmation

---

> **Script:** [`geo_exif.py`](../scripts/phase6/geo_exif.py)
