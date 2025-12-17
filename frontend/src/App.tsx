import { useState } from 'react'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'
import './App.css'

const AGENTS = [
  { id: 'sample_agent', name: 'アシスタント' },
  { id: 'joke_agent', name: 'ジョークエージェント' },
]

function App() {
  const [greeting, setGreeting] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0].id)

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
    <CopilotKit
      key={selectedAgent}
      runtimeUrl={import.meta.env.VITE_COPILOT_RUNTIME_URL}
      agent={selectedAgent}
      headers={{
        Authorization: `Bearer ${import.meta.env.VITE_ACCESS_TOKEN}`,
      }}
    >
      <CopilotSidebar>
        <h1>Greetings App</h1>
        <div className="card">
          <div className="agent-selector">
            <label htmlFor="agent-select">エージェント: </label>
            <select
              id="agent-select"
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
            >
              {AGENTS.map((agent) => (
                <option key={agent.id} value={agent.id}>
                  {agent.name}
                </option>
              ))}
            </select>
          </div>
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
