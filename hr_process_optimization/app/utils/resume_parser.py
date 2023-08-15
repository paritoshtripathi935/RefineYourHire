import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser
import os
import pandas as pd
from docx import Document
import sqlite3

class ResumeExtractor:
    def __init__(self):
        self.stopwords = nltk.corpus.stopwords.words('english')

    def read_docx(self, path):
        doc = Document(path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    def extract_resume_data(self, path):
        try:
            data = ResumeParser(path).get_extracted_data()
            experience = data.get('experience', '')
            education = data.get('education', '')
            skills = data.get('skills', '')
            name = data.get('name', '')
            email = data.get('email', '')
            projects = data.get('projects', '')

            return experience, education, skills, name, email, projects
        except Exception as e:
            print(f"Error extracting data from {path}: {str(e)}")
            return '', '', '', '', '', ''

    def process_resume(self, resume_path):
        experience, education, skills, name, email, projects = self.extract_resume_data(resume_path)
        return {
            'experience': experience,
            'education': education,
            'skills': skills,
            'name': name,
            'email': email,
            'projects': projects
        }

