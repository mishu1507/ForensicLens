def generate_narrative(timeline, incident_type, attacks):
    if not timeline:
        return "No suspicious activity was detected during the investigation."

    event_types = [e["type"] for e in timeline]
    narrative = []

    narrative.append(
        f"The forensic investigation identified a {incident_type.lower()} "
        "based on correlated analysis of uploaded log evidence."
    )

    if "AUTH_FAIL" in event_types:
        narrative.append(
            f"{event_types.count('AUTH_FAIL')} failed authentication attempts were observed."
        )

    if "AUTH_SUCCESS" in event_types and "AUTH_FAIL" in event_types:
        narrative.append(
            "A successful login following failed attempts suggests possible credential compromise."
        )

    if "USB" in event_types:
        narrative.append("Unauthorized USB device usage was detected.")

    if "FILE_COPY" in event_types:
        narrative.append("Sensitive file copy activity indicates potential data staging.")

    if "FILE_DELETE" in event_types:
        narrative.append("File deletion activity suggests possible trace removal.")

    if "NETWORK" in event_types:
        narrative.append("Outbound network communication raises concerns of data exfiltration.")

    if attacks:
        narrative.append(
            "Detected attack patterns include: " + ", ".join(attacks) + "."
        )

    narrative.append(
        f"The activity timeline began at {timeline[0]['timestamp']} "
        "and shows escalation rather than isolated events."
    )

    return " ".join(narrative)
