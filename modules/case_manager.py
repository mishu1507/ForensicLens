import os
import uuid

BASE_DIR = "uploads/cases"

def create_case():
    case_id = str(uuid.uuid4())[:8]
    case_path = os.path.join(BASE_DIR, case_id)
    os.makedirs(case_path, exist_ok=True)
    return case_id, case_path
