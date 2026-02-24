# 🚨 ACCIONES INMEDIATAS - FIXES CRÍTICOS

**Tiempo total:** ~1.5 horas  
**Criticidad:** 🔴 MÁXIMA - Hacer HOY antes de agregar efectos

---

## FIX #1: TerrainDataService Cache (15 min)

**Archivo:** `c:\py\ArcheoScope\viewer3d\services\TerrainDataService.ts`

### Cambio:

```diff
class TerrainDataService {
  private baseUrl: string
  private cache: Map<string, { 
    data: TerrainData
    timestamp: number 
  }> = new Map()
+
+ private readonly MAX_CACHE_ITEMS = 10
+ private readonly MAX_CACHE_AGE_MS = 30 * 60 * 1000  // 30 minutos

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl
+   // Limpiar caché antiguos cada 5 minutos
+   this.startCacheCleanup()
  }

+ private startCacheCleanup(): void {
+   setInterval(() => {
+     const now = Date.now()
+     for (const [key, { timestamp }] of this.cache.entries()) {
+       if (now - timestamp > this.MAX_CACHE_AGE_MS) {
+         console.log('🧹 Limpiando tile antiguo:', key)
+         this.cache.delete(key)
+       }
+     }
+   }, 5 * 60 * 1000)  // Cada 5 minutos
+ }

  async getTerrainData(
    latMin: number,
    latMax: number,
    lonMin: number,
    lonMax: number,
    resolution: number = 256
  ): Promise<TerrainData> {
    // Generar cache key
    const cacheKey = `${latMin.toFixed(4)}_${latMax.toFixed(4)}_${lonMin.toFixed(4)}_${lonMax.toFixed(4)}_${resolution}`
    
    // Buscar en caché local
    if (this.cache.has(cacheKey)) {
      console.log('✅ Terrain data from local cache:', cacheKey)
-     return this.cache.get(cacheKey)!
+     return this.cache.get(cacheKey)!.data
    }
    
    try {
      // ... request code ...
      
      const data: TerrainData = await response.json()
      
      // Cachear localmente - AHORA CON LÍMITE
-     this.cache.set(cacheKey, data)
+     this.cache.set(cacheKey, { data, timestamp: Date.now() })
+     
+     // Limpiar si exceeds max size
+     if (this.cache.size > this.MAX_CACHE_ITEMS) {
+       const oldest = Array.from(this.cache.entries())
+         .sort((a, b) => a[1].timestamp - b[1].timestamp)[0]
+       if (oldest) {
+         console.log('🧹 Cache lleno, removiendo oldest:', oldest[0])
+         this.cache.delete(oldest[0])
+       }
+     }
+     
+     console.log(`📊 Cache size: ${this.cache.size}/${this.MAX_CACHE_ITEMS}`)
      
      return data
    }
  }
}
```

**Testing:**
```typescript
// Verificar en DevTools:
// 1. Cambiar de ubicación 15 veces
// 2. Ver que cache.size nunca exceeds 10
// 3. Ver logs "Cache size: X/10"
```

---

## FIX #2: Backend Server State (Refactor) (45 min)

**Archivo principal:** `c:\py\ArcheoScope\backend\api\main.py`

### Paso 1: Cambiar state globals

```python
# ANTES (líneas 140-150):
system_components = {
    'rules_engine': None,
    'ai_assistant': None,
    'explainer': None,
    'geometric_engine': None,
    'environment_classifier': None,
    'core_anomaly_detector': None,
    'transparency': None
}

# AHORA (reemplazar con):
# NO GLOBALS - Usar app.state en su lugar
```

### Paso 2: Refactor startup

```python
# ANTES:
def initialize_system():
    try:
        system_components['rules_engine'] = ArchaeologicalRulesEngine()
        # ...
        return True
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

# AHORA:
def initialize_system_components():
    """Retorna dict de componentes inicializados sin usar globals"""
    components = {}
    try:
        components['rules_engine'] = ArchaeologicalRulesEngine()
        components['explainer'] = ScientificExplainer()
        components['geometric_engine'] = GeometricInferenceEngine()
        components['environment_classifier'] = EnvironmentClassifier()
        components['transparency'] = DataSourceTransparency()
        logger.info("✅ Sistema inicializado")
        return components
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {}
```

### Paso 3: Actualizar startup event

```python
@app.on_event("startup")
async def startup_event():
    """Inicializar sistema al arrancar."""
    logger.info("🚀 Iniciando ArcheoScope...")
    
    # Inicializar componentes en app.state (NO global)
    app.state.system_components = initialize_system_components()
    
    # BD
    try:
        if database_connection is not None:
            await database_connection.connect()
            site_count = await database_connection.count_sites()
            logger.info(f"✅ Base de datos conectada - {site_count:,} sitios")
        else:
            logger.warning("⚠️ Database no disponible")
    except Exception as e:
        logger.warning(f"⚠️ BD no disponible: {e}")
    
    # Científico
    try:
        from api.scientific_endpoint import init_db_pool
        await init_db_pool()
        logger.info("✅ Pool científico inicializado")
    except Exception as e:
        logger.warning(f"⚠️ Pool científico: {e}")
    
    # TIMT
    try:
        from api.timt_endpoints import init_timt_db_pool
        await init_timt_db_pool()
        logger.info("✅ Pool TIMT inicializado")
    except Exception as e:
        logger.warning(f"⚠️ Pool TIMT: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar conexiones y limpiar."""
    logger.info("🛑 Shutting down ArcheoScope...")
    
    # Cleanup de componentes
    if hasattr(app.state, 'system_components'):
        components = app.state.system_components
        for name, component in components.items():
            if component and hasattr(component, 'cleanup'):
                try:
                    component.cleanup()
                    logger.info(f"✅ Cleaned up {name}")
                except Exception as e:
                    logger.warning(f"⚠️ Error cleaning {name}: {e}")
    
    # BD
    try:
        if database_connection is not None:
            await database_connection.close()
            logger.info("✅ BD cerrada")
    except Exception as e:
        logger.warning(f"⚠️ Error cerrando BD: {e}")
```

### Paso 4: Crear helper para acceso

```python
from fastapi import Depends
from fastapi.exceptions import HTTPException

async def get_system_components():
    """Dependency injection para acceso a componentes"""
    if not hasattr(app.state, 'system_components'):
        raise HTTPException(status_code=503, detail="Sistema no inicializado")
    return app.state.system_components

async def get_component(name: str) = Depends(get_system_components):
    """Obtener componente específico"""
    components = await get_system_components()
    if name not in components or not components[name]:
        raise HTTPException(status_code=503, detail=f"{name} no disponible")
    return components[name]
```

### Paso 5: Actualizar endpoints

```python
# ANTES:
@app.get("/status", response_model=SystemStatus, tags=["Status"])
async def get_system_status():
    """Estado operacional del sistema."""
    backend_status = "operational" if all(system_components.values()) else "limited"
    ai_assistant = system_components.get('ai_assistant')
    ai_status = "available" if ai_assistant and ai_assistant.is_available else "offline"
    rules_engine = system_components.get('rules_engine')
    # ...

# AHORA:
@app.get("/status", response_model=SystemStatus, tags=["Status"])
async def get_system_status(
    components: dict = Depends(get_system_components)
):
    """Estado operacional del sistema."""
    backend_status = "operational" if all(components.values()) else "limited"
    ai_assistant = components.get('ai_assistant')
    ai_status = "available" if ai_assistant and ai_assistant.is_available else "offline"
    rules_engine = components.get('rules_engine')
```

---

## FIX #3: Backend Terrain Cache (10 min)

**Archivo:** `c:\py\ArcheoScope\backend\terrain_data_service.py`

### Cambio:

Si el archivo usa dict para cache:

```python
# ANTES:
class TerrainDataService:
    def __init__(self):
        self.memory_cache = {}
    
    def get_terrain_data(self, ...):
        if key not in self.memory_cache:
            # load data
            self.memory_cache[key] = tile  # 🔴 SIN LÍMITE

# AHORA - usar cachetools:
from cachetools import TTLCache
from functools import lru_cache

class TerrainDataService:
    def __init__(self):
        # Cache máx 50 tiles, expira después de 1 hora
        self.memory_cache = TTLCache(
            maxsize=50,
            ttl=3600,  # 1 hour
            timer=time.time
        )
        logger.info("✅ Terrain cache initialized: max 50 tiles, TTL 1 hour")
    
    def get_terrain_data(self, lat_min, lat_max, lon_min, lon_max, resolution):
        cache_key = f"{lat_min}_{lat_max}_{lon_min}_{lon_max}_{resolution}"
        
        # Buscar en caché
        if cache_key in self.memory_cache:
            logger.info(f"✅ Cache hit: {cache_key}")
            return self.memory_cache[cache_key]
        
        # Cargar datos...
        tile = self._load_terrain_tile(lat_min, lat_max, lon_min, lon_max, resolution)
        
        # Guardar en caché
        try:
            self.memory_cache[cache_key] = tile
            logger.info(f"📊 Cache stats: {len(self.memory_cache)}/50 tiles")
        except KeyError:
            # Cache full, elimina oldest automáticamente (TTLCache)
            logger.info("🧹 Cache full, old entry evicted")
            self.memory_cache[cache_key] = tile
        
        return tile
```

**O usar decorador (más simple):**

```python
from functools import lru_cache

class TerrainDataService:
    @lru_cache(maxsize=50)
    def get_terrain_data_cached(self, lat_min, lat_max, lon_min, lon_max, resolution):
        """Versión cacheada de get_terrain_data"""
        return self._load_terrain_tile(lat_min, lat_max, lon_min, lon_max, resolution)
```

**Instalar dependencia:**
```bash
pip install cachetools
```

---

## VERIFICACIÓN

Después de aplicar los 3 fixes:

### Frontend Test:
```typescript
// En DevTools Console:
// 1. Navegar a 20 ubicaciones diferentes
// 2. Verificar:
const service = new TerrainDataService()
service.cache.size <= 10  // ✅ Debe ser true

// 3. Memory (DevTools > Memory > Heap Snapshot)
// Antes: Creciente indefinidamente
// Después: Capped en ~100MB
```

### Backend Test:
```bash
# 1. Iniciar backend
python -m uvicorn backend.api.main:app --reload

# 2. Verificar en logs:
# ✅ "✅ Sistema inicializado"
# ✅ "✅ Pool científico inicializado"
# ✅ "✅ Pool TIMT inicializado"

# 3. Request de prueba:
curl http://localhost:8003/status

# 4. Verificar en logs después del request:
# Debe usar app.state, no globals
```

---

## PRÓXIMOS PASOS

Después de estos fixes (en orden):

1. ✅ **Hoy:** Aplicar los 3 fixes
2. ⏰ **Mañana:** Testing con 50+ operaciones
3. 📊 **Día 3:** Memory profiling
4. 🚀 **Día 4:** Ready para nuevos efectos

---

## ⚠️ ADVERTENCIAS

❌ **NO hacer:**
- Revertir cleanup de Three.js
- Agregar más caches sin límite
- Agregar variables globales en backend
- Agregar event listeners sin cleanup

✅ **SÍ hacer:**
- Test memoria después de cada cambio
- Usar app.state en lugar de globals
- Usar decoradores @lru_cache o TTLCache
- Agregar guards para graphicsPreset
- Documentar cleanup en nuevos componentes

