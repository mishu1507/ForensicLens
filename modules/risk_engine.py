def calculate_risk(events, attacks):
    score = 0

    for e in events:
        if e["type"] == "AUTH_FAIL":
            score += 2
        elif e["type"] == "NETWORK":
            score += 3
        elif e["type"] == "USB":
            score += 2
        elif e["type"] == "FILE_COPY":
            score += 3

    score += len(attacks) * 5

    if score >= 20:
        severity = "High"
    elif score >= 10:
        severity = "Medium"
    else:
        severity = "Low"

    return score, severity
