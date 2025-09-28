import React from 'react';
import './AboutSection.css';

const AboutSection = () => {
  return (
    <section id="about" className="about-section">
      <div className="about-section-container">
        <div className="about-content">
          <div className="about-header">
            <h2 className="about-title">About Guardian AI</h2>
            <div className="divider-red"></div>
          </div>
          
          <div className="about-content-main">
            <div className="about-text">
              <h3>Real-Time Protection for Young Gamers</h3>
              <p>
                Guardian AI is an advanced artificial intelligence system designed to protect children 
                during their online gaming experiences. Our cutting-edge voice and text monitoring technology 
                analyzes conversations and messages in real-time, detecting potential threats and harmful content 
                before they can impact your child's safety.
              </p>
              
              <h4>How It Works</h4>
              <p>
                Using state-of-the-art conversational AI, Guardian monitors both voice chats and text messages 
                during gaming sessions. When potentially harmful content is detected, our AI can immediately alert 
                parents or switch to a protective mode, ensuring your child's gaming experience 
                remains safe and enjoyable.
              </p>
            </div>
            
            <div className="about-stats">
              <div className="stat-item">
                <div className="stat-number">99.9%</div>
                <div className="stat-label">Accuracy Rate</div>
              </div>
              
              <div className="stat-item">
                <div className="stat-number">&lt;100ms</div>
                <div className="stat-label">Response Time</div>
              </div>
              
              <div className="stat-item">
                <div className="stat-number">24/7</div>
                <div className="stat-label">Monitoring</div>
              </div>
            </div>
            
            <div className="about-features">
              <div className="feature-item">
                <span className="feature-icon">🎮</span>
                <div className="feature-content">
                  <h5>Gaming-Focused</h5>
                  <p>Specifically designed for online gaming environments</p>
                </div>
              </div>
              
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <div className="feature-content">
                  <h5>Real-Time Analysis</h5>
                  <p>Instant threat detection and response</p>
                </div>
              </div>
              
              <div className="feature-item">
                <span className="feature-icon">🛡️</span>
                <div className="feature-content">
                  <h5>AI-Powered Protection</h5>
                  <p>Advanced machine learning for accurate detection</p>
                </div>
              </div>
              
              <div className="feature-item">
                <span className="feature-icon">👨‍👩‍👧‍👦</span>
                <div className="feature-content">
                  <h5>Parent Peace of Mind</h5>
                  <p>Keep your children safe while they have fun</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="about-cta">
            <h3>Ready to Protect Your Child?</h3>
            <p>Join thousands of families who trust Guardian AI to keep their children safe online.</p>
            <button className="cta-button">
              Get Started Today
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
