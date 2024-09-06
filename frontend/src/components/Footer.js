import React from 'react';

function Footer() {
  return (
    <footer style={styles.footer}>
      <p>&copy; 2023 Job Search Application. All rights reserved.</p>
    </footer>
  );
}

const styles = {
  footer: {
    backgroundColor: '#f8f9fa',
    padding: '1rem',
    marginTop: '2rem',
    textAlign: 'center',
  },
};

export default Footer;