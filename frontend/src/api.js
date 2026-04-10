const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ⚠️ MOCK — à remplacer quand M1 lance son backend
export async function uploadCourse(file, text) {
  // Simuler un délai réseau
  await new Promise(r => setTimeout(r, 800))
  // Retourner un faux course_id
  return { course_id: 'mock-001', title: file?.name || 'Cours collé' }
}

export function streamChat(courseId, mode, message, history) {
  // Simuler des réponses selon le mode
  const replies = {
    contradicteur: 'Êtes-vous vraiment sûr de cela ? En quoi cette affirmation tient-elle face au principe d\'inertie ?',
    socrate: 'Pourquoi pensez-vous que cette loi s\'applique dans tous les cas ?',
    jury: '[NOTE: 7/10] Bonne réponse mais incomplète. Question suivante : définissez la notion d\'inertie.'
  }
  const reply = replies[mode] || 'Réponse mock.'

  // Simuler un stream en retournant un ReadableStream
  const stream = new ReadableStream({
    start(controller) {
      const words = reply.split(' ')
      let i = 0
      const interval = setInterval(() => {
        if (i < words.length) {
          controller.enqueue(new TextEncoder().encode(words[i] + ' '))
          i++
        } else {
          clearInterval(interval)
          controller.close()
        }
      }, 80)
    }
  })

  return Promise.resolve({ ok: true, body: stream })
}

export async function checkHealth() {
  return true
}