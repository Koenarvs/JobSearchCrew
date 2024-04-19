from crewai import Task
from textwrap import dedent

class JobSearchTasks():
    def analyze_resume_task(self, agent, resume_text):
        return Task(
            description=dedent(f"""
            Analyze the provided resume to extract the following information:
            1. Candidate's name
            2. Candidate's key skills
            3. Relevant experience
            4. Notable qualifications
            5. Preferred work location (if explicitly stated in the resume)
                - If a specific location is mentioned, include both the location and "Remote/Work from Home" as options
                - If no location is specified, include only "Remote/Work from Home" as an option
                - If the resume explicitly states the candidate is not interested in remote work, include only the specified location
            6. Recommended job titles (5-10) that best match the candidate's qualifications
                - Start by considering the candidate's current and previous job titles as a baseline
                - Build upon these job titles based on the candidate's key skills, relevant experience, and domain expertise
                - Focus on job titles that directly relate to the candidate's background and highlight their growth and progression
                - Consider the candidate's seniority level and include appropriate job titles (e.g., Senior, Lead, Manager, Director)
                - Avoid generic or unrelated job titles that do not align with the candidate's experience
            7. Any other important information that could help match the candidate to suitable job opportunities

            Resume Text:
            {resume_text}
            """),
            expected_output=dedent("""
            Return a dictionary containing:
            {
                'name': 'Candidate's name',
                'key_skills': ['List', 'of', 'key', 'skills'],
                'experience': 'Brief overview of relevant experience',
                'qualifications': 'List of notable qualifications',
                'work_location': 'Preferred work location',
                'recommended_job_titles': ['List', 'of', 'recommended', 'job', 'titles'],
                'additional_info': 'Any other important information'
            }
            This dictionary should provide a concise yet comprehensive summary of the candidate's profile, detailing their strengths and suitability for potential job opportunities.
            """),
            agent=agent,
            result_context_key='resume_analysis'
        )

    def search_jobs_task(self, agent):
        return Task(
            description=dedent("""
            Use the SerperDevTool to conduct a comprehensive search for new job postings, specifically focusing on positions that are not part of the candidate's current or previous job titles as listed in their resume. Utilize the recommended job titles and work locations provided in the resume analysis as key filters for your search.

            It's crucial to ensure each search result reflects a specific, individual job opportunity—not a general listing that aggregates multiple jobs. If the search results include links to job boards or pages listing multiple job opportunities, refine your search criteria to target unique job postings. Each listing should be for a distinct position with a clear job title and detailed description available.

            Continue refining your search by using insights gained from previous results if the initial search yields fewer than 10 suitable postings. Your goal is to gather at least 10 specific job postings that closely match the candidate's desired job titles and locations, each with a detailed description and a direct application link.
            """),
            expected_output=dedent("""
            A structured list of at least 10 specific job postings, ensuring none are generic or aggregate listings, with each including:
            1. Job Title
            2. Company Name
            3. Detailed description of the role
            4. A valid link to apply
            The list should reflect the candidate's specified job titles and work locations, aligning closely with their career objectives and geographical preferences.
            """),
            agent=agent,
            context_provider=lambda context: {'resume_info': context.get('resume_analysis', [])},
            result_context_key='job_postings'
        )


    def match_jobs_task(self, agent):
        return Task(
            description="""Using the provided resume analysis and the list of job postings, compare the candidate's qualifications with the requirements of each job posting. Determine the best matches by evaluating how well the candidate's skills, experience, and recommended job titles align with the job requirements. When referring to the candidate, use their name as provided in the resume analysis.""",
            expected_output="A list of the top matching job postings, with an explanation of why the candidate is qualified for each position. The explanation should refer to the candidate by name.",
            agent=agent,
            context_provider=lambda context: {
                'resume_info': context.get('resume_analysis', []),
                'job_postings': context.get('job_postings', [])
            }
        )

    def write_report_task(self, agent):
        return Task(
            description="Generate a personalized report for the candidate, addressing them by name. Include a brief description of each matching job position, why the candidate is qualified, and a link to apply. Use the candidate's name consistently throughout the report.",
            expected_output="A well-formatted, personalized report that the candidate can use to apply for the selected job postings. The report should address the candidate by name throughout.",
            agent=agent,
            context_provider=lambda context: {
                'resume_info': context.get('resume_analysis', {}),
                'matched_job_postings': context.get('matched_job_postings', [])
            },
            report_format="""
            **Job Title and Company:** {title}, {company}

            **Job Description:** {description}

            **{candidate_name}'s Qualifications:** Your extensive experience and expertise in data engineering, specifically with technologies such as {skills}, make you a strong candidate for this role. Your background in {experience} aligns well with the job requirements.

            **Application Instructions:** Apply directly at the following link: {url}

            **Additional Recommendations:** Tailor your resume and cover letter to highlight your relevant projects and achievements in {highlights}. Emphasize your passion for data engineering and your ability to deliver impactful solutions, {candidate_name}.
            """
        )