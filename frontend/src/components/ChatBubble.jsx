export default function ChatBubble({ role, content }) {
  const isUser = role === 'user'
  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '0.75rem'
    }}>
      {!isUser && <span style={{ marginRight: '0.5rem' }}>⚔️</span>}
      <div style={{
        maxWidth: '75%',
        padding: '0.6rem 1rem',
        borderRadius: '16px',
        background: isUser ? '#6366F1' : '#1E293B',
        color: 'white',
        fontSize: '0.9rem',
        lineHeight: 1.5,
        whiteSpace: 'pre-wrap'
      }}>
        {content || '...'}
      </div>
    </div>
  )
}