'use client'

import { useRef, useMemo, forwardRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { detectBiome } from '@/utils/biome-detector'

interface VolcanicTerrainProps {
  location?: { lat: number, lon: number } | null
}

const VolcanicTerrain = forwardRef<THREE.Mesh, VolcanicTerrainProps>(
  function VolcanicTerrain({ location }, ref) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  // Usar ref externo si se proporciona, sino usar interno
  const actualRef = (ref as React.RefObject<THREE.Mesh>) || meshRef
  
  // Detectar si las coordenadas están en océano usando detectBiome
  const isInOcean = useMemo(() => {
    if (!location) return false
    const biome = detectBiome(location.lat, location.lon)
    console.log('VolcanicTerrain - Location:', location, 'Biome:', biome.type, 'isInOcean:', biome.type === 'ocean')
    return biome.type === 'ocean'
  }, [location])
  
  // Generar geometría con relieve procedural basado en coordenadas
  const geometry = useMemo(() => {
    // Terreno más grande para altiplano (Lago Titicaca es enorme)
    const isAltiplano = location && 
      Math.abs(location.lat) > 15.5 && Math.abs(location.lat) < 16.5 && 
      location.lon > -70 && location.lon < -68.5
    
    const terrainSize = isAltiplano ? 400 : 200 // Doble de grande para altiplano
    const geo = new THREE.PlaneGeometry(terrainSize, terrainSize, 100, 100)
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
      
      // Altiplano - relieve quebrado y erosionado con MONTAÑAS MUY ALTAS
      if (absLat > 15.5 && absLat < 16.5 && location.lon > -70 && location.lon < -68.5) {
        amplitudeFactor = 22.0  // Montañas el doble de altas (era 11.0)
        roughnessFactor = 16.0  // Muy rugoso, erosionado (era 8.0)
      }
      // Terreno más montañoso cerca de zonas volcánicas conocidas
      else if ((absLat > 10 && absLat < 30) || (absLat > 60)) {
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
      const baseNoise = 
        noise(x, y, 0.02, seed * 0.01) * 1.5 * amplitudeFactor +      // Ondulaciones grandes
        noise(x, y, 0.05, seed * 0.02) * 0.8 * amplitudeFactor        // Colinas medianas
      
      const ridgeNoise = 
        noise(x, y, 0.1, seed * 0.03) * 0.4 * roughnessFactor +       // Detalles pequeños
        noise(x, y, 0.2, seed * 0.04) * 0.2 * roughnessFactor +       // Micro-relieve
        noise(x, y, 0.35, seed * 0.05) * 0.15 * roughnessFactor       // Alta frecuencia (erosión)
      
      // Mezcla más dramática para altiplano: 50% base + 50% relieve quebrado
      const isAltiplanoTerrain = location && 
        Math.abs(location.lat) > 15.5 && Math.abs(location.lat) < 16.5 && 
        location.lon > -70 && location.lon < -68.5
      
      const height = isAltiplanoTerrain 
        ? baseNoise * 0.5 + ridgeNoise * 0.5  // Más quebrado para altiplano
        : baseNoise * 0.6 + ridgeNoise * 0.4  // Normal para otros terrenos
      
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
      
      // Altiplano - Lago Titicaca (PRIORIDAD MÁXIMA)
      if (absLat > 15.5 && absLat < 16.5 && location.lon > -70 && location.lon < -68.5) {
        baseColorType = 'altiplano'
      }
      // Isla de Pascua - tierra rojiza volcánica
      else if (absLat > 25 && absLat < 30 && location.lon < -100 && location.lon > -115) {
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
        
        if (colorType == 0) { // volcanic - MÁS VERDE
          darkColor = vec3(0.15, 0.25, 0.12);   // Verde oscuro
          mediumColor = vec3(0.25, 0.40, 0.20);  // Verde medio
          lightColor = vec3(0.35, 0.50, 0.28);   // Verde claro
          depthColor = vec3(0.10, 0.18, 0.08);   // Verde muy oscuro
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
        } else if (colorType == 3) { // tropical - MÁS VERDE VIBRANTE
          darkColor = vec3(0.12, 0.30, 0.15);    // Verde bosque oscuro
          mediumColor = vec3(0.20, 0.45, 0.22);  // Verde bosque medio
          lightColor = vec3(0.30, 0.55, 0.30);   // Verde bosque claro
          depthColor = vec3(0.08, 0.22, 0.10);   // Verde muy oscuro
        } else if (colorType == 5) { // altiplano - OCRE SECO
          darkColor = vec3(0.56, 0.54, 0.32);    // #8f8a52 - Verde oliva seco
          mediumColor = vec3(0.75, 0.66, 0.42);  // #bfa76a - Ocre claro
          lightColor = vec3(0.79, 0.69, 0.48);   // #c9b07a - Beige altiplano
          depthColor = vec3(0.63, 0.55, 0.36);   // #a18d5c - Marrón tierra
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
    else if (baseColorType === 'altiplano') colorTypeInt = 5
    
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
