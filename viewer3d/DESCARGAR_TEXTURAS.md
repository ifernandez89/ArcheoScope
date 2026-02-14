# 🌌 DESCARGAR TEXTURAS DEL SISTEMA SOLAR

## ⚡ DESCARGA RÁPIDA - Links Directos

### 1. 🔴 MARTE (8K)
**Opción A - Solar System Scope (Recomendado)**
1. Ve a: https://www.solarsystemscope.com/textures/
2. Busca "Mars" en la lista
3. Descarga "8K Mars"
4. Guarda como: `viewer3d/public/textures/mars_8k.jpg`

**Opción B - Wikimedia**
1. Ve a: https://commons.wikimedia.org/wiki/File:Solarsystemscope_texture_8k_mars.jpg
2. Click en la imagen para ver tamaño completo
3. Click derecho → "Guardar imagen como..."
4. Guarda como: `viewer3d/public/textures/mars_8k.jpg`

### 2. 🌙 LUNA (8K)
**Opción A - NASA (Mejor calidad)**
1. Ve a: https://svs.gsfc.nasa.gov/4720
2. Busca "lroc_color_poles_8k.tif" o "lroc_color_poles_4k.jpg"
3. Descarga el archivo JPG (más liviano)
4. Guarda como: `viewer3d/public/textures/moon_8k.jpg`

**Opción B - Solar System Scope**
1. Ve a: https://www.solarsystemscope.com/textures/
2. Busca "Moon"
3. Descarga "8K Moon"
4. Guarda como: `viewer3d/public/textures/moon_8k.jpg`

### 3. 🌟 VENUS ATMÓSFERA (8K)
**Solar System Scope**
1. Ve a: https://www.solarsystemscope.com/textures/
2. Busca "Venus Atmosphere"
3. Descarga "8K Venus Atmosphere"
4. Guarda como: `viewer3d/public/textures/venus_atmosphere_8k.jpg`

### 4. 🌟 VENUS SUPERFICIE (8K)
**Solar System Scope**
1. Ve a: https://www.solarsystemscope.com/textures/
2. Busca "Venus Surface"
3. Descarga "8K Venus Surface"
4. Guarda como: `viewer3d/public/textures/venus_surface_8k.jpg`

### 5. ☀️ SOL (4K-8K)
**Opción A - Solar System Scope**
1. Ve a: https://www.solarsystemscope.com/textures/
2. Busca "Sun"
3. Descarga "8K Sun"
4. Guarda como: `viewer3d/public/textures/sun_8k.jpg`

**Opción B - NASA SDO (Imágenes reales)**
1. Ve a: https://sdo.gsfc.nasa.gov/data/
2. Descarga imágenes del Sol en diferentes longitudes de onda
3. Usa para efectos especiales

## 📦 PACK COMPLETO (Más fácil)

### Gumroad - Free Solar System Textures
**URL**: https://downloadforfree.gumroad.com/l/qhvge

Incluye TODAS las texturas en un solo pack:
- Sol, Mercurio, Venus, Tierra, Luna, Marte, Júpiter, Saturno, Urano, Neptuno
- Resoluciones: 2K, 4K y 8K
- Formato: JPG
- Gratis (requiere email)

**Pasos**:
1. Ve al link
2. Ingresa tu email
3. Click "I want this!"
4. Descarga el ZIP
5. Extrae las texturas que necesites a `viewer3d/public/textures/`

## 🎯 TEXTURAS NECESARIAS PARA EL PROYECTO

Prioridad ALTA (para la obra contemplativa):
- ✅ `earth_8k.jpg` (ya tenemos)
- ✅ `earth_clouds_8k.jpg` (ya tenemos)
- ✅ `earth_night_8k.jpg` (ya tenemos)
- ⬜ `moon_8k.jpg` (NECESARIA)
- ⬜ `sun_8k.jpg` (NECESARIA)

Prioridad MEDIA (para expansión del sistema):
- ⬜ `mars_8k.jpg`
- ⬜ `venus_atmosphere_8k.jpg`

Prioridad BAJA (futuro):
- ⬜ `venus_surface_8k.jpg`
- ⬜ `mercury_8k.jpg`
- ⬜ `jupiter_8k.jpg`

## 📁 ESTRUCTURA DE CARPETAS

```
viewer3d/
└── public/
    └── textures/
        ├── earth_8k.jpg          ✅ Ya existe
        ├── earth_clouds_8k.jpg   ✅ Ya existe
        ├── earth_night_8k.jpg    ✅ Ya existe
        ├── moon_8k.jpg           ⬜ Descargar
        ├── sun_8k.jpg            ⬜ Descargar
        ├── mars_8k.jpg           ⬜ Descargar
        └── venus_atmosphere_8k.jpg ⬜ Descargar
```

## ⚙️ DESPUÉS DE DESCARGAR

1. Verifica que los archivos estén en `viewer3d/public/textures/`
2. Verifica que los nombres sean exactos (minúsculas, guiones bajos)
3. Ejecuta el build local para probar:
   ```powershell
   cd viewer3d
   npm run dev
   ```

## 🔧 OPTIMIZACIÓN (Opcional)

Si las texturas son muy pesadas (>20MB), puedes reducirlas:

```powershell
# Usando ImageMagick
magick convert moon_8k.jpg -quality 85 -resize 4096x2048 moon_4k.jpg
```

O usa herramientas online:
- https://squoosh.app/ (Google)
- https://tinypng.com/

## 📝 NOTAS

- Todas las texturas son dominio público (NASA/ESA)
- Formato recomendado: JPG (menor tamaño que PNG)
- Resolución recomendada: 8K para calidad, 4K para performance
- Las texturas se cargan bajo demanda (no afectan carga inicial)

## ❓ PROBLEMAS COMUNES

**"La textura no carga"**
- Verifica el nombre del archivo (exacto, minúsculas)
- Verifica que esté en `public/textures/`
- Verifica que sea JPG o PNG

**"La textura se ve pixelada"**
- Descarga versión 8K en lugar de 4K o 2K
- Verifica que no se haya comprimido demasiado

**"El sitio va lento"**
- Usa versiones 4K en lugar de 8K
- Comprime las imágenes con Squoosh
- Las texturas se cachean después de la primera carga
