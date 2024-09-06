import React from 'react';

function Header() {
  return (
    <header style={styles.header}>
      <h1>Job Search Application</h1>
      <nav>
        <ul style={styles.navList}>
          <li><a href="/">Home</a></li>
          <li><a href="/dashboard">Dashboard</a></li>
          <li><a href="/upload">Upload Resume</a></li>
        </ul>
      </nav>
    </header>
  );
}

const styles = {
  header: {
    backgroundColor: '#f8f9fa',
    padding: '1rem',
    marginBottom: '2rem',
  },
  navList: {
    listStyle: 'none',
    display: 'flex',
    justifyContent: 'center',
    padding: 0,
  },
  navList: {
    listStyle: 'none',
    display: 'flex',
    justifyContent: 'center',
    padding: 0,
  },
  navList: {
    marginRight: '1rem',
  },
};

export default Header;