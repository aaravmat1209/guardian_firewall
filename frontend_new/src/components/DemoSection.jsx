import React, { useState, useEffect, useRef } from 'react';
import ChatDemo from './Demo/ChatDemo';
import './DemoSection.css';

const DemoSection = () => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      {
        threshold: 0.3,
        rootMargin: '0px 0px -100px 0px'
      }
    );

    const currentRef = sectionRef.current;
    if (currentRef) {
      observer.observe(currentRef);
    }

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, []);

  return (
    <section 
      ref={sectionRef}
      className={`demo-section ${isVisible ? 'demo-section-visible' : ''}`}
      id="demo"
    >
      {/* Red gradient divider - EXACT Quantra style */}
      <div className="demo-section-divider"></div>
      
      <div className="demo-section-container">
        {/* Mascot-Hosted Section Header */}
        <div className="demo-section-header">
          <div className={`demo-mascot-intro ${isVisible ? 'animate' : ''}`}>
            <img 
              src="/mask.png" 
              alt="Guardian Angel" 
              className="demo-mascot-image"
            />
            <div className="demo-mascot-speech">
              <div className="speech-bubble">
                <p>"Let me show you how I protect children in real-time!"</p>
              </div>
            </div>
          </div>
          
          <h2 className={`demo-section-title ${isVisible ? 'animate' : ''}`}>
            GUARDIAN DEMONSTRATION
          </h2>
          <p className={`demo-section-subtitle ${isVisible ? 'animate' : ''}`}>
            Watch our AI mascot detect and prevent online threats
          </p>
        </div>

        {/* Demo Content */}
        <div className={`demo-section-content ${isVisible ? 'animate' : ''}`}>
          <ChatDemo />
        </div>
      </div>
    </section>
  );
};

export default DemoSection;
