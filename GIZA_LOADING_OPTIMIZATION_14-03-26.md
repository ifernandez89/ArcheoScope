# Optimización de carga de modelos 3D en Giza
**Fecha**: 14-03-26
**Problema**: Los modelos 3D en Giza tardaban demasiado en cargarse al entrar a las coordenadas

## Diagnóstico
Los modelos se estaban cargando de forma lazy (perezosa) DESPUÉS de que el componente se renderizaba, causando:
- Retraso visible de varios segundos
- Modelos apareciendo uno por uno
- Mala experiencia de usuario al entrar a Giza

## Solución implementada
Optimización de carga con preload anticipado y Suspense:

### 1. Preload anticipado al inicio del módulo
Movidos todos los `useGLTF.preload()` al INICIO del archivo (líneas 11-17):
```typescript
useGLTF.preload(getAssetPath('/sphinx_base.glb'))
useGLTF.preload(getAssetPath('/ramses2.glb'))
useGLTF.preload(getAssetPath('/hatshepsut.glb'))
useGLTF.preload(getAssetPath('/akenaton.glb'))
useGLTF.preload(getAssetPath('/momia.glb'))
useGLTF.preload(getAssetPath('/escab.glb'))
useGLTF.preload(getAssetPath('/piramidon.glb'))
```

### 2. Suspense boundary para loading state
Envuelto todo el contenido de GizaScene en `<Suspense>`:
- Muestra un loading placeholder mientras se cargan los modelos
- Placeholder con emoji 🏜️ y mensaje "Cargando Giza..."
- Estilo consistente con el resto de la UI

### 3. Eliminación de preloads duplicados
Eliminados los preloads duplicados que estaban dispersos en el archivo:
- Después de Sphinx (línea ~347)
- Después de PharaoStatue (líneas ~377-381)
- Después de Pyramidion (línea ~676)

## Modelos precargados
1. **sphinx_base.glb** - La Gran Esfinge
2. **ramses2.glb** - Estatua de Ramsés II (caída)
3. **hatshepsut.glb** - Estatua de Hatshepsut (de pie)
4. **akenaton.glb** - Estatua de Akhenaton (dentro de pirámide)
5. **momia.glb** - Momia movible
6. **escab.glb** - Escarabajo oculto
7. **piramidon.glb** - Piramidón de la Gran Pirámide

## Resultado
- Carga instantánea de todos los modelos al entrar a Giza
- Loading placeholder visible durante la carga inicial
- Mejor experiencia de usuario
- Sin retrasos ni apariciones progresivas

## Archivos modificados
- `viewer3d/components/GizaScene.tsx`

## Testing
- Build exitoso sin errores
- Todos los modelos se precargan correctamente
- Suspense funciona como esperado

## Notas técnicas
El preload se ejecuta cuando el módulo se importa por primera vez, lo que significa que los modelos comienzan a descargarse ANTES de que el usuario entre a Giza. Esto es especialmente efectivo si el usuario pasa por el menú o el globo antes de teletransportarse.
