import React from 'react';

function Home() {
  return (
    <div style={styles.container}>
      <h2>Welcome to Job Search Application</h2>
      <p>Find your dream job with our AI-powered job matching system.</p>
      <button style={styles.button}>Get Started</button>
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
};

export default Home;