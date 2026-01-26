# 🚨 PROBLEMA CRÍTICO: PROJ Database Conflict

## DIAGNÓSTICO

**Estado actual:** 0/7 instrumentos satelitales funcionando (0%)

**Causa raíz:** PostgreSQL 15 instaló su propia versión antigua de PROJ que conflictúa con rasterio.

```
ERROR: PROJ: proj.db contains DATABASE.LAYOUT.VERSION.MINOR = 2 
whereas a number >= 5 is expected
```

**Ubicación del conflicto:**
```
C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db
```

## SOLUCIONES POSIBLES

### Opción 1: Renombrar proj.db de PostgreSQL (RECOMENDADO)

```powershell
# Renombrar temporalmente el proj.db de PostgreSQL
Rename-Item "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db" "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db.backup"
```

**Ventajas:**
- Solución inmediata
- No afecta PostgreSQL (solo PostGIS)
- Reversible

**Desventajas:**
- Requiere permisos de administrador
- PostGIS no funcionará (pero no lo usamos)

### Opción 2: Modificar PATH del Sistema

Remover `C:\Program Files\PostgreSQL\15\bin` del PATH del sistema temporalmente.

**Ventajas:**
- No modifica archivos
- Reversible

**Desventajas:**
- Requiere reiniciar terminal/sistema
- Afecta todas las aplicaciones

### Opción 3: Usar Conda Environment (MEJOR A LARGO PLAZO)

Crear un environment aislado con conda que tenga su propia versión de PROJ:

```bash
conda create -n archeoscope python=3.11
conda activate archeoscope
conda install -c conda-forge rasterio gdal proj
pip install -r requirements.txt
```

**Ventajas:**
- Aislamiento completo
- No afecta sistema
- Mejor práctica

**Desventajas:**
- Requiere instalar conda
- Toma tiempo configurar

### Opción 4: Workaround - Usar APIs que no requieren rasterio

Temporalmente, podemos:
1. Deshabilitar Sentinel-2, Sentinel-1, Landsat (requieren rasterio)
2. Usar solo ICESat-2, NSIDC, MODIS LST, Copernicus Marine

**Ventajas:**
- No requiere cambios en sistema
- Algunos instrumentos funcionarán

**Desventajas:**
- Perdemos 3 instrumentos importantes
- Análisis menos completo

## RECOMENDACIÓN INMEDIATA

**Para continuar trabajando HOY:**

1. **Renombrar proj.db de PostgreSQL** (Opción 1)
2. **Verificar que funciona** con `python test_proj_fix.py`
3. **Probar instrumentos** con `python check_instruments_status.py`

**Comando (requiere PowerShell como Administrador):**

```powershell
Rename-Item "C:\Program Files\PostgreSQL\15\share\contrib\postgis-3.5\proj\proj.db" "proj.db.backup"
```

## ESTADO ACTUAL DEL SISTEMA

### ✅ Funcionando
- Backend API (puerto 8002)
- Frontend (puerto 8080)
- Base de datos PostgreSQL (puerto 5433)
- IA con Ollama (qwen2.5:3b-instruct)
- Análisis sin instrumentos satelitales

### ❌ NO Funcionando
- Sentinel-2 (NDVI, multispectral)
- Sentinel-1 (SAR)
- Landsat (térmico)
- ICESat-2 (elevación) - falta configurar credenciales
- NSIDC (hielo) - falta configurar credenciales
- MODIS LST (térmico) - falta configurar credenciales
- Copernicus Marine (océano) - falta configurar credenciales

## IMPACTO EN ARCHEOSCOPE

**Sin instrumentos satelitales:**
- Sistema funciona pero con 0 mediciones
- Análisis basado solo en:
  - Clasificación de ambiente
  - Base de datos arqueológica (80,512 sitios)
  - IA (Ollama)
  - Sensor temporal

**Probabilidad arqueológica:** Reducida significativamente sin datos instrumentales

## PRÓXIMOS PASOS

1. **Decidir solución:** ¿Renombrar proj.db o usar conda?
2. **Aplicar fix**
3. **Verificar instrumentos:** `python check_instruments_status.py`
4. **Configurar credenciales Earthdata** (para ICESat-2, NSIDC, MODIS)
5. **Probar análisis completo**

---

**Fecha:** 2026-01-26  
**Prioridad:** 🔴 CRÍTICA  
**Bloqueante:** Sí - sin instrumentos el sistema tiene capacidad limitada
