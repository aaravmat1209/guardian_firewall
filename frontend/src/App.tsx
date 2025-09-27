import './App.css'
import { ChatRoom } from './components/ChatRoom'
import { useState } from 'react'

function App() {
  const [currentView, setCurrentView] = useState('landing')

  if (currentView === 'chat') {
    return <ChatRoom />
  }

  return (
    <div className="landing">
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo">
            <span className="logo-icon">⬡</span>
            <span className="logo-text">Guardian</span>
          </div>
          <div className="nav-links">
            <button onClick={() => setCurrentView('chat')}>Live Chat Demo</button>
            <a href="#portal">Portal</a>
            <a href="#docs">Docs</a>
          </div>
        </div>
      </nav>

      <main className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Real-time grooming risk
            <span className="gradient-text"> firewall</span>
            <br />for game chats
          </h1>
          <p className="hero-subtitle">
            Guardian monitors live game chats, detects grooming risk at the conversation level,
            and intervenes with safety pauses, inline highlights, and guardian alert feeds.
          </p>
          <div className="hero-cta">
            <button className="btn-primary" onClick={() => setCurrentView('chat')}>
              View Live Demo
            </button>
            <button className="btn-secondary">Guardian Portal →</button>
          </div>
        </div>
        <div className="hero-visual">
          <div className="terminal">
            <div className="terminal-header">
              <div className="terminal-dots">
                <span></span><span></span><span></span>
              </div>
              <span className="terminal-title">guardian@firewall:~$</span>
            </div>
            <div className="terminal-body">
              <div className="terminal-line">
                <span className="prompt">$</span> guardian --monitor chat_session_abc123
              </div>
              <div className="terminal-line success">
                <span className="status">✓</span> Risk engine initialized
              </div>
              <div className="terminal-line warning">
                <span className="status">⚠</span> HIGH RISK detected: age probe + secrecy
              </div>
              <div className="terminal-line error">
                <span className="status">⏸</span> SAFETY PAUSE activated
              </div>
            </div>
          </div>
        </div>
      </main>

      <section className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">🔍</div>
          <h3>Multi-turn Detection</h3>
          <p>ML + precision rules track risk escalation across conversation history</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">⏸️</div>
          <h3>Safety Pause</h3>
          <p>Intercepts risky messages with suggested safe alternatives</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">📊</div>
          <h3>Guardian Portal</h3>
          <p>Real-time incident dashboard with one-click platform reporting</p>
        </div>
      </section>
    </div>
  )
}

export default App