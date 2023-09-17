import io
import json

from google.cloud import language_v1

data = """
{
  "message": "Resume updated successfully",
  "resumeData": {
    "experience": [
      "Anakin (Y Combinator 21)",
      "SOFTWARE ENGiNEER INTERN",
      "• Processed over 100 data points through AWS, Pandas, ECS, SQS, and S3 using Python.",
      "• Successfully bypassed Cloudflare, Akamai, and Imperva through various techniques and tools.",
      "• Contributed to ECS pipeline deployment using Jenkins for seamless application delivery and continuous integration.",
      "Software Development Intern",
      "THE ONE WORLD",
      "Bangalore",
      "Aug. 2022 ‑ Present",
      "Bangalore",
      "June. 2022 ‑ Aug. 2022",
      "• As a Software Development Intern at The One World, I helped design and develop a containerized fast API backend to support a large‑scale",
      "social media platform.",
      "In this role, I used a variety of tools including Docker, AWS, and PostgreSQL as the database.",
      "•",
      "Artificial Intelligence Intern",
      "THE ONE WORLD",
      "Bangalore",
      "Dec. 2021 ‑ May. 2022",
      "• As an Artificial Intelligence Intern at The One World, I worked on designing and building various types of models, ranging from recommendation",
      "engines to rooftop age detection.",
      "In addition, I developed a Dashboard using Dash Plotly and deployed them using AWS EC2.",
      "•",
      "Machine Learning Intern",
      "UFF FOODS",
      "Nagpur",
      "Aug. 2021 ‑ Nov. 2021",
      "• As a Machine Learning Intern at UFF Foods, I was responsible for ETL (Extract, Transform, and Load) for NLP.",
      "•",
      "In addition, I developed a Selenium scraper for Zomato."
    ],
    "education": "",
    "skills": [
      "Ai",
      "Hadoop",
      "Sql",
      "Programming",
      "Aws",
      "C",
      "Api",
      "Design",
      "Github",
      "Python",
      "Keras",
      "Docker",
      "Jira",
      "Pandas",
      "C++",
      "Selenium",
      "Algorithms",
      "Django",
      "Pyspark",
      "Architecture",
      "Database",
      "Analysis",
      "Mining",
      "Etl",
      "Postgresql",
      "Java",
      "Operating systems"
    ],
    "name": "Paritosh Tripathi",
    "email": "tripathiparitosh935@gmail.com",
    "projects": "",
    "user_id": 1,
    "resume_path": "app/resumes/ParitoshTripathi_Resume.pdf",
    "resume_id": "58709068-468e-403f-a924-2980446df514"
  }
}
"""
import json
resume_data = json.loads(data)
# Create a client
client = language_v1.LanguageServiceClient()

# Set the document type
document = {"type": "PLAIN_TEXT", "content": resume_data["experience"]}

# Request NER analysis
response = client.analyze_entities(document=document, encoding_type="UTF8")

# Parse the NER analysis results
entities = []
for entity in response.entities:
    entities.append({
        "type": entity.type_,
        "text": entity.name,
        "start_position": entity.start_position,
        "end_position": entity.end_position,
    })

# Extract the relevant information
positions = []
companies = []
start_dates = []
end_dates = []

for entity in entities:
    if entity["type"] == "ORGANIZATION":
        companies.append(entity["text"])
    elif entity["type"] == "DATE":
        if entity["text"].endswith("-"):
            start_dates.append(entity["text"][:-1])
        elif entity["text"].startswith("-"):
            end_dates.append(entity["text"][1:])
    elif entity["type"] == "PERSON":
        positions.append(entity["text"])

# Print the extracted information
print("Positions:", positions)
print("Companies:", companies)
print("Start dates:", start_dates)
print("End dates:", end_dates)
