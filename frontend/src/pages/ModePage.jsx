import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'

const MODES = [
  {
    id: 'contradicteur',
    emoji: '🥊',
    name: 'Contradicteur',
    desc: "L'IA contredit chaque réponse et cherche tes failles logiques.",
    color: '#6366F1',
    bg: '#1E1B4B'
  },
  {
    id: 'socrate',
    emoji: '🧑‍⚖️',
    name: 'Socrate',
    desc: "L'IA répond uniquement par des questions pour te guider.",
    color: '#06B6D4',
    bg: '#0C2233'
  },
  {
    id: 'jury',
    emoji: '📊',
    name: 'Jury',
    desc: "L'IA note chaque réponse de 0 à 10 avec justification.",
    color: '#F59E0B',
    bg: '#1C1506'
  }
]

export default function ModePage() {
  const { setMode, courseInfo } = useSession()
  const navigate = useNavigate()

  const handleSelect = (modeId) => {
    setMode(modeId)
    navigate('/debate')
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0F172A',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }}>
      <div style={{ width: '100%', maxWidth: '520px' }}>

        <h2 style={{ color: 'white', fontSize: '1.5rem', marginBottom: '0.25rem' }}>
          Choisis ton mode
        </h2>
        {courseInfo && (
          <p style={{ color: '#64748B', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            📖 {courseInfo.title}
          </p>
        )}

        {MODES.map((m) => (
          <div
            key={m.id}
            onClick={() => handleSelect(m.id)}
            style={{
              background: '#1E293B',
              border: `2px solid #334155`,
              borderRadius: '14px',
              padding: '1.25rem',
              marginBottom: '0.75rem',
              cursor: 'pointer',
              transition: 'border-color 0.2s, transform 0.1s'
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = m.color
              e.currentTarget.style.transform = 'scale(1.02)'
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = '#334155'
              e.currentTarget.style.transform = 'scale(1)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <span style={{
                fontSize: '1.5rem',
                background: m.bg,
                padding: '0.4rem',
                borderRadius: '8px'
              }}>
                {m.emoji}
              </span>
              <div>
                <h3 style={{ color: m.color, margin: 0, fontSize: '1rem' }}>
                  {m.name}
                </h3>
                <p style={{ color: '#94A3B8', margin: '0.2rem 0 0', fontSize: '0.82rem' }}>
                  {m.desc}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}