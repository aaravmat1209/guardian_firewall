import React, { useState, useEffect, useRef } from 'react';
import { Client, Room } from 'colyseus.js';
import './LiveChatRoom.css';

const LiveChatRoom = () => {
  const [client] = useState(() => new Client('ws://localhost:3001'));
  const [room, setRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [currentUser, setCurrentUser] = useState('Player_42');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectToRoom = async () => {
    try {
      if (room) {
        await room.leave();
      }

      const newRoom = await client.joinOrCreate('chat_room', { username: currentUser });
      setRoom(newRoom);
      setIsConnected(true);

      // Listen for state changes
      newRoom.state.messages.onAdd = (message, key) => {
        setMessages(prev => [...prev, message]);
      };

      newRoom.state.messages.onChange = (message, key) => {
        setMessages(prev => prev.map(m => m.id === key ? message : m));
      };

      // Listen for risk updates
      newRoom.onMessage('risk_update', (data) => {
        console.log('Risk update received:', data);
        // Update message with risk information
        setMessages(prev => prev.map(msg => 
          msg.id === data.messageId 
            ? { ...msg, riskLevel: data.riskLevel, riskScore: data.riskScore }
            : msg
        ));
      });

      console.log('Connected to FortCraft Arena chat as', currentUser);
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  };

  const sendMessage = () => {
    if (!room || !currentMessage.trim()) return;

    // Add message locally for immediate UI update
    const newMessage = {
      id: `msg_${Date.now()}`,
      username: currentUser,
      text: currentMessage,
      timestamp: Date.now(),
      riskLevel: 'pending',
      riskScore: 0
    };

    setMessages(prev => [...prev, newMessage]);
    room.send('chat_message', { text: currentMessage });
    setCurrentMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour12: true,
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'high': return '#DC2626';
      case 'medium': return '#F59E0B';
      case 'low': return '#10B981';
      default: return '#6B7280';
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return '✅';
      default: return '⏳';
    }
  };

  // Auto-connect on mount
  useEffect(() => {
    connectToRoom();
  }, []);

  return (
    <div className="live-chat-room">
      {/* FortCraft Arena Header */}
      <div className="chat-header">
        <div className="game-logo">
          <span className="game-icon">🎮</span>
          <div className="game-info">
            <h3>FORTCRAFT ARENA</h3>
            <p>TEAM CHAT</p>
          </div>
        </div>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
          </span>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <div className="empty-icon">💬</div>
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`message-bubble ${message.username === currentUser ? 'user-message' : 'other-message'}`}>
              <div className="message-header">
                <span className="username">{message.username}</span>
                <span className="timestamp">{formatTime(message.timestamp)}</span>
                {message.riskLevel && message.riskLevel !== 'pending' && (
                  <span 
                    className="risk-indicator"
                    style={{ color: getRiskColor(message.riskLevel) }}
                    title={`Risk Level: ${message.riskLevel} (${message.riskScore}%)`}
                  >
                    {getRiskIcon(message.riskLevel)}
                  </span>
                )}
              </div>
              <div className="message-content">
                <p>{message.text}</p>
                {message.riskLevel === 'high' && (
                  <div className="threat-alert">
                    <span className="alert-icon">🚨</span>
                    <span className="alert-text">THREAT DETECTED</span>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="chat-input">
        <div className="input-container">
          <input
            type="text"
            placeholder={`Message as ${currentUser}...`}
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            className="message-input"
            disabled={!isConnected}
          />
          <button
            onClick={sendMessage}
            disabled={!currentMessage.trim() || !isConnected}
            className="send-button"
          >
            Send
          </button>
        </div>
        <div className="input-footer">
          <span className="message-count">{messages.length} messages</span>
          <span className="user-info">Playing as: {currentUser}</span>
        </div>
      </div>
    </div>
  );
};

export default LiveChatRoom;

