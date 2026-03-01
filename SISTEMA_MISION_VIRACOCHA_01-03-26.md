# Sistema de Misión de Viracocha - 01/03/2026

## Resumen
Sistema completo de misión narrativa en Puma Punku con estado persistente, portal dimensional y recolección de items.

## Componentes Implementados

### 1. Portal Detector (`PortalDetector.tsx`)
- Detecta colisión entre la nave y la Puerta del Sol
- Radio de detección: 40 unidades (portalScale * 2)
- Cooldown de 5 segundos para evitar activaciones múltiples
- Teletransporta automáticamente al Lago Titicaca cuando se atraviesa

### 2. Sistema de Estado Persistente
Tres estados guardados en `sessionStorage`:

#### `puma_punku_block_moved`
- Se activa al mover cualquier bloque en Puma Punku
- Revela la estructura megalítica y a Viracocha
- Persiste entre cambios de ubicación

#### `viracocha_gate_revealed`
- Se activa al hacer click en Viracocha por primera vez
- Revela la Puerta del Sol con animación de fade-in (4 segundos)
- Persiste entre viajes

#### `item_magna_bowl_collected`
- Se activa al recoger la Magna Bowl en el Lago Titicaca
- Cambia el diálogo de Viracocha
- Persiste durante toda la sesión

### 3. Diálogo Dinámico de Viracocha
Dos mensajes según el estado de la misión:

**Sin Magna Bowl:**
```
"¡Atraviesa el portal, y tráeme lo que necesito!"
```

**Con Magna Bowl:**
```
"¡Gracias, viajero! Has traído lo que necesitaba."
```

### 4. Puerta del Sol
- Modelo: `puerta del sol front.glb`
- Posición: [70, 8, 60]
- Rotación: orientada hacia el este
- Escala: 20
- Aparece con fade-in de 4 segundos
- Copiada a `public/` y `out/` para GitHub Pages

### 5. Magna Bowl
- Modelo: `magna_bowl.glb`
- Ubicación: Lago Titicaca (-16.031003664299448, -69.49975772335767)
- Posición en escena: [0, 0.5, 0]
- Clickeable con outline verde
- Animación de desaparición al recogerla
- Copiada a `public/` y `out/` para GitHub Pages

## Flujo de la Misión

### Acto 1: Descubrimiento en Puma Punku
1. Usuario llega a Puma Punku
2. Mueve cualquier bloque → Estructura y Viracocha aparecen
3. Click en Viracocha → Pide que atravieses el portal
4. Puerta del Sol aparece lentamente

### Acto 2: Viaje al Lago Titicaca
1. Usuario atraviesa la Puerta del Sol con la nave
2. Teletransporte automático al Lago Titicaca
3. Magna Bowl visible en el centro del lago
4. Click en la bowl → Recolección con mensaje

### Acto 3: Regreso a Puma Punku
1. Usuario vuelve a Puma Punku (manualmente o por portal)
2. Estructura, Viracocha y puerta siguen visibles (estado persistente)
3. Click en Viracocha → Agradece por traer la Magna Bowl

## Archivos Modificados

### Nuevos Componentes
- `viewer3d/components/PortalDetector.tsx` - Detección de colisión con portal
- `viewer3d/components/SunGate.tsx` - Puerta del Sol con fade-in
- `viewer3d/components/DiscoveredItemInWorld.tsx` - Item recolectable en escena
- `viewer3d/components/ItemCollectedMessage.tsx` - Mensaje de recolección
- `viewer3d/components/ViracochaDialogue.tsx` - Diálogo místico

### Componentes Modificados
- `viewer3d/components/PumaPunkuScene.tsx` - Estado persistente de misión
- `viewer3d/components/ImmersiveScene.tsx` - Integración de sistema de misión
- `viewer3d/components/ObjectSelectionContext.tsx` - Estado persistente de blockMoved

### Modelos 3D Agregados
- `viewer3d/public/puerta del sol front.glb`
- `viewer3d/public/magna_bowl.glb`
- `viewer3d/out/puerta del sol front.glb`
- `viewer3d/out/magna_bowl.glb`

## Características Técnicas

### Persistencia de Estado
- Usa `sessionStorage` para mantener estado durante la sesión
- Se sincroniza automáticamente cada segundo
- No requiere backend ni base de datos

### Detección de Colisión
- Basada en distancia euclidiana 3D
- Considera posición y escala del portal
- Cooldown para evitar loops infinitos

### Animaciones
- Fade-in de 4 segundos para la Puerta del Sol
- Fade-out + escala up para items recolectados
- Diálogo flotante con desvanecimiento

### Integración con Sistema Existente
- Compatible con sistema de teletransporte
- Usa bioma detector para Lago Titicaca
- Integrado con sistema de items descubiertos

## Próximas Mejoras Sugeridas
- [ ] Agregar más items recolectables en otros sitios
- [ ] Sistema de inventario visual
- [ ] Más diálogos y misiones secundarias
- [ ] Efectos de partículas al atravesar portal
- [ ] Sonidos ambientales para cada evento
- [ ] Cinemáticas al completar misiones

## Notas de Desarrollo
- El estado persiste solo durante la sesión del navegador
- Para persistencia permanente, considerar localStorage o backend
- Los modelos GLB deben estar en `out/` para GitHub Pages
- El sistema es modular y fácil de extender con nuevas misiones
