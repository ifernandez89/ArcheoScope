// Sistema de voz mejorado con soporte para múltiples engines
// Soporta: Web Speech API (gratis) y ElevenLabs (premium)

export type VoiceEngine = 'browser' | 'elevenlabs'

export interface VoiceConfig {
  engine: VoiceEngine
  elevenLabsApiKey?: string
  elevenLabsVoiceId?: string
  rate?: number
  pitch?: number
  volume?: number
}

export class VoiceSystem {
  private config: VoiceConfig
  private speechSynthesis: SpeechSynthesis | null = null
  private currentUtterance: SpeechSynthesisUtterance | null = null

  constructor(config: VoiceConfig) {
    this.config = {
      rate: 0.9,
      pitch: 0.85,
      volume: 1.0,
      ...config
    }

    if (typeof window !== 'undefined') {
      this.speechSynthesis = window.speechSynthesis
    }
  }

  // Hablar usando el engine configurado
  async speak(text: string, onStart?: () => void, onEnd?: () => void): Promise<void> {
    if (this.config.engine === 'elevenlabs' && this.config.elevenLabsApiKey) {
      return this.speakWithElevenLabs(text, onStart, onEnd)
    } else {
      return this.speakWithBrowser(text, onStart, onEnd)
    }
  }

  // Hablar con Web Speech API (mejorado)
  private async speakWithBrowser(text: string, onStart?: () => void, onEnd?: () => void): Promise<void> {
    if (!this.speechSynthesis) {
      console.warn('Speech Synthesis no disponible')
      return
    }

    // Cancelar speech anterior
    this.speechSynthesis.cancel()

    // Preprocesar texto
    const processedText = this.preprocessText(text)

    const utterance = new SpeechSynthesisUtterance(processedText)
    
    // Seleccionar mejor voz
    const voices = this.speechSynthesis.getVoices()
    const bestVoice = this.selectBestVoice(voices)
    
    if (bestVoice) {
      utterance.voice = bestVoice
      console.log(`🎙️ Voz: ${bestVoice.name} (${bestVoice.lang})`)
    }
    
    // Configurar parámetros
    utterance.rate = this.config.rate || 0.9
    utterance.pitch = this.config.pitch || 0.85
    utterance.volume = this.config.volume || 1.0

    utterance.onstart = () => onStart?.()
    utterance.onend = () => onEnd?.()
    utterance.onerror = (e) => {
      console.error('Error en speech:', e)
      onEnd?.()
    }

    this.currentUtterance = utterance
    this.speechSynthesis.speak(utterance)
  }

  // Hablar con ElevenLabs (voz premium de IA)
  private async speakWithElevenLabs(text: string, onStart?: () => void, onEnd?: () => void): Promise<void> {
    if (!this.config.elevenLabsApiKey) {
      console.warn('ElevenLabs API key no configurada')
      return this.speakWithBrowser(text, onStart, onEnd)
    }

    onStart?.()

    try {
      const voiceId = this.config.elevenLabsVoiceId || 'pNInz6obpgDQGcFmaJgB' // Adam (voz masculina grave)
      
      const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
        method: 'POST',
        headers: {
          'Accept': 'audio/mpeg',
          'Content-Type': 'application/json',
          'xi-api-key': this.config.elevenLabsApiKey
        },
        body: JSON.stringify({
          text: text,
          model_id: 'eleven_multilingual_v2',
          voice_settings: {
            stability: 0.7,
            similarity_boost: 0.8,
            style: 0.5,
            use_speaker_boost: true
          }
        })
      })

      if (!response.ok) {
        throw new Error(`ElevenLabs error: ${response.status}`)
      }

      const audioBlob = await response.blob()
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio(audioUrl)

      audio.onended = () => {
        URL.revokeObjectURL(audioUrl)
        onEnd?.()
      }

      audio.onerror = () => {
        URL.revokeObjectURL(audioUrl)
        onEnd?.()
      }

      await audio.play()
    } catch (error) {
      console.error('Error con ElevenLabs, usando voz del navegador:', error)
      return this.speakWithBrowser(text, onStart, onEnd)
    }
  }

  // Seleccionar la mejor voz disponible
  private selectBestVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
    const voicePriority = [
      // Voces premium de Google
      'Google español',
      'Google español de Estados Unidos',
      'Google español de España',
      'Google español de México',
      // Voces de Microsoft (buena calidad)
      'Microsoft Helena - Spanish (Spain)',
      'Microsoft Pablo - Spanish (Spain)',
      'Microsoft Sabina - Spanish (Mexico)',
      'Microsoft Raul - Spanish (Mexico)',
      // Voces de Apple
      'Monica',
      'Jorge',
      'Juan',
      'Diego',
      'Paulina',
      // Genéricas
      'Spanish',
      'es-ES',
      'es-MX'
    ]

    for (const priorityName of voicePriority) {
      const voice = voices.find(v => 
        v.name.includes(priorityName) || 
        v.lang.includes(priorityName)
      )
      if (voice) return voice
    }

    // Fallback: cualquier voz en español
    const spanishVoice = voices.find(voice => 
      voice.lang.startsWith('es') || 
      voice.lang.includes('spa') ||
      voice.name.toLowerCase().includes('spanish')
    )

    return spanishVoice || voices[0]
  }

  // Preprocesar texto para mejor prosodia
  private preprocessText(text: string): string {
    let processed = text

    // Agregar pausas naturales
    processed = processed.replace(/\./g, '... ')
    processed = processed.replace(/,/g, ', ')
    processed = processed.replace(/;/g, '; ')
    processed = processed.replace(/:/g, ': ')
    processed = processed.replace(/\?/g, '? ')
    processed = processed.replace(/!/g, '! ')
    
    // Agregar énfasis en palabras clave
    const emphasisWords = [
      'ancestral', 'piedra', 'viento', 'mar', 'tiempo', 
      'sabiduría', 'misterio', 'sagrado', 'eterno'
    ]
    
    emphasisWords.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi')
      processed = processed.replace(regex, ` ${word} `)
    })

    // Limpiar espacios múltiples
    processed = processed.replace(/\s+/g, ' ').trim()

    return processed
  }

  // Detener speech actual
  stop(): void {
    if (this.speechSynthesis) {
      this.speechSynthesis.cancel()
    }
  }

  // Cambiar configuración
  updateConfig(config: Partial<VoiceConfig>): void {
    this.config = { ...this.config, ...config }
  }

  // Listar voces disponibles
  getAvailableVoices(): SpeechSynthesisVoice[] {
    if (!this.speechSynthesis) return []
    return this.speechSynthesis.getVoices()
  }
}

// Voces recomendadas de ElevenLabs para el Moai
export const ELEVENLABS_VOICES = {
  ADAM: 'pNInz6obpgDQGcFmaJgB', // Masculina, grave, autoritaria
  ANTONI: 'ErXwobaYiN019PkySvjV', // Masculina, cálida, narrativa
  ARNOLD: 'VR6AewLTigWG4xSOukaG', // Masculina, profunda, resonante
  CALLUM: 'N2lVS1w4EtoT3dr4eOWO', // Masculina, suave, contemplativa
  JOSEPH: 'Zlb1dXrM653N07WRdFW3', // Masculina, madura, sabia
}
