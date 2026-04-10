import { createContext, useContext, useState } from 'react'

const SessionContext = createContext(null)

export function SessionProvider({ children }) {
  const [courseId, setCourseId]     = useState(null)
  const [mode, setMode]             = useState(null)
  const [messages, setMessages]     = useState([])
  const [score, setScore]           = useState(null)
  const [courseInfo, setCourseInfo] = useState(null)

  const resetSession = () => {
    setCourseId(null)
    setMode(null)
    setMessages([])
    setScore(null)
    setCourseInfo(null)
  }

  return (
    <SessionContext.Provider value={{
      courseId, setCourseId,
      mode, setMode,
      messages, setMessages,
      score, setScore,
      courseInfo, setCourseInfo,
      resetSession
    }}>
      {children}
    </SessionContext.Provider>
  )
}

export function useSession() {
  const context = useContext(SessionContext)
  if (!context) throw new Error('useSession doit être dans un SessionProvider')
  return context
}