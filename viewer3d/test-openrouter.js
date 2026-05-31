// Script de prueba rápida para OpenRouter
// Uso: node test-openrouter.js

const API_KEY = process.env.OPENROUTER_API_KEY || 'sk-or-v1-tu-api-key-aqui'
const MODEL = 'qwen/qwen-2.5-7b-instruct:free'

async function testOpenRouter() {
  console.log('🧪 Probando OpenRouter...')
  console.log(`📦 Modelo: ${MODEL}`)
  console.log(`🔑 API Key: ${API_KEY.substring(0, 20)}...`)
  console.log('')

  const startTime = Date.now()

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://archeoscope.app',
        'X-Title': 'ArcheoScope Test'
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          {
            role: 'system',
            content: 'Eres un Moai ancestral de Rapa Nui. Hablas con calma y sabiduría.'
          },
          {
            role: 'user',
            content: '¿Quién eres?'
          }
        ],
        temperature: 0.7,
        max_tokens: 150
      })
    })

    const endTime = Date.now()
    const responseTime = endTime - startTime

    if (!response.ok) {
      const errorText = await response.text()
      console.error('❌ Error:', response.status, errorText)
      return
    }

    const data = await response.json()
    const message = data.choices[0].message.content
    const usage = data.usage

    console.log('✅ Respuesta recibida!')
    console.log(`⏱️  Tiempo: ${responseTime}ms`)
    console.log('')
    console.log('💬 Respuesta del Moai:')
    console.log('─'.repeat(60))
    console.log(message)
    console.log('─'.repeat(60))
    console.log('')
    console.log('📊 Uso de tokens:')
    console.log(`   Prompt: ${usage.prompt_tokens}`)
    console.log(`   Completion: ${usage.completion_tokens}`)
    console.log(`   Total: ${usage.total_tokens}`)
    console.log('')
    console.log('🎉 OpenRouter funciona correctamente!')

  } catch (error) {
    console.error('❌ Error:', error.message)
  }
}

testOpenRouter()
