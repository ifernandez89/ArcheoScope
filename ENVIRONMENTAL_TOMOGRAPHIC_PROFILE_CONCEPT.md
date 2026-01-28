# Environmental Tomographic Profile (ETP) - Concepto Oficial

## 🎯 DEFINICIÓN OFICIAL

**Environmental Tomographic Profile (ETP)**: Sistema de análisis volumétrico que genera perfiles explicables de territorios arqueológicos mediante cortes transversales multidimensionales (XZ/YZ) que integran datos superficiales, subsuperficiales y temporales para crear una representación tomográfica completa del paisaje arqueológico.

---

## 🔄 TRANSFORMACIÓN CONCEPTUAL

### ANTES: Sistema Detector
```
INPUT: Coordenadas → PROCESO: Análisis → OUTPUT: "Sitio detectado/no detectado"
```

### DESPUÉS: Sistema Explicador
```
INPUT: Territorio → PROCESO: Tomografía → OUTPUT: "Perfil explicable del paisaje"
```

---

## 📐 COMPONENTES DEL ETP

### 1. Cortes Tomográficos
- **Corte XZ** (Longitudinal): Perfil Este-Oeste con profundidad
- **Corte YZ** (Latitudinal): Perfil Norte-Sur con profundidad  
- **Corte XY** (Superficial): Vista cenital por capas de profundidad
- **Corte Temporal**: Evolución del territorio en el tiempo

### 2. Capas de Información
- **Superficie (0m)**: Topografía, vegetación, térmico
- **Subsuperficie (-0.5m a -5m)**: Penetración SAR, anomalías enterradas
- **Profundidad (-5m a -20m)**: Estructuras profundas, geología
- **Temporal**: Cambios estacionales, históricos, paleoclimáticos

### 3. Métricas Volumétricas
- **Densidad arqueológica por m³**
- **Gradiente de anomalías por profundidad**
- **Coherencia espacial 3D**
- **Persistencia temporal**

---

## 🔬 EVOLUCIÓN DEL ESS (Environmental Strangeness Score)

### ESS Tradicional (2D)
```python
ESS = Σ(anomalías_superficiales) / área_2d
```

### ESS Volumétrico (3D) - NUEVO
```python
ESS_volumetric = Σ(anomalías_por_capa * peso_profundidad) / volumen_3d

Donde:
- Capa_superficie: peso = 1.0
- Capa_subsuperficie: peso = 0.8  
- Capa_profunda: peso = 0.6
- Factor_coherencia_3d: multiplicador de consistencia espacial
```

### ESS Temporal (4D) - NUEVO
```python
ESS_temporal = ESS_volumetric * factor_persistencia_temporal

Donde:
- factor_persistencia = consistencia_anomalías_en_tiempo
- Incluye: estacional, anual, decenal, histórico
```

---

## 🏛️ APLICACIÓN ARQUEOLÓGICA

### Casos de Uso Transformados

#### ANTES: "¿Hay un sitio aquí?"
- Respuesta binaria: Sí/No
- Confianza: Alta/Media/Baja
- Evidencia: Lista de anomalías

#### DESPUÉS: "¿Qué cuenta este territorio?"
- **Perfil estratigráfico**: Qué hay en cada capa
- **Historia ocupacional**: Cuándo fue ocupado y abandonado
- **Función territorial**: Para qué se usó cada zona
- **Evolución paisajística**: Cómo cambió en el tiempo

### Ejemplos Concretos

#### ETP de Giza
```
Corte XZ (Este-Oeste):
- Superficie: Pirámides visibles, calzadas
- -2m: Cámaras funerarias, pasadizos
- -5m: Cimientos, sistemas de drenaje
- Temporal: Construcción Dinastía IV, modificaciones posteriores
```

#### ETP de Angkor
```
Corte YZ (Norte-Sur):
- Superficie: Templos emergentes, vegetación
- -1m: Muros enterrados, canales
- -3m: Sistemas hidráulicos complejos
- Temporal: Expansión siglos IX-XV, abandono gradual
```

---

## 🛰️ INTEGRACIÓN CON 15 INSTRUMENTOS

### Asignación por Profundidad

#### Superficie (0m)
- **Sentinel-2**: NDVI, multispectral
- **VIIRS**: Térmico diario, fuegos
- **SRTM**: Topografía detallada

#### Subsuperficie (-0.5m a -5m)
- **Sentinel-1**: SAR C-band penetración
- **PALSAR-2**: SAR L-band penetración profunda
- **ICESat-2**: Anomalías de elevación

#### Profundidad (-5m a -20m)
- **PALSAR-2**: Máxima penetración L-band
- **Análisis geofísico**: Inferencia de estructuras profundas

#### Temporal (Todas las capas)
- **ERA5**: Contexto climático histórico
- **CHIRPS**: Patrones de precipitación
- **Landsat**: Archivo temporal 1970-presente
- **MODIS**: Tendencias térmicas 2000-presente

---

## 📊 VISUALIZACIÓN REVOLUCIONARIA

### Vistas Tomográficas

#### 1. Vista de Cortes Transversales
```
    CORTE XZ (Longitudinal)
    ┌─────────────────────────┐ ← Superficie
    │ ████░░░░████░░░░████    │ ← -1m
    │ ██████░░██████░░██████  │ ← -2m  
    │ ████████████████████    │ ← -3m
    └─────────────────────────┘
    W                        E
```

#### 2. Vista Volumétrica 3D
```
Representación isométrica con:
- Capas de profundidad transparentes
- Gradientes de color por intensidad de anomalía
- Vectores de flujo temporal
- Puntos de máxima coherencia arqueológica
```

#### 3. Vista Temporal Animada
```
Timeline interactivo:
- Slider temporal: -2000 años → presente
- Capas que aparecen/desaparecen según período
- Evolución de anomalías en tiempo real
- Correlación con eventos climáticos
```

### Métricas Visuales

#### Dashboard ETP
```
┌─ PERFIL TOMOGRÁFICO ─────────────────────┐
│                                          │
│ ESS Superficial:    0.73 ████████░░      │
│ ESS Volumétrico:    0.68 ███████░░░      │  
│ ESS Temporal:       0.71 ████████░░      │
│                                          │
│ Coherencia 3D:      0.82 █████████░      │
│ Persistencia:       0.76 ████████░░      │
│                                          │
└──────────────────────────────────────────┘

┌─ CORTES TRANSVERSALES ──────────────────┐
│                                          │
│ [Vista XZ] [Vista YZ] [Vista XY] [4D]    │
│                                          │
│ ████████████████████████████████████     │
│ ██████░░░░██████░░░░██████░░░░██████     │
│ ████░░░░░░░░████░░░░░░░░████░░░░░░░░     │
│ ██░░░░░░░░░░░░██░░░░░░░░░░░░██░░░░░░     │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Estructura de Datos ETP

```python
@dataclass
class EnvironmentalTomographicProfile:
    """Perfil tomográfico ambiental completo."""
    
    # Identificación
    territory_id: str
    bounds: BoundingBox
    resolution_m: float
    
    # Cortes tomográficos
    xz_profile: TomographicSlice  # Longitudinal
    yz_profile: TomographicSlice  # Latitudinal  
    xy_profiles: List[TomographicSlice]  # Por profundidad
    temporal_profile: TemporalSlice
    
    # ESS evolucionado
    ess_superficial: float
    ess_volumetrico: float
    ess_temporal: float
    
    # Métricas 3D
    coherencia_3d: float
    persistencia_temporal: float
    densidad_arqueologica_m3: float
    
    # Interpretación
    narrative_explanation: str
    occupational_history: List[OccupationPeriod]
    territorial_function: TerritorialFunction
    landscape_evolution: LandscapeEvolution

@dataclass 
class TomographicSlice:
    """Corte tomográfico individual."""
    
    slice_type: str  # 'XZ', 'YZ', 'XY'
    depth_range: Tuple[float, float]  # metros
    
    # Datos por capa
    layers: List[TomographicLayer]
    
    # Anomalías detectadas
    anomalies: List[VolumetricAnomaly]
    
    # Métricas del corte
    slice_ess: float
    coherence_score: float
    
@dataclass
class TomographicLayer:
    """Capa individual en corte tomográfico."""
    
    depth_m: float
    instruments_data: Dict[str, Any]  # Datos de cada instrumento
    anomaly_intensity: float
    archaeological_probability: float
    
@dataclass
class VolumetricAnomaly:
    """Anomalía volumétrica detectada."""
    
    center_3d: Tuple[float, float, float]  # x, y, z
    extent_3d: Tuple[float, float, float]  # ancho, largo, profundidad
    intensity: float
    archaeological_type: str  # 'structure', 'burial', 'activity_area'
    temporal_range: Tuple[int, int]  # años
    confidence: float
```

### Pipeline de Procesamiento

```python
class ETProfileGenerator:
    """Generador de perfiles tomográficos ambientales."""
    
    def __init__(self, integrator_15_instruments):
        self.integrator = integrator_15_instruments
        self.depth_layers = [0, -0.5, -1, -2, -3, -5, -10, -20]  # metros
        
    async def generate_etp(self, bounds: BoundingBox) -> EnvironmentalTomographicProfile:
        """Generar perfil tomográfico completo."""
        
        # 1. Adquisición de datos por capas
        layered_data = await self._acquire_layered_data(bounds)
        
        # 2. Generación de cortes tomográficos
        xz_profile = self._generate_xz_slice(layered_data, bounds)
        yz_profile = self._generate_yz_slice(layered_data, bounds)
        xy_profiles = self._generate_xy_slices(layered_data, bounds)
        
        # 3. Análisis temporal
        temporal_profile = await self._generate_temporal_slice(bounds)
        
        # 4. Cálculo de ESS evolucionado
        ess_superficial = self._calculate_surface_ess(layered_data[0])
        ess_volumetrico = self._calculate_volumetric_ess(layered_data)
        ess_temporal = self._calculate_temporal_ess(temporal_profile)
        
        # 5. Métricas 3D
        coherencia_3d = self._calculate_3d_coherence(layered_data)
        persistencia = self._calculate_temporal_persistence(temporal_profile)
        
        # 6. Interpretación narrativa
        narrative = self._generate_territorial_narrative(
            xz_profile, yz_profile, temporal_profile
        )
        
        return EnvironmentalTomographicProfile(
            territory_id=f"ETP_{bounds.center_lat}_{bounds.center_lon}",
            bounds=bounds,
            xz_profile=xz_profile,
            yz_profile=yz_profile,
            xy_profiles=xy_profiles,
            temporal_profile=temporal_profile,
            ess_superficial=ess_superficial,
            ess_volumetrico=ess_volumetrico,
            ess_temporal=ess_temporal,
            coherencia_3d=coherencia_3d,
            persistencia_temporal=persistencia,
            narrative_explanation=narrative
        )
```

---

## 🎨 INTERFAZ VISUAL REVOLUCIONARIA

### Componentes de UI

#### 1. Visor Tomográfico Principal
```html
<div class="etp-viewer">
    <!-- Controles de navegación -->
    <div class="etp-controls">
        <button class="slice-btn active" data-slice="xz">Corte XZ</button>
        <button class="slice-btn" data-slice="yz">Corte YZ</button>
        <button class="slice-btn" data-slice="xy">Capas XY</button>
        <button class="slice-btn" data-slice="4d">Vista 4D</button>
    </div>
    
    <!-- Visualizador principal -->
    <div class="tomographic-display">
        <canvas id="etp-canvas" width="800" height="600"></canvas>
        
        <!-- Controles de profundidad -->
        <div class="depth-slider">
            <input type="range" min="0" max="20" value="0" id="depth-control">
            <label>Profundidad: <span id="depth-value">0m</span></label>
        </div>
        
        <!-- Timeline temporal -->
        <div class="temporal-slider">
            <input type="range" min="-2000" max="2024" value="2024" id="time-control">
            <label>Año: <span id="time-value">2024</span></label>
        </div>
    </div>
    
    <!-- Panel de métricas -->
    <div class="etp-metrics">
        <div class="metric">
            <label>ESS Superficial</label>
            <div class="progress-bar">
                <div class="progress" style="width: 73%"></div>
            </div>
            <span>0.73</span>
        </div>
        
        <div class="metric">
            <label>ESS Volumétrico</label>
            <div class="progress-bar">
                <div class="progress" style="width: 68%"></div>
            </div>
            <span>0.68</span>
        </div>
        
        <div class="metric">
            <label>ESS Temporal</label>
            <div class="progress-bar">
                <div class="progress" style="width: 71%"></div>
            </div>
            <span>0.71</span>
        </div>
    </div>
</div>
```

#### 2. Panel Narrativo
```html
<div class="territorial-narrative">
    <h3>Explicación del Territorio</h3>
    
    <div class="narrative-section">
        <h4>Historia Ocupacional</h4>
        <div class="timeline">
            <div class="period" data-start="-500" data-end="200">
                <span class="period-label">Ocupación Inicial</span>
                <p>Evidencia de asentamiento temprano con estructuras simples...</p>
            </div>
            <div class="period" data-start="200" data-end="800">
                <span class="period-label">Expansión</span>
                <p>Construcción de estructuras monumentales y sistemas hidráulicos...</p>
            </div>
        </div>
    </div>
    
    <div class="narrative-section">
        <h4>Función Territorial</h4>
        <ul class="function-list">
            <li><strong>Ceremonial:</strong> Templos y plazas en sector norte</li>
            <li><strong>Residencial:</strong> Estructuras domésticas en periferia</li>
            <li><strong>Productivo:</strong> Sistemas agrícolas en zona sur</li>
        </ul>
    </div>
    
    <div class="narrative-section">
        <h4>Evolución del Paisaje</h4>
        <p>El territorio muestra una transformación gradual desde un paisaje natural 
        hacia un sistema cultural complejo, con evidencia de manejo intensivo del agua 
        y modificación topográfica significativa...</p>
    </div>
</div>
```

---

## 🚀 IMPACTO TRANSFORMACIONAL

### Para la Arqueología
- **Análisis territorial** en lugar de detección puntual
- **Comprensión diacrónica** del paisaje
- **Integración multidisciplinaria** automática
- **Narrativas explicables** basadas en datos

### Para ArcheoScope
- **Diferenciación tecnológica** única en el mercado
- **Valor científico** exponencialmente mayor
- **Aplicabilidad** a gestión territorial y patrimonio
- **Escalabilidad** a análisis regionales

### Para los Usuarios
- **Comprensión intuitiva** del territorio
- **Toma de decisiones** informada para excavación
- **Planificación** de investigación optimizada
- **Comunicación** efectiva con stakeholders

---

## 📋 PLAN DE IMPLEMENTACIÓN

### Fase 1: Core ETP (2 semanas)
- [ ] Implementar estructura de datos ETP
- [ ] Desarrollar generador de cortes tomográficos
- [ ] Integrar con sistema de 15 instrumentos
- [ ] Calcular ESS volumétrico y temporal

### Fase 2: Visualización (2 semanas)  
- [ ] Desarrollar visor tomográfico interactivo
- [ ] Implementar controles de profundidad y tiempo
- [ ] Crear sistema de renderizado 3D
- [ ] Diseñar dashboard de métricas

### Fase 3: Narrativa (1 semana)
- [ ] Desarrollar generador de narrativas
- [ ] Implementar análisis de función territorial
- [ ] Crear sistema de historia ocupacional
- [ ] Integrar con visualización

### Fase 4: Testing (1 semana)
- [ ] Probar con sitios conocidos
- [ ] Validar narrativas generadas
- [ ] Optimizar performance
- [ ] Documentar casos de uso

---

## 🎯 RESULTADO ESPERADO

**ArcheoScope ETP transformará completamente la experiencia del usuario:**

### ANTES
```
Usuario: "¿Hay algo arqueológico en estas coordenadas?"
Sistema: "Sí, probabilidad 73%, 4 instrumentos convergentes"
```

### DESPUÉS  
```
Usuario: "¿Qué me cuenta este territorio?"
Sistema: "Este paisaje muestra una ocupación continua de 800 años, 
con una fase inicial ceremonial (siglos III-V), seguida de expansión 
residencial (siglos VI-VIII) y desarrollo de sistemas hidráulicos 
complejos (siglos IX-X). La evidencia volumétrica indica estructuras 
monumentales en superficie, sistemas de canales a -2m, y posibles 
cámaras funerarias a -5m. El análisis climático sugiere que el 
abandono gradual (siglo XI) coincide con un período de sequía 
documentado en los registros de precipitación."
```

**¡ESTO CAMBIA TODO! 🌍✨**