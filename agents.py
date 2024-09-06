import logging
from crewai import Agent
from utils import log_agent_output

class JobSearchAgents:
    def __init__(self, search_tool):
        self.search_tool = search_tool

    def resume_analyzer_agent(self):
        try:
            return Agent(
                role='Resume Analyzer',
                goal="""Your primary goal is to analyze the provided resume and create a comprehensive, structured summary of the candidate's profile.""",
                backstory="""As an expert Resume Analyzer, you possess deep insights into the structuring of resumes.""",
                allow_delegation=False,
                verbose=False,
                memory=True,
                step_callback=lambda x: log_agent_output(x, "Resume Analyzer"),
                tools=[]
            )
        except Exception as e:
            logging.error(f"Failed to initialize Resume Analyzer Agent: {str(e)}")
            return None

    def process_resume_information(self, resume_analysis):
        try:
            # Extract all relevant information from the resume analysis dictionary
            resume_info = {
                'candidate_name': resume_analysis.get('name', 'Unknown'),
                'key_skills': resume_analysis.get('key_skills', []),
                'relevant_experience': resume_analysis.get('experience', 'No experience listed'),
                'notable_qualifications': resume_analysis.get('qualifications', []),
                'work_location': resume_analysis.get('work_location', 'Remote/Work from Home'),
                'recommended_job_titles': resume_analysis.get('recommended_job_titles', []),
                'additional_info': resume_analysis.get('additional_info', 'No additional information provided')
            }
            return resume_info
        except Exception as e:
            logging.error(f"Error processing resume information: {str(e)}")
            return {}

    def job_searcher_agent(self):
        try:
            return Agent(
                role='Job Search Agent',
                goal="""Conduct a comprehensive search across various job sites, job boards, and company career pages. Focus on finding job postings that align closely with the candidate's skills and preferences.""",
                backstory="""With access to advanced search tools, you refine search results to find the best opportunities.""",
                tools=[self.search_tool],
                allow_delegation=False,
                max_execution_time=300,
                max_iter=50,
                verbose=True,
                memory=True,
                step_callback=lambda x: log_agent_output(x, "Job Search Agent")
            )
        except Exception as e:
            logging.error(f"Failed to initialize Job Search Agent: {str(e)}")
            return None

    def process_search_results(self, search_results):
        job_postings = []
        try:
            for result in search_results:
                job_postings.append({
                    'title': result['title'],
                    'company': result['company'],
                    'description': result['description'],
                    'url': result['url']
                })
        except Exception as e:
            logging.error(f"Error processing search results: {str(e)}")
        return job_postings

    def job_matcher_agent(self):
        try:
            return Agent(
                role='Job Matching Agent',
                goal="""Meticulously analyze the candidate's qualifications and match them with job postings.""",
                backstory="""You have a talent for aligning candidate profiles with job requirements.""",
                allow_delegation=False,
                verbose=False,
                memory=True,
                step_callback=lambda x: log_agent_output(x, "Job Matcher Agent"),
                tools=[]
            )
        except Exception as e:
            logging.error(f"Failed to initialize Job Matching Agent: {str(e)}")
            return None

    def report_writer_agent(self):
        try:
            return Agent(
                role='Report Writer',
                goal="""Generate a comprehensive job application report that showcases the candidate's qualifications for each matched job.""",
                backstory="""You are a talented Report Writer known for creating compelling job application materials.""",
                allow_delegation=False,
                verbose=False,
                memory=True,
                step_callback=lambda x: log_agent_output(x, "Report Writer"),
                tools=[]
            )
        except Exception as e:
            logging.error(f"Failed to initialize Report Writer Agent: {str(e)}")
            return None
