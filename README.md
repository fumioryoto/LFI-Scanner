***🔍 LFI Scanner (Nuclei + Python Runner)***
![Alt text for the screenshot](/Assets/Screenshot.png)

A scalable Local File Inclusion (LFI) detection setup using:

Nuclei for accurate vulnerability detection

Python CLI runner for:

Live progress UI

Payload timing & ETA

External payload loading (thousands supported)

Clean hit logging

Designed and tuned for Apache + mod_security environments.

***✨ Features***

📁 External payload file support (unlimited size)

📊 Real-time progress bar (payload count, timing, ETA)

⏱️ Per-payload execution timing

🎯 Logs only valid LFI hits

🛡️ Apache + mod_security friendly defaults

🔁 No inline payloads (clean & reusable templates)

🧠 Nuclei handles detection logic, Python handles UI

📦 Requirements

***Python 3.8+***

**Nuclei v2 / v3**

*tqdm Python module*

**Install dependencies:**
```bash
pip install tqdm
```

Verify nuclei:
```bash
nuclei -version
```
```bash
***📁 Project Structure***
.
├── lfi.yaml            # Nuclei LFI detection template
├── lfi_runner.py       # Python CLI runner with UI
├── lfi-payload.txt     # External LFI payload list
├── lfi-hits.txt        # Output file (auto-created)
└── README.md
```
**🧪 lfi.yaml (Nuclei Template)**

=> Uses external payload injection

=> Optimized for low false positives

=> Stops on first valid LFI match per payload

=> Supports common LFI parameters:

=> file

=> page

=> include

=> path

Payloads are passed dynamically using:
```bash
{{lfi}}
```
***🚀 lfi_runner.py (Python CLI Runner)***

*The runner:*

=> Loads payloads from a .txt file

=> Executes Nuclei per payload

=> Displays:

=> Progress bar

=> Execution time

=> Estimated time remaining

=> Saves only confirmed hits

▶️ Usage
Basic command
python3 lfi_runner.py -u https://example.com -l lfi-payload.txt

Full options
```bash
git clone https://github.com/fumioryoto/LFI-Scanner.git
cd LFI-Scanner/
python3 lfi_runner.py -u https://example.com -l lfi-payload.txt -t lfi.yaml -o results.txt
```
Arguments
Flag	Description
-u	Target URL
-l	Payload file (one payload per line)
-t	Nuclei template (default: lfi.yaml)
-o	Output file for hits
📄 Payload File Format

lfi-payload.txt

../etc/passwd
..%2fetc%2fpasswd
.%2e/%2e%2e/etc/passwd
..;/etc/passwd
..%252fetc%252fpasswd


✔ Supports thousands of payloads
✔ Encoded, obfuscated, mixed traversal allowed

🧾 Output Example

Terminal:
```bash
LFI Scan:  312/2000 [=====>----] 15% | time=0.41s | ETA 00:04:12
[HIT] ..%2fetc%2fpasswd (0.38s)
```

Saved to lfi-hits.txt:
```bash
[..%2fetc%2fpasswd] https://example.com/?file=..%2fetc%2fpasswd
```
***🛡️ Apache + mod_security Tuning***

Defaults are tuned to reduce WAF blocks:

Low concurrency

Rate limiting

Browser-like headers

No aggressive payload bursts

***You can adjust safely inside lfi_runner.py:***

CONCURRENCY = "10"
RATE_LIMIT  = "15"
TIMEOUT     = "7"

***⚠️ Important Notes***

This tool does not magically bypass WAFs

Payload effectiveness depends on:

Server configuration

PHP version

mod_security ruleset

php://input requires POST-based template

%00 payloads only work on very old PHP

***🧠 Recommended Workflow***

Recon parameters (ParamSpider, manual review)

Run low-noise payloads first

Review hits

Run high-noise payloads only if needed

Manually verify confirmed LFI paths

***📜 Legal Disclaimer***

This tool is intended for authorized security testing only.
Do NOT scan systems without explicit permission.

The author is not responsible for misuse.

***🔥 Future Extensions (Optional)***

POST-based LFI (php://input)

LFI → log poisoning → RCE chain

Windows LFI template

Automatic payload categorization

Auto-pause on WAF detection
