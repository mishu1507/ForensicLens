from modules.auth_detector import detect_auth_attacks

def calculate_risk(events):
    score = 0
    reasons = []
    attacks = detect_auth_attacks(events)

    # ---- Authentication attacks ----
    if "Brute Force Login Attempt" in attacks:
        score += 7
        reasons.append("Multiple failed authentication attempts indicate a brute force attack")

    # ---- Event-based scoring ----
    for e in events:
        if e["type"] == "USB":
            score += 3
            reasons.append("Unauthorized USB device usage detected")

        elif e["type"] == "FILE_COPY":
            score += 4
            reasons.append("Sensitive file copy activity detected")

        elif e["type"] == "FILE_DELETE":
            score += 3
            reasons.append("File deletion activity detected")

        elif e["type"] == "NETWORK":
            score += 5
            reasons.append("Suspicious outbound network communication detected")

    # Remove duplicate reasons
    reasons = list(set(reasons))

    return score, reasons, attacks
