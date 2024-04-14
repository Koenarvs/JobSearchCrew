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
            expected_output="""
            A well-structured summary of the candidate's profile, including:
            1. Candidate's name
            2. A list of the candidate's key skills, with a focus on those most relevant to their desired role
            3. A brief overview of the candidate's relevant experience, highlighting notable achievements and responsibilities
            4. Any notable qualifications, such as degrees, certifications, or awards
            5. The candidate's preferred work location and "Remote/Work from Home" if a location is specified (unless the candidate explicitly states they are not interested in remote work)
                - If no location is mentioned, include only "Remote/Work from Home"
            6. A list of 5-10 recommended job titles that best match the candidate's qualifications, starting with their current and previous job titles and building upon them based on their skills, experience, and domain expertise
            7. Any additional information that could help match the candidate to suitable job opportunities

            The summary should be concise yet comprehensive, providing a clear picture of the candidate's strengths and suitability for potential job opportunities.
            """,
            agent=agent,
            result_context_key='resume_analysis'
        )

    def search_jobs_task(self, agent):
        return Task(
            description=dedent("""
            Conduct a comprehensive search for specific, individual job postings that closely match the candidate's skills, experience, qualifications, and recommended job titles based on the resume analysis provided. Focus on finding detailed job descriptions with direct application links.

            For each job posting, include the following information:
            1. Job Title
            2. Company Name
            3. Detailed description of the role and requirements
            4. A valid and direct link to apply for the specific position

            Ensure that the job postings meet the following criteria:
            1. Each result must be a specific, individual job posting with a detailed description, not a general listing or aggregation of multiple jobs
            2. The job title, company name, detailed description, and a valid, direct application URL must be available for each posting
            3. The job aligns with the candidate's preferred work location(s), including remote work options if applicable
            4. The job title closely matches or is directly related to one of the recommended job titles from the resume analysis

            If the initial search yields fewer than 10 results that meet all the criteria, conduct additional targeted searches to find more relevant, specific job postings. Repeat the search process up to a maximum of 5 times or until you have at least 10 qualifying results, whichever comes first. If after 5 search attempts you still have fewer than 10 qualifying results, proceed with the available postings that fully meet the criteria.

            Once you have completed your search and reflection process, format the output as a structured list of specific job postings, with each posting containing the required information.
            """),
            expected_output=dedent("""
            A well-structured list of specific, individual job postings, with each posting containing:
            1. Job Title
            2. Company Name
            3. Detailed description of the role and requirements
            4. A valid and direct link to apply for the specific position

            The list should include a minimum of 10 job postings that closely match the candidate's skills, experience, qualifications, preferred work location(s) (including remote work options if applicable), and recommended job titles from the resume analysis.

            Each job posting must be a specific, individual listing with a detailed description and direct application link. General job listings or aggregations should not be included.

            If after 5 search attempts there are still fewer than 10 qualifying job postings that fully meet the criteria, provide the available postings that match all the requirements.

            The output should be formatted in a way that makes it easy for the next agent to perform a comparative analysis between the specific job postings and the candidate's resume.
            """),
            agent=agent,
            context_provider=lambda context: {'resume_info': context.get('resume_analysis', {})},
            result_context_key='job_postings'
        )
    def match_jobs_task(self, agent):
        return Task(
            description="""Using the provided resume analysis and the list of job postings, compare the candidate's qualifications with the requirements of each job posting. Determine the best matches by evaluating how well the candidate's skills, experience, and recommended job titles align with the job requirements. When referring to the candidate, use their name as provided in the resume analysis.""",
            expected_output="A list of the top matching job postings, with an explanation of why the candidate is qualified for each position. The explanation should refer to the candidate by name.",
            agent=agent,
            context_provider=lambda context: {
                'resume_info': context.get('resume_analysis', {}),
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