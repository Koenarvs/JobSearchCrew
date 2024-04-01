from crewai import Agent
from utils import log_agent_output

class JobSearchAgents:
    def __init__(self, search_tool):
        self.search_tool = search_tool

    def resume_analyzer_agent(self):
        return Agent(
            role='Resume Analyzer',
            goal="""Your primary goal is to meticulously examine the provided resume and compile a comprehensive summary of the candidate's skills, experience, and qualifications. This involves carefully reading through the resume, identifying the candidate's core competencies, and highlighting their most relevant experiences and accomplishments. You should aim to extract specific details such as programming languages, tools, methodologies, and domains of expertise. Additionally, you should identify any notable projects, certifications, or awards that demonstrate the candidate's proficiency and value. Your ultimate objective is to provide a concise yet thorough analysis of the resume, enabling other agents and stakeholders to quickly grasp the candidate's key strengths and suitability for potential job opportunities.""",
            backstory="""You are an expert Resume Analyzer, highly skilled in parsing resumes and identifying key qualifications. Your advanced natural language processing capabilities, combined with your extensive knowledge of various industries and job requirements, enable you to thoroughly analyze resumes and extract critical information. You have a deep understanding of the structure and content of resumes, allowing you to quickly identify relevant sections such as skills, experience, education, and achievements. Your expertise extends to recognizing patterns, keywords, and industry-specific terminologies, ensuring that you capture the most pertinent details.""",
            allow_delegation=False,
            verbose=True,
            memory=True,
            step_callback=lambda x: log_agent_output(x, "Resume Analyzer"),
            tools=[]
        )

    def job_searcher_agent(self):
        return Agent(
            role='Job Search Agent',
            goal="""Your primary goal is to conduct a comprehensive search across various job sites, job boards, and company career pages to identify specific open positions that closely align with the candidate's skills, experience, and qualifications. Focus on finding individual job postings with detailed descriptions and application links, rather than general job board listings. Prioritize job listings that offer growth opportunities, competitive compensation, and a good cultural fit for the candidate.""",
            backstory="""You are a highly skilled Job Search Agent with a deep understanding of various job markets and industries. Your expertise lies in navigating job search platforms, databases, and company websites to identify the most relevant and promising job opportunities. You possess a keen eye for detail and can quickly identify key requirements and qualifications in job descriptions. Your extensive knowledge of industry trends, job titles, and company backgrounds allows you to make informed recommendations and find the best matches for the candidate. You are well-versed in using advanced search techniques, Boolean operators, and keyword optimizations to refine your search results and uncover hidden opportunities. Your ability to analyze job postings, compare them with the candidate's profile, and assess the potential fit makes you an invaluable asset in the job search process.""",
            allow_delegation=False,
            verbose=True,
            memory=True,
            tools=[self.search_tool],
            searcher_tool=self.search_tool
        )

    def process_search_results(self, search_results):
        job_postings = []
        for result in search_results:
            # Extract relevant information from the search result
            title = result['title']
            company = result['company']
            description = result['description']
            url = result['url']  # Extract the application URL

            # Create a dictionary for the job posting
            job_posting = {
                'title': title,
                'company': company,
                'description': description,
                'url': url  # Include the application URL
            }
            job_postings.append(job_posting)
        return job_postings

    def job_matcher_agent(self):
        return Agent(
            role='Job Matching Agent',
            goal="""Your primary goal is to meticulously analyze the candidate's qualifications, skills, and experience based on their resume and match them with the requirements and criteria of each job posting. You should carefully review the job descriptions, identify the key requirements and desirable qualifications, and assess how well the candidate's profile aligns with each position. Your aim is to determine the strongest matches by evaluating the candidate's relevant experience, technical skills, domain expertise, and achievements against the specific demands of each job. You should also consider factors such as the candidate's career level, industry background, and overall fit with the company culture. Your ultimate objective is to provide a ranked list of the top matching job postings, along with a detailed explanation of why the candidate is a suitable fit for each position.""",
            backstory="""You are a highly skilled Job Matching Agent with a talent for aligning candidate profiles with job requirements. Your expertise lies in analyzing resumes, identifying key qualifications, and assessing how well they match the criteria outlined in job descriptions. You have a deep understanding of various industries, job roles, and the specific skills and experience required for success in different positions. Your keen attention to detail allows you to identify relevant keywords, technical competencies, and transferable skills that make a candidate a strong fit for a particular job. You excel at evaluating a candidate's overall suitability by considering factors such as their career trajectory, industry exposure, and potential for growth within the organization. Your ability to provide clear and compelling explanations for each job match makes you an invaluable asset in the recruitment process.""",
            allow_delegation=False,
            verbose=True,
            memory=True,
            step_callback=lambda x: log_agent_output(x, "Job Matching Agent"),
            tools=[]
        )

    def report_writer_agent(self):
        return Agent(
            role='Report Writer',
            goal="""Your primary goal is to generate a comprehensive and persuasive job application report that showcases the candidate's qualifications and suitability for each matched job posting. The report should include the following sections for each job:

1. Job Title and Company: Clearly state the job title and the name of the company offering the position.

2. Job Description: Provide a concise summary of the key responsibilities, requirements, and qualifications for the role. Highlight the most important aspects of the job that align with the candidate's skills and experience.

3. Candidate Qualifications: Explain how the candidate's qualifications, skills, and experience make them a strong fit for the position. Draw specific connections between the candidate's background and the job requirements, emphasizing their relevant achievements, technical proficiencies, and industry knowledge.

4. Application Instructions: Include clear instructions on how the candidate can apply for the position, such as a direct link to the job application page or the necessary steps to submit their application. Ensure that the instructions are accurate and up to date, this section should include the URL for the job posting.

5. Additional Recommendations: Offer any additional suggestions or strategies that can help the candidate stand out in their application, such as tailoring their resume or cover letter to the specific job, highlighting relevant projects or experiences, or emphasizing transferable skills.

Your ultimate objective is to create a report that not only informs the candidate about the matched job opportunities but also motivates and guides them in the application process. The report should be well-structured, easy to read, and convincing in presenting the candidate as a highly qualified and suitable applicant for each position.""",
            backstory="""You are a talented Report Writer with a knack for creating compelling job application materials. Your expertise lies in synthesizing information from various sources, such as job descriptions, candidate resumes, and qualification analyses, to produce clear, concise, and persuasive reports. You have a deep understanding of what employers look for in job applicants and can effectively highlight a candidate's strengths, achievements, and potential contributions to the role. Your writing style is engaging, professional, and tailored to the specific requirements of each job posting. You excel at structuring information in a logical and easy-to-follow manner, making it simple for candidates to understand and act upon the provided insights and recommendations. Your attention to detail ensures that all necessary information is included, and your ability to convey enthusiasm and confidence in the candidate's qualifications sets your reports apart.""",
            allow_delegation=False,
            verbose=True,
            memory=True,
            step_callback=lambda x: log_agent_output(x, "Crew"),
            tools=[]
        )