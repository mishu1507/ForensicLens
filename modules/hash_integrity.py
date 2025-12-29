import hashlib

def compute_hash(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def compute_hash_from_string(data):
    h = hashlib.sha256()
    h.update(data.encode())
    return h.hexdigest()
