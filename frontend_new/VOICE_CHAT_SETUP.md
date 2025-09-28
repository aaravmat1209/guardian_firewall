# Voice Chat Setup Instructions

## ElevenLabs Integration

To enable voice chat functionality, you need to set up your ElevenLabs API key:

### 1. Get Your ElevenLabs API Key
1. Go to [ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)
2. Create a new API key
3. Copy the API key

### 2. Set Environment Variable
Create a `.env` file in the `frontend_new` directory with:

```
REACT_APP_ELEVENLABS_API_KEY=your_actual_api_key_here
```

### 3. Agent Configuration
The voice chat is configured to use the ElevenLabs agent with ID: `agent_3901k66wwr5qfhjawxq25g5g9stf`

### 4. Features
- **Voice Chat Modal**: Choose between voice and text chat
- **Real-time Voice**: Connect to ElevenLabs agent for live conversation
- **Microphone Access**: Browser will request microphone permission
- **Audio Playback**: Agent responses are played automatically
- **Connection Status**: Visual indicators for connection state

### 5. Usage
1. Click "GET STARTED" in the navbar
2. Select "Voice Chat Simulation"
3. Click "Connect to Agent"
4. Allow microphone access when prompted
5. Start speaking to interact with the Guardian AI agent

### 6. Troubleshooting
- **Microphone Permission**: Ensure browser has microphone access
- **API Key**: Verify your ElevenLabs API key is correct
- **Network**: Check internet connection for API calls
- **Browser**: Use a modern browser with WebRTC support

### 7. Development Notes
- The voice chat component includes error handling
- Audio processing is handled through MediaRecorder API
- ElevenLabs SDK is used for agent communication
- Real-time audio streaming is supported
