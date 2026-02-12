'use client'

import { useState, useRef, useEffect } from 'react'
import type { OllamaResponse } from '@/ai/llm-integration'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  emotion?: string
  gesture?: string
  timestamp: Date
}

interface ChatInterfaceProps {
  onSendMessage: (message: string) => Promise<OllamaResponse | null>
  isActive: boolean
  onToggle: () => void
}

export default function ChatInterface({ onSendMessage, isActive, onToggle }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll al último mensaje
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Enviar mensaje
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading || !isActive) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await onSendMessage(inputValue)
      
      if (response) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: response.text,
          emotion: response.emotion,
          gesture: response.gesture,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, assistantMessage])
      }
    } catch (error) {
      console.error('Error enviando mensaje:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Manejar Enter
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: isActive 
            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            : 'linear-gradient(135deg, #999 0%, #666 100%)',
          border: 'none',
          color: 'white',
          fontSize: '28px',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
          zIndex: 1000,
          transition: 'transform 0.2s',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      >
        💬
      </button>

      {/* Panel de chat */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '90px',
          right: '20px',
          width: '380px',
          height: '500px',
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
                💬 Chat con IA
              </h3>
              <div style={{
                fontSize: '11px',
                color: isActive ? '#4ade80' : '#ef4444',
                marginTop: '3px'
              }}>
                {isActive ? '● Conectado' : '● Desconectado'}
              </div>
            </div>
            <button
              onClick={onToggle}
              style={{
                padding: '6px 12px',
                background: isActive ? 'rgba(239, 68, 68, 0.2)' : 'rgba(74, 222, 128, 0.2)',
                border: isActive ? '1px solid #ef4444' : '1px solid #4ade80',
                borderRadius: '6px',
                color: 'white',
                fontSize: '12px',
                cursor: 'pointer'
              }}
            >
              {isActive ? 'Desconectar' : 'Conectar'}
            </button>
          </div>

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
                {isActive 
                  ? 'Pregúntame sobre el modelo 3D...' 
                  : 'Conecta para comenzar a chatear'}
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
                    : 'rgba(255,255,255,0.1)',
                  color: 'white',
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}>
                  {msg.content}
                  {msg.emotion && (
                    <div style={{
                      fontSize: '11px',
                      color: 'rgba(255,255,255,0.6)',
                      marginTop: '5px'
                    }}>
                      😊 {msg.emotion}
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

            {isLoading && (
              <div style={{
                alignSelf: 'flex-start',
                padding: '10px 14px',
                borderRadius: '12px',
                background: 'rgba(255,255,255,0.1)',
                color: 'rgba(255,255,255,0.6)',
                fontSize: '14px'
              }}>
                <span className="typing-indicator">●●●</span>
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
              disabled={!isActive || isLoading}
              placeholder={isActive ? 'Escribe un mensaje...' : 'Conecta primero...'}
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
              disabled={!isActive || isLoading || !inputValue.trim()}
              style={{
                padding: '10px 20px',
                background: (!isActive || isLoading || !inputValue.trim())
                  ? 'rgba(255,255,255,0.1)'
                  : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px',
                fontWeight: 'bold',
                cursor: (!isActive || isLoading || !inputValue.trim()) ? 'not-allowed' : 'pointer',
                opacity: (!isActive || isLoading || !inputValue.trim()) ? 0.5 : 1
              }}
            >
              Enviar
            </button>
          </div>

          <style jsx>{`
            @keyframes typing {
              0%, 100% { opacity: 0.3; }
              50% { opacity: 1; }
            }
            .typing-indicator {
              animation: typing 1.5s infinite;
            }
          `}</style>
        </div>
      )}
    </>
  )
}
