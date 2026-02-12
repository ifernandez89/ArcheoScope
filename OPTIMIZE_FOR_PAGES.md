# Optimización para GitHub Pages

## 1. Reducir Textura del Globo

### Opción A: Usar textura 4K (Recomendado)
- Tamaño: ~2-3 MB (vs 8K que pesa ~15-20 MB)
- Calidad: Excelente para web
- Carga: Mucho más rápida

### Opción B: Usar textura 2K
- Tamaño: ~500 KB - 1 MB
- Calidad: Buena para demo
- Carga: Instantánea

### Dónde conseguir texturas optimizadas:
- https://www.solarsystemscope.com/textures/ (2K/4K gratis)
- https://planetpixelemporium.com/earth.html (varias resoluciones)

## 2. Optimizar Modelos 3D

Los modelos actuales (warrior.glb, moai.glb, sphinx.glb) ya son ligeros.
Si quieres optimizar más:

```bash
# Instalar gltf-pipeline
npm install -g gltf-pipeline

# Optimizar cada modelo
gltf-pipeline -i warrior.glb -o warrior-optimized.glb -d
gltf-pipeline -i moai.glb -o moai-optimized.glb -d
gltf-pipeline -i sphinx.glb -o sphinx-optimized.glb -d
```

## 3. Configuración para GitHub Pages

### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/ArcheoScope',
  assetPrefix: '/ArcheoScope/',
  images: {
    unoptimized: true,
  },
  // Optimizaciones
  compress: true,
  poweredByHeader: false,
}

module.exports = nextConfig
```

## 4. Estructura de Archivos

```
viewer3d/
├── public/
│   ├── earth-4k.jpg          # Textura optimizada 4K (~3 MB)
│   ├── warrior.glb           # ~500 KB
│   ├── moai.glb             # ~800 KB
│   ├── sphinx.glb           # ~600 KB
│   └── ...
├── components/
├── app/
└── ...
```

## 5. Tamaño Total Estimado

- Textura 4K: ~3 MB
- 3 Modelos: ~2 MB
- Código JS/CSS: ~500 KB
- **Total: ~5.5 MB** ✅ Perfecto para GitHub Pages

## 6. Tiempo de Carga Estimado

- Conexión rápida (50 Mbps): ~1 segundo
- Conexión media (10 Mbps): ~5 segundos
- Conexión lenta (2 Mbps): ~25 segundos

## 7. Features que Funcionarán

✅ Globo 3D interactivo
✅ Click para teletransportar
✅ Modo exploración con avatares
✅ Caminar (W/A/S/D)
✅ Rotar (Q/E)
✅ Cambiar entre avatares
✅ Modo órbita
✅ Simulación solar día/noche
✅ Estrellas en modo nocturno
✅ Terreno procedural
✅ Partículas ambientales
✅ Camera bob
✅ Grid de referencia

## 8. Features que NO Funcionarán

❌ Avatar conversacional con IA
❌ Procesamiento satelital
❌ Base de datos

## 9. Deploy Automático

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main, creador3D ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: viewer3d/package-lock.json
    
    - name: Install dependencies
      working-directory: ./viewer3d
      run: npm ci
    
    - name: Build Next.js
      working-directory: ./viewer3d
      run: npm run build
    
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: ./viewer3d/out

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## 10. URL Final

Tu demo estará en:
**https://ifernandez89.github.io/ArcheoScope/**

## 11. Ventajas

- ✅ Gratis
- ✅ Deploy automático
- ✅ SSL incluido
- ✅ CDN global
- ✅ Perfecto para portfolio
- ✅ Muestra tus habilidades 3D
- ✅ Interactivo y profesional

## 12. Próximos Pasos

1. Descargar textura 4K optimizada
2. Modificar `next.config.js`
3. Crear GitHub Action
4. Habilitar GitHub Pages en Settings
5. Push y esperar deploy (~2-3 minutos)
6. ¡Disfrutar tu demo en vivo!
