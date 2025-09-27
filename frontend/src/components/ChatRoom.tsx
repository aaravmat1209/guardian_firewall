import React, { useState, useEffect, useRef } from 'react';
import { Client, Room } from 'colyseus.js';

interface ChatMessage {
  id: string;
  username: string;
  text: string;
  timestamp: number;
  riskLevel?: string;
  riskScore?: number;
}

interface User {
  id: string;
  username: string;
  color: string;
  avatar: string;
}

interface Player {
  username: string;
  isOnline: boolean;
}

export const ChatRoom: React.FC = () => {
  const [client] = useState(() => new Client('ws://localhost:3001'));
  const [room, setRoom] = useState<Room | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [users, setUsers] = useState<User[]>([
    { id: '1', username: 'Alice', color: 'bg-pink-500', avatar: '👩' },
    { id: '2', username: 'Bob', color: 'bg-blue-500', avatar: '👨' },
    { id: '3', username: 'Charlie', color: 'bg-green-500', avatar: '🧑' },
    { id: '4', username: 'Diana', color: 'bg-purple-500', avatar: '👩‍💼' },
    { id: '5', username: 'Eve', color: 'bg-orange-500', avatar: '👩‍🎓' }
  ]);
  const [selectedUserId, setSelectedUserId] = useState('1');
  const [isEditing, setIsEditing] = useState<string | null>(null);
  const [editUsername, setEditUsername] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

      const selectedUser = users.find(u => u.id === selectedUserId);
      if (!selectedUser) return;

      const newRoom = await client.joinOrCreate('chat_room', { username: selectedUser.username });
      setRoom(newRoom);
      setIsConnected(true);

      // Listen for state changes
      newRoom.state.messages.onAdd = (message: ChatMessage, key: string) => {
        setMessages(prev => [...prev, message]);
      };

      newRoom.state.messages.onChange = (message: ChatMessage, key: string) => {
        setMessages(prev => prev.map(m => m.id === key ? message : m));
      };

      console.log('Connected to chat room as', selectedUser.username);
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  };

  const sendMessage = () => {
    if (!room || !currentMessage.trim()) return;

    const selectedUser = users.find(u => u.id === selectedUserId);
    if (!selectedUser) return;

    // Add message locally for immediate UI update
    const newMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      username: selectedUser.username,
      text: currentMessage,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, newMessage]);
    room.send('chat_message', { text: currentMessage });
    setCurrentMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const addNewUser = () => {
    const newUser: User = {
      id: Date.now().toString(),
      username: 'New User',
      color: 'bg-gray-500',
      avatar: '👤'
    };
    setUsers(prev => [...prev, newUser]);
  };

  const removeUser = (userId: string) => {
    if (users.length <= 1) return; // Keep at least one user
    setUsers(prev => prev.filter(u => u.id !== userId));
    if (selectedUserId === userId) {
      setSelectedUserId(users[0].id);
    }
  };

  const startEditing = (userId: string, currentUsername: string) => {
    setIsEditing(userId);
    setEditUsername(currentUsername);
  };

  const saveUsername = (userId: string) => {
    if (!editUsername.trim()) return;
    setUsers(prev => prev.map(u =>
      u.id === userId ? { ...u, username: editUsername.trim() } : u
    ));
    setIsEditing(null);
    setEditUsername('');
  };

  const cancelEditing = () => {
    setIsEditing(null);
    setEditUsername('');
  };

  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour12: true,
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  const selectedUser = users.find(u => u.id === selectedUserId);

  // Auto-connect on mount
  useEffect(() => {
    connectToRoom();
  }, []);

  return (
    <div className="h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header with User Selection */}
      <div className="bg-white shadow-lg border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">💬</span>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-800">Guardian Chat</h1>
                  <p className="text-sm text-gray-500">Real-time messaging platform</p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* User Selector */}
              <div className="flex items-center space-x-3">
                <span className="text-sm font-medium text-gray-600">Sending as:</span>
                <select
                  value={selectedUserId}
                  onChange={(e) => setSelectedUserId(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                >
                  {users.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.avatar} {user.username}
                    </option>
                  ))}
                </select>
              </div>

              {/* User Management */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={addNewUser}
                  className="px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm"
                >
                  + Add User
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex max-w-6xl mx-auto w-full">
        {/* User Management Panel */}
        <div className="w-80 bg-white shadow-lg border-r">
          <div className="p-4 border-b bg-gray-50">
            <h3 className="font-semibold text-gray-800">Manage Users</h3>
            <p className="text-xs text-gray-500 mt-1">Edit usernames and manage participants</p>
          </div>

          <div className="p-4 space-y-3 max-h-96 overflow-y-auto">
            {users.map(user => (
              <div key={user.id} className={`p-3 rounded-lg border-2 transition-all ${
                selectedUserId === user.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-10 h-10 ${user.color} rounded-full flex items-center justify-center text-white text-lg`}>
                      {user.avatar}
                    </div>
                    <div className="flex-1">
                      {isEditing === user.id ? (
                        <div className="space-y-2">
                          <input
                            type="text"
                            value={editUsername}
                            onChange={(e) => setEditUsername(e.target.value)}
                            className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                            onKeyPress={(e) => e.key === 'Enter' && saveUsername(user.id)}
                            autoFocus
                          />
                          <div className="flex space-x-1">
                            <button
                              onClick={() => saveUsername(user.id)}
                              className="px-2 py-1 bg-green-500 text-white rounded text-xs hover:bg-green-600"
                            >
                              Save
                            </button>
                            <button
                              onClick={cancelEditing}
                              className="px-2 py-1 bg-gray-500 text-white rounded text-xs hover:bg-gray-600"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="font-medium text-gray-800">{user.username}</div>
                          <div className="text-xs text-gray-500">ID: {user.id}</div>
                        </>
                      )}
                    </div>
                  </div>

                  {isEditing !== user.id && (
                    <div className="flex space-x-1">
                      <button
                        onClick={() => startEditing(user.id, user.username)}
                        className="p-1 text-blue-500 hover:bg-blue-100 rounded"
                        title="Edit username"
                      >
                        ✏️
                      </button>
                      {users.length > 1 && (
                        <button
                          onClick={() => removeUser(user.id)}
                          className="p-1 text-red-500 hover:bg-red-100 rounded"
                          title="Remove user"
                        >
                          🗑️
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col bg-white">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4 mx-auto">
                    <span className="text-2xl">💬</span>
                  </div>
                  <p className="text-gray-500">No messages yet. Start a conversation!</p>
                </div>
              </div>
            ) : (
              messages.map((message) => {
                const messageUser = users.find(u => u.username === message.username);
                return (
                  <div key={message.id} className="flex space-x-3 animate-fadeIn">
                    <div className={`w-10 h-10 ${messageUser?.color || 'bg-gray-500'} rounded-full flex items-center justify-center text-white flex-shrink-0`}>
                      {messageUser?.avatar || '👤'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-semibold text-gray-900">{message.username}</span>
                        <span className="text-xs text-gray-500">{formatTime(message.timestamp)}</span>
                      </div>
                      <div className="bg-gray-50 rounded-2xl px-4 py-2 inline-block max-w-md">
                        <p className="text-gray-800">{message.text}</p>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="border-t bg-gray-50 p-4">
            <div className="flex items-center space-x-3">
              {selectedUser && (
                <div className={`w-10 h-10 ${selectedUser.color} rounded-full flex items-center justify-center text-white flex-shrink-0`}>
                  {selectedUser.avatar}
                </div>
              )}
              <div className="flex-1">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    placeholder={`Message as ${selectedUser?.username}...`}
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!currentMessage.trim() || !isConnected}
                    className="px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between mt-2 px-2">
              <span className="text-xs text-gray-500">
                {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
              </span>
              <span className="text-xs text-gray-500">
                {messages.length} messages
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};