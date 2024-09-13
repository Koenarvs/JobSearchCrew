import React, { useState } from 'react';
import { uploadResume, getJobMatches } from '../services/api';

function Home() {
  const [filePath, setFilePath] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await uploadResume(filePath);
      const jobMatches = await getJobMatches();
      setResults(jobMatches);
    } catch (err) {
      setError('An error occurred while processing your request.');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2>Welcome to Job Search Application</h2>
      <p>Find your dream job with our AI-powered job matching system.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={filePath}
          onChange={(e) => setFilePath(e.target.value)}
          placeholder="Enter resume file path"
          style={styles.input}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? 'Processing...' : 'Search Jobs'}
        </button>
      </form>
      {error && <p style={styles.error}>{error}</p>}
      {results.length > 0 && (
        <div style={styles.results}>
          <h3>Job Matches:</h3>
          <ul>
            {results.map((job) => (
              <li key={job.id}>
                {job.title} at {job.company}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem',
    textAlign: 'center',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '1rem',
    fontSize: '1rem',
  },
  button: {
    backgroundColor: '#007bff',
    color: 'white',
    padding: '10px 20px',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '1rem',
    marginTop: '1rem',
  },
  error: {
    color: 'red',
    marginTop: '1rem',
  },
  results: {
    marginTop: '2rem',
    textAlign: 'left',
  },
};

export default Home;