import React from 'react';
import './MessageBubble.css';

const MessageBubble = ({ message, isUser, risk, isVisible, delay }) => {
  const isHighRisk = risk > 60;
  
  return (
    <div 
      className={`message-bubble ${isUser ? 'message-user' : 'message-other'} ${isHighRisk ? 'message-threat' : ''} ${isVisible ? 'message-visible' : ''}`}
      style={{
        '--delay': `${delay}ms`
      }}
    >
      <div className="message-content">
        <div className="message-author">
          {message.author}
        </div>
        <div className="message-text">
          {message.text}
        </div>
        {risk > 0 && (
          <div className="message-risk">
            Risk: {risk}%
          </div>
        )}
      </div>
      {isHighRisk && (
        <div className="message-threat-indicator">
          ⚠️
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
