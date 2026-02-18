import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Shader de terreno con múltiples texturas y splatting
 */
export const terrainVertexShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  varying float vElevation;
  
  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    vPosition = position;
    vElevation = position.z;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`

export const terrainFragmentShader = `
  uniform sampler2D grassTexture;
  uniform sampler2D rockTexture;
  uniform sampler2D sandTexture;
  uniform sampler2D snowTexture;
  uniform float minElevation;
  uniform float maxElevation;
  uniform float time;
  
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  varying float vElevation;
  
  void main() {
    // Normalizar elevación
    float normalizedHeight = (vElevation - minElevation) / (maxElevation - minElevation);
    
    // Samplear texturas
    vec4 grass = texture2D(grassTexture, vUv * 10.0);
    vec4 rock = texture2D(rockTexture, vUv * 10.0);
    vec4 sand = texture2D(sandTexture, vUv * 10.0);
    vec4 snow = texture2D(snowTexture, vUv * 10.0);
    
    // Mezclar texturas basado en altura
    vec4 color = sand;
    
    if (normalizedHeight > 0.2) {
      float blend = smoothstep(0.2, 0.3, normalizedHeight);
      color = mix(sand, grass, blend);
    }
    
    if (normalizedHeight > 0.5) {
      float blend = smoothstep(0.5, 0.6, normalizedHeight);
      color = mix(grass, rock, blend);
    }
    
    if (normalizedHeight > 0.8) {
      float blend = smoothstep(0.8, 0.9, normalizedHeight);
      color = mix(rock, snow, blend);
    }
    
    // Iluminación basada en normal
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float diffuse = max(dot(vNormal, lightDir), 0.0);
    
    // Aplicar iluminación
    color.rgb *= (0.5 + diffuse * 0.5);
    
    gl_FragColor = color;
  }
`

interface TerrainShaderMaterialProps {
  grassTexture?: THREE.Texture
  rockTexture?: THREE.Texture
  sandTexture?: THREE.Texture
  snowTexture?: THREE.Texture
  minElevation?: number
  maxElevation?: number
}

/**
 * Material de terreno con shader personalizado
 */
export function TerrainShaderMaterial({
  grassTexture,
  rockTexture,
  sandTexture,
  snowTexture,
  minElevation = 0,
  maxElevation = 100
}: TerrainShaderMaterialProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null)
  
  const uniforms = {
    grassTexture: { value: grassTexture },
    rockTexture: { value: rockTexture },
    sandTexture: { value: sandTexture },
    snowTexture: { value: snowTexture },
    minElevation: { value: minElevation },
    maxElevation: { value: maxElevation },
    time: { value: 0 }
  }
  
  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  return (
    <shaderMaterial
      ref={materialRef}
      vertexShader={terrainVertexShader}
      fragmentShader={terrainFragmentShader}
      uniforms={uniforms}
    />
  )
}

/**
 * Shader de agua realista
 */
export const waterVertexShader = `
  uniform float time;
  uniform float waveHeight;
  uniform float waveFrequency;
  
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  
  void main() {
    vUv = uv;
    vPosition = position;
    
    // Ondas procedurales
    vec3 pos = position;
    float wave1 = sin(pos.x * waveFrequency + time) * waveHeight;
    float wave2 = sin(pos.z * waveFrequency * 0.7 + time * 1.3) * waveHeight * 0.5;
    pos.y += wave1 + wave2;
    
    // Calcular normal para iluminación
    vec3 tangent = vec3(1.0, cos(pos.x * waveFrequency + time) * waveHeight * waveFrequency, 0.0);
    vec3 bitangent = vec3(0.0, cos(pos.z * waveFrequency * 0.7 + time * 1.3) * waveHeight * 0.5 * waveFrequency * 0.7, 1.0);
    vNormal = normalize(cross(tangent, bitangent));
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`

export const waterFragmentShader = `
  uniform vec3 waterColor;
  uniform vec3 foamColor;
  uniform float time;
  uniform float opacity;
  
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vPosition;
  
  void main() {
    // Iluminación
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float diffuse = max(dot(vNormal, lightDir), 0.0);
    
    // Especular (reflexión)
    vec3 viewDir = normalize(cameraPosition - vPosition);
    vec3 reflectDir = reflect(-lightDir, vNormal);
    float specular = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    
    // Espuma en crestas
    float foam = smoothstep(0.3, 0.5, vPosition.y);
    
    // Color final
    vec3 color = mix(waterColor, foamColor, foam);
    color += vec3(specular * 0.5);
    color *= (0.6 + diffuse * 0.4);
    
    gl_FragColor = vec4(color, opacity);
  }
`

interface WaterShaderMaterialProps {
  waterColor?: THREE.Color
  foamColor?: THREE.Color
  waveHeight?: number
  waveFrequency?: number
  opacity?: number
}

/**
 * Material de agua con shader personalizado
 */
export function WaterShaderMaterial({
  waterColor = new THREE.Color(0x0077be),
  foamColor = new THREE.Color(0xffffff),
  waveHeight = 0.5,
  waveFrequency = 0.5,
  opacity = 0.8
}: WaterShaderMaterialProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null)
  
  const uniforms = {
    waterColor: { value: waterColor },
    foamColor: { value: foamColor },
    waveHeight: { value: waveHeight },
    waveFrequency: { value: waveFrequency },
    opacity: { value: opacity },
    time: { value: 0 }
  }
  
  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  return (
    <shaderMaterial
      ref={materialRef}
      vertexShader={waterVertexShader}
      fragmentShader={waterFragmentShader}
      uniforms={uniforms}
      transparent
      side={THREE.DoubleSide}
    />
  )
}

/**
 * Shader de vegetación con animación de viento
 */
export const vegetationVertexShader = `
  uniform float time;
  uniform float windStrength;
  uniform vec3 windDirection;
  
  varying vec2 vUv;
  varying vec3 vNormal;
  
  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    
    vec3 pos = position;
    
    // Animación de viento (solo afecta la parte superior)
    float windEffect = pos.y * windStrength;
    pos.x += sin(time + pos.y * 2.0) * windEffect * windDirection.x;
    pos.z += cos(time + pos.y * 2.0) * windEffect * windDirection.z;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`

export const vegetationFragmentShader = `
  uniform sampler2D leafTexture;
  uniform vec3 baseColor;
  uniform float time;
  
  varying vec2 vUv;
  varying vec3 vNormal;
  
  void main() {
    vec4 texColor = texture2D(leafTexture, vUv);
    
    // Iluminación
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float diffuse = max(dot(vNormal, lightDir), 0.0);
    
    // Variación de color sutil
    vec3 color = baseColor * texColor.rgb;
    color *= (0.6 + diffuse * 0.4);
    
    // Subsurface scattering simulado
    float backlight = max(dot(vNormal, -lightDir), 0.0);
    color += vec3(0.1, 0.3, 0.1) * backlight * 0.3;
    
    gl_FragColor = vec4(color, texColor.a);
  }
`

interface VegetationShaderMaterialProps {
  leafTexture?: THREE.Texture
  baseColor?: THREE.Color
  windStrength?: number
  windDirection?: THREE.Vector3
}

/**
 * Material de vegetación con shader personalizado
 */
export function VegetationShaderMaterial({
  leafTexture,
  baseColor = new THREE.Color(0x2d5016),
  windStrength = 0.1,
  windDirection = new THREE.Vector3(1, 0, 0.5)
}: VegetationShaderMaterialProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null)
  
  const uniforms = {
    leafTexture: { value: leafTexture },
    baseColor: { value: baseColor },
    windStrength: { value: windStrength },
    windDirection: { value: windDirection },
    time: { value: 0 }
  }
  
  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  return (
    <shaderMaterial
      ref={materialRef}
      vertexShader={vegetationVertexShader}
      fragmentShader={vegetationFragmentShader}
      uniforms={uniforms}
      transparent
      side={THREE.DoubleSide}
    />
  )
}
