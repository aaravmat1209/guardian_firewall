import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import MascotSection from './components/MascotSection';
import DemoSection from './components/DemoSection';
import FloatingVoiceWidget from './components/FloatingVoiceWidget';
import './styles/globals.css';

function App() {
  const [showVoiceWidget] = useState(true); // Always show widget

  const handleGetStarted = () => {
    // Scroll to demo section instead of showing widget
    const demoSection = document.getElementById('demo');
    if (demoSection) {
      demoSection.scrollIntoView({ behavior: 'smooth' });
    }
  };



  return (
    <div className="App">
      <Navbar onGetStarted={handleGetStarted} />
      <main>
        <Hero />
        <MascotSection />
        <DemoSection />
      </main>

              {/* Floating Voice Widget */}
              {showVoiceWidget && (
                <FloatingVoiceWidget />
              )}
    </div>
  );
}

export default App;
