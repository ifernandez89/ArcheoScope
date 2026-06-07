'use client'

/**
 * IntroAmbientAudio
 * ─────────────────────────────────────────────────────────────────────────────
 * Audio ambiental para Landing, Menú y páginas estáticas (sin Three.js).
 * 
 * Genera un drone espacial suave usando Web Audio API directamente:
 * - Drone base: 136.10 Hz (frecuencia "Om" — patrón del proyecto)
 * - Armónico 1: 272.20 Hz (octava superior, muy suave)
 * - Pad de estrellas: ruido filtrado con LFO lento
 * - Reverb simulado con delay + feedback
 * 
 * Reglas:
 * - Se activa en primer gesto del usuario (AudioContext policy)
 * - Fade-in suave de 3s
 * - Fade-out de 1.5s al desmontar (al navegar a otra página)
 * - Respeta el volumen guardado en gameSettings (masterVolume)
 * - No hace nada en SSR
 */

import { useEffect, useRef } from 'react'

interface IntroAmbientAudioProps {
  /** Volumen base (0-1). Default: 0.18 — sutil, no intrusivo */
  volume?: number
}

export default function IntroAmbientAudio({ volume = 0.18 }: IntroAmbientAudioProps) {
  const ctxRef = useRef<AudioContext | null>(null)
  const gainRef = useRef<GainNode | null>(null)
  const activeRef = useRef(false)
  const unmountedRef = useRef(false)

  useEffect(() => {
    if (typeof window === 'undefined') return
    unmountedRef.current = false

    // Leer volumen guardado de gameSettings (si existe)
    let masterVol = volume
    try {
      const raw = localStorage.getItem('game_settings')
      if (raw) {
        const parsed = JSON.parse(raw)
        if (typeof parsed?.audio?.masterVolume === 'number') {
          masterVol = parsed.audio.masterVolume * volume
        }
      }
    } catch {}

    const startAudio = async () => {
      if (activeRef.current || unmountedRef.current) return
      activeRef.current = true

      try {
        const AudioCtxClass = window.AudioContext || (window as any).webkitAudioContext
        if (!AudioCtxClass) return

        const ctx = new AudioCtxClass()
        ctxRef.current = ctx
        
        // Forzar resume si el navegador lo inició suspendido
        if (ctx.state === 'suspended') {
          await ctx.resume()
        }

        // ── Master gain (fade-in) ──────────────────────────────────────────
        const masterGain = ctx.createGain()
        masterGain.gain.setValueAtTime(0, ctx.currentTime)
        masterGain.gain.linearRampToValueAtTime(masterVol, ctx.currentTime + 3.0)
        masterGain.connect(ctx.destination)
        gainRef.current = masterGain

        // ── Delay / reverb simulado ────────────────────────────────────────
        const delay = ctx.createDelay(2.0)
        delay.delayTime.value = 0.45
        const delayGain = ctx.createGain()
        delayGain.gain.value = 0.28
        delay.connect(delayGain)
        delayGain.connect(delay)          // feedback loop
        delayGain.connect(masterGain)

        const connectToChain = (node: AudioNode) => {
          node.connect(masterGain)
          node.connect(delay)
        }

        // ── Drone base: 136.10 Hz (Om cósmico) ────────────────────────────
        const drone1 = ctx.createOscillator()
        drone1.type = 'sine'
        drone1.frequency.value = 136.10
        const droneGain1 = ctx.createGain()
        droneGain1.gain.value = 0.55
        drone1.connect(droneGain1)
        connectToChain(droneGain1)
        drone1.start()

        // ── Armónico: 272.20 Hz (octava, muy suave) ───────────────────────
        const drone2 = ctx.createOscillator()
        drone2.type = 'sine'
        drone2.frequency.value = 272.20
        const droneGain2 = ctx.createGain()
        droneGain2.gain.value = 0.18
        drone2.connect(droneGain2)
        connectToChain(droneGain2)
        drone2.start()

        // ── Sub-armónico: 68.05 Hz (quinta inferior, cuerpo) ─────────────
        const drone3 = ctx.createOscillator()
        drone3.type = 'sine'
        drone3.frequency.value = 68.05
        const droneGain3 = ctx.createGain()
        droneGain3.gain.value = 0.30
        drone3.connect(droneGain3)
        connectToChain(droneGain3)
        drone3.start()

        // ── Pad de estrellas: ruido blanco filtrado ────────────────────────
        const bufferSize = ctx.sampleRate * 2 // 2s de ruido
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate)
        const noiseData = noiseBuffer.getChannelData(0)
        for (let i = 0; i < bufferSize; i++) {
          noiseData[i] = Math.random() * 2 - 1
        }
        const noiseSource = ctx.createBufferSource()
        noiseSource.buffer = noiseBuffer
        noiseSource.loop = true

        // Filtro pasa-banda angosto — crea textura etérea
        const noiseFilter = ctx.createBiquadFilter()
        noiseFilter.type = 'bandpass'
        noiseFilter.frequency.value = 800
        noiseFilter.Q.value = 0.8

        // LFO para modulación del filtro (movimiento lento)
        const lfo = ctx.createOscillator()
        lfo.type = 'sine'
        lfo.frequency.value = 0.08  // muy lento — 1 ciclo cada ~12s
        const lfoGain = ctx.createGain()
        lfoGain.gain.value = 400    // modula la frecuencia del filtro ±400Hz
        lfo.connect(lfoGain)
        lfoGain.connect(noiseFilter.frequency)
        lfo.start()

        const noiseGain = ctx.createGain()
        noiseGain.gain.value = 0.06  // muy sutil
        noiseSource.connect(noiseFilter)
        noiseFilter.connect(noiseGain)
        connectToChain(noiseGain)
        noiseSource.start()

        // ── LFO de volumen en el drone principal (respiración cósmica) ─────
        const breathLFO = ctx.createOscillator()
        breathLFO.type = 'sine'
        breathLFO.frequency.value = 0.05  // 1 ciclo cada 20s
        const breathGain = ctx.createGain()
        breathGain.gain.value = 0.08
        breathLFO.connect(breathGain)
        breathGain.connect(droneGain1.gain)
        breathLFO.start()

        console.log('🎵 IntroAmbientAudio: drone cósmico activo (136.10 Hz Om)')

      } catch (err) {
        console.warn('IntroAmbientAudio: error iniciando audio', err)
        activeRef.current = false
      }
    }

    // Activar en primer gesto del usuario
    const handleInteraction = () => {
      startAudio()
      // No remover listeners — permite reinicio si el context fue suspendido
    }

    window.addEventListener('click', handleInteraction, { once: false })
    window.addEventListener('keydown', handleInteraction, { once: false })
    window.addEventListener('touchstart', handleInteraction, { once: false })

    return () => {
      unmountedRef.current = true
      window.removeEventListener('click', handleInteraction)
      window.removeEventListener('keydown', handleInteraction)
      window.removeEventListener('touchstart', handleInteraction)

      // Fade-out suave al desmontar
      const ctx = ctxRef.current
      const gain = gainRef.current
      if (ctx && gain) {
        try {
          gain.gain.cancelScheduledValues(ctx.currentTime)
          gain.gain.setValueAtTime(gain.gain.value, ctx.currentTime)
          gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 1.5)
          // Cerrar AudioContext tras el fade-out
          setTimeout(() => {
            try { ctx.close() } catch {}
          }, 1600)
        } catch {}
      }
    }
  }, [volume])

  // Componente invisible — solo lógica de audio
  return null
}
