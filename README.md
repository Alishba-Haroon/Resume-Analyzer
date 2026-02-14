## Resume Analyzer

AI-powered Resume Analyzer built with Flask that evaluates resumes, extracts skills, matches them with job requirements, and provides insights for ATS optimization.

## 🚀 Features

* Resume upload (PDF/DOCX support)

* Automatic skill extraction using NLP

* Job-skill matching system

* Resume scoring logic

* History tracking of analyzed resumes

* Clean UI with Flask templates

## 🛠 Tech Stack

**Backend**: Python, Flask

**Database**: SQLite

**NLP Processing**: Custom skill extractor

**Frontend**: HTML, CSS

**Data Handling**: CSV (skills dataset)

## 📁 Project Structure
```bash
Resume_Analyzer/
│
├── data/
│   └── skills.csv
│
├── database/
│   └── models.py
│
├── nlp/
│   ├── matcher.py
│   ├── resume_parser.py
│   └── skill_extractor.py
│
├── static/
│   ├── css/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── result.html
│   └── history.html
│
├── app.py
├── requirements.txt
└── resume_analyzer.db
````
---

## ⚙️ Installation & Setup
````bash
git clone https://github.com/Alishba-Haroon/Resume-Analyzer.git
cd Resume-Analyzer
````
````bash
python -m venv venv
source venv/Scripts/activate  # Windows
````
````bash
pip install -r requirements.txt
python app.py
````
App will run at:
````bash
http://127.0.0.1:5000/
````
## 📊 Screenshots



<p align="center">
  <b> **Home Page** </b><br/><br/>
  <img src="https://github.com/Alishba-Haroon/Resume-Analyzer/blob/main/resume_analyzer/static/css/main.png" alt="Home Page" width="700"/>
</p>

<p align="center">
  <b> Background Design</b><br/><br/>
  <img src="https://github.com/Alishba-Haroon/Resume-Analyzer/blob/main/resume_analyzer/static/css/upload.png" alt="Background Design" width="700"/>
</p>

<p align="center">
  <b> Output View</b><br/><br/>
  <img src="https://github.com/Alishba-Haroon/Resume-Analyzer/blob/main/resume_analyzer/static/css/result.png" alt="Result" width="700"/>
</p>

<p align="center">
  <b> Analysis </b><br/><br/>
  <img src="https://github.com/Alishba-Haroon/Resume-Analyzer/blob/main/resume_analyzer/static/css/analysis.png" alt="Background Design" width="700"/>
</p>


## 📈 Future Improvements

* Deploy on Render / Railway

* Add JWT authentication

* Improve NLP accuracy with spaCy

* Add ATS score visualization charts

* Convert to REST API architecture

## 👩‍💻 Author

**Alishba Haroon**
**Aspiring AI Engineer | Data Science Enthusiast**

**GitHub**: https://github.com/Alishba-Haroon
