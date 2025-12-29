from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_report(case_id, timeline, severity, score, incident_type, file_hash):
    path = f"uploads/cases/{case_id}/forensic_report.pdf"

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        "<b>Digital Forensic Investigation Report</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Case Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    table = Table([
        ["Case ID", case_id],
        ["Incident Type", incident_type],
        ["Severity", severity],
        ["Risk Score", str(score)]
    ], colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Evidence Integrity</b>", styles["Heading2"]))
    elements.append(Paragraph(
        f"SHA-256 Evidence Hash:<br/><font size='9'>{file_hash}</font>",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("<b>Incident Timeline</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    timeline_table = [["Timestamp", "Event Type", "Description"]]

    for e in timeline:
        timeline_table.append([
            e["timestamp"],
            e["type"],
            e["raw"]
        ])

    table = Table(timeline_table, colWidths=[2*inch, 1.5*inch, 3*inch])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
    ]))

    elements.append(table)

    doc.build(elements)
