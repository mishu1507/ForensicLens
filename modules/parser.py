import re

def parse_logs(file_path):
    events = []

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Try to extract timestamp
            ts_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            timestamp = ts_match.group(1) if ts_match else "UNKNOWN_TIME"

            message = line.lower()
            event_type = "OTHER"

            # -------- AUTH --------
            if any(x in message for x in [
                "failed login",
                "failed password",
                "authentication failure",
                "login failed"
            ]):
                event_type = "AUTH_FAIL"

            elif any(x in message for x in [
                "login successful",
                "logged in successfully"
            ]):
                event_type = "AUTH_SUCCESS"

            # -------- USB --------
            elif "usb" in message and any(x in message for x in ["insert", "mount"]):
                event_type = "USB"

            # -------- FILE --------
            elif any(x in message for x in ["file uploaded", "file copied"]):
                event_type = "FILE_COPY"

            elif any(x in message for x in ["file deleted"]):
                event_type = "FILE_DELETE"

            # -------- NETWORK --------
            elif any(x in message for x in [
                "external ip",
                "outbound connection",
                "connection to"
            ]):
                event_type = "NETWORK"

            # Extract user & IP
            user = None
            ip = None

            u = re.search(r"user(name)?=([a-zA-Z0-9_]+)", message)
            i = re.search(r"ip=([\d\.]+)", message)

            if u:
                user = u.group(2)
            if i:
                ip = i.group(1)

            events.append({
                "timestamp": timestamp,
                "type": event_type,
                "raw": line,
                "user": user,
                "ip": ip
            })

    return events
