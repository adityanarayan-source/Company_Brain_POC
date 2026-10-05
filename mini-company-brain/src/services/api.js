const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Keeping HTTP calls here makes the React components independent from the backend URL.
export async function sendMessage(message) {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'demo-user', message }),
    })
    if (!response.ok) throw new Error(`API returned ${response.status}`)
    return response.json()
  } catch (error) {
    // The UI remains useful for a quick frontend demo when FastAPI is not running.
    if (error instanceof TypeError) return demoReply(message)
    throw error
  }
}

function demoReply(message) {
  const lower = message.toLowerCase()
  const isPreference = /from now on|prefer|keep my|no emojis|always give/.test(lower)
  const isAnalyze = /analy[sz]e|character|word count/.test(lower)
  const text = message.replace(/^analy[sz]e\s+(this\s+)?/i, '')
  const result = isAnalyze ? `Content has ${text.length} characters and ${text.trim() ? text.trim().split(/\s+/).length : 0} words.` : isPreference ? 'Got it — I saved that as a preference for future conversations.' : 'Here are three concise options for your request:\n\n1. A clear, customer-focused announcement.\n2. A practical product benefit with a strong hook.\n3. A short invitation to learn more.'
  return { response: result, activity: { memories: isPreference ? ['Preference saved from this message'] : [], tool: isAnalyze ? 'content_analyzer' : null, tool_result: isAnalyze ? 'Content analyzed' : 'No tool needed', status: 'success' } }
}
