# ATS matching logic
import re
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(resume_text, job_description):
    """
    Calculate ATS (Applicant Tracking System) compatibility score
    """
    if not resume_text or not job_description:
        return 50  # Default score
    
    # Convert to lowercase
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Initialize score
    score = 0
    max_score = 100
    
    # 1. Keyword matching (40 points)
    job_keywords = extract_keywords(job_lower)
    resume_keywords = extract_keywords(resume_lower)
    
    matching_keywords = set(job_keywords) & set(resume_keywords)
    keyword_score = min(40, len(matching_keywords) * 2)
    score += keyword_score
    
    # 2. TF-IDF similarity (30 points)
    tfidf_score = calculate_tfidf_similarity(resume_text, job_description)
    score += tfidf_score * 30
    
    # 3. Section presence check (20 points)
    section_score = check_resume_sections(resume_text)
    score += section_score
    
    # 4. Formatting bonus (10 points)
    formatting_score = check_formatting(resume_text)
    score += formatting_score
    
    # Ensure score is within bounds
    score = min(max_score, max(0, score))
    
    return round(score)

def extract_keywords(text):
    """Extract important keywords from text"""
    # Remove common words
    stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'have', 'from', 'will', 'are', 'not'}
    
    # Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # Filter and count
    filtered_words = [word for word in words if word not in stop_words]
    
    # Get most common words
    word_counts = Counter(filtered_words)
    common_words = [word for word, count in word_counts.most_common(20)]
    
    return common_words

def calculate_tfidf_similarity(text1, text2):
    """Calculate TF-IDF cosine similarity between two texts"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    except:
        return 0.5

def check_resume_sections(resume_text):
    """Check for important resume sections"""
    sections = [
        ('experience', ['experience', 'work history', 'employment']),
        ('education', ['education', 'qualification', 'degree']),
        ('skills', ['skill', 'technical skills', 'competencies']),
        ('contact', ['contact', 'email', 'phone', 'linkedin']),
        ('summary', ['summary', 'objective', 'profile'])
    ]
    
    score = 0
    text_lower = resume_text.lower()
    
    for section_name, keywords in sections:
        if any(keyword in text_lower for keyword in keywords):
            score += 4  # 4 points per section found
    
    return min(20, score)

def check_formatting(resume_text):
    """Check resume formatting"""
    score = 0
    
    # Check length (not too short, not too long)
    word_count = len(resume_text.split())
    if 200 <= word_count <= 800:
        score += 4
    
    # Check for bullet points
    if '*' in resume_text or '•' in resume_text or '- ' in resume_text:
        score += 3
    
    # Check for dates (experience timeline)
    date_patterns = [
        r'\b(20\d{2}|19\d{2})\b',  # Years
        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b',  # Months
    ]
    
    for pattern in date_patterns:
        if re.search(pattern, resume_text.lower()):
            score += 3
            break
    
    return min(10, score)

def analyze_job_fit(resume_text, job_description, skills_db):
    """Analyze job fit and provide detailed analysis"""
    if not resume_text or not job_description:
        return {
            'match_percentage': 0,
            'missing_skills': [],
            'strong_matches': [],
            'improvement_suggestions': []
        }
    
    # Extract skills from job description
    job_skills = extract_skills_from_job_description(job_description, skills_db)
    resume_skills = extract_skills_from_resume(resume_text, skills_db)
    
    # Calculate match percentage
    if not job_skills:
        match_percentage = 50
    else:
        matching_skills = set(job_skills) & set(resume_skills)
        match_percentage = min(100, int((len(matching_skills) / len(job_skills)) * 100))
    
    # Find missing skills
    missing_skills = list(set(job_skills) - set(resume_skills))[:5]
    
    # Find strong matches
    strong_matches = list(set(job_skills) & set(resume_skills))[:5]
    
    # Generate suggestions
    suggestions = generate_improvement_suggestions(resume_text, job_description, missing_skills)
    
    return {
        'match_percentage': match_percentage,
        'missing_skills': missing_skills,
        'strong_matches': strong_matches,
        'improvement_suggestions': suggestions
    }

def extract_skills_from_job_description(job_desc, skills_db):
    """Extract required skills from job description"""
    job_lower = job_desc.lower()
    found_skills = []
    
    for skill in skills_db:
        if skill in job_lower:
            found_skills.append(skill.title())
    
    # Also look for common requirement patterns
    requirement_patterns = [
        r'(?:knowledge|experience|proficient|skilled) in ([A-Za-z/\+#\.]+)',
        r'(?:must have|required|requirements?):? ([A-Za-z/\+#\.\s]+)',
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, job_desc, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                for skill in match:
                    if skill.strip() and len(skill.strip()) > 2:
                        found_skills.append(skill.strip().title())
            else:
                if match.strip() and len(match.strip()) > 2:
                    found_skills.append(match.strip().title())
    
    return list(set(found_skills))[:20]

def extract_skills_from_resume(resume_text, skills_db):
    """Extract skills from resume text"""
    from nlp.skill_extractor import extract_skills
    return extract_skills(resume_text, skills_db)

def generate_improvement_suggestions(resume_text, job_desc, missing_skills):
    """Generate improvement suggestions"""
    suggestions = []
    
    # Check for keywords
    job_keywords = extract_keywords(job_desc.lower())
    resume_keywords = extract_keywords(resume_text.lower())
    missing_keywords = set(job_keywords) - set(resume_keywords)
    
    if missing_keywords:
        suggestions.append(f"Add these keywords: {', '.join(list(missing_keywords)[:3])}")
    
    # Check for missing skills
    if missing_skills:
        suggestions.append(f"Develop these skills: {', '.join(missing_skills[:3])}")
    
    # Check resume length
    word_count = len(resume_text.split())
    if word_count < 150:
        suggestions.append("Add more details about your experience and projects")
    elif word_count > 1000:
        suggestions.append("Consider shortening your resume to 1-2 pages")
    
    # Check for action verbs
    action_verbs = ['developed', 'created', 'implemented', 'managed', 'led', 'improved', 'optimized']
    if not any(verb in resume_text.lower() for verb in action_verbs):
        suggestions.append("Use more action verbs (developed, created, implemented, etc.)")
    
    # Check for quantifiable achievements
    if not re.search(r'\d+%|\$\d+|\d+\s*(?:years?|months?)', resume_text):
        suggestions.append("Add quantifiable achievements (increased X by 20%, saved $Y, etc.)")
    
    return suggestions[:5] if suggestions else ["Your resume looks good! Consider tailoring it more specifically for each job application."]