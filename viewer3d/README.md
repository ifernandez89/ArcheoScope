# 🏛️ Archeoscope: The Forgotten Relics

Juego inmersivo de exploración arqueológica usando Next.js + React Three Fiber.

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
cd viewer3d
npm install
```

### 2. Iniciar servidor de desarrollo
```bash
npm run dev
```

El visualizador estará disponible en: `http://localhost:3000`

---

## 🎮 Controles

- **Click Izquierdo + Arrastrar**: Rotar el modelo
- **Click Derecho + Arrastrar**: Mover la cámara (pan)
- **Scroll**: Zoom in/out
- **Click en el modelo**: Toggle auto-rotación

---

## 🎨 Características

### Implementadas ✅
- ✅ Carga de modelos .glb/.gltf
- ✅ Controles de órbita (rotar, zoom, pan)
- ✅ Auto-rotación con toggle
- ✅ Iluminación realista (ambient, directional, point, spot)
- ✅ Sombras de contacto
- ✅ Grid de referencia
- ✅ Entorno HDR para reflejos
- ✅ Animaciones automáticas (si el modelo las tiene)
- ✅ Centrado y escalado automático
- ✅ Loading spinner con progreso
- ✅ UI con información y controles
- ✅ Responsive design

### Próximas Mejoras 🚧
- [ ] Selector de modelos (cambiar entre warrior, moai, sphinx, etc.)
- [ ] Panel de control de iluminación
- [ ] Selector de entornos (city, sunset, forest, etc.)
- [ ] Captura de screenshots
- [ ] Modo wireframe
- [ ] Mediciones y anotaciones
- [ ] Integración con API de ArcheoScope
- [ ] Galería de modelos arqueológicos
- [ ] Comparación lado a lado
- [ ] Export a diferentes formatos

---

## 📁 Estructura del Proyecto

```
viewer3d/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Página principal
│   └── globals.css         # Estilos globales
│
├── components/
│   ├── Scene3D.tsx         # Escena 3D principal
│   ├── ModelViewer.tsx     # Componente del modelo
│   ├── LoadingSpinner.tsx  # Spinner de carga
│   └── UI.tsx              # Interfaz de usuario
│
├── public/
│   └── warrior.glb         # Modelo 3D de prueba
│
├── package.json
├── tsconfig.json
└── next.config.js
```

---

## 🔧 Tecnologías

- **Next.js 14**: Framework React con App Router
- **React Three Fiber**: React renderer para Three.js
- **@react-three/drei**: Helpers y componentes útiles
- **Three.js**: Librería 3D WebGL
- **TypeScript**: Type safety

---

## 📦 Agregar Nuevos Modelos

### Opción 1: Archivo local
1. Coloca tu archivo `.glb` o `.gltf` en `public/`
2. Actualiza la ruta en `ModelViewer.tsx`:
```tsx
<ModelViewer modelPath="/tu-modelo.glb" />
```

### Opción 2: URL remota
```tsx
<ModelViewer modelPath="https://ejemplo.com/modelo.glb" />
```

### Opción 3: Desde ArcheoScope API
```tsx
<ModelViewer modelPath="http://localhost:8003/api/geometric-model/moai.glb" />
```

---

## 🎨 Personalización

### Cambiar iluminación
Edita `Scene3D.tsx`:
```tsx
<ambientLight intensity={0.5} />  // Luz ambiental
<directionalLight position={[10, 10, 5]} intensity={1} />  // Luz direccional
```

### Cambiar entorno
```tsx
<Environment preset="sunset" />  // city, sunset, dawn, night, warehouse, forest, apartment, studio, park, lobby
```

### Cambiar grid
```tsx
<Grid
  cellSize={1}           // Tamaño de celda
  cellColor="#6f6f6f"    // Color de celda
  sectionSize={5}        // Tamaño de sección
  sectionColor="#9d4b4b" // Color de sección
/>
```

---

## 🔗 Integración con ArcheoScope

### Cargar modelos desde la API
```tsx
const [modelPath, setModelPath] = useState('/warrior.glb')

// Después de generar un modelo en ArcheoScope
const response = await fetch('http://localhost:8003/api/geometric-inference-3d', {
  method: 'POST',
  body: JSON.stringify({ lat: -27.1261, lon: -109.2868 })
})

const result = await response.json()
setModelPath(`http://localhost:8003/api/geometric-model/${result.obj_filename}`)
```

---

## 🐛 Troubleshooting

### El modelo no se ve
- Verifica que el archivo `.glb` esté en `public/`
- Revisa la consola del navegador para errores
- Asegúrate de que la ruta sea correcta

### El modelo está muy grande/pequeño
El componente `ModelViewer` escala automáticamente, pero puedes ajustar:
```tsx
const scale = 2 / maxDim  // Cambiar el 2 por otro valor
```

### Las animaciones no funcionan
Verifica que el modelo tenga animaciones:
```tsx
console.log('Animaciones:', names)  // En ModelViewer.tsx
```

---

## 📚 Recursos

- [Three.js Docs](https://threejs.org/docs/)
- [React Three Fiber Docs](https://docs.pmnd.rs/react-three-fiber)
- [Drei Helpers](https://github.com/pmndrs/drei)
- [glTF Format](https://www.khronos.org/gltf/)

---

## 🎯 Próximos Pasos

1. **Selector de Modelos**: Crear un dropdown para cambiar entre diferentes modelos
2. **Integración API**: Conectar con ArcheoScope para cargar modelos generados
3. **Galería**: Mostrar thumbnails de todos los modelos disponibles
4. **Comparación**: Vista split para comparar dos modelos
5. **Anotaciones**: Agregar marcadores y notas en el modelo
6. **Export**: Permitir descargar screenshots o el modelo

---

## 🤝 Contribuir

Este visualizador es parte del proyecto ArcheoScope. Para agregar funcionalidades:

1. Crea una nueva rama
2. Implementa la funcionalidad
3. Prueba localmente
4. Crea un pull request

---

## 📄 Licencia

Parte del proyecto ArcheoScope.

---

**¡Disfruta explorando modelos 3D!** 🏛️✨
