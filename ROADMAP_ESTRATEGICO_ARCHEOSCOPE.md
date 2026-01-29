# 🗺️ ROADMAP ESTRATÉGICO - ArcheoScope

## ESTADO ACTUAL: CORE COMPLETO ✅

**Sistema operativo**: 5/5 instrumentos CORE funcionando  
**Capacidad**: Detección multi-ambiente (desierto, altiplano, mediterráneo)  
**Honestidad**: ESS calibrado, no infla scores

---

## 🎯 3 DIRECCIONES ESTRATÉGICAS

### 🥇 OPCIÓN A — ArcheoScope WATER (agua/paleohidrografía)

**Enfoque**: Detección de estructuras relacionadas con agua

**Stack instrumental**:
- ✅ SAR (penetración sedimentos)
- ✅ Térmico (humedad residual)
- ✅ NDVI (vegetación riparia)
- 🆕 CHIRPS (precipitación histórica)
- 🆕 ERA5 (paleoclima)
- 🆕 Copernicus Marine (costas fósiles)

**Casos de uso**:
- 🌊 Canales de irrigación antiguos
- 🏛️ Acueductos romanos
- 🏺 Cisternas subterráneas
- 🌴 Oasis abandonados
- 🚢 Puertos secos
- 🏖️ Costas fósiles (Doggerland)

**Ventajas**:
- ✅ Nicho claro (agua = civilización)
- ✅ Instrumentos ya disponibles
- ✅ Casos icónicos (Petra, Nazca, Angkor)
- ✅ Validación fácil (canales visibles)

**Complejidad**: MEDIA (2-3 semanas)

**Impacto científico**: ALTO (agua = asentamientos)

---

### 🥈 OPCIÓN B — ArcheoScope ISE (interior/subsuperficie)

**Enfoque**: Detección de estructuras internas (cámaras, vacíos, rellenos)

**Stack instrumental**:
- ✅ SAR (penetración profunda)
- ✅ Térmico (inercia térmica)
- ✅ DEM (anomalías topográficas)
- ❌ NDVI (ignorar vegetación)
- 🆕 GPR simulado (vacíos)
- 🆕 Gravimetría (densidad)

**Casos de uso**:
- 🔺 Cámaras en pirámides
- 🏛️ Tells (capas superpuestas)
- ⛰️ Montículos artificiales
- 🕳️ Túneles y galerías
- 🏺 Rellenos constructivos
- 🧱 Discontinuidades internas

**Ventajas**:
- ✅ Nicho ultra-específico
- ✅ Casos icónicos (Giza, Teotihuacán)
- ✅ Menos ruido (ignora vegetación)
- ✅ Validación directa (GPR real)

**Complejidad**: ALTA (4-6 semanas)

**Impacto científico**: MUY ALTO (cámaras ocultas)

**Riesgo**: Requiere validación GPR real

---

### 🥉 OPCIÓN C — ArcheoScope SCALE (escalado industrial)

**Enfoque**: Plataforma continental de detección masiva

**Stack técnico**:
- 🆕 Paralelización (multi-región)
- 🆕 Cache distribuido (tiles)
- 🆕 Heatmaps continentales
- 🆕 API pública
- 🆕 Dashboard interactivo
- 🆕 Sistema de priorización

**Casos de uso**:
- 🌍 Escaneo completo de Egipto
- 🗺️ Mapa de anomalías de Perú
- 📊 Ranking de candidatos por país
- 🔍 Búsqueda por tipo de estructura
- 📈 Evolución temporal (cambios)
- 🤝 Colaboración multi-usuario

**Ventajas**:
- ✅ Impacto masivo
- ✅ Plataforma vs herramienta
- ✅ Monetizable
- ✅ Escalable

**Complejidad**: MUY ALTA (3-6 meses)

**Impacto científico**: MEDIO (cantidad > calidad)

**Riesgo**: Infraestructura costosa

---

## 📊 COMPARACIÓN

| Criterio | WATER | ISE | SCALE |
|----------|-------|-----|-------|
| **Complejidad** | Media | Alta | Muy Alta |
| **Tiempo** | 2-3 sem | 4-6 sem | 3-6 meses |
| **Impacto científico** | Alto | Muy Alto | Medio |
| **Nicho** | Claro | Ultra-específico | General |
| **Validación** | Fácil | Media | Difícil |
| **Riesgo** | Bajo | Medio | Alto |
| **Monetización** | Media | Alta | Muy Alta |

---

## 🎯 RECOMENDACIÓN

### OPCIÓN A (WATER) — Mejor balance

**Por qué**:
1. ✅ Nicho claro y defendible
2. ✅ Instrumentos ya disponibles (CHIRPS, ERA5, Copernicus)
3. ✅ Casos icónicos para validar (Petra, Nazca, Angkor)
4. ✅ Complejidad manejable (2-3 semanas)
5. ✅ Impacto científico alto (agua = civilización)
6. ✅ Validación fácil (canales visibles en imágenes)

**Implementación**:
```python
# Módulo: backend/water/water_detection.py

class WaterArchaeologyDetector:
    """
    Detector especializado en estructuras relacionadas con agua.
    
    Detecta:
    - Canales de irrigación
    - Acueductos
    - Cisternas
    - Oasis abandonados
    - Puertos secos
    - Costas fósiles
    """
    
    def __init__(self):
        self.sar = Sentinel1SAR()
        self.thermal = LandsatThermal()
        self.ndvi = Sentinel2NDVI()
        self.chirps = CHIRPSConnector()
        self.era5 = ERA5Connector()
        self.copernicus = CopernicusMarineConnector()
    
    async def detect_irrigation_channels(self, bbox):
        """Detectar canales de irrigación antiguos."""
        
        # 1. SAR: Penetración sedimentos (canales rellenos)
        sar_data = await self.sar.get_data(bbox)
        
        # 2. Térmico: Humedad residual (canales retienen agua)
        thermal_data = await self.thermal.get_data(bbox)
        
        # 3. NDVI: Vegetación riparia (líneas verdes)
        ndvi_data = await self.ndvi.get_data(bbox)
        
        # 4. CHIRPS: Precipitación histórica (contexto)
        precip_data = await self.chirps.get_precipitation_history(bbox)
        
        # 5. Análisis integrado
        channels = self._analyze_water_signatures(
            sar_data, thermal_data, ndvi_data, precip_data
        )
        
        return channels
```

**Casos de validación**:
1. **Petra (Jordania)**: Sistema hidráulico nabateo
2. **Nazca (Perú)**: Acueductos subterráneos (puquios)
3. **Angkor (Camboya)**: Red de canales y reservorios
4. **Qanat (Irán)**: Túneles de irrigación
5. **Doggerland (Mar del Norte)**: Costa fósil

---

## 🚀 PRÓXIMOS PASOS (si eliges WATER)

### Fase 1: Prototipo (1 semana)
1. Crear módulo `backend/water/water_detection.py`
2. Implementar `detect_irrigation_channels()`
3. Integrar CHIRPS + ERA5 + Copernicus
4. Test en Petra (caso conocido)

### Fase 2: Validación (1 semana)
1. Test en 5 casos icónicos
2. Calibrar umbrales
3. Documentar firmas espectrales
4. Generar reporte científico

### Fase 3: Integración (1 semana)
1. Agregar a pipeline principal
2. Crear endpoint `/analyze/water`
3. Frontend: modo "Water Archaeology"
4. Documentación completa

**Tiempo total**: 3 semanas  
**Riesgo**: Bajo  
**Impacto**: Alto

---

## 💡 ALTERNATIVA: OPCIÓN B (ISE)

**Si prefieres ISE** (cámaras/vacíos):

**Ventajas**:
- Nicho ultra-específico (nadie más lo hace)
- Casos icónicos (Giza, Teotihuacán)
- Impacto científico muy alto

**Desventajas**:
- Complejidad alta (GPR simulado)
- Validación difícil (requiere GPR real)
- Tiempo: 4-6 semanas

**Implementación**:
```python
class SubsurfaceVoidDetector:
    """
    Detector de vacíos y cámaras internas.
    
    Ignora vegetación, enfoca en:
    - Anomalías SAR (discontinuidades)
    - Inercia térmica (vacíos)
    - Anomalías topográficas (hundimientos)
    """
    
    async def detect_internal_voids(self, bbox):
        # SAR: Penetración profunda
        # Térmico: Inercia térmica diferencial
        # DEM: Micro-hundimientos
        # GPR simulado: Vacíos
        pass
```

---

## 🎯 DECISIÓN REQUERIDA

**¿Qué dirección prefieres?**

1. **OPCIÓN A (WATER)** - Balance perfecto, 3 semanas
2. **OPCIÓN B (ISE)** - Alto impacto, 6 semanas
3. **OPCIÓN C (SCALE)** - Plataforma, 6 meses
4. **Ninguna** - Sistema actual es suficiente

---

## 📝 NOTAS IMPORTANTES

### Sistema actual (sin elegir ninguna opción)

**Ya puede detectar**:
- ✅ Anomalías vegetación (NDVI)
- ✅ Anomalías subsuperficie (SAR)
- ✅ Anomalías térmicas (Landsat)
- ✅ Anomalías topográficas (DEM)
- ✅ Contexto climático (ERA5)

**Es suficiente para**:
- Desiertos (Egipto, Perú)
- Altiplano (Andes, Tíbet)
- Zonas áridas (Medio Oriente)

**NO especializado en**:
- Agua (canales, acueductos)
- Vacíos (cámaras internas)
- Escala continental

---

## ✅ CONCLUSIÓN

**Sistema actual**: ✅ Operativo y científicamente defendible

**Próximo paso**: Elegir especialización (WATER, ISE, o SCALE)

**Recomendación**: OPCIÓN A (WATER) por balance tiempo/impacto

**Alternativa válida**: Ninguna - sistema actual es suficiente

---

**Fecha**: 2026-01-29  
**Estado**: Esperando decisión estratégica  
**CORE**: 100% operativo ✅
