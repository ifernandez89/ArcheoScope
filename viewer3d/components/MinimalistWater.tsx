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
      fresnelColor: { value: new THREE.Color('#87ceeb') }
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
      uniform vec3 fresnelColor;
      uniform float time;
      
      varying vec3 vNormal;
      varying vec3 vPosition;
      varying vec2 vUv;
      
      void main() {
        // Fresnel effect
        vec3 viewDirection = normalize(vPosition);
        float fresnel = pow(1.0 - abs(dot(viewDirection, vNormal)), 3.0);
        
        // Animated ripples
        float ripple = sin(vUv.x * 20.0 + time) * sin(vUv.y * 20.0 + time) * 0.5 + 0.5;
        ripple *= 0.1;
        
        // Mix water color with fresnel
        vec3 color = mix(waterColor, fresnelColor, fresnel * 0.6);
        color += ripple * 0.1;
        
        gl_FragColor = vec4(color, 0.85);
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
