import { Server, Room } from 'colyseus';
import { Schema, MapSchema, type } from '@colyseus/schema';
import http from 'http';
import express from 'express';
import cors from 'cors';

// Chat message schema
class ChatMessage extends Schema {
  constructor() {
    super();
    this.id = "";
    this.username = "";
    this.text = "";
    this.timestamp = 0;
    this.riskLevel = "pending";
    this.riskScore = 0;
  }
}
type(ChatMessage, "id", "string");
type(ChatMessage, "username", "string");
type(ChatMessage, "text", "string");
type(ChatMessage, "timestamp", "number");
type(ChatMessage, "riskLevel", "string");
type(ChatMessage, "riskScore", "number");

// Player schema
class Player extends Schema {
  constructor() {
    super();
    this.username = "";
    this.isOnline = true;
  }
}
type(Player, "username", "string");
type(Player, "isOnline", "boolean");

// Room state schema
class ChatRoomState extends Schema {
  constructor() {
    super();
    this.messages = new MapSchema();
    this.players = new MapSchema();
  }
}
type(ChatRoomState, "messages", { map: ChatMessage });
type(ChatRoomState, "players", { map: Player });

class ChatRoom extends Room {
  maxClients = 50;

  onCreate(options) {
    this.setState(new ChatRoomState());
    console.log("ChatRoom created with options:", options);

    // Handle incoming messages
    this.onMessage("chat_message", (client, message) => {
      this.handleChatMessage(client, message);
    });
  }

  onJoin(client, options) {
    console.log(`${client.sessionId} joined the chat room`);

    // Add player to room
    this.state.players.set(client.sessionId, new Player().assign({
      username: options.username || `User${Math.floor(Math.random() * 1000)}`,
      isOnline: true
    }));

    // Send welcome message
    this.broadcast("system_message", {
      text: `${this.state.players.get(client.sessionId).username} joined the chat`,
      type: "join"
    });
  }

  onLeave(client) {
    console.log(`${client.sessionId} left the chat room`);

    const player = this.state.players.get(client.sessionId);
    if (player) {
      this.broadcast("system_message", {
        text: `${player.username} left the chat`,
        type: "leave"
      });
      this.state.players.delete(client.sessionId);
    }
  }

  async handleChatMessage(client, messageData) {
    const player = this.state.players.get(client.sessionId);
    if (!player) return;

    console.log(`Message from ${player.username}: ${messageData.text}`);

    // Create message object
    const messageId = `msg_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
    const chatMessage = new ChatMessage();
    chatMessage.id = messageId;
    chatMessage.username = player.username;
    chatMessage.text = messageData.text;
    chatMessage.timestamp = Date.now();
    chatMessage.riskLevel = "pending";
    chatMessage.riskScore = 0;

    // Add to room state
    this.state.messages.set(messageId, chatMessage);

    try {
      // Send to Guardian AI for analysis
      const response = await fetch('http://localhost:8000/api/classify/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: messageData.text,
          conversation_history: this.getRecentMessages(),
          user_id: player.username
        })
      });

      if (response.ok) {
        const result = await response.json();

        // Update message with risk analysis
        chatMessage.riskLevel = result.risk_level;
        chatMessage.riskScore = result.confidence_score;

        // Broadcast risk update to all clients
        this.broadcast("risk_update", {
          messageId: messageId,
          riskLevel: result.risk_level,
          riskScore: result.confidence_score,
          explanations: result.explanations,
          shouldPause: result.should_pause
        });

        console.log(`Risk analysis: ${result.risk_level} (${result.confidence_score})`);
      }
    } catch (error) {
      console.error('Error analyzing message:', error);
      chatMessage.riskLevel = "error";
      chatMessage.riskScore = 0;
    }
  }

  getRecentMessages() {
    const messages = Array.from(this.state.messages.values())
      .sort((a, b) => a.timestamp - b.timestamp)
      .slice(-10); // Last 10 messages

    return messages.map(msg => ({
      role: "user",
      text: msg.text,
      username: msg.username
    }));
  }

  onDispose() {
    console.log("ChatRoom disposed");
  }
}

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());

// Create HTTP server
const server = http.createServer(app);

// Create Colyseus server
const gameServer = new Server({
  server: server,
});

// Register the chat room
gameServer.define('chat_room', ChatRoom);

// Health check endpoint
app.get('/health', (_, res) => {
  res.json({ status: 'ok', rooms: gameServer.rooms.size });
});

const port = process.env.PORT || 3001;
gameServer.listen(port);
console.log(`🚀 Colyseus Chat Server listening on port ${port}`);