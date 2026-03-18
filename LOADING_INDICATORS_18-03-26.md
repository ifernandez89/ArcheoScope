# Indicadores de Carga para Sitios Arqueológicos
**Fecha**: 18 de marzo de 2026

## Cambios Realizados

### 1. Indicadores de Carga Agregados

Se implementaron indicadores de "Cargando..." con `Suspense` para los 4 sitios arqueológicos oficiales:

#### ✅ Giza (ya existía)
- Emoji: 🏜️
- Mensaje: "Cargando Giza..."
- Modelos: Gran Pirámide, Esfinge, Templo del Valle, etc.

#### ✅ Puma Punku (agregado)
- Emoji: 🗿
- Mensaje: "Cargando Puma Punku..."
- Modelos: Bloques megalíticos, estructura, Viracocha, Puerta del Sol

#### ✅ Teotihuacán (agregado)
- Emoji: 🏛️
- Mensaje: "Cargando Teotihuacán..."
- Modelos: Kukulkán, Templo Mayor, Calendario Maya, Quetzalcoatl

#### ✅ Isla de Pascua (agregado)
- Emoji: 🗿
- Mensaje: "Cargando Isla de Pascua..."
- Modelos: Moai, Atlante

### 2. Implementación Técnica

Cada escena ahora usa el patrón `Suspense` de React:

```tsx
export default function SitioScene({ props }) {
  return (
    <Suspense fallback={<LoadingSitio />}>
      <SitioSceneContent {...props} />
    </Suspense>
  )
}

function LoadingSitio() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(0, 0, 0, 0.8)',
        padding: '20px 40px',
        borderRadius: '12px',
        color: 'white',
        fontFamily: 'system-ui, sans-serif',
        textAlign: 'center',
        border: '2px solid rgba(255, 215, 0, 0.3)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🏛️</div>
        <div>Cargando Sitio...</div>
      </div>
    </Html>
  )
}
```

### 3. Beneficios

✅ **Mejor UX**: El usuario ve un indicador visual mientras cargan los modelos 3D pesados
✅ **Feedback inmediato**: Especialmente útil en GitHub Pages donde la carga puede ser más lenta
✅ **Consistencia**: Todos los sitios oficiales tienen el mismo patrón de carga
✅ **No bloquea**: React Suspense permite que el resto de la UI siga funcionando

### 4. Archivos Modificados

1. `viewer3d/components/TeotihuacanScene.tsx`
   - Agregado `Suspense` wrapper
   - Agregado componente `LoadingTeotihuacan`
   - Separado contenido en `TeotihuacanSceneContent`

2. `viewer3d/components/PumaPunkuScene.tsx`
   - Agregado `Suspense` wrapper
   - Agregado componente `LoadingPumaPunku`
   - Separado contenido en `PumaPunkuSceneContent`

3. `viewer3d/components/EasterIslandScene.tsx`
   - Agregado `Suspense` wrapper
   - Agregado componente `LoadingEasterIsland`
   - Separado contenido en `EasterIslandSceneContent`

4. `viewer3d/components/GizaScene.tsx`
   - Ya tenía implementación de `Suspense` (no modificado)

## Verificación

✅ Build exitoso sin errores
✅ Diagnósticos: sin problemas de TypeScript
✅ Todos los sitios arqueológicos tienen indicadores de carga

## Sitios Cubiertos

| Sitio | Coordenadas | Emoji | Estado |
|-------|-------------|-------|--------|
| Giza | 29.9792°N, 31.1342°E | 🏜️ | ✅ Ya existía |
| Puma Punku | -16.5596°S, -68.6788°W | 🗿 | ✅ Agregado |
| Teotihuacán | 19.6925°N, -98.8438°W | 🏛️ | ✅ Agregado |
| Isla de Pascua | -27.1254°S, -109.2778°W | 🗿 | ✅ Agregado |

## Notas

- Veracruz (18.4667°N, -95.4500°W) está en la lista de coordenadas pero no tiene escena específica
- Los indicadores usan el mismo estilo visual para mantener consistencia
- El tiempo de carga varía según la conexión y el tamaño de los modelos
