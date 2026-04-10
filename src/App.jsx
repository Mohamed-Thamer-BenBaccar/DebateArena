import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { SessionProvider } from './context/SessionContext'
import UploadPage  from './pages/UploadPage'
import ModePage    from './pages/ModePage'
import DebatePage  from './pages/DebatePage'
import ReportPage  from './pages/ReportPage'

export default function App() {
  return (
    <BrowserRouter>
      <SessionProvider>
        <Routes>
          <Route path='/'       element={<UploadPage />}  />
          <Route path='/mode'   element={<ModePage />}    />
          <Route path='/debate' element={<DebatePage />}  />
          <Route path='/report' element={<ReportPage />}  />
        </Routes>
      </SessionProvider>
    </BrowserRouter>
  )
}