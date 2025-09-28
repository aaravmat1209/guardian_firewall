import React, { useState, useEffect, useRef } from 'react';
import './FloatingVoiceWidget.css';

const FloatingVoiceWidget = () => {
  const [widgetLoaded, setWidgetLoaded] = useState(false);
  const widgetRef = useRef(null);
  const agentId = 'agent_3901k66wwr5qfhjawxq25g5g9stf';

  useEffect(() => {
    // Check if script is already loaded (from HTML head)
    const checkScriptLoaded = () => {
      const existingScript = document.querySelector('script[src="https://unpkg.com/@elevenlabs/convai-widget-embed"]');
      if (existingScript) {
        // Wait a bit for the script to fully initialize
        setTimeout(() => {
          setWidgetLoaded(true);
        }, 500);
      } else {
        // Script not found, try again
        setTimeout(checkScriptLoaded, 100);
      }
    };

    checkScriptLoaded();
  }, []);

  useEffect(() => {
    if (widgetLoaded && widgetRef.current) {
      try {
        // Clear the container
        widgetRef.current.innerHTML = '';
        
        // Create the widget element
        const widgetElement = document.createElement('elevenlabs-convai');
        widgetElement.setAttribute('agent-id', agentId);
        
        // Append to container
        widgetRef.current.appendChild(widgetElement);
        
        console.log('Floating widget element created and appended');
      } catch (err) {
        console.error('Error creating floating widget element:', err);
      }
    }
  }, [widgetLoaded, agentId]);


  return (
    <div className="floating-widget-container">
      {widgetLoaded ? (
        <div ref={widgetRef} className="widget-content" />
      ) : (
        <div className="widget-loading">
          <div className="loading-spinner">⏳</div>
          <p>Loading Guardian AI...</p>
        </div>
      )}
    </div>
  );
};

export default FloatingVoiceWidget;
