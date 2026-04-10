import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'
import { streamChat } from '../api'

export default function DebatePage() {
  const { courseId, mode, messages, setMessages, score, setScore } = useSession()
  const navigate = useNavigate()

  const [input, setInput]     = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)

  // Rediriger si pas de cours chargé
  useEffect(() => {
    if (!courseId || !mode) navigate('/')
  }, [])

  // Scroll automatique vers le bas
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Extraire le score du texte Jury [NOTE: X/10]
  const extractScore = (text) => {
    const match = text.match(/\[NOTE:\s*(\d+)\/10\]/)
    return match ? parseInt(match[1]) : null
  }

  const handleSend = async () => {
    if (!input.trim() || sending) return

    const userMessage = input
    setInput('')
    setSending(true)

    const userMsg = { role: 'user', content: userMessage }
    setMessages(prev => [...prev, userMsg])

    // Ajouter bulle IA vide qui va se remplir
    setMessages(prev => [...prev, { role: 'ai', content: '' }])

    try {
      const history = messages.map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content
      }))

      const response = await streamChat(courseId, mode, userMessage, history)

      if (!response.ok) throw new Error('Erreur backend')

      // Lire le stream token par token
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullReply = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const token = decoder.decode(value)
        fullReply += token

        setMessages(prev => [
          ...prev.slice(0, -1),
          { role: 'ai', content: prev.at(-1).content + token }
        ])
      }

      // Extraire score si mode Jury
      const newScore = extractScore(fullReply)
      if (newScore !== null) setScore(newScore)

    } catch (err) {
      setMessages(prev => [
        ...prev.slice(0, -1),
        { role: 'ai', content: '[Erreur de connexion. Vérifie que le backend tourne.]' }
      ])
    } finally {
      setSending(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>

      {/* Header */}
      <div style={{
        padding: '1rem',
        borderBottom: '1px solid #e2e8f0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <span>Mode : <b>{mode}</b></span>
        {mode === 'jury' && score !== null && (
          <span>Score : <b>{score}/10</b></span>
        )}
        <button onClick={() => navigate('/report')}>Terminer</button>
      </div>

      {/* Zone messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem' }}>
        {messages.length === 0 && (
          <p style={{ color: '#94a3b8', textAlign: 'center' }}>
            Écris ta première réponse pour commencer le débat...
          </p>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
            marginBottom: '0.75rem'
          }}>
            <span style={{
              maxWidth: '75%',
              padding: '0.6rem 1rem',
              borderRadius: 16,
              background: msg.role === 'user' ? '#6366F1' : '#334155',
              color: 'white',
              fontSize: '0.9rem',
              lineHeight: 1.5,
              whiteSpace: 'pre-wrap'
            }}>
              {msg.content || '...'}
            </span>
          </div>
        ))}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: '1rem',
        borderTop: '1px solid #e2e8f0',
        display: 'flex',
        gap: '0.5rem'
      }}>
        <input
          style={{ flex: 1, padding: '0.6rem', fontSize: '0.9rem' }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder='Ta réponse...'
          disabled={sending}
        />
        <button
          onClick={handleSend}
          disabled={sending}
          style={{ padding: '0.6rem 1.5rem' }}
        >
          {sending ? '...' : 'Envoyer'}
        </button>
      </div>

    </div>
  )
}