import React, { useState, useEffect, useRef } from 'react';
import './VoiceChat.css';

const VoiceChat = ({ onClose }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  
  const audioRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const agentId = 'agent_3901k66wwr5qfhjawxq25g5g9stf';

  useEffect(() => {
    return () => {
      // Cleanup
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const connectToAgent = async () => {
    setIsConnecting(true);
    setError(null);

    try {
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Initialize media recorder
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudioInput(audioBlob);
      };

      setIsConnected(true);
      setConnectionStatus('connected');
      addMessage('system', 'Connected to Guardian AI Agent. You can now start speaking!');
      
      // Play the agent's first message
      setTimeout(() => {
        addMessage('agent', '🤖 Guardian AI: "hey that last game was so fun"');
        // You can add audio playback here if you want to play the first message
      }, 1000);
      
    } catch (err) {
      console.error('Failed to connect:', err);
      setError('Failed to access microphone. Please check permissions.');
    } finally {
      setIsConnecting(false);
    }
  };

  const processAudioInput = async (audioBlob) => {
    try {
      addMessage('user', '🎤 Speaking...');

      // Send to ElevenLabs agent using the correct API endpoint
      const apiKey = process.env.REACT_APP_ELEVENLABS_API_KEY;
      
      if (!apiKey || apiKey === 'your_elevenlabs_api_key_here') {
        setError('ElevenLabs API key not configured');
        addMessage('system', '❌ API key not found. Please check configuration.');
        return;
      }

      // Show processing message immediately
      addMessage('system', '🔄 Processing your message...');

      // Create FormData for the request
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.wav');

      // Use the correct ElevenLabs agent conversation endpoint
      const response = await fetch(`https://api.elevenlabs.io/v1/agents/${agentId}/conversation`, {
        method: 'POST',
        headers: {
          'xi-api-key': apiKey,
        },
        body: formData
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const responseData = await response.blob();
      
      // Play the response immediately
      if (responseData && responseData.size > 0) {
        const audioUrl = URL.createObjectURL(responseData);
        playAudio(audioUrl);
        addMessage('agent', '🤖 Guardian AI is responding...');
      } else {
        addMessage('agent', '🤖 Guardian AI: I heard you, but no audio response was generated');
      }
    } catch (err) {
      console.error('Failed to process audio:', err);
      setError('Failed to process voice input: ' + err.message);
      addMessage('system', '❌ Error: ' + err.message);
    }
  };

  const playAudio = (audioUrl) => {
    if (audioRef.current) {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
      setIsPlaying(true);
      
      audioRef.current.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
    }
  };

  const startRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'inactive') {
      audioChunksRef.current = [];
      mediaRecorderRef.current.start();
      setIsRecording(true);
      addMessage('system', 'Recording... Speak now.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      addMessage('system', 'Processing your message...');
    }
  };

  const addMessage = (type, content) => {
    const message = {
      id: Date.now(),
      type,
      content,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, message]);
  };

  const testApiConnection = async () => {
    try {
      addMessage('system', '🧪 Testing API connection...');
      
      const apiKey = process.env.REACT_APP_ELEVENLABS_API_KEY;
      
      if (!apiKey || apiKey === 'your_elevenlabs_api_key_here') {
        setError('ElevenLabs API key not configured');
        addMessage('system', '❌ API key not found in environment variables');
        return;
      }

      // Test the API by making a simple request
      const response = await fetch(`https://api.elevenlabs.io/v1/agents/${agentId}`, {
        method: 'GET',
        headers: {
          'xi-api-key': apiKey,
        }
      });

      if (response.ok) {
        const agentData = await response.json();
        addMessage('system', '✅ API connection successful!');
        addMessage('system', `🤖 Agent: ${agentData.name || 'Support agent'}`);
        addMessage('system', `🌐 Status: ${agentData.status || 'Active'}`);
        setError(null);
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (err) {
      console.error('API test failed:', err);
      setError('API test failed: ' + err.message);
      addMessage('system', '❌ API test failed: ' + err.message);
    }
  };

  const disconnect = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    setIsConnected(false);
    setConnectionStatus('disconnected');
    setIsRecording(false);
    setIsPlaying(false);
    setMessages([]);
  };

  return (
    <div className="voice-chat-container">
      <div className="voice-chat-header">
        <div className="voice-chat-title">
          <span className="voice-chat-icon">🎤</span>
          <h2>Guardian AI Voice Chat</h2>
        </div>
        <button className="voice-chat-close" onClick={onClose}>
          ×
        </button>
      </div>

      <div className="voice-chat-content">
        {/* Connection Status */}
        <div className="voice-status">
          <div className={`status-indicator ${connectionStatus}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {connectionStatus === 'connected' ? 'CONNECTED' : 
               connectionStatus === 'connecting' ? 'CONNECTING...' : 'DISCONNECTED'}
            </span>
          </div>
          <div className="agent-info">
            <span className="agent-id">Agent: {agentId}</span>
            <span className="api-status">
              API: {process.env.REACT_APP_ELEVENLABS_API_KEY ? '✅ Configured' : '❌ Missing'}
            </span>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="voice-error">
            <span className="error-icon">⚠️</span>
            <span className="error-text">{error}</span>
          </div>
        )}

        {/* Messages */}
        <div className="voice-messages">
          {messages.length === 0 ? (
            <div className="voice-empty">
              <div className="empty-icon">💬</div>
              <p>No messages yet. Connect to start your conversation with Guardian AI.</p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`voice-message ${message.type}`}>
                <div className="message-content">
                  <span className="message-text">{message.content}</span>
                  <span className="message-time">{message.timestamp}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Controls */}
        <div className="voice-controls">
          {!isConnected ? (
            <div className="voice-controls-disconnected">
              <button 
                className="voice-btn connect-btn"
                onClick={connectToAgent}
                disabled={isConnecting}
              >
                {isConnecting ? 'Connecting...' : 'Connect to Agent'}
              </button>
              
              <button 
                className="voice-btn test-btn"
                onClick={testApiConnection}
                disabled={isConnecting}
              >
                Test API Connection
              </button>
            </div>
          ) : (
            <div className="voice-controls-active">
              <button 
                className={`voice-btn record-btn ${isRecording ? 'recording' : ''}`}
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isPlaying}
              >
                {isRecording ? 'Stop Recording' : 'Start Recording'}
              </button>
              
              <button 
                className="voice-btn disconnect-btn"
                onClick={disconnect}
              >
                Disconnect
              </button>
            </div>
          )}
        </div>

        {/* Audio Element */}
        <audio ref={audioRef} />
      </div>
    </div>
  );
};

export default VoiceChat;
