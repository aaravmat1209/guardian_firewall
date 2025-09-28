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
        {/* Centered Content - Clean Layout */}
        <div className="hero-content">
            {/* Simple Tagline Only */}
            <h1 className={`hero-title ${isVisible ? 'animate' : ''}`}>
              <div className="hero-guardian-text">
                <img src="/pqnd_pro.png" alt="GUARDIAN" className="hero-guardian-image" />
              </div>
              <span className="hero-title-line hero-title-accent">
                REAL TIME PROTECTION
              </span>
              <span className="hero-title-line">
                FOR YOUNG GAMERS.
              </span>
            </h1>
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
