import nltk
from pyresparser import ResumeParser
from docx import Document
nltk.download('stopwords')

class ResumeExtractor:
    def __init__(self):
        self.stopwords = nltk.corpus.stopwords.words('english')

    async def read_docx(self, path):
        doc = Document(path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    async def extract_resume_data(self, path):
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
            return ValueError('Error in extracting resume data')

    async def process_resume(self, resume_path):
        experience, education, skills, name, email, projects = await self.extract_resume_data(resume_path)
        return {
            'experience': experience,
            'education': education,
            'skills': skills,
            'name': name,
            'email': email,
            'projects': projects
        }
