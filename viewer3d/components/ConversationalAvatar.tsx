'use client'

import { useState, useEffect, useRef } from 'react'
import { AvatarBrain, MOAI_PERSONALITY, type AvatarResponse } from '@/ai/avatar-brain'
import { AvatarBody, IntelligentGaze } from '@/ai/avatar-body'
import { OpenRouterIntegration, OPENROUTER_MODELS } from '@/ai/openrouter-integration'
import { AIAnimator } from '@/ai/animator'
import { ExpressionSystem } from '@/ai/expression-system'
import { ProximityDetector } from '@/systems/proximity-detector'

interface Message {
  id: string
  role: 'user' | 'avatar'
  content: string
  emotion?: string
  timestamp: Date
}

interface ConversationalAvatarProps {
  model: THREE.Object3D | null
  camera: THREE.Camera | null
  onResponse?: (response: AvatarResponse) => void
}

export default function ConversationalAvatar({
  model,
  camera,
  onResponse
}: ConversationalAvatarProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [proximityDistance, setProximityDistance] = useState<number | null>(null)
  const [showProximityIndicator, setShowProximityIndicator] = useState(false)
  
  // Referencias a sistemas
  const brainRef = useRef<AvatarBrain | null>(null)
  const bodyRef = useRef<AvatarBody | null>(null)
  const gazeRef = useRef<IntelligentGaze | null>(null)
  const proximityRef = useRef<ProximityDetector | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const speechSynthesisRef = useRef<SpeechSynthesis | null>(null)

  // Inicializar sistemas
  useEffect(() => {
    if (!model || !camera) return

    let isMounted = true

    // Función para inicializar el avatar con la API key desde BD
    const initializeAvatar = async () => {
      try {
        // Obtener API key desde la base de datos (encriptada)
        console.log('🔐 Obteniendo API key desde base de datos...')
        const response = await fetch('http://127.0.0.1:8000/api/credentials/openrouter/api_key')
        
        if (!response.ok) {
          throw new Error('No se pudo obtener la API key desde la BD')
        }

        const data = await response.json()
        
        if (!data.success || !data.value) {
          throw new Error('API key no disponible en la base de datos')
        }

        const openrouterApiKey = data.value
        const openrouterModel = process.env.NEXT_PUBLIC_OPENROUTER_MODEL || 'arcee-ai/trinity-mini:free'
        
        console.log('✅ API key obtenida desde BD')
        
        if (!isMounted) return

        const llm = new OpenRouterIntegration({
          apiKey: openrouterApiKey,
          model: openrouterModel,
          temperature: 0.7,
          maxTokens: 300
        })

        const animator = new AIAnimator()
        const expressions = new ExpressionSystem()

        // Crear cerebro con personalidad
        const brain = new AvatarBrain(MOAI_PERSONALITY, llm as any)
        brainRef.current = brain

        // Crear cuerpo con presencia
        const body = new AvatarBody(model, animator, expressions, {
          enableBreathing: true,
          enableBlinking: true,
          enableGaze: true,
          enableSubtleMovement: true,
          breathingIntensity: 0.015,
          blinkFrequency: 4
        })
        bodyRef.current = body

        // Iniciar presencia
        body.startPresence()

        // Crear mirada inteligente
        const gaze = new IntelligentGaze(body, camera)
        gazeRef.current = gaze
        gaze.start()

        // Inicializar Speech Synthesis
        if (typeof window !== 'undefined' && window.speechSynthesis) {
          speechSynthesisRef.current = window.speechSynthesis
        }

        // Inicializar detector de proximidad
        if (model && camera) {
          const proximity = new ProximityDetector(camera, model, {
            activationDistance: 5,
            greetingDistance: 3,
            onEnterProximity: () => {
              console.log('👋 Usuario entró en zona de proximidad')
              setShowProximityIndicator(true)
            },
            onExitProximity: () => {
              console.log('👋 Usuario salió de zona de proximidad')
              setShowProximityIndicator(false)
            },
            onGreetingDistance: () => {
              console.log('🗿 Usuario cerca - Saludo automático')
              handleAutoGreeting()
            }
          })
          proximityRef.current = proximity
          proximity.start()

          // Actualizar distancia cada frame
          const updateDistance = () => {
            if (proximityRef.current && isMounted) {
              setProximityDistance(proximityRef.current.getCurrentDistance())
            }
            if (isMounted) {
              requestAnimationFrame(updateDistance)
            }
          }
          updateDistance()
        }

        // Conectar automáticamente
        await autoConnect(llm as any)

        console.log('🗿 Avatar conversacional inicializado con OpenRouter desde BD')
        
      } catch (error) {
        console.error('❌ Error inicializando avatar:', error)
        setIsConnected(false)
        
        // Mostrar mensaje al usuario
        const errorMsg: Message = {
          id: Date.now().toString(),
          role: 'avatar',
          content: 'No se pudo conectar con el sistema. Verifica que la API key esté configurada en la base de datos.',
          emotion: 'confused',
          timestamp: new Date()
        }
        setMessages([errorMsg])
      }
    }

    // Inicializar de forma asíncrona
    initializeAvatar()

    return () => {
      isMounted = false
      if (bodyRef.current) {
        bodyRef.current.stopPresence()
      }
      if (gazeRef.current) {
        gazeRef.current.stop()
      }
      if (proximityRef.current) {
        proximityRef.current.stop()
      }
      if (speechSynthesisRef.current) {
        speechSynthesisRef.current.cancel()
      }
    }
  }, [model, camera])

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Conectar automáticamente
  const autoConnect = async (llm: any) => {
    const available = await llm.checkAvailability()
    if (available) {
      setIsConnected(true)
      console.log('✅ OpenRouter conectado automáticamente')
      
      // Mensaje de bienvenida
      const welcomeMsg: Message = {
        id: Date.now().toString(),
        role: 'avatar',
        content: 'Saludos, viajero. Soy un Moai ancestral de Rapa Nui. ¿Qué te trae ante mí?',
        emotion: 'neutral',
        timestamp: new Date()
      }
      setMessages([welcomeMsg])
    } else {
      console.warn('⚠️ OpenRouter no disponible. Verifica la API key.')
    }
  }

  // Saludo automático cuando el usuario se acerca
  const handleAutoGreeting = async () => {
    if (!isConnected || !brainRef.current || !bodyRef.current) return

    // Evitar múltiples saludos
    if (messages.some(m => m.content.includes('acercas') || m.content.includes('bienvenido'))) {
      return
    }

    console.log('🗿 Generando saludo automático...')

    try {
      // Generar saludo contextual
      const greetingPrompt = 'Un viajero se acerca a ti. Salúdalo brevemente de forma ancestral y misteriosa.'
      const response = await brainRef.current.processMessage(greetingPrompt)

      // Ejecutar respuesta física
      await bodyRef.current.executeResponse(response)

      // Agregar saludo a mensajes
      const greetingMsg: Message = {
        id: Date.now().toString(),
        role: 'avatar',
        content: response.text,
        emotion: response.emotion,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, greetingMsg])

      // Hablar el saludo
      if (voiceEnabled) {
        speak(response.text)
      }

      // Abrir chat automáticamente
      setIsOpen(true)
    } catch (error) {
      console.error('Error en saludo automático:', error)
    }
  }

  // Función para hablar con TTS mejorado
  const speak = (text: string) => {
    if (!voiceEnabled || !speechSynthesisRef.current) return

    // Cancelar cualquier speech anterior
    speechSynthesisRef.current.cancel()

    // Preprocesar texto para mejor prosodia
    const processedText = preprocessTextForSpeech(text)

    const utterance = new SpeechSynthesisUtterance(processedText)
    
    // Buscar la mejor voz disponible
    const voices = speechSynthesisRef.current.getVoices()
    const bestVoice = selectBestVoice(voices)
    
    if (bestVoice) {
      utterance.voice = bestVoice
      console.log(`🎙️ Usando voz: ${bestVoice.name} (${bestVoice.lang})`)
    }
    
    // Configurar parámetros para voz más natural y ancestral
    utterance.rate = 0.9 // Ligeramente más lento pero no tanto
    utterance.pitch = 0.85 // Grave pero no demasiado
    utterance.volume = 1.0 // Volumen completo

    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = () => setIsSpeaking(false)

    speechSynthesisRef.current.speak(utterance)
  }

  // Seleccionar la mejor voz disponible
  const selectBestVoice = (voices: SpeechSynthesisVoice[]) => {
    // Prioridad de voces (de mejor a peor calidad)
    const voicePriority = [
      // Voces premium de Google (si están disponibles)
      'Google español',
      'Google español de Estados Unidos',
      'Google español de España',
      'Google español de México',
      // Voces de Microsoft (buena calidad)
      'Microsoft Helena - Spanish (Spain)',
      'Microsoft Pablo - Spanish (Spain)',
      'Microsoft Sabina - Spanish (Mexico)',
      'Microsoft Raul - Spanish (Mexico)',
      // Voces de Apple (macOS/iOS)
      'Monica',
      'Jorge',
      'Juan',
      'Diego',
      'Paulina',
      // Voces genéricas en español
      'Spanish',
      'es-ES',
      'es-MX',
      'es-US'
    ]

    // Buscar por prioridad
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
      voice.name.toLowerCase().includes('spanish') ||
      voice.name.toLowerCase().includes('español')
    )

    return spanishVoice || voices[0] // Última opción: primera voz disponible
  }

  // Preprocesar texto para mejor prosodia
  const preprocessTextForSpeech = (text: string): string => {
    let processed = text

    // Agregar pausas naturales después de puntuación
    processed = processed.replace(/\./g, '... ') // Pausa larga después de punto
    processed = processed.replace(/,/g, ', ') // Pausa corta después de coma
    processed = processed.replace(/;/g, '; ') // Pausa media después de punto y coma
    processed = processed.replace(/:/g, ': ') // Pausa después de dos puntos
    
    // Agregar énfasis en palabras clave (usando SSML-like markup que algunos engines entienden)
    const emphasisWords = ['ancestral', 'piedra', 'viento', 'mar', 'tiempo', 'sabiduría', 'misterio']
    emphasisWords.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi')
      processed = processed.replace(regex, ` ${word} `) // Espacio extra para énfasis
    })

    // Limpiar espacios múltiples
    processed = processed.replace(/\s+/g, ' ').trim()

    return processed
  }

  // Cargar voces cuando estén disponibles
  useEffect(() => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      // Las voces se cargan de forma asíncrona
      const loadVoices = () => {
        const voices = window.speechSynthesis.getVoices()
        if (voices.length > 0) {
          console.log('🎙️ Voces disponibles:', voices.map(v => `${v.name} (${v.lang})`))
        }
      }

      // Cargar voces inmediatamente
      loadVoices()

      // Y también cuando cambien (algunos navegadores lo necesitan)
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices
      }
    }
  }, [])

  // Conectar/desconectar
  const handleToggleConnection = async () => {
    if (!brainRef.current) return

    if (!isConnected) {
      try {
        // Obtener API key desde la base de datos
        console.log('🔐 Obteniendo API key desde BD para reconexión...')
        const response = await fetch('http://127.0.0.1:8000/api/credentials/openrouter/api_key')
        
        if (!response.ok) {
          throw new Error('No se pudo obtener la API key desde la BD')
        }

        const data = await response.json()
        
        if (!data.success || !data.value) {
          throw new Error('API key no disponible')
        }

        const openrouterApiKey = data.value
        const openrouterModel = process.env.NEXT_PUBLIC_OPENROUTER_MODEL || 'arcee-ai/trinity-mini:free'
        
        const llm = new OpenRouterIntegration({
          apiKey: openrouterApiKey,
          model: openrouterModel
        })

        const available = await llm.checkAvailability()
        if (!available) {
          alert('OpenRouter no está disponible. Verifica la conexión.')
          return
        }

        setIsConnected(true)
        
        // Mensaje de bienvenida
        const welcomeMsg: Message = {
          id: Date.now().toString(),
          role: 'avatar',
          content: 'Saludos, viajero. Soy un Moai ancestral de Rapa Nui. ¿Qué te trae ante mí?',
          emotion: 'neutral',
          timestamp: new Date()
        }
        setMessages([welcomeMsg])
        
        if (voiceEnabled) {
          speak(welcomeMsg.content)
        }
      } catch (error) {
        console.error('❌ Error al reconectar:', error)
        alert('No se pudo conectar. Verifica que la API key esté configurada en la base de datos.')
      }
    } else {
      setIsConnected(false)
      brainRef.current.reset()
      setMessages([])
      if (speechSynthesisRef.current) {
        speechSynthesisRef.current.cancel()
      }
    }
  }

  // Enviar mensaje
  const handleSend = async () => {
    if (!inputValue.trim() || isThinking || !isConnected || !brainRef.current || !bodyRef.current) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsThinking(true)

    try {
      // Procesar con el cerebro
      const response = await brainRef.current.processMessage(inputValue)

      // Ejecutar respuesta física
      await bodyRef.current.executeResponse(response)

      // Agregar respuesta a mensajes
      const avatarMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'avatar',
        content: response.text,
        emotion: response.emotion,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, avatarMessage])

      // Hablar la respuesta
      if (voiceEnabled) {
        speak(response.text)
      }

      // Callback opcional
      if (onResponse) {
        onResponse(response)
      }
    } catch (error) {
      console.error('Error procesando mensaje:', error)
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'avatar',
        content: 'Las piedras guardan silencio... intenta de nuevo.',
        emotion: 'confused',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsThinking(false)
    }
  }

  // Manejar Enter
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Obtener estado emocional
  const getEmotionalState = () => {
    if (!brainRef.current) return null
    return brainRef.current.getEmotionalState()
  }

  const emotionalState = getEmotionalState()

  return (
    <>
      {/* Botón flotante con indicador de estado */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '70px',
          height: '70px',
          borderRadius: '50%',
          background: isConnected 
            ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
            : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
          border: showProximityIndicator 
            ? '3px solid #fbbf24'
            : '3px solid rgba(255,255,255,0.3)',
          color: 'white',
          fontSize: '32px',
          cursor: 'pointer',
          boxShadow: showProximityIndicator
            ? '0 4px 30px rgba(251, 191, 36, 0.8), 0 0 20px rgba(251, 191, 36, 0.5)'
            : isConnected 
              ? '0 4px 20px rgba(16, 185, 129, 0.5)'
              : '0 4px 20px rgba(239, 68, 68, 0.5)',
          zIndex: 1000,
          transition: 'all 0.3s ease',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          animation: showProximityIndicator ? 'pulse-proximity 2s infinite' : 'none'
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        title={isConnected ? '🗿 Moai Conectado' : '🗿 Moai Desconectado'}
      >
        🗿
        {/* Indicador de voz */}
        {isSpeaking && (
          <div style={{
            position: 'absolute',
            top: '-5px',
            right: '-5px',
            width: '20px',
            height: '20px',
            borderRadius: '50%',
            background: '#fbbf24',
            animation: 'pulse 1s infinite'
          }}>
            🔊
          </div>
        )}
        {/* Indicador de conexión */}
        <div style={{
          position: 'absolute',
          bottom: '5px',
          right: '5px',
          width: '12px',
          height: '12px',
          borderRadius: '50%',
          background: isConnected ? '#10b981' : '#ef4444',
          border: '2px solid white',
          boxShadow: '0 0 10px rgba(0,0,0,0.3)'
        }} />
        {/* Indicador de proximidad */}
        {showProximityIndicator && proximityDistance !== null && (
          <div style={{
            position: 'absolute',
            top: '-30px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(251, 191, 36, 0.9)',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '10px',
            fontWeight: 'bold',
            whiteSpace: 'nowrap'
          }}>
            {proximityDistance.toFixed(1)}m
          </div>
        )}
      </button>

      {/* Panel conversacional */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '90px',
          right: '20px',
          width: '400px',
          height: '550px',
          background: 'rgba(0, 0, 0, 0.9)',
          backdropFilter: 'blur(10px)',
          borderRadius: '12px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          zIndex: 999,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden'
        }}>
          {/* Header */}
          <div style={{
            padding: '15px 20px',
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <h3 style={{
                margin: 0,
                color: 'white',
                fontSize: '16px',
                fontWeight: 'bold'
              }}>
                🗿 Moai Ancestral
              </h3>
              <div style={{
                fontSize: '11px',
                color: isConnected ? '#10b981' : '#ef4444',
                marginTop: '3px',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}>
                <span style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: isConnected ? '#10b981' : '#ef4444',
                  display: 'inline-block',
                  animation: isConnected ? 'pulse 2s infinite' : 'none'
                }} />
                {isConnected ? 'OpenRouter Activo' : 'OpenRouter Desconectado'}
              </div>
            </div>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              {/* Toggle de voz */}
              <button
                onClick={() => setVoiceEnabled(!voiceEnabled)}
                style={{
                  padding: '6px 10px',
                  background: voiceEnabled ? 'rgba(16, 185, 129, 0.2)' : 'rgba(107, 114, 128, 0.2)',
                  border: voiceEnabled ? '1px solid #10b981' : '1px solid #6b7280',
                  borderRadius: '6px',
                  color: 'white',
                  fontSize: '16px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                title={voiceEnabled ? 'Voz activada' : 'Voz desactivada'}
              >
                {voiceEnabled ? '🔊' : '🔇'}
              </button>
              {/* Botón de reconectar (solo si está desconectado) */}
              {!isConnected && (
                <button
                  onClick={handleToggleConnection}
                  style={{
                    padding: '6px 12px',
                    background: 'rgba(16, 185, 129, 0.2)',
                    border: '1px solid #10b981',
                    borderRadius: '6px',
                    color: 'white',
                    fontSize: '12px',
                    cursor: 'pointer'
                  }}
                >
                  Reconectar
                </button>
              )}
            </div>
          </div>

          {/* Estado emocional */}
          {isConnected && emotionalState && (
            <div style={{
              padding: '10px 20px',
              background: 'rgba(102, 126, 234, 0.1)',
              borderBottom: '1px solid rgba(255,255,255,0.1)',
              fontSize: '11px',
              color: 'rgba(255,255,255,0.7)'
            }}>
              <div style={{ display: 'flex', gap: '15px' }}>
                <span>Ánimo: {emotionalState.mood > 0 ? '😊' : emotionalState.mood < 0 ? '😔' : '😐'} {emotionalState.mood.toFixed(0)}</span>
                <span>Energía: ⚡ {emotionalState.energy.toFixed(0)}</span>
                <span>Interés: 👁️ {emotionalState.engagement.toFixed(0)}</span>
              </div>
            </div>
          )}

          {/* Mensajes */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '15px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            {messages.length === 0 && (
              <div style={{
                textAlign: 'center',
                color: 'rgba(255,255,255,0.5)',
                fontSize: '14px',
                marginTop: '20px'
              }}>
                {isConnected 
                  ? 'El Moai aguarda tus palabras...' 
                  : 'Conectando con el Moai ancestral...'}
              </div>
            )}

            {messages.map(msg => (
              <div
                key={msg.id}
                style={{
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '80%'
                }}
              >
                <div style={{
                  padding: '10px 14px',
                  borderRadius: '12px',
                  background: msg.role === 'user' 
                    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                    : 'rgba(139, 92, 46, 0.3)',
                  border: msg.role === 'avatar' ? '1px solid rgba(139, 92, 46, 0.5)' : 'none',
                  color: 'white',
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}>
                  {msg.content}
                  {msg.emotion && msg.role === 'avatar' && (
                    <div style={{
                      fontSize: '10px',
                      color: 'rgba(255,255,255,0.5)',
                      marginTop: '5px'
                    }}>
                      {msg.emotion}
                    </div>
                  )}
                </div>
                <div style={{
                  fontSize: '10px',
                  color: 'rgba(255,255,255,0.4)',
                  marginTop: '3px',
                  textAlign: msg.role === 'user' ? 'right' : 'left'
                }}>
                  {msg.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}

            {isThinking && (
              <div style={{
                alignSelf: 'flex-start',
                padding: '10px 14px',
                borderRadius: '12px',
                background: 'rgba(139, 92, 46, 0.3)',
                border: '1px solid rgba(139, 92, 46, 0.5)',
                color: 'rgba(255,255,255,0.6)',
                fontSize: '14px'
              }}>
                <span className="thinking">El Moai contempla...</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div style={{
            padding: '15px',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            display: 'flex',
            gap: '10px'
          }}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={!isConnected || isThinking}
              placeholder={isConnected ? 'Habla con el Moai...' : 'Conecta primero...'}
              style={{
                flex: 1,
                padding: '10px 14px',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px',
                outline: 'none'
              }}
            />
            <button
              onClick={handleSend}
              disabled={!isConnected || isThinking || !inputValue.trim()}
              style={{
                padding: '10px 20px',
                background: (!isConnected || isThinking || !inputValue.trim())
                  ? 'rgba(255,255,255,0.1)'
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px',
                fontWeight: 'bold',
                cursor: (!isConnected || isThinking || !inputValue.trim()) ? 'not-allowed' : 'pointer',
                opacity: (!isConnected || isThinking || !inputValue.trim()) ? 0.5 : 1
              }}
            >
              Enviar
            </button>
          </div>

          <style jsx>{`
            @keyframes thinking {
              0%, 100% { opacity: 0.4; }
              50% { opacity: 1; }
            }
            .thinking {
              animation: thinking 1.5s infinite;
            }
            @keyframes pulse {
              0%, 100% { 
                opacity: 1;
                transform: scale(1);
              }
              50% { 
                opacity: 0.7;
                transform: scale(1.1);
              }
            }
            @keyframes pulse-proximity {
              0%, 100% { 
                transform: scale(1);
                box-shadow: 0 4px 30px rgba(251, 191, 36, 0.8), 0 0 20px rgba(251, 191, 36, 0.5);
              }
              50% { 
                transform: scale(1.05);
                box-shadow: 0 4px 40px rgba(251, 191, 36, 1), 0 0 30px rgba(251, 191, 36, 0.8);
              }
            }
          `}</style>
        </div>
      )}
    </>
  )
}
