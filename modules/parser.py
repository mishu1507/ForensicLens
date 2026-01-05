import re
import os

def parse_logs(file_paths):
    events = []

    for file_path in file_paths:
        with open(file_path, "r", errors="ignore") as f:
            for line in f:
                raw_line = line.strip()
                if not raw_line:
                    continue

                ts_match = re.search(
                    r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)",
                    raw_line
                )

                timestamp = ts_match.group(1) if ts_match else "UNKNOWN_TIME"

                message = raw_line.lower()
                event_type = "OTHER"

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

                elif "usb" in message and any(x in message for x in ["insert", "inserted", "mount"]):
                    event_type = "USB"

                elif "file copied" in message or "file copied from" in message:
                    event_type = "FILE_COPY"

                elif "file deleted" in message:
                    event_type = "FILE_DELETE"

                elif any(x in message for x in [
                    "external ip",
                    "outbound connection",
                    "connection to"
                ]):
                    event_type = "NETWORK"

                user = None
                ip = None

                u = re.search(r"user=([a-zA-Z0-9_.-]+)", message)
                i = re.search(r"ip=([\d\.]+)", message)

                if u:
                    user = u.group(1)
                if i:
                    ip = i.group(1)

                events.append({
                    "timestamp": timestamp,
                    "type": event_type,
                    "raw": raw_line,
                    "user": user,
                    "ip": ip,
                    "source_file": os.path.basename(file_path)
                })

    return events
