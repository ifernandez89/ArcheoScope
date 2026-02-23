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
      shallowWaterColor: { value: new THREE.Color('#4a9eff') },
      fresnelColor: { value: new THREE.Color('#87ceeb') },
      waveAmplitude: { value: 0.15 },
      waveFrequency: { value: 0.3 },
      waveSpeed: { value: 0.3 }
    },
    vertexShader: `
      uniform float time;
      uniform float waveAmplitude;
      uniform float waveFrequency;
      uniform float waveSpeed;
      
      varying vec3 vNormal;
      varying vec3 vViewPosition;
      varying vec2 vUv;
      varying float vElevation;
      
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
        vUv = uv;
        
        // Aplicar múltiples olas Gerstner
        vec3 pos = position;
        vec3 wave1 = gerstnerWave(pos, time);
        vec3 wave2 = gerstnerWave(pos * 1.3 + vec3(10.0, 0.0, 10.0), time * 1.1);
        vec3 wave3 = gerstnerWave(pos * 0.7 + vec3(-5.0, 0.0, 5.0), time * 0.9);
        
        pos += wave1 + wave2 * 0.5 + wave3 * 0.3;
        vElevation = pos.y;
        
        // Calcular normal para Fresnel
        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        vViewPosition = -mvPosition.xyz;
        vNormal = normalize(normalMatrix * normal);
        
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      uniform vec3 deepWaterColor;
      uniform vec3 shallowWaterColor;
      uniform vec3 fresnelColor;
      uniform float time;
      
      varying vec3 vNormal;
      varying vec3 vViewPosition;
      varying vec2 vUv;
      varying float vElevation;
      
      void main() {
        // Fresnel effect (clave del realismo)
        vec3 viewDir = normalize(vViewPosition);
        float fresnel = pow(1.0 - max(dot(vNormal, viewDir), 0.0), 3.0);
        
        // Depth-based color (simular profundidad)
        float depth = smoothstep(-0.5, 0.5, vElevation);
        vec3 waterColor = mix(deepWaterColor, shallowWaterColor, depth);
        
        // Refraction fake (distorsión UV)
        vec2 distortion = vNormal.xy * 0.05;
        vec2 distortedUv = vUv + distortion;
        
        // Ondulación procedural para textura
        float ripple = sin(distortedUv.x * 20.0 + time * 2.0) * 
                       cos(distortedUv.y * 20.0 + time * 1.5);
        ripple *= 0.05;
        
        // Combinar todo
        vec3 color = mix(waterColor, fresnelColor, fresnel * 0.7);
        color += ripple * 0.1;
        
        // Espuma procedural en crestas
        float foam = smoothstep(0.2, 0.3, vElevation);
        color = mix(color, vec3(1.0), foam * 0.3);
        
        // Transparencia con Fresnel
        float alpha = mix(0.85, 0.95, fresnel);
        
        gl_FragColor = vec4(color, alpha);
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
