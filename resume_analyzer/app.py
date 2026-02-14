from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
import uuid
from datetime import datetime

# Custom modules
from nlp.resume_parser import extract_text_from_resume
from nlp.skill_extractor import extract_skills, load_skills_from_csv
from nlp.matcher import calculate_ats_score, analyze_job_fit
from database.models import init_db, save_analysis, get_analysis_history

app = Flask(__name__)
app.secret_key = 'resume-analyzer-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Initialize database
init_db()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    """Upload and analyze resume"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Get job description
            job_description = request.form.get('job_description', '')
            
            # Process resume
            try:
                # Extract text from resume
                resume_text = extract_text_from_resume(filepath)
                
                # Load skills database
                skills_db = load_skills_from_csv('data/skills.csv')
                
                # Extract skills
                skills = extract_skills(resume_text, skills_db)
                
                # Calculate ATS score
                ats_score = calculate_ats_score(resume_text, job_description)
                
                # Analyze job fit
                job_fit = analyze_job_fit(resume_text, job_description, skills_db)
                
                # Save to database
                analysis_id = save_analysis(
                    filename=filename,
                    resume_text=resume_text[:500],  # Store first 500 chars
                    skills=','.join(skills),
                    ats_score=ats_score,
                    job_description=job_description[:500]
                )
                
                # Prepare result data
                result = {
                    'id': analysis_id,
                    'filename': filename,
                    'skills': skills,
                    'ats_score': ats_score,
                    'job_fit': job_fit,
                    'resume_text_preview': resume_text[:300] + '...' if len(resume_text) > 300 else resume_text,
                    'total_skills': len(skills),
                    'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'job_description': job_description
                }
                
                # Store in session
                session['last_analysis'] = result
                
                # Redirect to result page
                return render_template('result.html', result=result)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(request.url)
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash('Allowed file types: PDF, DOCX, TXT', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/history')
def history():
    """View analysis history"""
    history_data = get_analysis_history(limit=10)
    return render_template('history.html', history=history_data)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for resume analysis"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        skills_db = load_skills_from_csv('data/skills.csv')
        skills = extract_skills(resume_text, skills_db)
        ats_score = calculate_ats_score(resume_text, job_description)
        job_fit = analyze_job_fit(resume_text, job_description, skills_db)
        
        return jsonify({
            'success': True,
            'skills': skills,
            'ats_score': ats_score,
            'job_fit': job_fit,
            'total_skills': len(skills)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/demo')
def demo():
    """Demo page with sample analysis"""
    sample_result = {
        'filename': 'sample_resume.pdf',
        'skills': ['Python', 'Flask', 'SQL', 'Machine Learning', 'NLP', 'HTML/CSS'],
        'ats_score': 85,
        'job_fit': {
            'match_percentage': 78,
            'missing_skills': ['Docker', 'AWS'],
            'strong_matches': ['Python', 'Machine Learning', 'Flask']
        },
        'total_skills': 6,
        'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return render_template('result.html', result=sample_result)

if __name__ == '__main__':
    # Create uploads folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)