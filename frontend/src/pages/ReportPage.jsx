import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'

export default function ReportPage() {
  const { messages, score, mode, courseInfo, resetSession } = useSession()
  const navigate = useNavigate()

  const nbTours = messages.filter(m => m.role === 'user').length

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: '0 auto' }}>
      <h1>📊 Résultats du débat</h1>

      <div style={{
        background: '#f1f5f9',
        borderRadius: 12,
        padding: '1.5rem',
        marginTop: '1rem'
      }}>
        {courseInfo && (
          <p>📖 Cours : <b>{courseInfo.title}</b></p>
        )}
        <p>🎯 Mode : <b>{mode}</b></p>
        <p>💬 Réponses données : <b>{nbTours}</b></p>
        {score !== null && (
          <p>⭐ Dernier score Jury : <b>{score}/10</b></p>
        )}
      </div>

      <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
        <button
          onClick={() => navigate('/mode')}
          style={{ padding: '0.75rem 1.5rem' }}
        >
          🔀 Changer de mode
        </button>

        <button
          onClick={() => { resetSession(); navigate('/') }}
          style={{ padding: '0.75rem 1.5rem' }}
        >
          🔄 Nouveau cours
        </button>
      </div>
    </div>
  )
}