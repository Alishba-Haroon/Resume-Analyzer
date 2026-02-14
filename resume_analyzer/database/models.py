# Database models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class ResumeAnalysis(db.Model):
    """Model for storing resume analysis results"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    resume_text = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    ats_score = db.Column(db.Integer, nullable=False, default=0)
    job_description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'skills': self.skills.split(',') if self.skills else [],
            'ats_score': self.ats_score,
            'job_description': self.job_description,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

def init_db():
    """Initialize database"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'resume_analyzer.db')
    
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return db

def save_analysis(filename, resume_text, skills, ats_score, job_description):
    """Save analysis to database"""
    from flask import Flask
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'resume_analyzer.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        analysis = ResumeAnalysis(
            filename=filename,
            resume_text=resume_text,
            skills=skills,
            ats_score=ats_score,
            job_description=job_description
        )
        db.session.add(analysis)
        db.session.commit()
        return analysis.id

def get_analysis_history(limit=10):
    """Get analysis history"""
    from flask import Flask
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'resume_analyzer.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).limit(limit).all()
        return [analysis.to_dict() for analysis in analyses]