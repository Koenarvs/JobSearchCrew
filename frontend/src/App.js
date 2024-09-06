import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import './styles/global.css';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <Home />
        <Dashboard />
      </main>
      <Footer />
    </div>
  );
}

export default App;