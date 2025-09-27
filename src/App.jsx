import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import DemoSection from './components/DemoSection';
import './styles/globals.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <Hero />
        <DemoSection />
        {/* Future sections will be added here */}
        <section id="features" className="section">
          <div className="container">
            <div className="divider-red"></div>
            <h2 className="text-center">Advanced Features</h2>
            <p className="text-center text-gray">
              Real-time monitoring, AI-powered threat detection, and comprehensive analytics
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
