// LLM Integration - Ollama Integration for AI Control
// Connects to local Ollama instance for conversational AI

export interface OllamaConfig {
  baseUrl: string
  model: string
  temperature?: number
  maxTokens?: number
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface OllamaResponse {
  text: string
  emotion?: string
  gesture?: string
  action?: string
}

export interface ConversationContext {
  modelName: string
  modelDescription: string
  currentScene: string
  userHistory: string[]
}

export class LLMIntegration {
  private config: OllamaConfig
  private conversationHistory: ChatMessage[] = []
  private context: ConversationContext | null = null

  constructor(config?: Partial<OllamaConfig>) {
    this.config = {
      baseUrl: 'http://localhost:11434',
      model: 'llama2',
      temperature: 0.7,
      maxTokens: 500,
      ...config
    }
  }

  // Verificar si Ollama está disponible
  async checkAvailability(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`)
      return response.ok
    } catch (error) {
      console.error('❌ Ollama no disponible:', error)
      return false
    }
  }

  // Listar modelos disponibles
  async listModels(): Promise<string[]> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`)
      const data = await response.json()
      return data.models?.map((m: any) => m.name) || []
    } catch (error) {
      console.error('❌ Error listando modelos:', error)
      return []
    }
  }

  // Establecer contexto de conversación
  setContext(context: ConversationContext): void {
    this.context = context
    
    // Agregar mensaje de sistema con contexto
    this.conversationHistory = [{
      role: 'system',
      content: `Eres un guía arqueológico virtual. Estás mostrando el modelo 3D: ${context.modelName}. 
Descripción: ${context.modelDescription}. 
Escena actual: ${context.currentScene}.
Responde de forma educativa, amigable y concisa. 
Puedes expresar emociones (happy, curious, excited, neutral) y gestos (wave, nod, turn).
Formato de respuesta: [EMOTION:emotion] [GESTURE:gesture] texto`
    }]
  }

  // Enviar mensaje y obtener respuesta
  async sendMessage(userMessage: string): Promise<OllamaResponse> {
    // Agregar mensaje del usuario
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    })

    try {
      const response = await fetch(`${this.config.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.config.model,
          messages: this.conversationHistory,
          stream: false,
          options: {
            temperature: this.config.temperature,
            num_predict: this.config.maxTokens
          }
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      const assistantMessage = data.message?.content || ''

      // Agregar respuesta al historial
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      })

      // Parsear respuesta
      return this.parseResponse(assistantMessage)

    } catch (error) {
      console.error('❌ Error en LLM:', error)
      return {
        text: 'Lo siento, no puedo responder en este momento.',
        emotion: 'neutral',
        gesture: undefined
      }
    }
  }

  // Parsear respuesta del LLM
  private parseResponse(text: string): OllamaResponse {
    let emotion: string | undefined
    let gesture: string | undefined
    let cleanText = text

    // Extraer emoción
    const emotionMatch = text.match(/\[EMOTION:(\w+)\]/)
    if (emotionMatch) {
      emotion = emotionMatch[1]
      cleanText = cleanText.replace(emotionMatch[0], '').trim()
    }

    // Extraer gesto
    const gestureMatch = text.match(/\[GESTURE:(\w+)\]/)
    if (gestureMatch) {
      gesture = gestureMatch[1]
      cleanText = cleanText.replace(gestureMatch[0], '').trim()
    }

    return {
      text: cleanText,
      emotion,
      gesture
    }
  }

  // Generar respuesta a pregunta sobre el modelo
  async askAboutModel(question: string): Promise<OllamaResponse> {
    if (!this.context) {
      return {
        text: 'No hay contexto establecido.',
        emotion: 'confused'
      }
    }

    const enhancedQuestion = `Pregunta sobre ${this.context.modelName}: ${question}`
    return this.sendMessage(enhancedQuestion)
  }

  // Generar descripción narrativa
  async generateNarration(topic: string): Promise<string> {
    const prompt = `Genera una narración breve (2-3 oraciones) sobre: ${topic}`
    const response = await this.sendMessage(prompt)
    return response.text
  }

  // Sugerir siguiente acción
  async suggestAction(): Promise<OllamaResponse> {
    const prompt = 'Sugiere algo interesante que el usuario podría explorar o preguntar sobre este modelo.'
    return this.sendMessage(prompt)
  }

  // Limpiar historial
  clearHistory(): void {
    const systemMessage = this.conversationHistory[0]
    this.conversationHistory = systemMessage ? [systemMessage] : []
  }

  // Obtener historial
  getHistory(): ChatMessage[] {
    return [...this.conversationHistory]
  }

  // Cambiar modelo
  setModel(modelName: string): void {
    this.config.model = modelName
  }

  // Obtener configuración
  getConfig(): OllamaConfig {
    return { ...this.config }
  }
}

// Conversation Manager - Gestor de conversaciones
export class ConversationManager {
  private llm: LLMIntegration
  private isActive: boolean = false
  private onResponse?: (response: OllamaResponse) => void

  constructor(llm: LLMIntegration) {
    this.llm = llm
  }

  // Iniciar conversación
  async start(context: ConversationContext): Promise<boolean> {
    // Verificar disponibilidad
    const available = await this.llm.checkAvailability()
    if (!available) {
      console.error('❌ Ollama no está disponible')
      return false
    }

    this.llm.setContext(context)
    this.isActive = true
    console.log('💬 Conversación iniciada')
    return true
  }

  // Detener conversación
  stop(): void {
    this.isActive = false
    this.llm.clearHistory()
    console.log('💬 Conversación detenida')
  }

  // Enviar mensaje
  async sendMessage(message: string): Promise<OllamaResponse | null> {
    if (!this.isActive) {
      console.warn('⚠️ Conversación no activa')
      return null
    }

    const response = await this.llm.sendMessage(message)
    
    if (this.onResponse) {
      this.onResponse(response)
    }

    return response
  }

  // Registrar callback de respuesta
  setOnResponse(callback: (response: OllamaResponse) => void): void {
    this.onResponse = callback
  }

  // Verificar si está activo
  isConversationActive(): boolean {
    return this.isActive
  }

  // Obtener LLM
  getLLM(): LLMIntegration {
    return this.llm
  }
}

// Quick Responses - Respuestas rápidas sin LLM
export class QuickResponses {
  private responses: Map<string, string[]> = new Map([
    ['greeting', [
      '¡Hola! Bienvenido al tour arqueológico.',
      '¡Saludos! ¿Qué te gustaría explorar?',
      '¡Hola! Estoy aquí para guiarte.'
    ]],
    ['thanks', [
      '¡De nada! ¿Algo más?',
      'Un placer ayudarte.',
      'Siempre a tu servicio.'
    ]],
    ['unknown', [
      'Interesante pregunta. Déjame pensar...',
      'No estoy seguro, pero puedo investigar.',
      'Esa es una buena pregunta.'
    ]],
    ['help', [
      'Puedes preguntarme sobre el modelo, su historia o características.',
      'Estoy aquí para responder tus preguntas sobre arqueología.',
      'Pregúntame lo que quieras sobre este sitio.'
    ]]
  ])

  // Obtener respuesta rápida
  getResponse(category: string): string {
    const options = this.responses.get(category) || this.responses.get('unknown')!
    return options[Math.floor(Math.random() * options.length)]
  }

  // Detectar categoría de mensaje
  detectCategory(message: string): string {
    const lower = message.toLowerCase()

    if (lower.match(/hola|hello|hi|saludos/)) return 'greeting'
    if (lower.match(/gracias|thanks|thank you/)) return 'thanks'
    if (lower.match(/ayuda|help|cómo/)) return 'help'

    return 'unknown'
  }

  // Responder automáticamente
  autoRespond(message: string): string {
    const category = this.detectCategory(message)
    return this.getResponse(category)
  }
}
