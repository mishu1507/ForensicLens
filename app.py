from flask import Flask, render_template, request, send_from_directory
import os

from modules.case_manager import create_case
from modules.hash_integrity import compute_hash, compute_hash_from_string
from modules.parser import parse_logs
from modules.timeline import build_timeline
from modules.risk_engine import calculate_risk
from modules.severity_explainer import determine_severity
from modules.incident_analyzer import classify_incident
from modules.narrative_generator import generate_narrative
from modules.report_generator import generate_report

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("logfiles")
    case_id, case_path = create_case()

    all_events = []
    combined_hash = ""

    for file in files:
        path = os.path.join(case_path, file.filename)
        file.save(path)
        combined_hash += compute_hash(path)
        all_events.extend(parse_logs(path))

    final_hash = compute_hash_from_string(combined_hash)

    timeline = build_timeline(all_events)
    risk_score, reasons, attacks = calculate_risk(timeline)
    severity = determine_severity(risk_score)
    incident_type = classify_incident(timeline, attacks)
    narrative = generate_narrative(timeline, incident_type, attacks)

    generate_report(case_id, timeline, severity, risk_score, incident_type, final_hash)

    return render_template(
        "dashboard.html",
        case_id=case_id,
        timeline=timeline,
        risk_score=risk_score,
        severity=severity,
        incident_type=incident_type,
        narrative=narrative,
        attacks=attacks,
        report_file="forensic_report.pdf"
    )

@app.route("/download/<case_id>/<filename>")
def download(case_id, filename):
    return send_from_directory(f"uploads/cases/{case_id}", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
