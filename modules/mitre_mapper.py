def map_mitre(events):
    techniques = []

    for e in events:
        if e["type"] == "AUTH_FAIL":
            techniques.append("T1110 – Brute Force")

        if e["type"] == "USB":
            techniques.append("T1092 – Peripheral Device Discovery")

        if e["type"] == "NETWORK":
            techniques.append("T1041 – Exfiltration Over C2")

    return list(set(techniques))
