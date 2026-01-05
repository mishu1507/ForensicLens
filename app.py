from flask import (
    Flask, render_template, request,
    redirect, url_for, session,
    make_response
)
import os
import uuid

from modules.workspace_manager import create_workspace, cleanup_workspace
from modules.parser import parse_logs
from modules.auth_detector import detect_attacks
from modules.incident_analyzer import classify_incident
from modules.risk_engine import calculate_risk
from modules.timeline import build_timeline
from modules.narrative_generator import generate_narrative
from modules.report_generator import generate_report
from modules.hash_integrity import calculate_hashes

app = Flask(__name__)
app.secret_key = "forensiclens-secret-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    workspace = create_workspace()
    case_id = str(uuid.uuid4())

    uploaded_files = request.files.getlist("logfiles")
    log_paths = []

    for f in uploaded_files:
        path = os.path.join(workspace, f.filename)
        f.save(path)
        log_paths.append(path)

    events = parse_logs(log_paths)
    attacks = detect_attacks(events)
    incident_type = classify_incident(events, attacks)
    risk_score, severity = calculate_risk(events, attacks)
    timeline = build_timeline(events)
    narrative = generate_narrative(timeline, incident_type, severity, attacks)
    file_hashes = calculate_hashes(log_paths)

    session[case_id] = {
        "workspace": workspace,
        "incident_type": incident_type,
        "risk_score": risk_score,
        "severity": severity,
        "timeline": timeline,
        "narrative": narrative,
        "file_hashes": file_hashes,
        "attacks": attacks
    }

    session["current_case"] = case_id
    return redirect(url_for("chain_of_custody"))


@app.route("/chain-of-custody", methods=["GET", "POST"])
def chain_of_custody():
    if request.method == "POST":
        session["investigator_name"] = request.form["investigator_name"]
        session["investigator_id"] = request.form["investigator_id"]
        session["organization"] = request.form["organization"]

        case_id = session.get("current_case")
        return redirect(url_for("dashboard", case_id=case_id))

    return render_template("chain_of_custody.html")


@app.route("/dashboard/<case_id>")
def dashboard(case_id):
    data = session.get(case_id)
    if not data:
        return redirect(url_for("index"))

    return render_template(
        "dashboard.html",
        case_id=case_id,
        incident_type=data["incident_type"],
        severity=data["severity"],
        risk_score=data["risk_score"],
        timeline=data["timeline"],
        narrative=data["narrative"],
        report_file="Forensic_Report.pdf"
    )


@app.route("/download/<case_id>")
def download(case_id):
    data = session.get(case_id)
    if not data:
        return "Session expired", 404

    report_path = generate_report(
        data["workspace"],
        case_id,
        session.get("investigator_name", "Unknown"),
        session.get("investigator_id", "N/A"),
        session.get("organization", "N/A"),
        data["file_hashes"],
        data["incident_type"],
        data["attacks"],
        data["timeline"],
        data["risk_score"],
        data["severity"],
        data["narrative"]
    )

    with open(report_path, "rb") as f:
        pdf_bytes = f.read()

    cleanup_workspace(data["workspace"])
    session.pop(case_id, None)

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="Forensic_Report_{case_id}.pdf"'
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
