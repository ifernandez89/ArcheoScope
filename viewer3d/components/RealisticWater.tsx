/**
 * RealisticWater - Agua realista con Fresnel, Reflection y Refraction
 * 
 * Niveles implementados:
 * - Nivel 2: Fresnel (cambio según ángulo de visión)
 * - Nivel 3: Reflection (reflexión dinámica)
 * - Nivel 4: Refraction fake (distorsión UV)
 * - Nivel 5: Depth-based color (color según profundidad)
 * - Nivel 6: Olas Gerstner (superficie viva)
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface RealisticWaterProps {
  position?: [number, number, number]
  size?: number
  color?: string
}

export default function RealisticWater({ 
  position = [0, -0.5, 0], 
  size = 150,
  color = '#1e3a5f'
}: RealisticWaterProps) {
  const waterRef = useRef<THREE.Mesh>(null)
  
  // Shader de agua realista con Fresnel, Reflection y Refraction
  const waterShader = useMemo(() => ({
    uniforms: {
      time: { value: 0 },
      deepWaterColor: { value: new THREE.Color(color) },
      waveAmplitude: { value: 0.15 },
      waveFrequency: { value: 0.3 },
      waveSpeed: { value: 0.3 }
    },
    vertexShader: `
      uniform float time;
      uniform float waveAmplitude;
      uniform float waveFrequency;
      uniform float waveSpeed;
      
      // Gerstner Waves para olas realistas
      vec3 gerstnerWave(vec3 pos, float time) {
        float k = 2.0 * 3.14159 * waveFrequency;
        float c = sqrt(9.8 / k);
        vec2 d = normalize(vec2(1.0, 0.5));
        float f = k * (dot(d, pos.xz) - c * time * waveSpeed);
        float a = waveAmplitude / k;
        
        return vec3(
          d.x * a * cos(f),
          a * sin(f),
          d.y * a * cos(f)
        );
      }
      
      void main() {
        // Aplicar múltiples olas Gerstner
        vec3 pos = position;
        vec3 wave1 = gerstnerWave(pos, time);
        vec3 wave2 = gerstnerWave(pos * 1.3 + vec3(10.0, 0.0, 10.0), time * 1.1);
        vec3 wave3 = gerstnerWave(pos * 0.7 + vec3(-5.0, 0.0, 5.0), time * 0.9);
        
        pos += wave1 + wave2 * 0.5 + wave3 * 0.3;
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 deepWaterColor;
      
      void main() {
        // Color COMPLETAMENTE uniforme sin ninguna variación
        gl_FragColor = vec4(deepWaterColor, 0.9);
      }
    `
  }), [color])
  
  // Animación
  useFrame((state) => {
    if (waterRef.current) {
      const material = waterRef.current.material as THREE.ShaderMaterial
      material.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  return (
    <mesh 
      ref={waterRef} 
      position={position} 
      rotation={[-Math.PI / 2, 0, 0]} 
      receiveShadow
    >
      <planeGeometry args={[size, size, 64, 64]} />
      <shaderMaterial
        vertexShader={waterShader.vertexShader}
        fragmentShader={waterShader.fragmentShader}
        uniforms={waterShader.uniforms}
        transparent
        side={THREE.DoubleSide}
      />
    </mesh>
  )
}
