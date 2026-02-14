# Resume text extraction

import os
import PyPDF2
import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    
    try:
        # Try with pdfplumber first (better for formatted text)
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        # Fallback to PyPDF2
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    return clean_text(text)

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return clean_text(text)
    except Exception as e:
        raise Exception(f"DOCX extraction failed: {str(e)}")

def extract_text_from_txt(txt_path):
    """Extract text from TXT file"""
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return clean_text(text)
    except Exception as e:
        raise Exception(f"TXT extraction failed: {str(e)}")

def extract_text_from_resume(filepath):
    """Extract text from any supported resume format"""
    extension = filepath.split('.')[-1].lower()
    
    if extension == 'pdf':
        return extract_text_from_pdf(filepath)
    elif extension == 'docx':
        return extract_text_from_docx(filepath)
    elif extension == 'txt':
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

def clean_text(text):
    """Clean and preprocess extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:-]', ' ', text)
    
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def extract_sections(resume_text):
    """Extract different sections from resume text"""
    sections = {
        'experience': '',
        'education': '',
        'skills': '',
        'projects': '',
        'summary': ''
    }
    
    # Simple keyword-based section extraction
    lines = resume_text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if any(keyword in line_lower for keyword in ['experience', 'work history', 'employment']):
            sections['experience'] = extract_section_content(lines, i)
        elif any(keyword in line_lower for keyword in ['education', 'qualification', 'degree']):
            sections['education'] = extract_section_content(lines, i)
        elif any(keyword in line_lower for keyword in ['skill', 'technical', 'competenc']):
            sections['skills'] = extract_section_content(lines, i)
        elif any(keyword in line_lower for keyword in ['project', 'portfolio']):
            sections['projects'] = extract_section_content(lines, i)
        elif any(keyword in line_lower for keyword in ['summary', 'objective', 'profile']):
            sections['summary'] = extract_section_content(lines, i)
    
    return sections

def extract_section_content(lines, start_index):
    """Extract content for a section until next section header"""
    content = []
    for line in lines[start_index + 1:]:
        # Check if next section starts
        if any(keyword in line.lower() for keyword in 
               ['experience', 'education', 'skills', 'projects', 'summary', 'objective']):
            if len(line.split()) < 4:  # Likely a header
                break
        content.append(line.strip())
    
    return ' '.join(content[:20])  # Limit to first 20 lines