const API_BASE_URL = 'http://localhost:5000';  // Adjust this if your backend is on a different port

export const uploadResume = async (filePath) => {
  const response = await fetch(`${API_BASE_URL}/api/upload_resume`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ file_path: filePath }),
  });

  if (!response.ok) {
    throw new Error('Failed to upload resume');
  }

  return response.json();
};

export const getJobMatches = async () => {
  const response = await fetch(`${API_BASE_URL}/api/job_matches`);

  if (!response.ok) {
    throw new Error('Failed to fetch job matches');
  }

  return response.json();
};