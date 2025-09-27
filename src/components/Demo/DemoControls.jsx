import React from 'react';
import './DemoControls.css';

const DemoControls = ({ onRunPredator, onRunNormal, onReset, isPlaying, currentScenario }) => {
  return (
    <div className="demo-controls">
      <h3 className="demo-controls-title">DEMO SCENARIOS</h3>
      
      <div className="demo-controls-buttons">
        <button 
          className={`btn btn-primary demo-btn ${isPlaying && currentScenario === 'predator' ? 'btn-playing' : ''}`}
          onClick={onRunPredator}
          disabled={isPlaying}
        >
          <span className="btn-text">RUN PREDATOR SCENARIO</span>
          {isPlaying && currentScenario === 'predator' && (
            <div className="btn-playing-indicator">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </button>
        
        <button 
          className={`btn btn-secondary demo-btn ${isPlaying && currentScenario === 'normal' ? 'btn-playing' : ''}`}
          onClick={onRunNormal}
          disabled={isPlaying}
        >
          <span className="btn-text">NORMAL CHAT</span>
          {isPlaying && currentScenario === 'normal' && (
            <div className="btn-playing-indicator">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </button>
        
        <button 
          className="btn btn-secondary demo-btn demo-btn-reset"
          onClick={onReset}
          disabled={isPlaying}
        >
          <span className="btn-text">RESET DEMO</span>
        </button>
      </div>
      
      <div className="demo-controls-info">
        <p className="demo-info-text">
          Select a scenario to see Guardian AI's real-time threat detection in action.
        </p>
      </div>
    </div>
  );
};

export default DemoControls;
