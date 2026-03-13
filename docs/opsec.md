# OPSEC — Operational Security for the Researcher

> **[← Back to README](../README.md)**

> A section often missing from OSINT guides but critical for anyone doing real work.
> **If you leave digital footprints during investigation — you've already failed.**

---

## 1. Infrastructure Setup

### Minimum Viable Stack

```
Physical machine
  └── VPN (Mullvad or ProtonVPN — no-logs, paid with crypto)
       └── VM (Whonix / Tails OS)
            └── Tor Browser or hardened Firefox
                 └── Residential proxy (for sites blocking Tor)
```

### VM Isolation
- **Whonix** — routes all traffic through Tor automatically
- **Tails** — amnesic OS, leaves no trace on disk after shutdown

```bash
# Whonix via VirtualBox
# Download from https://www.whonix.org/wiki/VirtualBox
# Import both Whonix-Gateway and Whonix-Workstation OVA
# All traffic from Workstation routes through Gateway (Tor)
# Never install personal software on Workstation
```

---

## 2. Account & Identity Hygiene

| Rule | Implementation |
|------|---------------|
| Burn accounts | 1 target = 1 account set. Never reuse. |
| Temp email | temp-mail.org, guerrillamail.com |
| Virtual SIM | SMS-activate.org, 5sim.net for OTP verification |
| Payments | Monero (XMR) — never link credit card to OSINT infrastructure |
| Browser fingerprint | Canvas Blocker + uBlock Origin + Random Agent Spoofer |

### Firefox Hardening (user.js)

```javascript
// Disable WebRTC — leaks real IP even through VPN
user_pref("media.peerconnection.enabled", false);

// Resist fingerprinting — spoofs timezone, canvas, fonts
user_pref("privacy.resistFingerprinting", true);

// Block canvas fingerprinting
user_pref("privacy.resistFingerprinting.block_mozAddonManager", true);

// Disable telemetry
user_pref("toolkit.telemetry.enabled", false);
```

---

## 3. Sandbox for Malware-Infected Files

Darknet databases and Telegram leak files are frequently laced with infostealers.

**Never open untrusted files on your main machine.**

| Tool | Type | Link |
|------|------|------|
| Any.run | Online interactive sandbox | https://any.run |
| Cuckoo Sandbox | Self-hosted | https://cuckoosandbox.org |
| Dangerzone | Converts doc → safe PDF | https://dangerzone.rocks |

```bash
# Cuckoo Sandbox setup
pip install cuckoo
cuckoo init && cuckoo community
cuckoo -d  # start daemon

# Submit file for analysis
cuckoo submit --timeout 120 suspicious_file.exe

# View report
cuckoo web -H 127.0.0.1 -p 8080
```

---

## 4. Log & Trail Minimization

- Clear browser history, cookies, DNS cache after every session
- Use RAM-disk for temporary files (`tmpfs` on Linux)
- Wipe metadata from any files you create before sharing

```bash
# Strip all metadata from images
exiftool -all= output.jpg

# Strip metadata from PDF
mat2 document.pdf

# Wipe free disk space (Linux)
shred -vz -n 3 /dev/sdX
```

---

> **OPSEC is not paranoia — it is discipline. A single slip exposes the entire operation and potentially the operator.**
