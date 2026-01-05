# 🔐 ForensicLens – Automated Digital Forensics & Incident Reconstruction System

ForensicLens is a web-based digital forensics platform designed to automate post-incident investigations. The system analyzes authentication, system, USB, and network logs to reconstruct incident timelines, detect attacks, assess severity, and generate professional forensic reports.


## 🚀 Features

- 🔍 Multi-log analysis (authentication, system, USB, network logs)
- 🧠 Brute force attack detection
- 🕒 Incident timeline reconstruction
- 📊 Risk scoring and severity classification
- 🧾 Dynamic, evidence-driven attack narrative generation
- 📄 Automated PDF forensic report generation
- 🎨 Interactive dashboard with visualizations


## 🛠️ Technology Stack

| Component       | Technology            |
|-----------------|-----------------------|
| Backend         | Python                |
| Web Framework   | Flask                 |
| Frontend        | HTML, CSS, JavaScript |
| Visualization   | Chart.js              |
| PDF Reports     | ReportLab             |
| Security        | SHA-256 hashing       |



## 📁 Project Structure
FORENSICLENS/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│ ├── parser.py
│ ├── auth_detector.py
│ ├── risk_engine.py
│ ├── incident_analyzer.py
│ ├── narrative_generator.py
│ ├── report_generator.py
│
├── templates/
│ ├── index.html
│ ├── dashboard.html
│
├── static/
│ └── style.css
│
├── uploads/
│ └── cases/



## ⚙️ Installation & Setup

 Clone or download the project

git clone <repository-url>
cd ForensicLens

pip install -r requirements.txt
Run the application

python app.py
Open the application in your browser

http://127.0.0.1:5000