import React, { useState, useRef } from 'react';
import MessageBubble from './MessageBubble';
import ThreatMeter from './ThreatMeter';
import DemoControls from './DemoControls';
import './ChatDemo.css';

const ChatDemo = () => {
  const [messages, setMessages] = useState([]);
  const [currentRisk, setCurrentRisk] = useState(0);
  const [currentPatterns, setCurrentPatterns] = useState([]);
  const [confidence] = useState(95);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentScenario, setCurrentScenario] = useState(null);
  const [visibleMessages, setVisibleMessages] = useState([]);
  const chatContainerRef = useRef(null);

  // Scenario data
  const predatorScenario = [
    { author: "Player_42", text: "hey you're really good at this game!", risk: 0, patterns: [] },
    { author: "You", text: "thanks! been playing for a while", risk: 0, patterns: [] },
    { author: "Player_42", text: "how old are you?", risk: 30, patterns: [{ name: "Age inquiry", severity: "medium" }] },
    { author: "You", text: "why do you want to know?", risk: 0, patterns: [] },
    { author: "Player_42", text: "just curious, what grade are you in?", risk: 45, patterns: [{ name: "Age inquiry", severity: "medium" }, { name: "Personal info request", severity: "medium" }] },
    { author: "Player_42", text: "do you have discord? we could play together", risk: 65, patterns: [{ name: "Age inquiry", severity: "medium" }, { name: "Personal info request", severity: "medium" }, { name: "External platform", severity: "high" }] },
    { author: "Player_42", text: "don't tell your parents but I have a secret to share", risk: 85, patterns: [{ name: "Age inquiry", severity: "medium" }, { name: "Personal info request", severity: "medium" }, { name: "External platform", severity: "high" }, { name: "Secrecy request", severity: "high" }] },
    { author: "Player_42", text: "can you send me a picture of yourself?", risk: 95, patterns: [{ name: "Age inquiry", severity: "medium" }, { name: "Personal info request", severity: "medium" }, { name: "External platform", severity: "high" }, { name: "Secrecy request", severity: "high" }, { name: "Image request", severity: "high" }] }
  ];

  const normalScenario = [
    { author: "TeamMate_5", text: "nice shot!", risk: 0, patterns: [] },
    { author: "You", text: "thanks, good teamwork", risk: 0, patterns: [] },
    { author: "TeamMate_5", text: "want to try the new map?", risk: 0, patterns: [] },
    { author: "You", text: "sure, sounds fun", risk: 0, patterns: [] },
    { author: "TeamMate_5", text: "I'll grab some better gear first", risk: 0, patterns: [] },
    { author: "TeamMate_5", text: "ready when you are!", risk: 0, patterns: [] }
  ];

  const playScenario = async (scenario, scenarioName) => {
    setIsPlaying(true);
    setCurrentScenario(scenarioName);
    setMessages([]);
    setVisibleMessages([]);
    setCurrentRisk(0);
    setCurrentPatterns([]);

    for (let i = 0; i < scenario.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setMessages(prev => [...prev, scenario[i]]);
      setVisibleMessages(prev => [...prev, i]);
      setCurrentRisk(scenario[i].risk);
      setCurrentPatterns(scenario[i].patterns);
      
      // Scroll to bottom
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }
    }

    setIsPlaying(false);
    setCurrentScenario(null);
  };

  const handleRunPredator = () => {
    playScenario(predatorScenario, 'predator');
  };

  const handleRunNormal = () => {
    playScenario(normalScenario, 'normal');
  };

  const handleReset = () => {
    setMessages([]);
    setVisibleMessages([]);
    setCurrentRisk(0);
    setCurrentPatterns([]);
    setIsPlaying(false);
    setCurrentScenario(null);
  };

  return (
    <div className="chat-demo">
      {/* Demo Controls */}
      <DemoControls
        onRunPredator={handleRunPredator}
        onRunNormal={handleRunNormal}
        onReset={handleReset}
        isPlaying={isPlaying}
        currentScenario={currentScenario}
      />

      {/* Main Demo Interface */}
      <div className="chat-demo-interface">
        {/* Chat Window */}
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-game-info">
              <div className="chat-game-title">FORTCRAFT ARENA</div>
              <div className="chat-game-subtitle">Team Chat</div>
            </div>
            <div className="chat-status">
              <div className="chat-status-indicator"></div>
              <span>LIVE</span>
            </div>
          </div>
          
          <div className="chat-messages" ref={chatContainerRef}>
            {messages.length === 0 ? (
              <div className="chat-empty">
                <div className="chat-empty-icon">💬</div>
                <div className="chat-empty-text">Select a scenario to start the demo</div>
              </div>
            ) : (
              messages.map((message, index) => (
                <MessageBubble
                  key={index}
                  message={message}
                  isUser={message.author === "You"}
                  risk={message.risk}
                  isVisible={visibleMessages.includes(index)}
                  delay={0}
                />
              ))
            )}
          </div>
          
          <div className="chat-input">
            <div className="chat-input-field">
              <input 
                type="text" 
                placeholder="Type a message..." 
                disabled 
              />
              <button className="chat-send-btn" disabled>
                SEND
              </button>
            </div>
          </div>
        </div>

        {/* Threat Analysis Panel */}
        <div className="threat-analysis">
          <div className="threat-analysis-header">
            <h3 className="threat-analysis-title">THREAT ANALYSIS</h3>
            <div className="threat-analysis-status">
              <div className="threat-status-indicator"></div>
              <span>MONITORING</span>
            </div>
          </div>
          
          <ThreatMeter
            riskLevel={currentRisk}
            patterns={currentPatterns}
            confidence={confidence}
            isActive={messages.length > 0}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatDemo;
