import { useState } from 'react'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'
import './App.css'

function App() {
  const [greeting, setGreeting] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchGreeting = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/greetings`)
      const data = await response.json()
      setGreeting(data.message)
    } catch (error) {
      setGreeting('エラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  return (
    <CopilotKit runtimeUrl={import.meta.env.VITE_COPILOT_RUNTIME_URL} agent="sample_agent">
      <CopilotSidebar>
        <h1>Greetings App</h1>
        <div className="card">
          <button onClick={fetchGreeting} disabled={loading}>
            {loading ? '読み込み中...' : '挨拶を取得'}
          </button>
          <p className="greeting">{greeting}</p>
        </div>
      </CopilotSidebar>
    </CopilotKit>
  )
}

export default App
