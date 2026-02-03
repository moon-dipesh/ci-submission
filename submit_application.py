import os
import json
import hmac
import hashlib
import datetime
import requests

# Read & sanitize env vars
NAME = os.environ["NAME"].strip()
EMAIL = os.environ["EMAIL"].strip()
RESUME_LINK = os.environ["RESUME_LINK"].strip()
REPOSITORY_LINK = os.environ["REPOSITORY_LINK"].strip()
ACTION_RUN_LINK = os.environ["ACTION_RUN_LINK"].strip()
SIGNING_SECRET = os.environ["SIGNING_SECRET"].strip().encode("utf-8")

ENDPOINT = "https://b12.io/apply/submission"

# ISO 8601 UTC timestamp
timestamp = datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

payload = {
    "timestamp": timestamp,
    "name": NAME,
    "email": EMAIL,
    "resume_link": RESUME_LINK,
    "repository_link": REPOSITORY_LINK,
    "action_run_link": ACTION_RUN_LINK,
}

# Canonical JSON (THIS MUST NOT CHANGE)
body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

# HMAC-SHA256 signature
digest = hmac.new(
    SIGNING_SECRET,
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": str(len(body)),
    "X-Signature-256": f"sha256={digest}",
}

response = requests.post(
    ENDPOINT,
    data=body,
    headers=headers,
    timeout=30,
)

response.raise_for_status()

print("Receipt:", response.json()["receipt"])
