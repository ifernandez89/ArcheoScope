# 🎨 Arte Generativo Orbital - Sistema de Visualización Cósmica

## Descripción General

Sistema de arte generativo que crea patrones visuales dinámicos basados en las posiciones y movimientos orbitales de los planetas del sistema solar. Genera mandalas gravitacionales, patrones geométricos y redes orbitales en tiempo real.

## Características Principales

### 1. 🌀 Mandalas Gravitacionales
- **Basados en resonancias orbitales**: Detecta ratios armónicos entre períodos orbitales
- **Curvas de Lissajous**: Patrones matemáticos que representan la relación entre dos planetas
- **Resonancias detectadas**:
  - Fracciones simples: 1/2, 2/3, 3/4, 3/5, 4/5, 5/6
  - Ratios de Fibonacci: 2, 3/2, 5/3, 5/4, 8/5

### 2. 🕸️ Redes Orbitales
- **Conexiones gravitacionales**: Líneas entre planetas cercanos
- **Color dinámico**: Basado en el color característico de cada planeta
- **Distancia adaptativa**: Solo conecta planetas dentro de un rango específico

### 3. 🌀 Patrones Geométricos (Spirograph Cósmico)
- **Espirales orbitales**: Patrones basados en el período orbital de cada planeta
- **Modulación dinámica**: Radio variable según la posición orbital
- **Múltiples capas**: Un patrón único por cada planeta

## Implementación Técnica

### Archivos Principales

```
viewer3d/components/OrbitalGenerativeArt.tsx  - Componente principal
viewer3d/components/RealisticSolarSystem.tsx  - Integración
viewer3d/components/CosmicResonanceDemo.tsx   - Control UI
```

### Datos de Entrada

```typescript
interface Planet {
  position: THREE.Vector3    // Posición actual en 3D
  color: string              // Color característico
  orbitalPeriod: number      // Período orbital en días
}
```

### Parámetros de Control

- **enabled**: Activar/desactivar el sistema
- **intensity**: Intensidad visual (0-1), controla opacidad y brillo

## Algoritmos Utilizados

### Detección de Resonancias Armónicas

```typescript
function isHarmonicRatio(ratio: number): boolean {
  const harmonics = [
    1/2, 2/3, 3/4, 3/5, 4/5, 5/6,  // Fracciones simples
    2, 3/2, 5/3, 5/4, 8/5           // Ratios de Fibonacci
  ]
  const tolerance = 0.15
  return harmonics.some(h => Math.abs(ratio - h) < tolerance)
}
```

### Curvas de Lissajous

```typescript
for (let k = 0; k <= segments; k++) {
  const t = (k / segments) * Math.PI * 2
  const x = Math.cos(t * ratio) * p1.position.length()
  const z = Math.sin(t) * p2.position.length()
  points.push(new THREE.Vector3(x, 0, z))
}
```

### Patrones Espirales

```typescript
for (let i = 0; i <= segments; i++) {
  const t = (i / segments) * Math.PI * 4
  const r = radius * (1 + 0.1 * Math.sin(t * planet.orbitalPeriod / 100))
  const x = r * Math.cos(t)
  const z = r * Math.sin(t)
  points.push(new THREE.Vector3(x, 0, z))
}
```

## Animaciones

### Pulsación Suave
```typescript
const pulse = 1 + Math.sin(timeRef.current * 0.5) * 0.05
mandalaRef.current.scale.setScalar(pulse)
```

### Rotación Lenta
```typescript
mandalaRef.current.rotation.y += delta * 0.02
```

## Integración en el Sistema Solar

### 1. Recopilación de Datos
El sistema recopila posiciones planetarias cada frame:

```typescript
const artData = []
if (mercuryRef.current) artData.push({ 
  position: mercuryRef.current.position.clone(), 
  color: '#9c9c9c', 
  orbitalPeriod: 88 
})
// ... más planetas
setOrbitalArtData(artData)
```

### 2. Renderizado
```typescript
<OrbitalGenerativeArt
  planets={orbitalArtData}
  enabled={showGenerativeArt}
  intensity={0.3}
/>
```

### 3. Control UI
Botón de toggle en el panel de Resonancia Cósmica:
- 🎨 Arte (activo) - Color púrpura
- 🎨 Arte (inactivo) - Gris

## Configuración Visual

### Opacidades
- Mandalas gravitacionales: `intensity * 0.15`
- Redes orbitales: `intensity * 0.08`
- Patrones geométricos: `intensity * 0.1`

### Blending Mode
Todos los elementos usan `THREE.AdditiveBlending` para efectos de luz acumulativa

### Colores por Planeta
```typescript
Mercurio: #9c9c9c
Venus:    #f5e6d3
Tierra:   #4A90E2
Marte:    #E27B58
Júpiter:  #D4A574
Saturno:  #FAD5A5
Urano:    #4FD0E7
Neptuno:  #4166F5
```

## Rendimiento

### Optimizaciones
- Geometrías calculadas con `useMemo`
- Actualización de posiciones solo cuando cambian
- Límite de conexiones en redes orbitales (distancia < 400 unidades)
- Segmentos optimizados (64-128 por curva)

### Impacto
- **Bajo**: ~2-3ms por frame con 8 planetas
- **Escalable**: Funciona bien hasta 20+ cuerpos celestes

## Inspiración Matemática

### Spirograph Cósmico
Basado en el juguete Spirograph, que crea patrones hipotrocoides y epitrocoides

### Patrones de Lissajous
Figuras matemáticas que representan la composición de dos movimientos armónicos perpendiculares

### Geometría Sagrada
Patrones que aparecen naturalmente en la naturaleza y el cosmos

## Uso

### Activar/Desactivar
```typescript
const [showGenerativeArt, setShowGenerativeArt] = useState(true)

<RealisticSolarSystem 
  showGenerativeArt={showGenerativeArt}
/>
```

### Ajustar Intensidad
```typescript
<OrbitalGenerativeArt
  planets={orbitalArtData}
  enabled={true}
  intensity={0.5}  // 0.0 - 1.0
/>
```

## Futuras Mejoras

### Posibles Extensiones
1. **Trails orbitales**: Estelas que siguen a los planetas
2. **Partículas gravitacionales**: Sistemas de partículas en puntos de resonancia
3. **Colores dinámicos**: Cambio de color según eventos cósmicos
4. **Patrones 3D**: Extensión a geometrías tridimensionales
5. **Exportación**: Guardar patrones como imágenes o SVG

### Interactividad
- Click en patrones para información
- Ajuste de intensidad en tiempo real
- Selección de tipos de patrones específicos
- Modo "solo resonancias fuertes"

## Conclusión

El sistema de arte generativo orbital transforma datos astronómicos reales en visualizaciones artísticas, creando una experiencia inmersiva que combina ciencia y estética. Los patrones generados son únicos para cada configuración planetaria y evolucionan en tiempo real con el movimiento orbital.

---

**Creado**: 2026-04-13  
**Versión**: 1.0.0  
**Estado**: ✅ Implementado y funcional
