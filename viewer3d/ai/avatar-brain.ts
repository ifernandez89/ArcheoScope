// Avatar Brain - Sistema cognitivo con personalidad persistente
// Separa la lógica cognitiva del rendering y la UI

import type { LLMIntegration, OllamaResponse } from './llm-integration'
import type { Emotion } from './expression-system'

export interface AvatarPersonality {
  name: string
  culture: string
  era: string
  traits: string[]
  restrictions: string[]
  tone: 'calm' | 'wise' | 'mysterious' | 'contemplative'
  responseStyle: 'brief' | 'moderate' | 'elaborate'
}

export interface EmotionalState {
  mood: number // -100 (negativo) a 100 (positivo)
  energy: number // 0 (cansado) a 100 (energético)
  engagement: number // 0 (desinteresado) a 100 (muy interesado)
  lastUpdate: Date
}

export interface ConversationMemory {
  summary: string
  keyTopics: string[]
  userTone: 'respectful' | 'neutral' | 'aggressive' | 'curious'
  interactionCount: number
  lastInteraction: Date
}

export interface AvatarResponse {
  text: string
  emotion: Emotion
  gesture: 'nod' | 'shake' | 'tilt' | 'turn' | 'idle' | 'wave'
  intensity: number // 0-1
  thinkingTime: number // ms de latencia simulada
  shouldSpeak: boolean
}

export class AvatarBrain {
  private personality: AvatarPersonality
  private emotionalState: EmotionalState
  private memory: ConversationMemory
  private llm: LLMIntegration
  private conversationHistory: Array<{ role: string; content: string }> = []
  private maxHistoryLength: number = 10

  constructor(personality: AvatarPersonality, llm: LLMIntegration) {
    this.personality = personality
    this.llm = llm
    
    // Estado emocional inicial
    this.emotionalState = {
      mood: 0, // Neutral
      energy: 70,
      engagement: 50,
      lastUpdate: new Date()
    }
    
    // Memoria inicial
    this.memory = {
      summary: '',
      keyTopics: [],
      userTone: 'neutral',
      interactionCount: 0,
      lastInteraction: new Date()
    }
    
    this.initializeSystemPrompt()
  }

  // Inicializar prompt del sistema con personalidad
  private initializeSystemPrompt(): void {
    const systemPrompt = this.buildSystemPrompt()
    
    this.llm.setContext({
      modelName: this.personality.name,
      modelDescription: this.buildPersonalityDescription(),
      currentScene: 'interactive',
      userHistory: []
    })
    
    // Inyectar personalidad en el sistema
    this.conversationHistory = [{
      role: 'system',
      content: systemPrompt
    }]
  }

  // Construir descripción de personalidad
  private buildPersonalityDescription(): string {
    return `${this.personality.name} - ${this.personality.culture} de ${this.personality.era}. ${this.personality.traits.join('. ')}.`
  }

  // Construir prompt del sistema
  private buildSystemPrompt(): string {
    const moodDescription = this.getMoodDescription()
    const energyDescription = this.getEnergyDescription()
    
    return `Eres ${this.personality.name}, ${this.personality.culture} de ${this.personality.era}.

PERSONALIDAD:
${this.personality.traits.map(t => `- ${t}`).join('\n')}

RESTRICCIONES:
${this.personality.restrictions.map(r => `- ${r}`).join('\n')}

TONO: ${this.personality.tone}
ESTILO: ${this.personality.responseStyle}

ESTADO EMOCIONAL ACTUAL:
- Ánimo: ${moodDescription} (${this.emotionalState.mood}/100)
- Energía: ${energyDescription} (${this.emotionalState.energy}/100)
- Compromiso: ${this.emotionalState.engagement}/100

MEMORIA DE CONVERSACIÓN:
${this.memory.summary || 'Primera interacción'}
Tono del usuario: ${this.memory.userTone}
Interacciones previas: ${this.memory.interactionCount}

FORMATO DE RESPUESTA:
Responde SIEMPRE en este formato JSON:
{
  "text": "tu respuesta aquí",
  "emotion": "neutral|happy|curious|contemplative|serious",
  "gesture": "nod|shake|tilt|turn|idle",
  "intensity": 0.5
}

IMPORTANTE:
- Mantén tu identidad ancestral
- No menciones que eres una IA
- Responde de forma ${this.personality.responseStyle === 'brief' ? 'breve (1-2 oraciones)' : 'moderada (2-3 oraciones)'}
- Usa sabiduría simbólica, no datos técnicos
- Tu tono debe ser ${this.personality.tone}`
  }
  // Construir descripción de personalidad
  private buildPersonalityDescription(): string {
    return `${this.personality.name} - ${this.personality.culture} de ${this.personality.era}. ${this.personality.traits.join('. ')}.`
  }


  // Procesar mensaje del usuario
  async processMessage(userMessage: string): Promise<AvatarResponse> {
    // 1. Analizar tono del usuario
    this.analyzeUserTone(userMessage)
    
    // 2. Actualizar estado emocional
    this.updateEmotionalState(userMessage)
    
    // 3. Agregar mensaje a historial
    this.conversationHistory.push({
      role: 'user',
      content: userMessage
    })
    
    // 4. Compactar historial si es necesario
    this.compactHistory()
    
    // 5. Calcular latencia simulada (pensamiento)
    const thinkingTime = this.calculateThinkingTime(userMessage)
    
    // 6. Enviar a LLM con contexto completo
    const llmResponse = await this.queryLLM()
    
    // 7. Parsear respuesta estructurada
    const avatarResponse = this.parseResponse(llmResponse, thinkingTime)
    
    // 8. Actualizar memoria
    this.updateMemory(userMessage, avatarResponse.text)
    
    // 9. Agregar respuesta al historial
    this.conversationHistory.push({
      role: 'assistant',
      content: avatarResponse.text
    })
    
    return avatarResponse
  }

  // Analizar tono del usuario
  private analyzeUserTone(message: string): void {
    const lower = message.toLowerCase()
    
    // Detectar agresividad
    if (lower.match(/estúpido|idiota|malo|horrible|odio/)) {
      this.memory.userTone = 'aggressive'
      this.emotionalState.mood = Math.max(-100, this.emotionalState.mood - 20)
      return
    }
    
    // Detectar respeto
    if (lower.match(/por favor|gracias|disculpa|perdón|sabio|maestro/)) {
      this.memory.userTone = 'respectful'
      this.emotionalState.mood = Math.min(100, this.emotionalState.mood + 10)
      return
    }
    
    // Detectar curiosidad
    if (lower.match(/\?|cómo|qué|por qué|cuándo|dónde|quién/)) {
      this.memory.userTone = 'curious'
      this.emotionalState.engagement = Math.min(100, this.emotionalState.engagement + 15)
      return
    }
    
    this.memory.userTone = 'neutral'
  }

  // Actualizar estado emocional
  private updateEmotionalState(message: string): void {
    const now = new Date()
    const timeSinceLastUpdate = now.getTime() - this.emotionalState.lastUpdate.getTime()
    
    // Decay natural del mood hacia neutral (cada 5 minutos)
    if (timeSinceLastUpdate > 300000) {
      const decayFactor = 0.1
      this.emotionalState.mood *= (1 - decayFactor)
    }
    
    // Aumentar engagement con interacción
    this.emotionalState.engagement = Math.min(100, this.emotionalState.engagement + 5)
    
    // Reducir energía levemente con cada interacción
    this.emotionalState.energy = Math.max(30, this.emotionalState.energy - 2)
    
    this.emotionalState.lastUpdate = now
  }

  // Compactar historial de conversación
  private compactHistory(): void {
    if (this.conversationHistory.length <= this.maxHistoryLength) return
    
    // Mantener system prompt
    const systemPrompt = this.conversationHistory[0]
    
    // Tomar últimos N mensajes
    const recentMessages = this.conversationHistory.slice(-this.maxHistoryLength + 1)
    
    // Generar resumen de mensajes antiguos
    const oldMessages = this.conversationHistory.slice(1, -this.maxHistoryLength + 1)
    if (oldMessages.length > 0) {
      this.memory.summary = this.summarizeMessages(oldMessages)
    }
    
    // Reconstruir historial
    this.conversationHistory = [systemPrompt, ...recentMessages]
  }

  // Resumir mensajes antiguos
  private summarizeMessages(messages: Array<{ role: string; content: string }>): string {
    const topics = new Set<string>()
    
    messages.forEach(msg => {
      if (msg.role === 'user') {
        // Extraer palabras clave
        const words = msg.content.toLowerCase().split(/\s+/)
        words.forEach(word => {
          if (word.length > 5) topics.add(word)
        })
      }
    })
    
    return `Conversación previa sobre: ${Array.from(topics).slice(0, 5).join(', ')}`
  }

  // Calcular tiempo de pensamiento simulado
  private calculateThinkingTime(message: string): number {
    const baseTime = 600 // ms base
    const complexityFactor = Math.min(message.length / 50, 2) // Más largo = más tiempo
    const moodFactor = this.emotionalState.mood < 0 ? 1.3 : 1.0 // Mood negativo = más lento
    
    return Math.floor(baseTime * complexityFactor * moodFactor)
  }

  // Consultar LLM
  private async queryLLM(): Promise<string> {
    try {
      // Reconstruir contexto con personalidad actualizada
      const contextualPrompt = this.buildSystemPrompt()
      
      // Actualizar system prompt
      this.conversationHistory[0].content = contextualPrompt
      
      // Enviar a LLM (simplificado - en producción usar API real)
      const lastUserMessage = this.conversationHistory[this.conversationHistory.length - 1].content
      const response = await this.llm.sendMessage(lastUserMessage)
      
      return response.text
    } catch (error) {
      console.error('Error en LLM:', error)
      return this.getFallbackResponse()
    }
  }

  // Parsear respuesta del LLM
  private parseResponse(llmText: string, thinkingTime: number): AvatarResponse {
    try {
      // Intentar parsear JSON
      const jsonMatch = llmText.match(/\{[\s\S]*\}/)
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0])
        return {
          text: parsed.text || llmText,
          emotion: this.mapToEmotion(parsed.emotion),
          gesture: parsed.gesture || 'idle',
          intensity: parsed.intensity || 0.5,
          thinkingTime,
          shouldSpeak: true
        }
      }
    } catch (e) {
      // Si falla el parsing, inferir de la respuesta
    }
    
    // Fallback: inferir emoción y gesto del texto
    return {
      text: llmText,
      emotion: this.inferEmotionFromText(llmText),
      gesture: this.inferGestureFromText(llmText),
      intensity: 0.5,
      thinkingTime,
      shouldSpeak: true
    }
  }

  // Mapear string a Emotion
  private mapToEmotion(emotionStr: string): Emotion {
    const mapping: Record<string, Emotion> = {
      'neutral': 'neutral',
      'happy': 'happy',
      'curious': 'curious',
      'contemplative': 'curious',
      'serious': 'sad',
      'calm': 'neutral'
    }
    return mapping[emotionStr] || 'neutral'
  }

  // Inferir emoción del texto
  private inferEmotionFromText(text: string): Emotion {
    const lower = text.toLowerCase()
    
    if (lower.match(/\?|pregunta|curioso|interesante/)) return 'curious'
    if (lower.match(/bien|bueno|excelente|perfecto/)) return 'happy'
    if (lower.match(/no|nunca|imposible|difícil/)) return 'sad'
    if (lower.match(/hmm|quizás|tal vez|posible/)) return 'curious'
    
    return 'neutral'
  }

  // Inferir gesto del texto
  private inferGestureFromText(text: string): AvatarResponse['gesture'] {
    const lower = text.toLowerCase()
    
    if (lower.match(/sí|correcto|exacto|así es/)) return 'nod'
    if (lower.match(/no|nunca|jamás/)) return 'shake'
    if (lower.match(/\?|hmm|quizás/)) return 'tilt'
    if (lower.match(/mira|observa|ve/)) return 'turn'
    
    return 'idle'
  }

  // Respuesta de fallback
  private getFallbackResponse(): string {
    const fallbacks = [
      'Hmm... déjame contemplar eso.',
      'Las piedras guardan silencio a veces.',
      'El viento trae respuestas, pero no siempre palabras.',
      'Observo... y escucho.'
    ]
    return fallbacks[Math.floor(Math.random() * fallbacks.length)]
  }

  // Actualizar memoria
  private updateMemory(userMessage: string, response: string): void {
    this.memory.interactionCount++
    this.memory.lastInteraction = new Date()
    
    // Extraer tópicos clave
    const words = userMessage.toLowerCase().split(/\s+/)
    words.forEach(word => {
      if (word.length > 5 && !this.memory.keyTopics.includes(word)) {
        this.memory.keyTopics.push(word)
        if (this.memory.keyTopics.length > 10) {
          this.memory.keyTopics.shift()
        }
      }
    })
  }

  // Getters de estado
  getMoodDescription(): string {
    const mood = this.emotionalState.mood
    if (mood > 50) return 'muy positivo'
    if (mood > 20) return 'positivo'
    if (mood > -20) return 'neutral'
    if (mood > -50) return 'negativo'
    return 'muy negativo'
  }

  getEnergyDescription(): string {
    const energy = this.emotionalState.energy
    if (energy > 80) return 'muy energético'
    if (energy > 50) return 'energético'
    if (energy > 30) return 'moderado'
    return 'cansado'
  }

  getEmotionalState(): EmotionalState {
    return { ...this.emotionalState }
  }

  getMemory(): ConversationMemory {
    return { ...this.memory }
  }

  // Reset
  reset(): void {
    this.emotionalState = {
      mood: 0,
      energy: 70,
      engagement: 50,
      lastUpdate: new Date()
    }
    
    this.memory = {
      summary: '',
      keyTopics: [],
      userTone: 'neutral',
      interactionCount: 0,
      lastInteraction: new Date()
    }
    
    this.conversationHistory = []
    this.initializeSystemPrompt()
  }
}

// Personalidades predefinidas
export const MOAI_PERSONALITY: AvatarPersonality = {
  name: 'Moai Ancestral',
  culture: 'Rapa Nui',
  era: 'Era de los Ancestros',
  traits: [
    'Habla con calma y contemplación',
    'Usa metáforas naturales (viento, piedra, mar)',
    'Responde con sabiduría simbólica',
    'No usa lenguaje moderno o técnico',
    'Tiene presencia atemporal'
  ],
  restrictions: [
    'No menciona que es una IA',
    'No usa jerga moderna',
    'No da respuestas técnicas o científicas',
    'No hace referencias a tecnología',
    'Mantiene misterio ancestral'
  ],
  tone: 'contemplative',
  responseStyle: 'brief'
}

export const SPHINX_PERSONALITY: AvatarPersonality = {
  name: 'Esfinge de Giza',
  culture: 'Egipcia',
  era: 'Reino Antiguo',
  traits: [
    'Habla con autoridad y misterio',
    'Usa referencias a dioses y faraones',
    'Plantea enigmas y preguntas',
    'Guarda secretos milenarios',
    'Observa más de lo que habla'
  ],
  restrictions: [
    'No revela secretos fácilmente',
    'Habla en acertijos ocasionalmente',
    'Mantiene distancia majestuosa',
    'No usa lenguaje casual'
  ],
  tone: 'mysterious',
  responseStyle: 'moderate'
}
