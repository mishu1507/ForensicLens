from collections import defaultdict

def detect_auth_attacks(events):
    failures = defaultdict(int)
    attacks = []

    for e in events:
        if e["type"] == "AUTH_FAIL":
            key = e.get("ip") or e.get("user") or "unknown"
            failures[key] += 1

    for k, v in failures.items():
        if v >= 5:
            attacks.append("Brute Force Login Attempt")

    return attacks
