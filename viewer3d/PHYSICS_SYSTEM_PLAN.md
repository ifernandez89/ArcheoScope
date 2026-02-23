# Sistema de Física de Resonancia Dimensional - Plan de Implementación

**Branch**: hrmBackendWorld  
**Fecha**: 23 de Febrero, 2026  
**Estado**: 📋 PLANIFICACIÓN

## Concepto Core

Sistema de física estilizada sci-fi que simula "resonancia dimensional" usando:
- Física básica (Rapier.js)
- Reglas personalizadas encima
- Efectos visuales (shaders GLSL)
- Audio reactivo

**NO es física realista. Es física CREÍBLE y ALIENÍGENA.**

---

## Arquitectura Propuesta

```
viewer3d/
├── physics/
│   ├── ResonanceSystem.ts          # Sistema principal
│   ├── AnomalyField.ts              # Campo de anomalía individual
│   ├── PhysicsWorld.ts              # Wrapper de Rapier
│   └── types.ts                     # Tipos TypeScript
├── shaders/
│   ├── spatial-distortion.glsl      # Shader de distorsión
│   └── resonance-field.glsl         # Shader de campo visible
└── components/
    ├── ResonanceField.tsx           # Componente React
    └── AnomalyZone.tsx              # Zona de anomalía
```

---

## Fase 1: Setup Básico (Nivel 1 Demo)

### 1.1 Instalar Rapier
```bash
npm install @dimforge/rapier3d-compat
```

### 1.2 Crear PhysicsWorld.ts
```typescript
import RAPIER from '@dimforge/rapier3d-compat'

export class PhysicsWorld {
  world: RAPIER.World
  
  constructor() {
    this.world = new RAPIER.World({ x: 0, y: -9.8, z: 0 })
  }
  
  update(deltaTime: number) {
    this.world.step()
  }
  
  createRigidBody(position: Vector3, mass: number) {
    // Crear cuerpo rígido básico
  }
}
```

### 1.3 Crear ResonanceSystem.ts
```typescript
export class ResonanceSystem {
  anomalies: AnomalyField[] = []
  
  // Función clave: obtener resonancia en posición
  getResonanceAtPosition(x: number, y: number, z: number): number {
    let totalResonance = 0
    
    for (const anomaly of this.anomalies) {
      const distance = Math.sqrt(
        Math.pow(x - anomaly.x, 2) +
        Math.pow(y - anomaly.y, 2) +
        Math.pow(z - anomaly.z, 2)
      )
      
      if (distance < anomaly.radius) {
        const factor = 1 - (distance / anomaly.radius)
        totalResonance += anomaly.intensity * factor
      }
    }
    
    return totalResonance
  }
  
  update(deltaTime: number) {
    // Actualizar todas las anomalías
  }
  
  applyToRigidBody(body: RigidBody, position: Vector3) {
    const resonance = this.getResonanceAtPosition(position.x, position.y, position.z)
    
    // Modificar masa aparente
    const newMass = body.mass() * (1 + resonance * 0.5)
    
    // Modificar gravedad
    if (resonance > 0.5) {
      body.setGravityScale(-1) // Flotar
    }
  }
  
  applyToShader(material: ShaderMaterial, position: Vector3) {
    const resonance = this.getResonanceAtPosition(position.x, position.y, position.z)
    material.uniforms.resonance.value = resonance
  }
  
  applyToAudio(sound: AudioNode, position: Vector3) {
    const resonance = this.getResonanceAtPosition(position.x, position.y, position.z)
    // Cambiar pitch según resonancia
  }
}
```

### 1.4 Crear AnomalyField.ts
```typescript
export interface AnomalyField {
  x: number
  y: number
  z: number
  radius: number
  intensity: number
  frequency: number // Para oscilación
  type: 'gravity' | 'mass' | 'spatial' | 'temporal'
}

export class Anomaly {
  field: AnomalyField
  time: number = 0
  
  update(deltaTime: number) {
    this.time += deltaTime
    
    // Oscilación de intensidad
    const oscillation = Math.sin(this.time * this.field.frequency)
    return this.field.intensity * oscillation
  }
}
```

---

## Fase 2: Efectos Visuales

### 2.1 Shader de Distorsión Espacial
```glsl
// spatial-distortion.glsl
uniform float time;
uniform vec3 anomalyCenter;
uniform float anomalyRadius;
uniform float distortionStrength;

varying vec3 vWorldPosition;

void main() {
  vec3 worldPos = (modelMatrix * vec4(position, 1.0)).xyz;
  
  float dist = distance(worldPos, anomalyCenter);
  
  if (dist < anomalyRadius) {
    float factor = 1.0 - (dist / anomalyRadius);
    float distortion = sin(dist * 5.0 - time * 2.0) * distortionStrength * factor;
    
    vec3 distortedPos = worldPos + normal * distortion;
    gl_Position = projectionMatrix * viewMatrix * vec4(distortedPos, 1.0);
  } else {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
  
  vWorldPosition = worldPos;
}
```

### 2.2 Componente ResonanceField.tsx
```typescript
export default function ResonanceField({ 
  position, 
  radius, 
  intensity 
}: ResonanceFieldProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const shader = useMemo(() => ({
    uniforms: {
      time: { value: 0 },
      anomalyCenter: { value: new THREE.Vector3(...position) },
      anomalyRadius: { value: radius },
      intensity: { value: intensity }
    },
    vertexShader: `...`,
    fragmentShader: `...`
  }), [position, radius, intensity])
  
  useFrame((state) => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.ShaderMaterial
      material.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[radius, 32, 32]} />
      <shaderMaterial
        vertexShader={shader.vertexShader}
        fragmentShader={shader.fragmentShader}
        uniforms={shader.uniforms}
        transparent
        opacity={0.3}
      />
    </mesh>
  )
}
```

---

## Fase 3: Integración con Sistema Existente

### 3.1 Modificar WalkableAvatar
```typescript
// Agregar física de Rapier al avatar
const rigidBody = useRef<RAPIER.RigidBody>()

useEffect(() => {
  // Crear rigid body para el avatar
  rigidBody.current = physicsWorld.createRigidBody(
    avatarPosition,
    75 // masa en kg
  )
}, [])

useFrame(() => {
  // Aplicar resonancia al avatar
  resonanceSystem.applyToRigidBody(rigidBody.current, avatarPosition)
})
```

### 3.2 Detectar Zonas de Anomalía por Bioma
```typescript
// En biome-detector.ts
export function detectAnomalies(lat: number, lon: number): AnomalyField[] {
  const anomalies: AnomalyField[] = []
  
  // Machu Picchu tiene anomalía gravitacional
  if (isNear(lat, lon, -13.1631, -72.5450)) {
    anomalies.push({
      x: 0, y: 5, z: 0,
      radius: 20,
      intensity: 0.8,
      frequency: 0.5,
      type: 'gravity'
    })
  }
  
  // Nazca tiene anomalía espacial
  if (isNear(lat, lon, -14.7390, -75.1300)) {
    anomalies.push({
      x: 0, y: 2, z: 0,
      radius: 50,
      intensity: 1.2,
      frequency: 0.3,
      type: 'spatial'
    })
  }
  
  return anomalies
}
```

---

## Fase 4: Audio Reactivo

### 4.1 Web Audio API (Simple)
```typescript
export class ResonanceAudio {
  audioContext: AudioContext
  oscillator: OscillatorNode
  
  constructor() {
    this.audioContext = new AudioContext()
    this.oscillator = this.audioContext.createOscillator()
  }
  
  updateFromResonance(resonance: number) {
    // Cambiar frecuencia según resonancia
    const baseFreq = 220 // La3
    const newFreq = baseFreq * (1 + resonance * 0.5)
    this.oscillator.frequency.setValueAtTime(newFreq, this.audioContext.currentTime)
  }
}
```

---

## Demo Nivel 1 (MVP)

**Ubicación**: Machu Picchu  
**Elementos**:
1. ✅ 1 anomalía gravitacional en el centro
2. ✅ Campo visible con shader ondulante
3. ✅ Gravedad invertida al entrar (flotar)
4. ✅ Masa aumenta cerca del centro (movimiento lento)
5. ✅ Sonido que cambia pitch según distancia

**Resultado esperado**:
- Jugador se acerca → escucha tono cambiando
- Entra al campo → empieza a flotar
- Se mueve más lento cerca del centro
- Efecto visual de "espacio vibrando"

---

## Ventajas de Esta Arquitectura

✅ **Modular**: No rompe nada existente  
✅ **Incremental**: Podemos implementar fase por fase  
✅ **Performante**: Rapier es muy rápido  
✅ **Extensible**: Fácil agregar nuevos tipos de anomalías  
✅ **Coherente**: Todo usa la misma función `getResonanceAtPosition()`  

---

## Próximos Pasos

1. ¿Instalamos Rapier y creamos la estructura base?
2. ¿Implementamos el shader de distorsión primero?
3. ¿Empezamos con una anomalía simple en Machu Picchu?

**Tu decisión** 🎯
