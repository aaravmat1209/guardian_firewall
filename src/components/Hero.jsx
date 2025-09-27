import React, { useState, useEffect } from 'react';
import '../styles/Hero.css';

const Hero = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // EXACT Quantra timing - trigger animations immediately
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          {/* Main Heading - EXACT Quantra structure */}
          <h1 className={`hero-title ${isVisible ? 'animate' : ''}`}>
            <span className="hero-title-line">
              GUARDIAN AI:
            </span>
            <span className="hero-title-line hero-title-accent">
              PROTECTING CHILDREN
            </span>
            <span className="hero-title-line">
              WHERE HARM BEGINS
            </span>
          </h1>

          {/* Subtitle - EXACT Quantra positioning */}
          <p className={`hero-subtitle ${isVisible ? 'animate' : ''}`}>
            Advanced AI monitoring for gaming chat platforms. Real-time threat detection 
            and intelligent content filtering to keep children safe in digital environments.
          </p>

          {/* Action Buttons - EXACT Quantra layout */}
          <div className={`hero-actions ${isVisible ? 'animate' : ''}`}>
            <a href="#demo" className="btn btn-primary hero-btn-primary">
              SEE DEMO
            </a>
            <a href="#features" className="btn btn-secondary hero-btn-secondary">
              LEARN MORE
            </a>
          </div>

          {/* Stats - EXACT Quantra style */}
          <div className={`hero-stats ${isVisible ? 'animate' : ''}`}>
            <div className="hero-stat">
              <div className="hero-stat-number">99.7%</div>
              <div className="hero-stat-label">ACCURACY</div>
            </div>
            <div className="hero-stat-divider"></div>
            <div className="hero-stat">
              <div className="hero-stat-number">&lt;100MS</div>
              <div className="hero-stat-label">RESPONSE TIME</div>
            </div>
            <div className="hero-stat-divider"></div>
            <div className="hero-stat">
              <div className="hero-stat-number">24/7</div>
              <div className="hero-stat-label">MONITORING</div>
            </div>
          </div>
        </div>

        {/* Scroll Indicator - EXACT Quantra positioning */}
        <div className={`hero-scroll ${isVisible ? 'animate' : ''}`}>
          <div className="hero-scroll-line"></div>
          <div className="hero-scroll-text">SCROLL</div>
        </div>
      </div>

      {/* Background Grid - EXACT Quantra style */}
      <div className="hero-background">
        <div className="hero-grid"></div>
      </div>
    </section>
  );
};

export default Hero;
