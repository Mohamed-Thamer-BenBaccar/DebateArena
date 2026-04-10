import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSession } from '../context/SessionContext'
import { uploadCourse } from '../api'

export default function UploadPage() {
  const [file, setFile]       = useState(null)
  const [text, setText]       = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const { setCourseId, setCourseInfo } = useSession()
  const navigate = useNavigate()

  const handleUpload = async () => {
    if (!file && !text.trim()) {
      setError('Colle du texte ou choisis un fichier.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const data = await uploadCourse(file, text)
      setCourseId(data.course_id)
      setCourseInfo({ title: data.title || 'Cours' })
      navigate('/mode')
    } catch (err) {
      setError(err.message || 'Erreur. Réessayer.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: '0 auto' }}>
      <h1>⚔️ DebateArena</h1>
      <h2>Upload ton cours</h2>

      <input
        type='file'
        accept='.pdf,.docx,.txt'
        onChange={(e) => { setFile(e.target.files[0]); setText('') }}
      />

      <p style={{ textAlign: 'center', margin: '1rem 0', color: '#64748B' }}>— ou —</p>

      <textarea
        rows={6}
        style={{ width: '100%' }}
        placeholder='Colle le texte du cours ici...'
        value={text}
        onChange={(e) => { setText(e.target.value); setFile(null) }}
      />

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button
        onClick={handleUpload}
        disabled={loading}
        style={{ marginTop: '1rem', padding: '0.75rem 2rem' }}
      >
        {loading ? '⏳ Chargement...' : 'Commencer le débat →'}
      </button>
    </div>
  )
}