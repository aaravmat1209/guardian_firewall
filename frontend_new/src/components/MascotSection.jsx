import React, { useState, useEffect, useRef } from 'react';
import './MascotSection.css';
import guardianLogo from '../assets/images/guardian_logo.png';

const MascotSection = () => {
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
      className={`mascot-section ${isVisible ? 'mascot-section-visible' : ''}`}
      id="meet-guardian"
    >
      <div className="mascot-section-container">
        {/* Section Header */}
        <div className="mascot-section-header">
          <h2 className={`mascot-section-title ${isVisible ? 'animate' : ''}`}>
            MEET YOUR GUARDIAN ANGEL
          </h2>
          <p className={`mascot-section-subtitle ${isVisible ? 'animate' : ''}`}>
            Your AI-powered protector watching over children 24/7
          </p>
        </div>

        {/* Mascot Showcase */}
        <div className="mascot-showcase">
          {/* Large Mascot Display */}
          <div className={`mascot-display ${isVisible ? 'animate' : ''}`}>
            <img 
              src={guardianLogo} 
              alt="Guardian AI Angel Mascot" 
              className="mascot-hero-image"
            />
            <div className="mascot-name">
              <h3>GUARDIAN ANGEL</h3>
              <p>AI Protector</p>
            </div>
          </div>

          {/* Mascot Story */}
          <div className="mascot-story">
            <div className={`mascot-story-item ${isVisible ? 'animate' : ''}`}>
              <div className="mascot-story-icon">🛡️</div>
              <div className="mascot-story-content">
                <h4>ALWAYS WATCHING</h4>
                <p>I monitor gaming chats 24/7, ensuring children are safe from online predators and harmful content.</p>
              </div>
            </div>

            <div className={`mascot-story-item ${isVisible ? 'animate' : ''}`}>
              <div className="mascot-story-icon">⚡</div>
              <div className="mascot-story-content">
                <h4>LIGHTNING FAST</h4>
                <p>My AI brain processes messages in under 100ms, detecting threats before they can cause harm.</p>
              </div>
            </div>

            <div className={`mascot-story-item ${isVisible ? 'animate' : ''}`}>
              <div className="mascot-story-icon">❤️</div>
              <div className="mascot-story-content">
                <h4>CARING PROTECTOR</h4>
                <p>I understand the difference between playful banter and real danger, protecting without being intrusive.</p>
              </div>
            </div>

            <div className={`mascot-story-item ${isVisible ? 'animate' : ''}`}>
              <div className="mascot-story-icon">🧠</div>
              <div className="mascot-story-content">
                <h4>ALWAYS LEARNING</h4>
                <p>My AI constantly evolves, learning new threat patterns to stay ahead of those who would harm children.</p>
              </div>
            </div>
          </div>
        </div>


        {/* Mascot Quote */}
        <div className={`mascot-quote ${isVisible ? 'animate' : ''}`}>
          <blockquote>
            "Every child deserves to play safely online. I'm here to make sure they can."
          </blockquote>
          <cite>— Guardian Angel, AI Protector</cite>
        </div>
      </div>
    </section>
  );
};

export default MascotSection;
