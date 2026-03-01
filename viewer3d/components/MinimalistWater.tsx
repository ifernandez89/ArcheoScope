'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface MinimalistWaterProps {
  position?: [number, number, number]
  size?: number
  color?: string
}

export default function MinimalistWater({
  position = [0, -0.5, 0],
  size = 100,
  color = '#1e3a5f'
}: MinimalistWaterProps) {
  const waterRef = useRef<THREE.Mesh>(null)

  // Shader de agua con Fresnel y reflexión sutil
  const waterShader = {
    uniforms: {
      time: { value: 0 },
      waterColor: { value: new THREE.Color(color) },
      shallowColor: { value: new THREE.Color(color === '#2a5a8f' ? '#4a8abf' : '#2a5a8f') }, // Más claro para gradiente
      fresnelColor: { value: new THREE.Color('#87ceeb') },
      isAltiplano: { value: color === '#2a5a8f' ? 1.0 : 0.0 },
      lakeSize: { value: size }
    },
    vertexShader: `
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      uniform float time;
      
      // Simple wave function
      vec3 wave(vec3 pos) {
        float wave1 = sin(pos.x * 0.5 + time * 0.5) * 0.1;
        float wave2 = sin(pos.z * 0.3 + time * 0.3) * 0.08;
        return vec3(pos.x, pos.y + wave1 + wave2, pos.z);
      }
      
      void main() {
        vUv = uv;
        vNormal = normalize(normalMatrix * normal);
        
        // Apply waves
        vec3 pos = wave(position);
        vPosition = (modelViewMatrix * vec4(pos, 1.0)).xyz;
        
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform vec3 waterColor;
      uniform vec3 shallowColor;
      uniform vec3 fresnelColor;
      uniform float time;
      uniform float isAltiplano;
      uniform float lakeSize;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      
      // Función de ruido para distorsión orgánica
      float noise(vec2 p) {
        return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
      }
      
      void main() {
        // Forma de medialuna para Lago Titicaca (solo si isAltiplano)
        float alpha = 1.0;
        
        if (isAltiplano > 0.5) {
          // Coordenadas centradas (-1 a 1)
          vec2 centered = (vUv - 0.5) * 2.0;
          
          // Forma base elíptica (más ancho en vertical que horizontal)
          vec2 ellipse = centered;
          ellipse.x *= 1.3; // Comprimir horizontalmente para hacer más ancho verticalmente
          float dist = length(ellipse);
          
          // Crear forma de herradura/medialuna
          // Estrechar en el centro superior para crear la forma característica
          float narrowing = smoothstep(-0.3, 0.6, centered.y) * 0.35; // Estrechamiento en parte superior
          float horizontalCut = abs(centered.x) * narrowing;
          
          // Distorsión orgánica para bordes irregulares (penínsulas)
          float n1 = noise(vUv * 8.0 + time * 0.05);
          float n2 = noise(vUv * 15.0);
          float distortion = (n1 * 0.15 + n2 * 0.08);
          
          // Máscara del lago con forma irregular
          float lakeMask = smoothstep(0.88 + distortion, 0.72, dist + horizontalCut);
          
          alpha = lakeMask;
          
          // Descartar fragmentos fuera del lago
          if (alpha < 0.05) discard;
        }
        
        // Fresnel effect (más fuerte para altiplano)
        vec3 viewDirection = normalize(vPosition);
        float fresnelPower = mix(3.0, 2.2, isAltiplano); // Más fuerte en altiplano
        float fresnel = pow(1.0 - abs(dot(viewDirection, vNormal)), fresnelPower);
        
        // Gradiente de profundidad (del centro hacia afuera)
        float distFromCenter = length(vUv - 0.5) * 2.0; // 0 en centro, 1 en borde
        vec3 depthColor = mix(waterColor, shallowColor, distFromCenter * 0.6);
        
        // Animated ripples (más sutiles en altiplano)
        float rippleIntensity = mix(0.1, 0.05, isAltiplano);
        float ripple = sin(vUv.x * 20.0 + time) * sin(vUv.y * 20.0 + time) * 0.5 + 0.5;
        ripple *= rippleIntensity;
        
        // Mix depth color with fresnel (más intenso en altiplano)
        float fresnelMix = mix(0.6, 0.75, isAltiplano);
        vec3 color = mix(depthColor, fresnelColor, fresnel * fresnelMix);
        color += ripple * 0.1;
        
        // Transparencia ligeramente mayor en altiplano (agua más clara)
        float finalAlpha = mix(0.85, 0.88, isAltiplano) * alpha;
        
        gl_FragColor = vec4(color, finalAlpha);
      }
    `
  }

  useFrame((state) => {
    if (waterRef.current) {
      const material = waterRef.current.material as THREE.ShaderMaterial
      material.uniforms.time.value = state.clock.elapsedTime
    }
  })

  return (
    <mesh ref={waterRef} position={position} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[size, size, 32, 32]} />
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
