export default function ScoreBar({ score }) {
  if (score === null || score === undefined) return null
  const pct = (score / 10) * 100
  const color = score >= 8 ? '#10B981' : score >= 5 ? '#F59E0B' : '#EF4444'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <span style={{ fontSize: '0.8rem', color: '#94A3B8' }}>Score</span>
      <div style={{
        width: '120px', height: '8px',
        background: '#334155', borderRadius: '999px', overflow: 'hidden'
      }}>
        <div style={{
          width: `${pct}%`, height: '100%',
          background: color, borderRadius: '999px',
          transition: 'width 0.5s ease'
        }} />
      </div>
      <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color }}>{score}/10</span>
    </div>
  )
}