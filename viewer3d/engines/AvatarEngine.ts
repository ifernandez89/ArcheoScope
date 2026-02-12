/**
 * AvatarEngine - Motor de avatar inteligente
 * Responsable de: IA, Emoción, Animación, Memoria
 */

export type Emotion = 'neutral' | 'happy' | 'thinking' | 'explaining' | 'surprised'
export type Gesture = 'idle' | 'point_left' | 'point_right' | 'wave' | 'nod' | 'shake_head'

export interface AvatarState {
  emotion: Emotion
  gesture: Gesture
  isSpeaking: boolean
  lookAtTarget: { x: number, y: number, z: number } | null
}

export interface ConversationContext {
  siteName?: string
  culture?: string
  period?: string
  location?: { lat: number, lon: number }
  userHistory: string[]
}

export class AvatarEngine {
  private static instance: AvatarEngine
  private state: AvatarState
  private context: ConversationContext
  
  private constructor() {
    this.state = {
      emotion: 'neutral',
      gesture: 'idle',
      isSpeaking: false,
      lookAtTarget: null
    }
    
    this.context = {
      userHistory: []
    }
  }
  
  static getInstance(): AvatarEngine {
    if (!AvatarEngine.instance) {
      AvatarEngine.instance = new AvatarEngine()
    }
    return AvatarEngine.instance
  }
  
  /**
   * Actualizar estado del avatar
   */
  setState(newState: Partial<AvatarState>): void {
    this.state = { ...this.state, ...newState }
    console.log('🤖 AvatarEngine: Estado actualizado:', this.state)
  }
  
  /**
   * Obtener estado actual
   */
  getState(): AvatarState {
    return { ...this.state }
  }
  
  /**
   * Establecer contexto de conversación
   */
  setContext(context: Partial<ConversationContext>): void {
    this.context = { ...this.context, ...context }
    console.log('💭 AvatarEngine: Contexto actualizado')
  }
  
  /**
   * Obtener contexto
   */
  getContext(): ConversationContext {
    return { ...this.context }
  }
  
  /**
   * Agregar mensaje al historial
   */
  addToHistory(message: string): void {
    this.context.userHistory.push(message)
    
    // Mantener solo últimos 10 mensajes
    if (this.context.userHistory.length > 10) {
      this.context.userHistory.shift()
    }
  }
  
  /**
   * Determinar emoción basada en respuesta IA
   */
  determineEmotion(text: string): Emotion {
    const lowerText = text.toLowerCase()
    
    if (lowerText.includes('interesante') || lowerText.includes('fascinante')) {
      return 'surprised'
    }
    if (lowerText.includes('construido') || lowerText.includes('ubicado')) {
      return 'explaining'
    }
    if (lowerText.includes('?') || lowerText.includes('quizás')) {
      return 'thinking'
    }
    if (lowerText.includes('!') || lowerText.includes('increíble')) {
      return 'happy'
    }
    
    return 'neutral'
  }
  
  /**
   * Determinar gesto basado en respuesta IA
   */
  determineGesture(text: string): Gesture {
    const lowerText = text.toLowerCase()
    
    if (lowerText.includes('izquierda') || lowerText.includes('oeste')) {
      return 'point_left'
    }
    if (lowerText.includes('derecha') || lowerText.includes('este')) {
      return 'point_right'
    }
    if (lowerText.includes('hola') || lowerText.includes('bienvenido')) {
      return 'wave'
    }
    if (lowerText.includes('sí') || lowerText.includes('correcto')) {
      return 'nod'
    }
    if (lowerText.includes('no') || lowerText.includes('incorrecto')) {
      return 'shake_head'
    }
    
    return 'idle'
  }
  
  /**
   * Procesar respuesta de IA y actualizar estado
   */
  processAIResponse(text: string): void {
    const emotion = this.determineEmotion(text)
    const gesture = this.determineGesture(text)
    
    this.setState({
      emotion,
      gesture,
      isSpeaking: true
    })
    
    // Volver a idle después de hablar
    setTimeout(() => {
      this.setState({
        gesture: 'idle',
        isSpeaking: false
      })
    }, 3000)
  }
  
  /**
   * Generar prompt contextual para IA
   */
  generateContextualPrompt(userMessage: string): string {
    const { siteName, culture, period, location } = this.context
    
    let prompt = `Eres un guía arqueológico experto y amigable. `
    
    if (siteName) {
      prompt += `Estamos en ${siteName}, un sitio de la cultura ${culture} del período ${period}. `
    }
    
    if (location) {
      prompt += `Ubicado en las coordenadas ${location.lat.toFixed(4)}°, ${location.lon.toFixed(4)}°. `
    }
    
    prompt += `\n\nUsuario pregunta: ${userMessage}\n\nResponde de forma breve, educativa y entusiasta.`
    
    return prompt
  }
  
  /**
   * Limpiar estado
   */
  reset(): void {
    this.state = {
      emotion: 'neutral',
      gesture: 'idle',
      isSpeaking: false,
      lookAtTarget: null
    }
    
    this.context = {
      userHistory: []
    }
    
    console.log('🔄 AvatarEngine: Estado reiniciado')
  }
}

export default AvatarEngine.getInstance()
