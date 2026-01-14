#!/usr/bin/env python3
# LFi Scanner With Nuclei template.
###############################################################################
#Author  : Nahid
#Telegram: t.me/fumioryoto
#Web     : https://fumioryoto.github.io/
###############################################################################
import argparse
import subprocess
import time
from pathlib import Path
from tqdm import tqdm

# ================= DEFAULTS =================
DEFAULT_TEMPLATE = "lfi.yaml"
DEFAULT_OUTPUT = "lfi-hits.txt"
CONCURRENCY = "10"
RATE_LIMIT = "15"
TIMEOUT = "7"

HEADERS = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept: text/html,application/xhtml+xml",
    "Accept-Language: en-US,en;q=0.9",
]
# ============================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Nuclei LFI runner with progress UI (external payload file)"
    )
    parser.add_argument(
        "-u", "--url", required=True, help="Target URL (https://example.com)"
    )
    parser.add_argument(
        "-l", "--list", required=True, help="Payload file (one payload per line)"
    )
    parser.add_argument(
        "-t", "--template", default=DEFAULT_TEMPLATE, help="Nuclei template file"
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT, help="File to save hits"
    )
    return parser.parse_args()


def load_payloads(file_path):
    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            payload = line.strip()
            if payload:
                yield payload


def run_nuclei(target, template, payload):
    cmd = [
        "nuclei",
        "-u", target,
        "-t", template,
        "-var", f"lfi_payloads={payload}",
        "-c", CONCURRENCY,
        "-rl", RATE_LIMIT,
        "-timeout", TIMEOUT,
        "-retries", "0",
        "-silent",
        "-nc"
    ]

    for h in HEADERS:
        cmd.extend(["-H", h])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def main():
    args = parse_args()

    if not Path(args.list).exists():
        print(f"[!] Payload file not found: {args.list}")
        return

    payloads = list(load_payloads(args.list))
    total = len(payloads)

    if total == 0:
        print("[!] Payload file is empty")
        return

    print(f"[+] Target   : {args.url}")
    print(f"[+] Payloads : {total}")
    print(f"[+] Template : {args.template}\n")

    start_all = time.time()

    with tqdm(total=total, desc="LFI Scan", unit="payload") as pbar:
        for payload in payloads:
            start = time.time()
            output = run_nuclei(args.url, args.template, payload)
            elapsed = round(time.time() - start, 2)

            if output:
                with open(args.output, "a") as f:
                    f.write(f"[{payload}] {output}\n")
                tqdm.write(f"[HIT] {payload} ({elapsed}s)")

            pbar.set_postfix(time=f"{elapsed}s")
            pbar.update(1)

    total_time = round(time.time() - start_all, 2)
    print(f"\n[✔] Finished in {total_time}s")
    print(f"[✔] Hits saved to {args.output}")


if __name__ == "__main__":
    main()
