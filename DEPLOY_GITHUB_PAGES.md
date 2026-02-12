# Deploy a GitHub Pages

## Configuración para Next.js Static Export

### 1. Modificar next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/ArcheoScope',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
```

### 2. Agregar script de build en package.json

```json
{
  "scripts": {
    "build": "next build",
    "export": "next build && next export"
  }
}
```

### 3. Crear GitHub Action

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      working-directory: ./viewer3d
      run: npm ci
    
    - name: Build
      working-directory: ./viewer3d
      run: npm run build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./viewer3d/out
```

### 4. Habilitar GitHub Pages

1. Ve a Settings → Pages
2. Source: Deploy from a branch
3. Branch: gh-pages / root
4. Save

### 5. Acceder

Tu sitio estará en: `https://ifernandez89.github.io/ArcheoScope/`

## ⚠️ Limitaciones

- No funcionará el avatar conversacional (necesita backend)
- No habrá procesamiento de datos satelitales
- Solo visualización estática de modelos 3D

## 💡 Recomendación

Para un proyecto completo, considera:
- **Frontend**: Vercel o Netlify
- **Backend**: Render.com o Railway
- **Base de datos**: Supabase o Vercel Postgres
