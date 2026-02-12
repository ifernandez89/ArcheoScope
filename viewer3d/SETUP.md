# Setup Guide - Viewer3D

## 📦 Instalación de Dependencias

### Opción 1: Instalación Completa (Recomendada)

Si tienes conexión a internet estable:

```bash
cd viewer3d
npm install
```

Esto instalará todas las dependencias incluyendo:
- `@react-three/postprocessing` - Efectos visuales
- `zustand` - Estado global
- `postprocessing` - Librería de efectos
- `leva` - Panel de controles

### Opción 2: Instalación Manual (Si hay problemas de red)

Si `npm install` falla por problemas de red, instala las dependencias una por una:

```bash
cd viewer3d

# Dependencias core (ya instaladas)
npm install next@14.1.0 react@18.2.0 react-dom@18.2.0
npm install three@0.161.0
npm install @react-three/fiber@8.15.16
npm install @react-three/drei@9.96.0

# Nuevas dependencias del Core Engine
npm install @react-three/postprocessing@2.16.0
npm install zustand@4.5.0
npm install postprocessing@6.34.3
npm install leva@0.9.35

# Dev dependencies
npm install -D typescript@5 @types/node@20 @types/react@18 @types/react-dom@18 @types/three@0.161.0
```

## 🚀 Iniciar el Servidor

### Windows
```bash
start_viewer3d.bat
```

### Linux/Mac
```bash
cd viewer3d
npm run dev
```

El servidor estará disponible en: `http://localhost:3000`

## ✅ Verificar Instalación

### 1. Verificar que todas las dependencias están instaladas

```bash
cd viewer3d
npm list @react-three/postprocessing zustand postprocessing leva
```

Deberías ver:
```
├── @react-three/postprocessing@2.16.0
├── zustand@4.5.0
├── postprocessing@6.34.3
└── leva@0.9.35
```

### 2. Verificar que el servidor compila sin errores

Después de iniciar el servidor, deberías ver:

```
✓ Ready in 2.5s
○ Local:        http://localhost:3000
```

Sin errores de "Module not found".

## 🔧 Habilitar Postprocessing

Una vez instaladas las dependencias, descomenta las líneas en `components/Scene3D.tsx`:

```typescript
// Buscar estas líneas comentadas:
// import { EffectComposer, Bloom, SSAO } from '@react-three/postprocessing'

// Y este bloque:
/*
<EffectComposer>
  <Bloom 
    intensity={0.3} 
    luminanceThreshold={0.9} 
    luminanceSmoothing={0.9}
  />
  <SSAO 
    samples={31}
    radius={5}
    intensity={30}
  />
</EffectComposer>
*/
```

Descomenta ambos para habilitar los efectos visuales.

## 🐛 Troubleshooting

### Error: "Module not found: @react-three/postprocessing"

**Solución**: Las dependencias no están instaladas. Ejecuta:
```bash
cd viewer3d
npm install @react-three/postprocessing postprocessing
```

### Error: "Cannot find module 'zustand'"

**Solución**: Instala zustand:
```bash
cd viewer3d
npm install zustand
```

### Error: Network timeout durante npm install

**Solución**: 
1. Verifica tu conexión a internet
2. Intenta con un registro diferente:
   ```bash
   npm config set registry https://registry.npmjs.org/
   ```
3. O instala las dependencias una por una (ver Opción 2 arriba)

### El servidor no inicia en el puerto 3000

**Solución**: El puerto puede estar ocupado. Usa otro puerto:
```bash
npm run dev -- -p 3001
```

### Errores de TypeScript

**Solución**: Asegúrate de tener los tipos instalados:
```bash
npm install -D @types/three @types/react @types/react-dom
```

## 📊 Estado de las Dependencias

### ✅ Ya Instaladas (desde sesión anterior)
- next@14.1.0
- react@18.2.0
- react-dom@18.2.0
- three@0.161.0
- @react-three/fiber@8.15.16
- @react-three/drei@9.96.0
- typescript@5

### ⏳ Pendientes de Instalar
- @react-three/postprocessing@2.16.0
- zustand@4.5.0
- postprocessing@6.34.3
- leva@0.9.35

## 🎯 Próximos Pasos

Una vez instaladas todas las dependencias:

1. ✅ Habilitar postprocessing en `Scene3D.tsx`
2. ✅ Probar los controles del Core Engine
3. ✅ Experimentar con el sistema de iluminación
4. ✅ Explorar el sistema de eventos
5. ✅ Revisar la documentación en `CORE_ENGINE.md`

## 📚 Recursos

- [Next.js Docs](https://nextjs.org/docs)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Zustand](https://github.com/pmndrs/zustand)
- [Postprocessing](https://github.com/pmndrs/postprocessing)
- [Core Engine Docs](./CORE_ENGINE.md)
