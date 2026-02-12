// OpenRouter Integration - API compatible con OpenAI
// Soporta modelos gratuitos y de pago de múltiples proveedores

export interface OpenRouterConfig {
  apiKey: string
  model?: string
  baseUrl?: string
  temperature?: number
  maxTokens?: number
}

export interface OpenRouterMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface OpenRouterResponse {
  text: string
  model: string
  usage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

export class OpenRouterIntegration {
  private config: OpenRouterConfig
  private conversationHistory: OpenRouterMessage[] = []

  constructor(config: OpenRouterConfig) {
    this.config = {
      baseUrl: 'https://openrouter.ai/api/v1',
      model: 'qwen/qwen-2.5-7b-instruct:free', // Modelo gratuito por defecto
      temperature: 0.7,
      maxTokens: 500,
      ...config
    }
  }

  // Enviar mensaje y obtener respuesta
  async sendMessage(userMessage: string): Promise<OpenRouterResponse> {
    try {
      // Agregar mensaje del usuario al historial
      this.conversationHistory.push({
        role: 'user',
        content: userMessage
      })

      // Preparar payload
      const payload = {
        model: this.config.model,
        messages: this.conversationHistory,
        temperature: this.config.temperature,
        max_tokens: this.config.maxTokens,
        stream: false
      }

      // Hacer request a OpenRouter
      const response = await fetch(`${this.config.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': window.location.origin,
          'X-Title': 'ArcheoScope 3D Viewer'
        },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`OpenRouter error: ${response.status} - ${errorText}`)
      }

      const data = await response.json()

      // Extraer respuesta
      const assistantMessage = data.choices[0].message.content
      const modelUsed = data.model || this.config.model

      // Agregar respuesta al historial
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      })

      return {
        text: assistantMessage,
        model: modelUsed,
        usage: data.usage
      }
    } catch (error) {
      console.error('Error en OpenRouter:', error)
      throw error
    }
  }

  // Verificar disponibilidad de la API
  async checkAvailability(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/models`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.config.apiKey}`
        }
      })

      return response.ok
    } catch (error) {
      console.error('Error verificando OpenRouter:', error)
      return false
    }
  }

  // Establecer contexto del sistema
  setContext(context: { modelName: string; modelDescription: string; currentScene: string; userHistory: any[] }): void {
    // Si ya hay un system message, reemplazarlo
    if (this.conversationHistory.length > 0 && this.conversationHistory[0].role === 'system') {
      this.conversationHistory[0].content = `${context.modelDescription}\n\nEscena actual: ${context.currentScene}`
    } else {
      // Agregar system message al inicio
      this.conversationHistory.unshift({
        role: 'system',
        content: `${context.modelDescription}\n\nEscena actual: ${context.currentScene}`
      })
    }
  }

  // Limpiar historial
  clearHistory(): void {
    this.conversationHistory = []
  }

  // Obtener historial
  getHistory(): OpenRouterMessage[] {
    return [...this.conversationHistory]
  }

  // Actualizar configuración
  updateConfig(config: Partial<OpenRouterConfig>): void {
    this.config = { ...this.config, ...config }
  }
}

// Modelos recomendados de OpenRouter
export const OPENROUTER_MODELS = {
  // Modelos GRATUITOS (excelentes para testing)
  QWEN_2_5_7B_FREE: 'qwen/qwen-2.5-7b-instruct:free',
  QWEN_3_CODER_FREE: 'qwen/qwen3-coder:free',
  LLAMA_3_1_8B_FREE: 'meta-llama/llama-3.1-8b-instruct:free',
  MISTRAL_7B_FREE: 'mistralai/mistral-7b-instruct:free',
  
  // Modelos de PAGO (mejor calidad)
  GPT_4O_MINI: 'openai/gpt-4o-mini', // $0.15/1M tokens - Excelente calidad/precio
  CLAUDE_3_5_HAIKU: 'anthropic/claude-3.5-haiku', // $0.80/1M tokens - Muy rápido
  GEMINI_2_FLASH: 'google/gemini-2.0-flash-exp:free', // GRATIS temporalmente
  QWEN_2_5_72B: 'qwen/qwen-2.5-72b-instruct', // $0.35/1M tokens - Muy potente
}

// Configuración recomendada para el Moai
export const MOAI_OPENROUTER_CONFIG: Partial<OpenRouterConfig> = {
  model: OPENROUTER_MODELS.QWEN_2_5_7B_FREE, // Gratis y bueno
  temperature: 0.7,
  maxTokens: 300 // Respuestas breves y contemplativas
}
