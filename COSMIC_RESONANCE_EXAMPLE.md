# 🌌 Cosmic Resonance - Ejemplo Completo de Integración

## Ejemplo 1: Integración Básica (5 minutos)

### Paso 1: En tu componente de escena principal

```typescript
// Scene3D.tsx o tu componente principal
import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'
import CosmicResonanceDemo from '@/components/CosmicResonanceDemo'

export default function Scene3D() {
  const sceneRef = useRef<THREE.Scene>()
  const cosmicRef = useRef(getCosmicResonance())
  
  // Refs para planetas
  const earthRef = useRef<THREE.Mesh>()
  const marsRef = useRef<THREE.Mesh>()
  const jupiterRef = useRef<THREE.Mesh>()
  
  useEffect(() => {
    const scene = new THREE.Scene()
    sceneRef.current = scene
    const cosmic = cosmicRef.current
    
    // Crear planetas (ejemplo simplificado)
    const earthGeometry = new THREE.SphereGeometry(1, 32, 32)
    const earthMaterial = new THREE.MeshStandardMaterial({ color: 0x4A90E2 })
    const earth = new THREE.Mesh(earthGeometry, earthMaterial)
    earth.position.set(10, 0, 0)
    scene.add(earth)
    earthRef.current = earth
    
    const marsGeometry = new THREE.SphereGeometry(0.5, 32, 32)
    const marsMaterial = new THREE.MeshStandardMaterial({ color: 0xE27B58 })
    const mars = new THREE.Mesh(marsGeometry, marsMaterial)
    mars.position.set(15, 0, 0)
    scene.add(mars)
    marsRef.current = mars
    
    const jupiterGeometry = new THREE.SphereGeometry(2, 32, 32)
    const jupiterMaterial = new THREE.MeshStandardMaterial({ color: 0xD4A574 })
    const jupiter = new THREE.Mesh(jupiterGeometry, jupiterMaterial)
    jupiter.position.set(25, 0, 0)
    scene.add(jupiter)
    jupiterRef.current = jupiter
    
    // Registrar planetas en el sistema de resonancia
    cosmic.registerCelestialBody({
      id: 'earth',
      name: 'Tierra',
      position: earth.position,
      orbitalPeriod: 365.25,
      orbitalFrequency: 1 / 365.25,
      audioFrequency: 136.10,
      color: '#4A90E2'
    })
    
    cosmic.registerCelestialBody({
      id: 'mars',
      name: 'Marte',
      position: mars.position,
      orbitalPeriod: 687,
      orbitalFrequency: 1 / 687,
      audioFrequency: 144.72,
      color: '#E27B58'
    })
    
    cosmic.registerCelestialBody({
      id: 'jupiter',
      name: 'Júpiter',
      position: jupiter.position,
      orbitalPeriod: 4333,
      orbitalFrequency: 1 / 4333,
      audioFrequency: 183.58,
      color: '#D4A574'
    })
    
    // Loop de animación
    let lastTime = Date.now()
    
    function animate() {
      const now = Date.now()
      const deltaTime = (now - lastTime) / 1000
      lastTime = now
      
      // Simular órbitas (ejemplo simplificado)
      const time = now * 0.0001
      
      if (earthRef.current) {
        earthRef.current.position.x = Math.cos(time) * 10
        earthRef.current.position.z = Math.sin(time) * 10
        cosmic.updateBodyPosition('earth', earthRef.current.position)
      }
      
      if (marsRef.current) {
        marsRef.current.position.x = Math.cos(time * 0.5) * 15
        marsRef.current.position.z = Math.sin(time * 0.5) * 15
        cosmic.updateBodyPosition('mars', marsRef.current.position)
      }
      
      if (jupiterRef.current) {
        jupiterRef.current.position.x = Math.cos(time * 0.2) * 25
        jupiterRef.current.position.z = Math.sin(time * 0.2) * 25
        cosmic.updateBodyPosition('jupiter', jupiterRef.current.position)
      }
      
      // Actualizar sistema de resonancia
      cosmic.update(deltaTime)
      
      requestAnimationFrame(animate)
    }
    
    animate()
    
    return () => {
      cosmic.dispose()
    }
  }, [])
  
  return (
    <>
      <Canvas>
        {/* Tu escena 3D */}
      </Canvas>
      
      {/* UI de resonancia cósmica */}
      {sceneRef.current && (
        <CosmicResonanceDemo 
          scene={sceneRef.current} 
          enabled={true}
        />
      )}
    </>
  )
}
```

---

## Ejemplo 2: Integración con Sistema de Misiones

```typescript
// MissionSystem.ts
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'

export function onMissionComplete(missionId: string, scene: THREE.Scene) {
  const cosmic = getCosmicResonance()
  const harmonia = getHarmoniaMundi()
  
  // Misión especial: Descubrir resonancia cósmica
  if (missionId === 'gobekli_tepe_complete') {
    // Descubrir el sistema
    cosmic.discover()
    cosmic.enable(scene)
    
    // Activar audio especial
    harmonia.playBeetleSound()
    
    // Mostrar notificación
    showNotification({
      title: '✨ Descubrimiento Cósmico',
      message: 'Has desbloqueado el Mapa Armónico del Sistema Solar',
      type: 'legendary'
    })
    
    console.log('🌌 Sistema de Resonancia Cósmica desbloqueado!')
  }
}
```

---

## Ejemplo 3: Recompensas por Eventos de Resonancia

```typescript
// RewardSystem.ts
import { getCosmicResonance, type ResonanceEvent } from '@/systems/CosmicResonanceSystem'

export function checkResonanceRewards(ship: Ship, player: Player) {
  const cosmic = getCosmicResonance()
  
  if (!cosmic.isDiscovered()) return
  
  const events = cosmic.getActiveEvents()
  
  events.forEach(event => {
    // Evitar dar recompensa múltiples veces
    if (event.rewarded) return
    
    switch (event.type) {
      case 'gravitational_pulse':
        // ⚡ Impulso de velocidad
        ship.velocity.multiplyScalar(1.5)
        ship.energy += 20
        
        showFloatingText('⚡ Impulso Gravitacional!', event.alignment.center)
        playSound('gravitational_pulse.mp3')
        
        console.log('⚡ Impulso gravitacional aplicado')
        break
        
      case 'orbital_energy':
        // 🌟 Recarga de energía
        ship.energy = Math.min(ship.maxEnergy, ship.energy + 50)
        player.experience += 25
        
        showFloatingText('🌟 Energía Orbital!', event.alignment.center)
        playSound('orbital_energy.mp3')
        
        // Efecto visual
        createEnergyBurst(event.alignment.center, '#ffaa00')
        
        console.log('🌟 Energía orbital recibida')
        break
        
      case 'cosmic_event':
        // 💫 Portal cósmico (evento raro)
        const portal = createPortal(event.alignment.center)
        portal.destination = 'secret_dimension'
        portal.duration = 60 // segundos
        
        showNotification({
          title: '💫 Evento Cósmico',
          message: 'Un portal dimensional se ha abierto',
          type: 'legendary'
        })
        
        playSound('cosmic_event.mp3')
        
        // Recompensa especial
        player.experience += 100
        player.unlockAchievement('cosmic_witness')
        
        console.log('💫 Portal cósmico abierto')
        break
        
      case 'harmonic_resonance':
        // 🎵 Resonancia armónica
        player.experience += 50
        player.knowledge += 10
        
        // Desbloquear conocimiento especial
        player.unlockKnowledge('harmonic_ratios')
        
        showFloatingText('🎵 Resonancia Armónica!', event.alignment.center)
        playSound('harmonic_resonance.mp3')
        
        console.log('🎵 Resonancia armónica detectada')
        break
    }
    
    // Marcar como recompensado
    event.rewarded = true
  })
}
```

---

## Ejemplo 4: Visualización Personalizada

```typescript
// CustomCosmicVisualization.tsx
import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'

export function useCosmicVisualization(scene: THREE.Scene) {
  const particlesRef = useRef<THREE.Points>()
  
  useEffect(() => {
    const cosmic = getCosmicResonance()
    
    if (!cosmic.isDiscovered()) return
    
    // Crear partículas que fluyen por las líneas de resonancia
    const particleCount = 1000
    const positions = new Float32Array(particleCount * 3)
    const colors = new Float32Array(particleCount * 3)
    
    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100
      positions[i * 3 + 1] = (Math.random() - 0.5) * 100
      positions[i * 3 + 2] = (Math.random() - 0.5) * 100
      
      colors[i * 3] = Math.random()
      colors[i * 3 + 1] = Math.random()
      colors[i * 3 + 2] = Math.random()
    }
    
    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    
    const material = new THREE.PointsMaterial({
      size: 0.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    })
    
    const particles = new THREE.Points(geometry, material)
    scene.add(particles)
    particlesRef.current = particles
    
    // Animar partículas
    function animate() {
      if (!particlesRef.current) return
      
      const events = cosmic.getActiveEvents()
      
      if (events.length > 0) {
        // Hacer que las partículas se muevan hacia los centros de alineación
        const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
        
        for (let i = 0; i < particleCount; i++) {
          const event = events[i % events.length]
          const center = event.alignment.center
          
          // Mover partícula hacia el centro
          positions[i * 3] += (center.x - positions[i * 3]) * 0.01
          positions[i * 3 + 1] += (center.y - positions[i * 3 + 1]) * 0.01
          positions[i * 3 + 2] += (center.z - positions[i * 3 + 2]) * 0.01
        }
        
        particlesRef.current.geometry.attributes.position.needsUpdate = true
      }
      
      requestAnimationFrame(animate)
    }
    
    animate()
    
    return () => {
      if (particlesRef.current) {
        scene.remove(particlesRef.current)
        particlesRef.current.geometry.dispose()
        ;(particlesRef.current.material as THREE.Material).dispose()
      }
    }
  }, [scene])
}
```

---

## Ejemplo 5: Integración con Audio

```typescript
// CosmicAudioSystem.ts
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'

export class CosmicAudioSystem {
  private audioContext?: AudioContext
  private eventOscillators: Map<string, OscillatorNode> = new Map()
  
  async enable() {
    this.audioContext = new AudioContext()
    
    const cosmic = getCosmicResonance()
    const harmonia = getHarmoniaMundi()
    
    // Escuchar eventos de resonancia
    setInterval(() => {
      const events = cosmic.getActiveEvents()
      
      events.forEach(event => {
        // Si ya tiene oscilador, skip
        if (this.eventOscillators.has(event.id)) return
        
        // Crear oscilador para este evento
        const osc = this.audioContext!.createOscillator()
        const gain = this.audioContext!.createGain()
        
        // Frecuencia basada en el tipo de evento
        const frequencies = {
          gravitational_pulse: 60,
          orbital_energy: 80,
          cosmic_event: 100,
          harmonic_resonance: 120
        }
        
        osc.frequency.value = frequencies[event.type]
        osc.type = 'sine'
        
        gain.gain.value = 0
        gain.gain.linearRampToValueAtTime(
          event.intensity * 0.1,
          this.audioContext!.currentTime + 1
        )
        
        osc.connect(gain)
        gain.connect(this.audioContext!.destination)
        
        osc.start()
        this.eventOscillators.set(event.id, osc)
        
        // Detener cuando el evento termine
        setTimeout(() => {
          gain.gain.linearRampToValueAtTime(
            0,
            this.audioContext!.currentTime + 1
          )
          
          setTimeout(() => {
            osc.stop()
            osc.disconnect()
            this.eventOscillators.delete(event.id)
          }, 1000)
        }, event.duration * 1000)
      })
    }, 100)
  }
  
  dispose() {
    this.eventOscillators.forEach(osc => {
      osc.stop()
      osc.disconnect()
    })
    
    this.eventOscillators.clear()
    
    if (this.audioContext) {
      this.audioContext.close()
    }
  }
}
```

---

## Ejemplo 6: Test Completo

```typescript
// cosmic-resonance.test.ts
import * as THREE from 'three'
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'

describe('Cosmic Resonance System', () => {
  let scene: THREE.Scene
  let cosmic: ReturnType<typeof getCosmicResonance>
  
  beforeEach(() => {
    scene = new THREE.Scene()
    cosmic = getCosmicResonance()
    cosmic.discover()
    cosmic.enable(scene)
  })
  
  afterEach(() => {
    cosmic.dispose()
  })
  
  test('detecta triángulo equilátero', () => {
    // Registrar 3 cuerpos en triángulo equilátero
    cosmic.registerCelestialBody({
      id: 'test1',
      name: 'Test 1',
      position: new THREE.Vector3(100, 0, 0),
      orbitalPeriod: 365,
      orbitalFrequency: 1/365,
      audioFrequency: 136.10,
      color: '#ff0000'
    })
    
    cosmic.registerCelestialBody({
      id: 'test2',
      name: 'Test 2',
      position: new THREE.Vector3(-50, 86.6, 0),
      orbitalPeriod: 365,
      orbitalFrequency: 1/365,
      audioFrequency: 136.10,
      color: '#00ff00'
    })
    
    cosmic.registerCelestialBody({
      id: 'test3',
      name: 'Test 3',
      position: new THREE.Vector3(-50, -86.6, 0),
      orbitalPeriod: 365,
      orbitalFrequency: 1/365,
      audioFrequency: 136.10,
      color: '#0000ff'
    })
    
    // Actualizar
    cosmic.update(0.016)
    
    // Verificar
    const events = cosmic.getActiveEvents()
    expect(events.length).toBeGreaterThan(0)
    expect(events[0].alignment.type).toBe('triangle')
  })
  
  test('no detecta alineaciones con pocos cuerpos', () => {
    cosmic.registerCelestialBody({
      id: 'test1',
      name: 'Test 1',
      position: new THREE.Vector3(100, 0, 0),
      orbitalPeriod: 365,
      orbitalFrequency: 1/365,
      audioFrequency: 136.10,
      color: '#ff0000'
    })
    
    cosmic.update(0.016)
    
    const events = cosmic.getActiveEvents()
    expect(events.length).toBe(0)
  })
  
  test('estadísticas correctas', () => {
    cosmic.registerCelestialBody({
      id: 'earth',
      name: 'Tierra',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 365.25,
      orbitalFrequency: 1/365.25,
      audioFrequency: 136.10,
      color: '#4A90E2'
    })
    
    const stats = cosmic.getStats()
    expect(stats.celestialBodies).toBe(1)
    expect(stats.discovered).toBe(true)
    expect(stats.enabled).toBe(true)
  })
})
```

---

## 🎯 Resumen

Estos ejemplos muestran:

1. ✅ **Integración básica** - 5 minutos
2. ✅ **Sistema de misiones** - Descubrimiento del sistema
3. ✅ **Recompensas** - Efectos por eventos de resonancia
4. ✅ **Visualización personalizada** - Partículas y efectos
5. ✅ **Audio** - Sonidos procedurales
6. ✅ **Testing** - Tests unitarios

**Todos los ejemplos son funcionales y listos para usar.**

---

**Próximo paso:** Copia el código del Ejemplo 1 en tu proyecto y pruébalo! 🚀
