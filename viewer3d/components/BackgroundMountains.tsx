'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

interface BackgroundMountainsProps {
  biomeType?: string
}

export default function BackgroundMountains({ biomeType }: BackgroundMountainsProps) {
  // Solo renderizar para altiplano
  if (biomeType !== 'altiplano') return null

  const mountainGeometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(2000, 400, 200, 50)
    const positions = geo.attributes.position.array as Float32Array

    // Generar silueta de montañas
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const y = positions[i + 1]

      // Múltiples picos con diferentes alturas
      const peak1 = Math.sin(x * 0.003) * 150
      const peak2 = Math.sin(x * 0.007 + 2) * 100
      const peak3 = Math.sin(x * 0.012 + 5) * 80
      const peak4 = Math.sin(x * 0.02 + 8) * 50

      // Combinar picos
      const height = peak1 + peak2 + peak3 + peak4

      // Solo afectar la parte superior (y > 0)
      if (y > 0) {
        positions[i + 2] = height * (y / 200) // Gradiente de altura
      }
    }

    geo.attributes.position.needsUpdate = true
    geo.computeVertexNormals()

    return geo
  }, [])

  const mountainMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: `
        varying vec3 vPosition;
        varying vec3 vNormal;
        varying float vHeight;
        
        void main() {
          vPosition = position;
          vNormal = normal;
          vHeight = position.z;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vPosition;
        varying vec3 vNormal;
        varying float vHeight;
        
        void main() {
          // Colores de montaña andina
          vec3 baseColor = vec3(0.45, 0.42, 0.35); // Marrón montaña
          vec3 peakColor = vec3(0.65, 0.62, 0.55); // Picos más claros
          vec3 shadowColor = vec3(0.25, 0.23, 0.20); // Sombras oscuras
          
          // Gradiente por altura
          float heightFactor = clamp(vHeight / 150.0, 0.0, 1.0);
          vec3 color = mix(baseColor, peakColor, heightFactor);
          
          // Iluminación simple
          vec3 lightDir = normalize(vec3(1.0, 1.0, 0.5));
          float diffuse = max(dot(vNormal, lightDir), 0.0);
          
          // Aplicar sombras en laderas
          color = mix(shadowColor, color, 0.4 + diffuse * 0.6);
          
          // Fade con distancia (perspectiva atmosférica)
          float fade = 1.0 - clamp(vPosition.y / 200.0, 0.0, 1.0);
          vec3 skyColor = vec3(0.29, 0.48, 0.72); // #4a7bb7
          color = mix(skyColor, color, fade * 0.7);
          
          gl_FragColor = vec4(color, fade * 0.8);
        }
      `,
      transparent: true,
      side: THREE.DoubleSide,
      depthWrite: false
    })
  }, [])

  return (
    <group>
      {/* Cordillera norte */}
      <mesh
        geometry={mountainGeometry}
        material={mountainMaterial}
        position={[0, 50, -800]}
        rotation={[0, 0, 0]}
      />
      
      {/* Cordillera sur */}
      <mesh
        geometry={mountainGeometry}
        material={mountainMaterial}
        position={[0, 50, 800]}
        rotation={[0, Math.PI, 0]}
      />
      
      {/* Cordillera este */}
      <mesh
        geometry={mountainGeometry}
        material={mountainMaterial}
        position={[800, 50, 0]}
        rotation={[0, Math.PI / 2, 0]}
      />
      
      {/* Cordillera oeste */}
      <mesh
        geometry={mountainGeometry}
        material={mountainMaterial}
        position={[-800, 50, 0]}
        rotation={[0, -Math.PI / 2, 0]}
      />
    </group>
  )
}
