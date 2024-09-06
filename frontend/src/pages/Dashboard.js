import React from 'react';

function Dashboard() {
  return (
    <div style={styles.container}>
      <h2>Your Dashboard</h2>
      <div style={styles.stats}>
        <div style={styles.statItem}>
          <h3>Resumes Uploaded</h3>
          <p>1</p>
        </div>
        <div style={styles.statItem}>
          <h3>Job Matches</h3>
          <p>15</p>
        </div>
        <div style={styles.statItem}>
          <h3>Applications Sent</h3>
          <p>5</p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem',
  },
  stats: {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: '2rem',
  },
  statItem: {
    backgroundColor: '#f8f9fa',
    padding: '1rem',
    borderRadius: '5px',
    textAlign: 'center',
  },
};

export default Dashboard;