import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Client } from 'colyseus.js';
import MessageBubble from './MessageBubble';
import './LiveChatRoom.css';

const LiveChatRoom = () => {
  const [client] = useState(() => new Client('ws://localhost:3001'));
  const [room, setRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [currentUser, setCurrentUser] = useState('user_77');
  const [selectedUser, setSelectedUser] = useState('user_77');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectToRoom = useCallback(async () => {
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

      console.log('Connected to FortCraft Arena chat as', selectedUser);
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  }, [client, currentUser]);

  const switchUser = (username) => {
    setSelectedUser(username);
    setCurrentUser(username);
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

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };


  // Auto-connect on mount
  useEffect(() => {
    connectToRoom();
  }, [connectToRoom]);

  return (
    <div className="live-chat-room">
      {/* User Controls */}
      <div className="user-controls">
        <div className="user-selector">
          <button
            className={`user-btn ${selectedUser === 'user_77' ? 'active' : ''}`}
            onClick={() => switchUser('user_77')}
          >
            👤 user_77
          </button>
          <button
            className={`user-btn ${selectedUser === 'Pred_15' ? 'active' : ''}`}
            onClick={() => switchUser('Pred_15')}
          >
            🕴️ Pred_15
          </button>
        </div>
        <div className="current-user-display">
          Playing as: <strong>{currentUser}</strong>
        </div>
      </div>

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
            <MessageBubble
              key={message.id}
              message={{
                author: message.username,
                text: message.text,
                risk: message.riskScore || 0
              }}
              isUser={message.username === 'user_77'}
              risk={message.riskScore || 0}
              isVisible={true}
              delay={0}
            />
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
            onKeyDown={handleKeyDown}
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

