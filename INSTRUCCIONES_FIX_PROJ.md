# 🔧 INSTRUCCIONES: Activar Instrumentos Satelitales

## PROBLEMA

Los instrumentos satelitales NO están funcionando (0/7) debido a un conflicto entre PostgreSQL y rasterio.

## SOLUCIÓN (2 minutos)

### Paso 1: Abrir PowerShell como Administrador

1. Presiona `Windows + X`
2. Selecciona **"Windows PowerShell (Administrador)"** o **"Terminal (Administrador)"**
3. Click en **"Sí"** cuando pregunte por permisos

### Paso 2: Ejecutar el comando

Copia y pega este comando en PowerShell:

```powershell
Rename-Item "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db" "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db.backup"
```

Presiona Enter.

### Paso 3: Verificar

En tu PowerShell normal (no administrador), ejecuta:

```bash
python test_proj_fix.py
```

Deberías ver:
```
✅ CRS creado exitosamente
✅ PROJ funcionando correctamente
🎉 FIX DE PROJ EXITOSO
```

### Paso 4: Reiniciar Backend

```bash
# El backend se reiniciará automáticamente
# O manualmente:
# Ctrl+C en la terminal del backend
# python run_archeoscope.py
```

### Paso 5: Probar Instrumentos

```bash
python check_instruments_status.py
```

Deberías ver:
```
✅ sentinel_2
✅ sentinel_1  
✅ landsat
📊 Resumen: 3/7 instrumentos funcionando (42.9%)
```

## ALTERNATIVA: Script Automático

También puedes ejecutar:

```powershell
# Click derecho en fix_proj_conflict.ps1
# -> Ejecutar con PowerShell (como Administrador)
```

## ¿QUÉ HACE ESTE FIX?

- Renombra `proj.db` de PostgreSQL a `proj.db.backup`
- PostgreSQL seguirá funcionando normalmente
- Solo PostGIS se verá afectado (no lo usamos)
- Los instrumentos satelitales funcionarán

## REVERTIR (si necesitas PostGIS)

```powershell
Rename-Item "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db.backup" "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db"
```

## DESPUÉS DEL FIX

Una vez funcionando, tendrás:

- ✅ Sentinel-2 (NDVI, multispectral)
- ✅ Sentinel-1 (SAR)
- ✅ Landsat (térmico)
- ⏳ ICESat-2 (requiere configurar credenciales Earthdata)
- ⏳ NSIDC (requiere configurar credenciales Earthdata)
- ⏳ MODIS LST (requiere configurar credenciales Earthdata)
- ⏳ Copernicus Marine (requiere configurar credenciales)

**3/7 instrumentos funcionando inmediatamente**  
**7/7 instrumentos después de configurar credenciales**

---

**¿Necesitas ayuda?** Avísame si tienes algún problema ejecutando estos pasos.
