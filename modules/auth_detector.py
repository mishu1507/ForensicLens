def detect_attacks(events):
    attacks = []

    auth_fail_count = 0
    for e in events:
        if e.get("type") == "AUTH_FAIL":
            auth_fail_count += 1

    if auth_fail_count >= 5:
        attacks.append("Brute Force Login Attempt")

    for e in events:
        if e.get("type") == "USB":
            attacks.append("Unauthorized USB Usage")
            break

    for e in events:
        if e.get("type") == "FILE_COPY":
            attacks.append("Suspicious File Copy Activity")
            break

    for e in events:
        if e.get("type") == "NETWORK":
            attacks.append("Suspicious Network Communication")
            break

    return list(set(attacks))
