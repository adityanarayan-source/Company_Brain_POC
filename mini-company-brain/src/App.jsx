import { useState } from 'react'
import { sendMessage } from './services/api'

const starterMessage = { role: 'assistant', content: 'Welcome to your Mini Company Brain. Try asking me to create content, analyze text, calculate something, or search company information.' }

function ActivityPanel({ activity }) {
  const memories = activity?.memories || []
  return <aside className="activity-panel">
    <div className="panel-heading"><div><span className="eyebrow">LIVE TRACE</span><h2>Agent activity</h2></div><span className={`status-dot ${activity?.status === 'error' ? 'error' : ''}`} /></div>
    <section className="activity-section"><p className="section-label">Memory retrieved</p>{memories.length ? memories.map((memory) => <div className="memory-item" key={memory}>{memory}</div>) : <p className="muted">No saved preferences yet.</p>}</section>
    <section className="activity-section two-column"><div><p className="section-label">Tool used</p><strong>{activity?.tool || 'None'}</strong></div><div><p className="section-label">Status</p><strong className={activity?.status === 'error' ? 'danger' : 'success'}>{activity?.status || 'Ready'}</strong></div></section>
    <section className="activity-section"><p className="section-label">Tool result</p><p className="result-box">{activity?.tool_result || 'Ask a question to see the agent work.'}</p></section>
    <div className="activity-note"><span>i</span> Memory persists when you start a new conversation.</div>
  </aside>
}

function App() {
  const [messages, setMessages] = useState([starterMessage])
  const [input, setInput] = useState('')
  const [activity, setActivity] = useState({ memories: [], status: 'ready' })
  const [loading, setLoading] = useState(false)

  async function handleSend(event) {
    event.preventDefault()
    const message = input.trim()
    if (!message || loading) return
    setInput('')
    setMessages((current) => [...current, { role: 'user', content: message }])
    setLoading(true)
    try {
      const result = await sendMessage(message)
      setMessages((current) => [...current, { role: 'assistant', content: result.response }])
      setActivity(result.activity)
    } catch (error) {
      setMessages((current) => [...current, { role: 'assistant', content: `I could not reach the brain API. ${error.message}` }])
      setActivity({ memories: [], status: 'error', tool_result: 'Backend unavailable' })
    } finally { setLoading(false) }
  }

  return <main className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-mark">✦</div><div><h1>Mini Company Brain</h1><p>Memory + Agents + Tools</p></div></div><div className="header-meta"><span className="online-dot" />Demo workspace <span className="avatar">DU</span></div></header>
    <div className="workspace">
      <section className="chat-card"><div className="chat-heading"><div><span className="eyebrow">CONVERSATION</span><h2>Company brain assistant</h2></div><button className="new-button" onClick={() => { setMessages([starterMessage]); setActivity({ memories: [], status: 'ready' }) }}>↻ New conversation</button></div>
        <div className="messages">{messages.map((message, index) => <div className={`message-row ${message.role}`} key={`${message.role}-${index}`}><div className="message-avatar">{message.role === 'user' ? 'DU' : '✦'}</div><div className="message-body"><span className="message-label">{message.role === 'user' ? 'You' : 'Brain assistant'}</span><div className="bubble">{message.content}</div></div></div>)}{loading && <div className="message-row assistant"><div className="message-avatar">✦</div><div className="message-body"><span className="message-label">Brain assistant</span><div className="bubble typing">Thinking<span>.</span><span>.</span><span>.</span></div></div></div>}</div>
        <form className="composer" onSubmit={handleSend}><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask your company brain anything..." aria-label="Message" /><button type="submit" disabled={loading || !input.trim()}>Send <span>↗</span></button></form><p className="composer-hint">Try: “From now on keep content short, professional and give me 3 options.”</p>
      </section><ActivityPanel activity={activity} />
    </div><footer><span>MINI COMPANY BRAIN POC</span><span>Persistent memory · Observable tools · Local demo</span></footer>
  </main>
}

export default App
