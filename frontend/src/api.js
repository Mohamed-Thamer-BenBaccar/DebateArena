const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function uploadCourse(file, text) {
  const formData = new FormData()
  if (file) formData.append('file', file)
  if (text?.trim()) formData.append('text', text.trim())

  const response = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    body: formData
  })

  if (!response.ok) {
    let detail = 'Erreur upload'
    try {
      const errorData = await response.json()
      detail = errorData?.detail || detail
    } catch {
      // ignore json parsing error
    }
    throw new Error(detail)
  }

  return response.json()
}

export function streamChat(courseId, mode, message, history) {
  return fetch(`${BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      course_id: courseId,
      mode,
      message,
      history
    })
  })
}

export async function checkHealth() {
  const response = await fetch(`${BASE_URL}/health`)
  if (!response.ok) return false
  const data = await response.json()
  return data?.status === 'ok'
}