import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'
import { streamChat } from '../api'
import ChatBubble from '../components/ChatBubble'
import ModeTag from '../components/ModeTag'
import ScoreBar from '../components/ScoreBar'
import TypingIndicator from '../components/TypingIndicator'

export default function DebatePage() {
  const { courseId, mode, messages, setMessages, score, setScore } = useSession()
  const navigate = useNavigate()

  const [input, setInput]     = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    if (!courseId || !mode) navigate('/')
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const extractScore = (text) => {
    const match = text.match(/\[NOTE:\s*(\d+)\/10\]/)
    return match ? parseInt(match[1]) : null
  }

  const handleSend = async () => {
    if (!input.trim() || sending) return

    const userMessage = input
    setInput('')
    setSending(true)

    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setMessages(prev => [...prev, { role: 'ai', content: '' }])

    try {
      const history = messages.map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content
      }))

      const response = await streamChat(courseId, mode, userMessage, history)
      if (!response.ok) throw new Error('Erreur backend')

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullReply = ''
      let buffer = ''
      let ended = false

      while (!ended) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const events = buffer.split('\n\n')
        buffer = events.pop() || ''

        for (const rawEvent of events) {
          const lines = rawEvent.split('\n')
          const eventLine = lines.find(line => line.startsWith('event:'))
          const dataLine = lines.find(line => line.startsWith('data:'))
          if (!eventLine || !dataLine) continue

          const eventType = eventLine.replace('event:', '').trim()
          const dataPayload = dataLine.replace('data:', '').trim()

          if (eventType === 'token') {
            try {
              const parsed = JSON.parse(dataPayload)
              const token = parsed?.token || ''
              fullReply += token
              setMessages(prev => [
                ...prev.slice(0, -1),
                { role: 'ai', content: prev.at(-1).content + token }
              ])
            } catch {
              // Ignore malformed token payload
            }
          }

          if (eventType === 'done') {
            ended = true
            break
          }

          if (eventType === 'error') {
            throw new Error('Erreur stream SSE')
          }
        }
      }

      const newScore = extractScore(fullReply)
      if (newScore !== null) setScore(newScore)

    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setMessages(prev => [
        ...prev.slice(0, -1),
        { role: 'ai', content: '[Erreur de connexion.]' }
      ])
    } finally {
      setSending(false)
    }
  }

  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      height: '100vh', background: '#0F172A', color: 'white'
    }}>

      {/* Header */}
      <div style={{
        padding: '0.75rem 1rem',
        borderBottom: '1px solid #1E293B',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <ModeTag mode={mode} />
        {mode === 'jury' && <ScoreBar score={score} />}
        <button
          onClick={() => navigate('/report')}
          style={{
            background: 'transparent',
            color: '#64748B',
            border: '1px solid #334155',
            padding: '0.25rem 0.75rem',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          Terminer
        </button>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem' }}>
        {messages.length === 0 && (
          <p style={{ color: '#475569', textAlign: 'center', marginTop: '2rem' }}>
            Écris ta première réponse pour commencer...
          </p>
        )}
        {messages.map((msg, i) => (
          <ChatBubble key={i} role={msg.role} content={msg.content} />
        ))}
        {sending && messages.at(-1)?.content === '' && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: '1rem',
        borderTop: '1px solid #1E293B',
        display: 'flex', gap: '0.5rem'
      }}>
        <input
          style={{
            flex: 1, padding: '0.6rem 1rem',
            background: '#1E293B', border: 'none',
            borderRadius: '12px', color: 'white',
            fontSize: '0.9rem', outline: 'none'
          }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder='Ta réponse...'
          disabled={sending}
        />
        <button
          onClick={handleSend}
          disabled={sending}
          style={{
            background: '#6366F1', color: 'white',
            border: 'none', borderRadius: '12px',
            padding: '0.6rem 1.5rem', cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          {sending ? '...' : 'Envoyer'}
        </button>
      </div>
    </div>
  )
}