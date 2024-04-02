from crewai import Task
from textwrap import dedent

class JobSearchTasks():
    def analyze_resume_task(self, agent, resume_text):
        return Task(
            description=dedent(f"""Analyze the provided resume to extract the candidate's skills, experience, and qualifications: {resume_text}"""),
            expected_output="""A summary of the candidate's key skills, experience, and qualifications.""",
            agent=agent,
            result_context_key='resume_analysis'
        )

    def search_jobs_task(self, agent):
        return Task(
            description="""Conduct a comprehensive search for specific job opportunities that closely match the candidate's skills, experience, and qualifications based on the resume analysis provided. Focus on finding individual job postings with detailed descriptions and direct application links.""",
            expected_output="A list of specific job postings, including the job title, company name, detailed description, and a direct link to apply for each position.",
            agent=agent,
            context_provider=lambda context: {'job_postings': context.get('job_postings', [])},
            result_context_key='job_postings'
        )


    def match_jobs_task(self, agent):
        return Task(
            description="""Using the provided resume analysis and the list of job postings, compare the candidate's qualifications with the requirements of each job posting. Determine the best matches by evaluating how well the candidate's skills and experience align with the job requirements.""",
            expected_output="A list of the top matching job postings, with an explanation of why the candidate is qualified for each position.",
            agent=agent,
            context_provider=lambda context: {
                'resume_analysis': context.get('resume_analysis', ''),
                'job_postings': context.get('job_postings', [])
            }
        )

    def write_report_task(self, agent):
        return Task(
            description="Generate a report with a brief description of each matching job position, why the candidate is qualified, and a link to apply.",
            expected_output="A well-formatted report that the candidate can use to apply for the selected job postings.",
            agent=agent,
            context_provider=lambda context: {
                'matched_job_postings': context.get('matched_job_postings', [])
            },
            report_format="""
**Job Title and Company:** {title}, {company}

**Job Description:** {description}

**Candidate Qualifications:** Your extensive experience and expertise in data engineering, specifically with technologies such as {skills}, make you a strong candidate for this role. Your background in {experience} aligns well with the job requirements.

**Application Instructions:** Apply directly at the following link: {url}

**Additional Recommendations:** Tailor your resume and cover letter to highlight your relevant projects and achievements in {highlights}. Emphasize your passion for data engineering and your ability to deliver impactful solutions.
"""
        )