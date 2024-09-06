from crewai_tools import tool
import requests
import os

@tool("Google Jobs API Search")
def search_google_jobs_api(api_key, query: str, location: str, distance: int = -1, language: str = "en_GB", remoteOnly: bool = False, datePosted: str = '', employmentTypes: str = '', index: int = 0) -> dict:
    """Searches for job listings using Google's Job API."""
    host = "jobs-api14.p.rapidapi.com"
    base_url = "https://jobs-api14.p.rapidapi.com/list"
    
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': host
    }
    params = {
        'query': query,
        'location': location,
        'distance': str(distance),
        'language': language,
        'remoteOnly': str(remoteOnly).lower(),
        'datePosted': datePosted,
        'employmentTypes': employmentTypes,
        'index': str(index)
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch data", "status_code": response.status_code}
    return response.json()
