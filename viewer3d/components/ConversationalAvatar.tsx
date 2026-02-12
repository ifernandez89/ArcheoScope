'use client'

import { useState, useEffect, useRef } from 'react'
import { AvatarBrain, MOAI_PERSONALITY, type AvatarResponse } from '@/ai/avatar-brain'
import { AvatarBody, IntelligentGaze } from '@/ai/avatar-body'
import { LLMIntegration } from '@/ai/llm-integration'
import { AIAnimator } from '@/ai/animator'
import { ExpressionSystem } from '@/ai/expression-system'

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
  
  // Referencias a sistemas
  const brainRef = useRef<AvatarBrain | null>(null)
  const bodyRef = useRef<AvatarBody | null>(null)
  const gazeRef = useRef<IntelligentGaze | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const speechSynthesisRef = useRef<SpeechSynthesis | null>(null)

  // Inicializar sistemas
  useEffect(() => {
    if (!model || !camera) return

    const llm = new LLMIntegration({
      baseUrl: 'http://localhost:11434',
      model: 'qwen3:1.7b', // Modelo ultra-ligero y rápido
      temperature: 0.7
    })

    const animator = new AIAnimator()
    const expressions = new ExpressionSystem()

    // Crear cerebro con personalidad
    const brain = new AvatarBrain(MOAI_PERSONALITY, llm)
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

    // Conectar automáticamente
    autoConnect(llm)

    console.log('🗿 Avatar conversacional inicializado')

    return () => {
      body.stopPresence()
      gaze.stop()
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
  const autoConnect = async (llm: LLMIntegration) => {
    const available = await llm.checkAvailability()
    if (available) {
      setIsConnected(true)
      console.log('✅ Ollama conectado automáticamente')
      
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
      console.warn('⚠️ Ollama no disponible. Inicia: ollama serve')
    }
  }

  // Función para hablar con TTS
  const speak = (text: string) => {
    if (!voiceEnabled || !speechSynthesisRef.current) return

    // Cancelar cualquier speech anterior
    speechSynthesisRef.current.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    
    // Configurar voz (buscar voz en español si está disponible)
    const voices = speechSynthesisRef.current.getVoices()
    const spanishVoice = voices.find(voice => 
      voice.lang.startsWith('es') || voice.lang.startsWith('spa')
    )
    
    if (spanishVoice) {
      utterance.voice = spanishVoice
    }
    
    // Configurar parámetros para voz ancestral
    utterance.rate = 0.85 // Más lento, contemplativo
    utterance.pitch = 0.8 // Más grave
    utterance.volume = 0.9

    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = () => setIsSpeaking(false)

    speechSynthesisRef.current.speak(utterance)
  }

  // Conectar/desconectar
  const handleToggleConnection = async () => {
    if (!brainRef.current) return

    if (!isConnected) {
      // Verificar Ollama
      const llm = new LLMIntegration({
        baseUrl: 'http://localhost:11434',
        model: 'qwen3:1.7b'
      })

      const available = await llm.checkAvailability()
      if (!available) {
        alert('Ollama no está disponible. Asegúrate de que esté corriendo:\n\nollama serve')
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
          border: '3px solid rgba(255,255,255,0.3)',
          color: 'white',
          fontSize: '32px',
          cursor: 'pointer',
          boxShadow: isConnected 
            ? '0 4px 20px rgba(16, 185, 129, 0.5)'
            : '0 4px 20px rgba(239, 68, 68, 0.5)',
          zIndex: 1000,
          transition: 'all 0.3s ease',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative'
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
                {isConnected ? 'Ollama Activo' : 'Ollama Desconectado'}
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
                  : 'Inicia Ollama para hablar con el Moai:\n\nollama serve'}
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
          `}</style>
        </div>
      )}
    </>
  )
}
