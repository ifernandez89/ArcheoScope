'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface PhysicalSkyProps {
  sunPosition: THREE.Vector3
  turbidity?: number
  rayleigh?: number
  mieCoefficient?: number
  mieDirectionalG?: number
  elevation?: number
  azimuth?: number
}

export default function PhysicalSky({
  sunPosition,
  turbidity = 2,
  rayleigh = 1,
  mieCoefficient = 0.005,
  mieDirectionalG = 0.8,
  elevation = 2,
  azimuth = 180
}: PhysicalSkyProps) {
  const skyRef = useRef<THREE.Mesh>(null)

  // Shader del cielo físico (simplificado de Three.js Sky)
  const skyShader = useMemo(() => ({
    uniforms: {
      turbidity: { value: turbidity },
      rayleigh: { value: rayleigh },
      mieCoefficient: { value: mieCoefficient },
      mieDirectionalG: { value: mieDirectionalG },
      sunPosition: { value: sunPosition },
      up: { value: new THREE.Vector3(0, 1, 0) }
    },
    vertexShader: `
      varying vec3 vWorldPosition;
      
      void main() {
        vec4 worldPosition = modelMatrix * vec4(position, 1.0);
        vWorldPosition = worldPosition.xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform float turbidity;
      uniform float rayleigh;
      uniform float mieCoefficient;
      uniform float mieDirectionalG;
      uniform vec3 sunPosition;
      uniform vec3 up;
      
      varying vec3 vWorldPosition;
      
      const float e = 2.71828182845904523536028747135266249775724709369995957;
      const float pi = 3.141592653589793238462643383279502884197169;
      
      // Atmospheric scattering
      vec3 totalRayleigh(vec3 lambda) {
        return (8.0 * pow(pi, 3.0) * pow(pow(1.0003, 2.0) - 1.0, 2.0) * (6.0 + 3.0 * 0.035)) / (3.0 * 2.545E25 * pow(lambda, vec3(4.0)) * (6.0 - 7.0 * 0.035));
      }
      
      float rayleighPhase(float cosTheta) {
        return (3.0 / (16.0 * pi)) * (1.0 + pow(cosTheta, 2.0));
      }
      
      vec3 totalMie(vec3 lambda, vec3 K, float T) {
        float c = (0.2 * T) * 10E-18;
        return 0.434 * c * pi * pow((2.0 * pi) / lambda, vec3(0.0)) * K;
      }
      
      float hgPhase(float cosTheta, float g) {
        return (1.0 / (4.0 * pi)) * ((1.0 - pow(g, 2.0)) / pow(1.0 - 2.0 * g * cosTheta + pow(g, 2.0), 1.5));
      }
      
      float sunIntensity(float zenithAngleCos) {
        zenithAngleCos = clamp(zenithAngleCos, -1.0, 1.0);
        return 1000.0 * max(0.0, 1.0 - pow(e, -((0.008 / (pow(zenithAngleCos, 0.253) + 0.00516 * 0.008)) * 0.008)));
      }
      
      vec3 Uncharted2Tonemap(vec3 x) {
        float A = 0.15;
        float B = 0.50;
        float C = 0.10;
        float D = 0.20;
        float E = 0.02;
        float F = 0.30;
        return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F;
      }
      
      void main() {
        vec3 direction = normalize(vWorldPosition);
        
        // Optical length
        float zenithAngle = acos(max(0.0, dot(up, direction)));
        float inverse = 1.0 / (cos(zenithAngle) + 0.15 * pow(93.885 - ((zenithAngle * 180.0) / pi), -1.253));
        float sR = 8.4E3 * inverse;
        float sM = 1.25E3 * inverse;
        
        // Combined extinction factor
        vec3 Fex = exp(-(totalRayleigh(vec3(680E-9, 550E-9, 450E-9)) * sR + totalMie(vec3(680E-9, 550E-9, 450E-9), vec3(0.686, 0.678, 0.666), turbidity) * sM));
        
        // In-scattering
        float cosTheta = dot(direction, normalize(sunPosition));
        
        float rPhase = rayleighPhase(cosTheta * 0.5 + 0.5);
        vec3 betaRTheta = totalRayleigh(vec3(680E-9, 550E-9, 450E-9)) * rPhase;
        
        float mPhase = hgPhase(cosTheta, mieDirectionalG);
        vec3 betaMTheta = totalMie(vec3(680E-9, 550E-9, 450E-9), vec3(0.686, 0.678, 0.666), turbidity) * mPhase;
        
        vec3 Lin = pow(sunIntensity(dot(normalize(sunPosition), up)) * ((betaRTheta + betaMTheta) / (totalRayleigh(vec3(680E-9, 550E-9, 450E-9)) + totalMie(vec3(680E-9, 550E-9, 450E-9), vec3(0.686, 0.678, 0.666), turbidity))) * (1.0 - Fex), vec3(1.5));
        Lin *= mix(vec3(1.0), pow(sunIntensity(dot(normalize(sunPosition), up)) * ((betaRTheta + betaMTheta) / (totalRayleigh(vec3(680E-9, 550E-9, 450E-9)) + totalMie(vec3(680E-9, 550E-9, 450E-9), vec3(0.686, 0.678, 0.666), turbidity))) * Fex, vec3(1.0 / 2.0)), clamp(pow(1.0 - dot(up, normalize(sunPosition)), 5.0), 0.0, 1.0));
        
        // Night sky
        vec3 nightSky = vec3(0.0, 0.0, 0.0);
        vec3 L0 = vec3(0.1) * Fex;
        
        // Composition + solar disc
        float sundisk = smoothstep(0.03, 0.026, distance(direction, normalize(sunPosition)));
        L0 += (sunIntensity(dot(normalize(sunPosition), up)) * 19000.0 * Fex) * sundisk;
        
        vec3 texColor = (Lin + L0) * 0.04 + vec3(0.0, 0.0003, 0.00075);
        
        // Tonemap
        vec3 curr = Uncharted2Tonemap((log2(2.0 / pow(1.0, 4.0))) * texColor);
        vec3 color = curr * vec3(1.0, 1.0, 1.0);
        
        vec3 retColor = pow(color, vec3(1.0 / (1.2 + (1.2 * sundisk))));
        
        gl_FragColor = vec4(retColor, 1.0);
      }
    `
  }), [turbidity, rayleigh, mieCoefficient, mieDirectionalG, sunPosition])

  useFrame(() => {
    if (skyRef.current) {
      const material = skyRef.current.material as THREE.ShaderMaterial
      material.uniforms.sunPosition.value.copy(sunPosition)
    }
  })

  return (
    <mesh ref={skyRef} scale={[450000, 450000, 450000]}>
      <sphereGeometry args={[1, 32, 15]} />
      <shaderMaterial
        fragmentShader={skyShader.fragmentShader}
        vertexShader={skyShader.vertexShader}
        uniforms={skyShader.uniforms}
        side={THREE.BackSide}
        depthWrite={false}
      />
    </mesh>
  )
}
