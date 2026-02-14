# Skill extraction logic
import re
import pandas as pd
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('punkt')
    nltk.download('stopwords')

def load_skills_from_csv(csv_path):
    """Load skills database from CSV file"""
    try:
        df = pd.read_csv(csv_path, header=None)
        skills = set()
        for col in df.columns:
            skills.update(df[col].dropna().str.lower().tolist())
        return skills
    except Exception as e:
        print(f"Error loading skills CSV: {e}")
        # Return default skills if CSV not found
        return get_default_skills()

def get_default_skills():
    """Return default skills set"""
    return {
        'python', 'flask', 'django', 'fastapi', 'javascript', 'react', 'vue', 'angular',
        'html', 'css', 'bootstrap', 'tailwind', 'sql', 'mysql', 'postgresql', 'mongodb',
        'aws', 'docker', 'kubernetes', 'git', 'github', 'jenkins', 'linux',
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch',
        'pandas', 'numpy', 'scikit-learn', 'opencv', 'tableau', 'power bi',
        'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'devops'
    }

def extract_skills(resume_text, skills_db):
    """Extract skills from resume text"""
    if not resume_text:
        return []
    
    text_lower = resume_text.lower()
    found_skills = set()
    
    # Direct matching
    for skill in skills_db:
        if skill in text_lower:
            found_skills.add(skill.title())
    
    # Pattern matching for programming languages
    programming_patterns = {
        r'python': 'Python',
        r'javascript|js\b': 'JavaScript',
        r'java\b(?!script)': 'Java',
        r'c\+\+|cpp': 'C++',
        r'c#|csharp': 'C#',
        r'php': 'PHP',
        r'ruby': 'Ruby',
        r'go\b|golang': 'Go',
        r'rust': 'Rust',
        r'swift': 'Swift',
        r'kotlin': 'Kotlin',
        r'typescript|ts\b': 'TypeScript',
        r'sql': 'SQL',
        r'html': 'HTML',
        r'css': 'CSS'
    }
    
    for pattern, skill_name in programming_patterns.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_skills.add(skill_name)
    
    # Framework matching
    framework_patterns = {
        r'react(\.js)?\b': 'React',
        r'angular\b': 'Angular',
        r'vue(\.js)?\b': 'Vue.js',
        r'django\b': 'Django',
        r'flask\b': 'Flask',
        r'express(\.js)?\b': 'Express.js',
        r'spring\b': 'Spring',
        r'laravel\b': 'Laravel',
        r'rails|ruby on rails': 'Ruby on Rails',
        r'asp\.net': 'ASP.NET',
        r'node(\.js)?\b': 'Node.js'
    }
    
    for pattern, skill_name in framework_patterns.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_skills.add(skill_name)
    
    # Tool matching
    tool_patterns = {
        r'docker\b': 'Docker',
        r'kubernetes|k8s': 'Kubernetes',
        r'aws\b': 'AWS',
        r'azure\b': 'Azure',
        r'gcp|google cloud': 'Google Cloud',
        r'git\b': 'Git',
        r'jenkins\b': 'Jenkins',
        r'ansible\b': 'Ansible',
        r'terraform\b': 'Terraform',
        r'grafana\b': 'Grafana',
        r'prometheus\b': 'Prometheus'
    }
    
    for pattern, skill_name in tool_patterns.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_skills.add(skill_name)
    
    # Extract skills from skills section using NLTK
    sentences = nltk.sent_tokenize(resume_text)
    stop_words = set(stopwords.words('english'))
    
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Check for bi-grams and tri-grams
        for i in range(len(filtered_words) - 1):
            bigram = f"{filtered_words[i]} {filtered_words[i+1]}"
            if bigram in skills_db:
                found_skills.add(bigram.title())
        
        for i in range(len(filtered_words) - 2):
            trigram = f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}"
            if trigram in skills_db:
                found_skills.add(trigram.title())
    
    return sorted(list(found_skills))

def extract_experience(resume_text):
    """Extract years of experience from resume"""
    experience_patterns = [
        r'(\d+)\+?\s*years?.*experience',
        r'experience.*(\d+)\+?\s*years?',
        r'(\d+)\s*yr',
        r'(\d+)\s*y\.'
    ]
    
    text_lower = resume_text.lower()
    
    for pattern in experience_patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                years = int(match.group(1))
                return years
            except:
                continue
    
    # Default if no experience found
    return 0

def extract_education(resume_text):
    """Extract education information"""
    education_keywords = {
        'phd': 'PhD',
        'doctorate': 'PhD',
        'masters?': "Master's",
        'msc?': 'MSc',
        'm\.?tech': 'M.Tech',
        'mba': 'MBA',
        'bachelor': "Bachelor's",
        'b\.?tech': 'B.Tech',
        'bsc': 'BSc',
        'be': 'BE',
        'diploma': 'Diploma',
        'high school': 'High School'
    }
    
    found_degrees = []
    
    for pattern, degree in education_keywords.items():
        if re.search(pattern, resume_text.lower()):
            found_degrees.append(degree)
    
    return list(set(found_degrees))