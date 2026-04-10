export default function TypingIndicator() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
      <span>⚔️</span>
      <div style={{
        background: '#1E293B', padding: '0.6rem 1rem',
        borderRadius: '16px', display: 'flex', gap: '4px'
      }}>
        {[0,1,2].map(i => (
          <span key={i} style={{
            width: '8px', height: '8px',
            background: '#94A3B8', borderRadius: '50%',
            display: 'inline-block',
            animation: `bounce 1.2s ${i * 0.15}s infinite`
          }} />
        ))}
      </div>
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  )
}