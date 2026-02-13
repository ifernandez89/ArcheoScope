'use client'

import { useRef, useMemo, forwardRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface VolcanicTerrainProps {
  location?: { lat: number, lon: number } | null
}

const VolcanicTerrain = forwardRef<THREE.Mesh, VolcanicTerrainProps>(
  function VolcanicTerrain({ location }, ref) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  // Usar ref externo si se proporciona, sino usar interno
  const actualRef = (ref as React.RefObject<THREE.Mesh>) || meshRef
  
  // Detectar si las coordenadas están en océano abierto
  const isInOcean = useMemo(() => {
    if (!location) return false
    
    const { lat, lon } = location
    
    // Océano Pacífico - la mayor parte del planeta
    // Longitud entre -180 y -70 (excluyendo costas de América)
    if (lon < -70) {
      // Excluir costa oeste de América del Norte (lat > 30, lon > -130)
      if (lat > 30 && lon > -130) return false
      
      // Excluir costa oeste de América del Sur (lat < -10, lon > -85)
      if (lat < -10 && lon > -85) return false
      
      // Excluir costa de Chile (lat < -15, lon > -75)
      if (lat < -15 && lon > -75) return false
      
      // Excluir Alaska (lat > 50, lon > -170)
      if (lat > 50 && lon > -170) return false
      
      // Todo lo demás en esta longitud es océano Pacífico
      return true
    }
    
    // Océano Pacífico occidental (Asia-Oceanía)
    // Longitud entre 100 y 180
    if (lon > 100) {
      // Excluir Australia (lat < -10, lon < 155)
      if (lat < -10 && lat > -45 && lon < 155) return false
      
      // Excluir Asia (lat > 0, lon < 140)
      if (lat > 0 && lon < 140) return false
      
      // Todo lo demás es océano
      return true
    }
    
    // Océano Atlántico central
    if (lon > -50 && lon < -10) {
      // Excluir costas de África y América del Sur
      if (Math.abs(lat) > 40) return false
      if (lat > 10 && lon > -30) return false // África
      if (lat < -5 && lon < -30) return false // Brasil
      return true
    }
    
    // Océano Índico
    if (lon > 40 && lon < 100) {
      // Excluir África (lon < 55, lat > -35)
      if (lon < 55 && lat > -35) return false
      // Excluir India (lat > 5, lon < 80)
      if (lat > 5 && lon < 80) return false
      return true
    }
    
    return false
  }, [location])
  
  // Generar geometría con relieve procedural basado en coordenadas
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(200, 200, 100, 100)
    const positions = geo.attributes.position.array as Float32Array
    
    // Usar coordenadas como semilla para variación
    const seed = location ? (location.lat * 1000 + location.lon * 1000) : 0
    
    // Función de ruido Perlin simplificado con semilla
    const noise = (x: number, y: number, scale: number, offset: number) => {
      return Math.sin((x + offset) * scale) * Math.cos((y + offset) * scale)
    }
    
    // Determinar tipo de terreno según latitud
    let amplitudeFactor = 1.5  // Aumentado de 1.0 a 1.5 (más relieve por defecto)
    let roughnessFactor = 1.2  // Aumentado de 1.0 a 1.2 (más rugoso por defecto)
    
    if (location) {
      const absLat = Math.abs(location.lat)
      
      // Terreno más montañoso cerca de zonas volcánicas conocidas
      if ((absLat > 10 && absLat < 30) || (absLat > 60)) {
        amplitudeFactor = 2.0  // Más montañoso
        roughnessFactor = 1.8
      } else if (absLat < 10) {
        amplitudeFactor = 1.2  // Más relieve que antes (era 0.6)
        roughnessFactor = 1.0
      }
      
      // Isla de Pascua - muy volcánico
      if (absLat > 25 && absLat < 30 && location.lon < -100 && location.lon > -115) {
        amplitudeFactor = 2.5
        roughnessFactor = 2.0
      }
      
      // Machu Picchu - montañoso
      if (absLat > 10 && absLat < 15 && location.lon < -70 && location.lon > -75) {
        amplitudeFactor = 3.0
        roughnessFactor = 2.5
      }
    }
    
    // Aplicar múltiples octavas de ruido para relieve natural
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const y = positions[i + 1]
      
      // Combinar diferentes frecuencias de ruido con semilla única
      const height = 
        noise(x, y, 0.02, seed * 0.01) * 1.5 * amplitudeFactor +      // Ondulaciones grandes
        noise(x, y, 0.05, seed * 0.02) * 0.8 * amplitudeFactor +      // Colinas medianas
        noise(x, y, 0.1, seed * 0.03) * 0.4 * roughnessFactor +       // Detalles pequeños
        noise(x, y, 0.2, seed * 0.04) * 0.2 * roughnessFactor         // Micro-relieve
      
      positions[i + 2] = height
    }
    
    geo.attributes.position.needsUpdate = true
    geo.computeVertexNormals()
    
    return geo
  }, [location?.lat, location?.lon])
  
  // Material volcánico con variación procedural de color según ubicación
  const material = useMemo(() => {
    // Determinar paleta de colores según ubicación
    let baseColorType = 'volcanic'
    
    if (location) {
      const absLat = Math.abs(location.lat)
      
      // Isla de Pascua - tierra rojiza volcánica
      if (absLat > 25 && absLat < 30 && location.lon < -100 && location.lon > -115) {
        baseColorType = 'volcanic-red'
      }
      // Machu Picchu - tierra andina
      else if (absLat > 10 && absLat < 15 && location.lon < -70 && location.lon > -75) {
        baseColorType = 'andean'
      }
      // Zonas tropicales - más verde
      else if (absLat < 10) {
        baseColorType = 'tropical'
      }
      // Zonas desérticas
      else if (absLat > 20 && absLat < 35) {
        baseColorType = 'desert'
      }
    }
    
    // Shader personalizado para variación de color por altura y ruido
    const vertexShader = `
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      void main() {
        vPosition = position;
        vNormal = normal;
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `
    
    const fragmentShader = `
      uniform float time;
      uniform int colorType;
      varying vec3 vPosition;
      varying vec3 vNormal;
      varying vec2 vUv;
      
      // Función de ruido simplificada
      float noise(vec2 p) {
        return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
      }
      
      void main() {
        // Paletas de colores según tipo de terreno
        vec3 darkColor, mediumColor, lightColor, depthColor;
        
        if (colorType == 0) { // volcanic
          darkColor = vec3(0.25, 0.15, 0.1);
          mediumColor = vec3(0.35, 0.25, 0.15);
          lightColor = vec3(0.45, 0.35, 0.25);
          depthColor = vec3(0.2, 0.12, 0.08);
        } else if (colorType == 1) { // volcanic-red (Isla de Pascua)
          darkColor = vec3(0.3, 0.12, 0.08);
          mediumColor = vec3(0.4, 0.2, 0.12);
          lightColor = vec3(0.5, 0.3, 0.2);
          depthColor = vec3(0.25, 0.1, 0.05);
        } else if (colorType == 2) { // andean (Machu Picchu)
          darkColor = vec3(0.2, 0.18, 0.12);
          mediumColor = vec3(0.3, 0.28, 0.2);
          lightColor = vec3(0.4, 0.38, 0.3);
          depthColor = vec3(0.15, 0.13, 0.08);
        } else if (colorType == 3) { // tropical
          darkColor = vec3(0.2, 0.25, 0.15);
          mediumColor = vec3(0.3, 0.35, 0.2);
          lightColor = vec3(0.4, 0.45, 0.3);
          depthColor = vec3(0.15, 0.2, 0.1);
        } else { // desert
          darkColor = vec3(0.35, 0.3, 0.2);
          mediumColor = vec3(0.45, 0.4, 0.3);
          lightColor = vec3(0.55, 0.5, 0.4);
          depthColor = vec3(0.3, 0.25, 0.15);
        }
        
        // Variación por altura
        float heightFactor = (vPosition.z + 3.0) / 6.0;
        heightFactor = clamp(heightFactor, 0.0, 1.0);
        
        // Ruido procedural para variación natural
        float n1 = noise(vUv * 50.0);
        float n2 = noise(vUv * 100.0);
        float n3 = noise(vUv * 200.0);
        float noiseValue = n1 * 0.5 + n2 * 0.3 + n3 * 0.2;
        
        // Mezclar colores según altura y ruido
        vec3 baseColor = mix(darkColor, mediumColor, heightFactor);
        baseColor = mix(baseColor, lightColor, noiseValue);
        
        // Zonas oscuras en depresiones (simulando sombras de contacto)
        float depression = smoothstep(-2.0, 0.5, vPosition.z);
        baseColor = mix(depthColor, baseColor, depression);
        
        // Iluminación básica usando normal
        vec3 lightDir = normalize(vec3(1.0, 1.0, 0.5));
        float diffuse = max(dot(vNormal, lightDir), 0.0);
        
        // Aplicar iluminación sutil
        vec3 finalColor = baseColor * (0.5 + diffuse * 0.5);
        
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `
    
    // Determinar tipo de color como entero
    let colorTypeInt = 0
    if (baseColorType === 'volcanic-red') colorTypeInt = 1
    else if (baseColorType === 'andean') colorTypeInt = 2
    else if (baseColorType === 'tropical') colorTypeInt = 3
    else if (baseColorType === 'desert') colorTypeInt = 4
    
    return new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: {
        time: { value: 0 },
        colorType: { value: colorTypeInt }
      }
    })
  }, [location?.lat, location?.lon])
  
  // Actualizar tiempo para animaciones sutiles si es necesario
  useFrame((state) => {
    if (material.uniforms) {
      material.uniforms.time.value = state.clock.elapsedTime
    }
  })
  
  // No renderizar terreno si está en océano abierto
  if (isInOcean) {
    return null
  }
  
  return (
    <mesh 
      ref={actualRef}
      geometry={geometry}
      material={material}
      rotation={[-Math.PI / 2, 0, 0]} 
      position={[0, 0, 0]} 
      receiveShadow
    />
  )
})

export default VolcanicTerrain
