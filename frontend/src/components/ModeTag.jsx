const CONFIG = {
  contradicteur: { color: '#6366F1', emoji: '🥊', label: 'Contradicteur' },
  socrate:       { color: '#06B6D4', emoji: '🧑‍⚖️', label: 'Socrate' },
  jury:          { color: '#F59E0B', emoji: '📊', label: 'Jury' },
}

export default function ModeTag({ mode }) {
  const { color, emoji, label } = CONFIG[mode] || CONFIG.contradicteur
  return (
    <span style={{
      background: color,
      color: 'white',
      padding: '0.25rem 0.75rem',
      borderRadius: '999px',
      fontSize: '0.8rem',
      fontWeight: 'bold'
    }}>
      {emoji} {label}
    </span>
  )
}