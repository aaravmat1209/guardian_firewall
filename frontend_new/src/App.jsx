import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import MascotSection from './components/MascotSection';
import DemoSection from './components/DemoSection';
import AboutSection from './components/AboutSection';
import FloatingVoiceWidget from './components/FloatingVoiceWidget';
import './styles/globals.css';

function App() {
  const [showVoiceWidget, setShowVoiceWidget] = useState(true); // Always show widget

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
        <AboutSection />
      </main>

              {/* Floating Voice Widget */}
              {showVoiceWidget && (
                <FloatingVoiceWidget />
              )}
    </div>
  );
}

export default App;
