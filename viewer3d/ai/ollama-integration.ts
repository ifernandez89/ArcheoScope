// Ollama Integration - API local para modelos LLM
// Compatible con gemma2:2b y otros modelos de Ollama

export interface OllamaConfig {
  baseUrl?: string
  model?: string
  temperature?: number
  maxTokens?: number
}

export interface OllamaMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface OllamaResponse {
  text: string
  model: string
  usage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

export class OllamaIntegration {
  private config: OllamaConfig
  private conversationHistory: OllamaMessage[] = []

  constructor(config: OllamaConfig = {}) {
    this.config = {
      baseUrl: 'http://localhost:11434',
      model: 'gemma2:2b',
      temperature: 0.7,
      maxTokens: 500,
      ...config
    }
  }

  // Enviar mensaje y obtener respuesta
  async sendMessage(userMessage: string): Promise<OllamaResponse> {
    try {
      // Agregar mensaje del usuario al historial
      this.conversationHistory.push({
        role: 'user',
        content: userMessage
      })

      // Preparar payload para Ollama
      const payload = {
        model: this.config.model,
        messages: this.conversationHistory,
        stream: false,
        options: {
          temperature: this.config.temperature,
          num_predict: this.config.maxTokens
        }
      }

      // Hacer request a Ollama
      const response = await fetch(`${this.config.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Ollama error: ${response.status} - ${errorText}`)
      }

      const data = await response.json()

      // Extraer respuesta
      const assistantMessage = data.message.content
      const modelUsed = data.model || this.config.model

      // Agregar respuesta al historial
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      })

      return {
        text: assistantMessage,
        model: modelUsed,
        usage: {
          prompt_tokens: data.prompt_eval_count || 0,
          completion_tokens: data.eval_count || 0,
          total_tokens: (data.prompt_eval_count || 0) + (data.eval_count || 0)
        }
      }
    } catch (error) {
      console.error('Error en Ollama:', error)
      throw error
    }
  }

  // Verificar disponibilidad de Ollama
  async checkAvailability(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`, {
        method: 'GET'
      })

      if (!response.ok) return false

      const data = await response.json()
      
      // Verificar si el modelo está disponible
      const models = data.models || []
      const modelExists = models.some((m: any) => m.name === this.config.model)
      
      if (!modelExists) {
        console.warn(`⚠️ Modelo ${this.config.model} no encontrado en Ollama`)
        console.log('📋 Modelos disponibles:', models.map((m: any) => m.name))
      }

      return response.ok
    } catch (error) {
      console.error('Error verificando Ollama:', error)
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
  getHistory(): OllamaMessage[] {
    return [...this.conversationHistory]
  }

  // Actualizar configuración
  updateConfig(config: Partial<OllamaConfig>): void {
    this.config = { ...this.config, ...config }
  }
}

// Modelos recomendados de Ollama
export const OLLAMA_MODELS = {
  GEMMA2_2B: 'gemma2:2b',      // Rápido y ligero
  GEMMA2_9B: 'gemma2:9b',      // Más potente
  LLAMA3_8B: 'llama3:8b',      // Excelente calidad
  MISTRAL_7B: 'mistral:7b',    // Muy bueno
  PHI3_MINI: 'phi3:mini',      // Ultra rápido
  QWEN2_5_7B: 'qwen2.5:7b'     // Multilingüe
}

// Configuración recomendada para el Moai con Ollama
export const MOAI_OLLAMA_CONFIG: Partial<OllamaConfig> = {
  model: OLLAMA_MODELS.GEMMA2_2B,
  temperature: 0.7,
  maxTokens: 300
}
