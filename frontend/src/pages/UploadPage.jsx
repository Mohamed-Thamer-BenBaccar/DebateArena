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
    <div style={{
      minHeight: '100vh',
      background: '#0F172A',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '520px',
        background: '#1E293B',
        borderRadius: '16px',
        padding: '2rem',
        boxShadow: '0 25px 50px rgba(0,0,0,0.5)'
      }}>
        {/* Logo */}
        <h1 style={{ color: 'white', fontSize: '1.8rem', margin: '0 0 0.25rem' }}>
          ⚔️ DebateArena
        </h1>
        <p style={{ color: '#64748B', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          Upload ton cours et débats avec l'IA
        </p>

        {/* Zone fichier */}
        <label style={{
          display: 'block',
          border: '2px dashed #334155',
          borderRadius: '12px',
          padding: '1.5rem',
          textAlign: 'center',
          cursor: 'pointer',
          marginBottom: '1rem',
          transition: 'border-color 0.2s'
        }}>
          <span style={{ fontSize: '2rem' }}>📁</span>
          <p style={{ color: '#94A3B8', margin: '0.5rem 0 0', fontSize: '0.85rem' }}>
            {file ? file.name : 'Cliquer pour choisir un PDF, DOCX ou TXT'}
          </p>
          <input
            type='file'
            accept='.pdf,.docx,.txt'
            style={{ display: 'none' }}
            onChange={(e) => { setFile(e.target.files[0]); setText('') }}
          />
        </label>

        {/* Séparateur */}
        <div style={{
          display: 'flex', alignItems: 'center',
          gap: '0.75rem', margin: '1rem 0'
        }}>
          <div style={{ flex: 1, height: '1px', background: '#334155' }} />
          <span style={{ color: '#475569', fontSize: '0.8rem' }}>ou</span>
          <div style={{ flex: 1, height: '1px', background: '#334155' }} />
        </div>

        {/* Textarea */}
        <textarea
          rows={5}
          style={{
            width: '100%',
            background: '#0F172A',
            border: '1px solid #334155',
            borderRadius: '12px',
            padding: '0.75rem',
            color: 'white',
            fontSize: '0.85rem',
            resize: 'vertical',
            outline: 'none',
            boxSizing: 'border-box'
          }}
          placeholder='Colle le texte du cours ici...'
          value={text}
          onChange={(e) => { setText(e.target.value); setFile(null) }}
        />

        {/* Erreur */}
        {error && (
          <p style={{ color: '#EF4444', fontSize: '0.85rem', margin: '0.5rem 0' }}>
            {error}
          </p>
        )}

        {/* Bouton */}
        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            width: '100%',
            marginTop: '1rem',
            padding: '0.85rem',
            background: loading ? '#4338CA' : '#6366F1',
            color: 'white',
            border: 'none',
            borderRadius: '12px',
            fontSize: '1rem',
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? '⏳ Analyse en cours...' : 'Commencer le débat →'}
        </button>
      </div>
    </div>
  )
}