import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Client } from 'colyseus.js';
import MessageBubble from './MessageBubble';
import ThreatMeter from './ThreatMeter';
import './LiveChatRoom.css';

const LiveChatRoom = () => {
  const [client] = useState(() => new Client('ws://localhost:3001'));
  const [room, setRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [currentUser, setCurrentUser] = useState('user_77');
  const [selectedUser, setSelectedUser] = useState('user_77');
  const [currentRisk, setCurrentRisk] = useState(0);
  const [currentPatterns, setCurrentPatterns] = useState([]);
  const [confidence, setConfidence] = useState(0);
  const [currentExplanations, setCurrentExplanations] = useState([]);
  const [conversationTrend, setConversationTrend] = useState("stable");
  const messagesEndRef = useRef(null);
  const chatMessagesRef = useRef(null);
  const inputRef = useRef(null);
  const [userScrolled, setUserScrolled] = useState(false);

  const scrollToBottom = () => {
    // Only scroll if input is not focused to prevent input jumping
    if (document.activeElement !== inputRef.current) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  const checkIfScrolledToBottom = () => {
    if (chatMessagesRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = chatMessagesRef.current;
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10; // 10px tolerance
      return isAtBottom;
    }
    return true;
  };

  const handleScroll = () => {
    const isAtBottom = checkIfScrolledToBottom();
    setUserScrolled(!isAtBottom);
  };

  useEffect(() => {
    // Only auto-scroll if user hasn't manually scrolled up
    if (!userScrolled) {
      scrollToBottom();
    }
  }, [messages, userScrolled]);

  const connectToRoom = useCallback(async (username) => {
    try {
      if (room) {
        await room.leave();
      }

      const newRoom = await client.joinOrCreate('chat_room', { username: username || currentUser });
      setRoom(newRoom);
      setIsConnected(true);

      // Listen for state changes - wait for state to be ready
      newRoom.onStateChange((state) => {
        if (state.messages) {
          const messagesArray = Array.from(state.messages.values());
          setMessages(messagesArray);
        }
      });


      // Listen for system messages (join/leave notifications)
      newRoom.onMessage('system_message', (data) => {
        console.log('System message:', data);
      });

      // Listen for Guardian AI analysis updates
      newRoom.onMessage('guardian_ai_update', (data) => {
        console.log('🚨 Guardian AI analysis received:', data);
        console.log('🔍 FRONTEND DEBUG - Patterns received:', data.patterns);
        console.log('🔍 FRONTEND DEBUG - Patterns array length:', data.patterns ? data.patterns.length : 'undefined');
        console.log('🔄 Updating ThreatMeter with:', {
          riskScore: data.riskScore,
          patterns: data.patterns,
          confidence: data.confidence
        });

        // Update threat meter with real Guardian AI data
        setCurrentRisk(data.riskScore);
        setCurrentPatterns(data.patterns || []);
        setConfidence(data.confidence);
        setCurrentExplanations(data.explanations || []);
        setConversationTrend(data.conversationTrend || "stable");

        console.log('🔍 FRONTEND DEBUG - currentPatterns state after update:', data.patterns || []);
        console.log('🔍 FRONTEND DEBUG - currentExplanations state after update:', data.explanations || []);
        console.log('🔍 FRONTEND DEBUG - conversationTrend state after update:', data.conversationTrend || "stable");

        // Update message with Guardian AI analysis
        setMessages(prev => prev.map(msg =>
          msg.id === data.messageId
            ? {
                ...msg,
                riskLevel: data.riskLevel,
                riskScore: data.riskScore,
                guardianAnalysis: {
                  explanations: data.explanations,
                  action: data.action,
                  confidence: data.confidence
                }
              }
            : msg
        ));
      });

      console.log('Connected to FortCraft Arena chat as', username || currentUser);
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  }, [client]);

  const switchUser = (username) => {
    setSelectedUser(username);
    setCurrentUser(username);
    // Reconnect with new username
    connectToRoom(username);
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

    // Reset scroll state so it scrolls to show your own message
    setUserScrolled(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };


  // Auto-connect on mount only
  useEffect(() => {
    connectToRoom();
  }, []);

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

      {/* Main Chat Interface - Grid Layout like Demo */}
      <div className="chat-demo-interface">
        {/* Chat Window */}
        <div className="chat-window">
          {/* FortCraft Arena Header */}
          <div className="chat-header">
            <div className="chat-game-info">
              <div className="chat-game-title">FORTCRAFT ARENA</div>
              <div className="chat-game-subtitle">Team Chat</div>
            </div>
            <div className="chat-status">
              <div className="chat-status-indicator"></div>
              <span>{isConnected ? 'LIVE' : 'OFFLINE'}</span>
            </div>
          </div>

          {/* Chat Messages */}
          <div
            className="chat-messages"
            ref={chatMessagesRef}
            onScroll={handleScroll}
          >
            {messages.length === 0 ? (
              <div className="chat-empty">
                <div className="chat-empty-icon">💬</div>
                <div className="chat-empty-text">No messages yet. Start the conversation!</div>
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
            <div className="chat-input-field">
              <input
                ref={inputRef}
                type="text"
                placeholder={`Message as ${currentUser}...`}
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={!isConnected}
              />
              <button 
                className="chat-send-btn" 
                onClick={sendMessage}
                disabled={!currentMessage.trim() || !isConnected}
              >
                SEND
              </button>
            </div>
          </div>
        </div>

        {/* Threat Analysis Panel - Right Side */}
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
            explanations={currentExplanations}
            conversationTrend={conversationTrend}
            isActive={messages.length > 0}
          />
        </div>
      </div>
    </div>
  );
};

export default LiveChatRoom;

