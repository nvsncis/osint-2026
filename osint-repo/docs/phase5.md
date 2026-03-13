# Phase 5 — Cross-Analysis and Link Visualization

> **[← Back to README](../README.md)**

It is not enough to collect a mountain of raw data. It must be consolidated into a single graph, filtering out false correlations (e.g., namesakes).

---

## 1. Identity Fusion

Combine OSINT and breach data.

| Selector Type | Examples |
|--------------|---------|
| **Hard** (definitive) | Reused emails, phone numbers, Apple/GAIA IDs, PGP keys |
| **Soft** (probabilistic) | Identical nicknames, avatar hashes, stylometry, temporal patterns |

### Avatar Hash Matching (Perceptual Hash)

```python
pip install imagehash Pillow requests

import imagehash
from PIL import Image
import requests
from io import BytesIO

def get_phash(url):
    r = requests.get(url, timeout=5)
    img = Image.open(BytesIO(r.content))
    return imagehash.phash(img)

# Compare avatars from different platforms
hash1 = get_phash('https://vk.com/photo_url')
hash2 = get_phash('https://t.me/avatar_url')
diff = hash1 - hash2  # < 10 = likely same image
print(f'Hash diff: {diff} — {"MATCH" if diff < 10 else "DIFFERENT"}')
```

---

## 2. Automation Toolset

### Snoop
Asynchronously searches username across 5,300+ sites. Detects hidden emails and phones on discovered pages.

See full usage in [Phase 3](phase3.md#mass-username-reconnaissance-snoop).

### ThreatNG (Commercial)
Generates variations of corporate domains and finds links to ransomware operations.

---

## 3. Graph Building (Maltego)

Maltego remains the standard. Operates on entity relationships (Person, Domain, IP) and transforms.

### Custom Python Transform

For closed corporate databases or logs — spin up your own private Transform Hub via Docker.

```bash
pip install maltego-trx
```

```python
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

@registry.register_transform(display_name='Email to Breaches',
                              input_entity='maltego.EmailAddress',
                              description='Check email in breach databases')
class EmailToBreaches(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        email = request.Value
        breaches = check_email(email)
        for breach in breaches:
            entity = response.addEntity('maltego.Phrase', breach['Name'])
            entity.addProperty('breach.date', breach['BreachDate'])
```

### The Analyst's Task
Find **"bridge identifiers"** — nodes that connect different clusters (e.g., a work email and a personal crypto wallet) into a single digital identity.

---

> **Script:** [`identity_fusion.py`](../scripts/phase5/identity_fusion.py)
