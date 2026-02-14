# Texturas del Sistema Solar - Guía de Descarga

## Texturas Gratuitas de Alta Calidad (8K)

### 🌙 Luna
**Fuente**: NASA LRO (Lunar Reconnaissance Orbiter)
- **URL Oficial**: https://svs.gsfc.nasa.gov/4720
- **Resolución**: 8K (8192x4096)
- **Archivo**: `lroc_color_poles_8k.tif`
- **Descarga directa**: https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_poles_8k.tif
- **Guardar en**: `viewer3d/public/textures/moon_8k.jpg`

### 🔴 Marte
**Fuente**: Wikimedia Commons / Solar System Scope
- **URL**: https://commons.wikimedia.org/wiki/File:Solarsystemscope_texture_8k_mars.jpg
- **Resolución**: 8K (8192x4096)
- **Descarga directa**: https://upload.wikimedia.org/wikipedia/commons/0/02/Solarsystemscope_texture_8k_mars.jpg
- **Guardar en**: `viewer3d/public/textures/mars_8k.jpg`

### 🌟 Venus (Superficie)
**Fuente**: Gumroad - Free Textures
- **URL**: https://downloadforfree.gumroad.com/l/free-venus-surface-8k-textures
- **Resolución**: 8K (8192x4096)
- **Nota**: Requiere registro gratuito en Gumroad
- **Guardar en**: `viewer3d/public/textures/venus_surface_8k.jpg`

### 🌟 Venus (Atmósfera)
**Fuente**: Wikimedia Commons
- **URL**: https://commons.wikimedia.org/wiki/File:Solarsystemscope_texture_8k_venus_atmosphere.jpg
- **Descarga directa**: https://upload.wikimedia.org/wikipedia/commons/5/54/Solarsystemscope_texture_8k_venus_atmosphere.jpg
- **Guardar en**: `viewer3d/public/textures/venus_atmosphere_8k.jpg`

### ☀️ Sol
**Fuente**: Gumroad - Free Textures
- **URL**: https://downloadforfree.gumroad.com/l/free-sun-8k-textures
- **Resolución**: 4K (4096x2048)
- **Nota**: Requiere registro gratuito en Gumroad
- **Guardar en**: `viewer3d/public/textures/sun_8k.jpg`

### ☀️ Sol (Alternativa - SDO)
**Fuente**: NASA Solar Dynamics Observatory
- **URL**: https://sdo.gsfc.nasa.gov/assets/img/browse/
- **Resolución**: Variable
- **Nota**: Imágenes reales del Sol en diferentes longitudes de onda

## Instrucciones de Descarga

### Opción 1: Descarga Manual
1. Visita cada URL
2. Descarga la imagen en máxima resolución
3. Guarda en `viewer3d/public/textures/` con el nombre indicado
4. Convierte TIF a JPG si es necesario (para reducir tamaño)

### Opción 2: Descarga Automática (PowerShell)
```powershell
# Crear directorio si no existe
New-Item -ItemType Directory -Force -Path "viewer3d/public/textures"

# Descargar Marte
Invoke-WebRequest -Uri "https://upload.wikimedia.org/wikipedia/commons/0/02/Solarsystemscope_texture_8k_mars.jpg" -OutFile "viewer3d/public/textures/mars_8k.jpg"

# Descargar Venus Atmósfera
Invoke-WebRequest -Uri "https://upload.wikimedia.org/wikipedia/commons/5/54/Solarsystemscope_texture_8k_venus_atmosphere.jpg" -OutFile "viewer3d/public/textures/venus_atmosphere_8k.jpg"

# Descargar Luna (TIF - grande!)
Invoke-WebRequest -Uri "https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_poles_8k.tif" -OutFile "viewer3d/public/textures/moon_8k.tif"
```

### Opción 3: Wikimedia Commons (Todas disponibles)
Busca en: https://commons.wikimedia.org/wiki/Category:Planetary_maps
- Todas las texturas de Solar System Scope están disponibles
- Dominio público
- Alta resolución

## Texturas Adicionales Recomendadas

### 🌍 Tierra (Ya tenemos)
- ✅ `earth_8k.jpg`
- ✅ `earth_clouds_8k.jpg`
- ✅ `earth_night_8k.jpg`

### 🌙 Luna - Normal Map (Opcional)
**Para relieve realista**
- **URL**: https://svs.gsfc.nasa.gov/4720
- **Archivo**: `ldem_16_uint.tif`
- **Uso**: Displacement/Normal map

### 🔴 Marte - Normal Map (Opcional)
**Para relieve realista**
- **URL**: https://commons.wikimedia.org/wiki/File:Mars_Viking_MDIM21_ClrMosaic_global_1024.jpg
- **Uso**: Bump/Normal map

## Notas Importantes

1. **Tamaño de archivos**: Las texturas 8K son grandes (10-30 MB cada una)
2. **Formato**: Preferir JPG sobre TIF para web (menor tamaño)
3. **Licencia**: Todas son dominio público (NASA/ESA)
4. **Optimización**: Considerar versiones 4K para mejor performance

## Conversión TIF a JPG

Si descargas archivos TIF, convierte a JPG:

```powershell
# Usando ImageMagick (si está instalado)
magick convert moon_8k.tif -quality 90 moon_8k.jpg

# O usar herramientas online:
# - https://convertio.co/tif-jpg/
# - https://www.zamzar.com/convert/tif-to-jpg/
```

## Referencias

- **NASA 3D Resources**: https://nasa3d.arc.nasa.gov/
- **NASA SVS**: https://svs.gsfc.nasa.gov/
- **Wikimedia Planetary Maps**: https://commons.wikimedia.org/wiki/Category:Planetary_maps
- **Solar System Scope**: https://www.solarsystemscope.com/textures/
