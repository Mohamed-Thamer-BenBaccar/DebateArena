import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'

const MODES = [
  {
    id: 'contradicteur',
    emoji: '🥊',
    name: 'Contradicteur',
    desc: "L'IA contredit chaque réponse et cherche tes failles.",
    color: '#6366F1'
  },
  {
    id: 'socrate',
    emoji: '🧑‍⚖️',
    name: 'Socrate',
    desc: "L'IA répond uniquement par des questions.",
    color: '#06B6D4'
  },
  {
    id: 'jury',
    emoji: '📊',
    name: 'Jury',
    desc: "L'IA note chaque réponse de 0 à 10.",
    color: '#F59E0B'
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
    <div style={{ padding: '2rem', maxWidth: 600, margin: '0 auto' }}>
      <h2>Choisis ton mode</h2>
      {courseInfo && (
        <p style={{ color: '#64748B' }}>Cours : {courseInfo.title}</p>
      )}

      {MODES.map((m) => (
        <div
          key={m.id}
          onClick={() => handleSelect(m.id)}
          style={{
            border: `2px solid ${m.color}`,
            borderRadius: 12,
            padding: '1.25rem',
            marginBottom: '1rem',
            cursor: 'pointer'
          }}
        >
          <h3 style={{ color: m.color, margin: 0 }}>
            {m.emoji} {m.name}
          </h3>
          <p style={{ color: '#64748B', margin: '0.25rem 0 0' }}>
            {m.desc}
          </p>
        </div>
      ))}
    </div>
  )
}