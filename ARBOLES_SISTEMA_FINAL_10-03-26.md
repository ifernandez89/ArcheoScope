# Sistema de Árboles Final - 10/03/2026

## Resumen
Implementación del sistema definitivo de árboles 3D con 3 modelos seleccionados, distribución aleatoria y corrección de bugs de renderizado.

## Cambios Realizados

### 1. Selección de Modelos de Árboles
- **Modelos finales seleccionados**: 3 árboles de la carpeta `models_3d/trees/`
  - `tree_new.glb` (new.glb) - Tipo 'default'
  - `tree_new2.glb` (new2.glb) - Tipo 'tree1'
  - `tree_new3.glb` (new3.glb) - Tipo 'tree2'
- **Modelos descartados**: tree_blender.glb y tree_new4.glb (problemas de orientación)
- **Ubicación**: `viewer3d/public/`

### 2. Distribución de Árboles por Bioma
- **Tropical**: 25 árboles
- **Templado**: 25 árboles
- **Altiplano** (Puma Punku): 20 árboles
- **Desierto**: 15 árboles
- **Ártico**: 20 árboles
- **Distribución equitativa**: 33% de cada tipo en todas las escenas

### 3. Características de los Árboles
- **Altura mínima**: 2.2m (mitad de Viracocha)
- **Altura máxima**: 5m (ligeramente superior a Viracocha 4.4m)
- **Escala**: 0.1 (ajustada para visibilidad óptima)
- **Rotación**: Aleatoria en eje Y
- **Posicionamiento**: Aleatorio respetando zonas de exclusión

### 4. Zonas de Exclusión Estrictas

#### Puma Punku
- Estructura principal: radio 25m en [8, -8]
- Viracocha: radio 15m en [13.634, 0.83]
- Puerta del Sol: radio 20m en [70, 60]
- Bloques dispersos: radio 8m cada uno (8 bloques)

#### Giza
- Gran Pirámide: radio 80m en [0, 0]
- Esfinge: radio 30m en [100, 50]
- Templo del Valle: radio 50m en [0, 0]

### 5. Corrección de Bugs de Renderizado

#### Problema: Parpadeo y cambio de tamaño
**Causa**: Clonación del modelo en cada render sin `useMemo`

**Solución aplicada en**:
- `Tree3DModel.tsx`: Clonación con `useMemo` + clonación de materiales
- `Rock3DModel.tsx`: Mismo fix aplicado a las rocas

```typescript
const clonedScene = useMemo(() => {
  const cloned = scene.clone(true)
  return cloned
}, [scene])
```

### 6. Configuración de Rotaciones por Modelo
- **tree_blender.glb**: `[Math.PI / 2, 0, 0]` (90° en X) - DESCARTADO
- **Nuevos modelos**: Sin rotación base hardcodeada (orientación correcta)

### 7. Tecla M para Menú
- **Funcionalidad**: Toggle (aparece/desaparece)
- **Implementación**: `setShowMenu(prev => !prev)`
- **Ubicación**: `Scene3D.tsx`

## Archivos Modificados

### Componentes
- `viewer3d/components/EnvironmentElements.tsx`
  - Sistema de distribución de árboles
  - Zonas de exclusión estrictas
  - Lógica de posicionamiento aleatorio
  
- `viewer3d/components/Tree3DModel.tsx`
  - Mapeo de modelos nuevos
  - Fix de clonación con useMemo
  - Clonación de materiales

- `viewer3d/components/Rock3DModel.tsx`
  - Fix de parpadeo con useMemo
  - Clonación de materiales

- `viewer3d/components/Scene3D.tsx`
  - Tecla M reactivada como toggle

### Modelos
- `viewer3d/public/tree_new.glb`
- `viewer3d/public/tree_new2.glb`
- `viewer3d/public/tree_new3.glb`

## Resultados

✅ Sistema de árboles estable sin parpadeo
✅ Distribución equitativa de 3 tipos de árboles
✅ 20-30 árboles por escena (según bioma)
✅ Respeto estricto de zonas de exclusión
✅ Altura controlada (no excede a Viracocha)
✅ Rocas sin parpadeo
✅ Menú con tecla M funcional

## Próximos Pasos
- Implementar sistema especial para junglas/bosques densos
- Considerar LOD para optimización en escenas con muchos árboles
- Evaluar texturas adicionales para variedad visual
