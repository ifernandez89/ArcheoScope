## 🚀 ArcheoScope Planetary

**Rama**: `planetary-exploration`  
**Objetivo**: Sistema de exploración planetaria para Marte y Luna

---

## 🎯 Visión

ArcheoScope Planetary es la evolución natural del sistema terrestre hacia la exploración planetaria:

- **De**: Detectar paisajes antropizados en Tierra
- **A**: Detectar paisajes habitables en Marte y Luna
- **Ventaja**: El sistema ya está diseñado para ambientes extremos sin vida biológica

---

## 📡 Instrumentos Soportados

### Marte
- **HiRISE**: 25-50 cm/pixel (imágenes de alta resolución)
- **CTX**: 6 m/pixel (contexto regional)
- **THEMIS**: 100 m/pixel (térmico)
- **MOLA**: 463 m/pixel (altimetría)
- **SHARAD**: 15 m penetración (radar subsuperficial)
- **CRISM**: 18 m/pixel (espectral)

### Luna
- **LRO NAC**: 0.5-2 m/pixel (imágenes de alta resolución)
- **LOLA**: 5 m/pixel (altimetría)
- **Diviner**: 200 m/pixel (térmico)
- **Mini-RF**: 30 m/pixel (radar)
- **M³**: Espectral (mineralogía)

---

## 🎯 Aplicaciones

### 1. Selección de Sitios de Aterrizaje
- Análisis de pendientes y rugosidad
- Detección de rocas peligrosas
- Evaluación de accesibilidad
- **Caso de uso**: Artemis (Luna), Mars Sample Return

### 2. Detección de Recursos
- Hielo en polos y cráteres sombreados
- Minerales valiosos (ISRU)
- Agua congelada subsuperficial
- **Caso de uso**: Bases lunares, misiones tripuladas

### 3. Análisis Geológico
- Reconstrucción de paleolacustres
- Mapeo de flujos de lava
- Estratigrafía de cráteres
- **Caso de uso**: Ciencia planetaria

### 4. Seguimiento de Cambios
- Nuevos impactos
- Erosión eólica (Marte)
- Cambios térmicos estacionales
- **Caso de uso**: Dinámica planetaria

---

## 🚀 Quick Start

### Instalación

```bash
# Clonar rama planetary
git clone -b planetary-exploration https://github.com/ifernandez89/ArcheoScope.git
cd ArcheoScope

# Instalar dependencias
pip install -r requirements-planetary.txt
```

### Test Básico - Jezero Crater

```bash
python test_planetary_jezero.py
```

Este test verifica la cobertura de datos en Jezero Crater (sitio de Perseverance).

### Uso Programático

```python
from backend.planetary.mars.ode_connector import CTXConnector

# Crear conector
ctx = CTXConnector()

# Buscar productos en Jezero Crater
products = ctx.search_products(
    instrument='ctx',
    lat_min=17.88,
    lat_max=18.88,
    lon_min=77.08,
    lon_max=78.08
)

print(f"Encontrados {len(products)} productos CTX")
```

---

## 📊 Planetary Exploration Score (PES)

Similar a ESS (Explanatory Strangeness Score), pero adaptado para exploración planetaria:

```
PES = (
    0.30 * habitability_score +      # Recursos (agua, minerales)
    0.25 * accessibility_score +     # Pendientes, rugosidad
    0.20 * scientific_interest +     # Geología, historia
    0.15 * safety_score +            # Riesgos de aterrizaje
    0.10 * coverage_score            # Disponibilidad de datos
)
```

### Interpretación

| PES | Interpretación | Acción |
|-----|----------------|--------|
| 0.00-0.30 | Bajo interés | Descartar |
| 0.30-0.50 | Interés moderado | Monitorear |
| 0.50-0.70 | Alto interés | Análisis detallado |
| 0.70-1.00 | Interés crítico | Prioridad máxima |

---

## 🗺️ Zonas Prioritarias

### Marte

#### 1. Jezero Crater (Perseverance)
- **Coords**: 18.38°N, 77.58°E
- **Interés**: Paleolacustre, delta antiguo
- **Estado**: ✅ Datos completos

#### 2. Gale Crater (Curiosity)
- **Coords**: 5.4°S, 137.8°E
- **Interés**: Monte Sharp, capas sedimentarias
- **Estado**: ✅ Datos completos

#### 3. Valles Marineris
- **Coords**: 14°S, 59°W
- **Interés**: Cañón gigante, estratigrafía
- **Estado**: ⚠️ Cobertura parcial

#### 4. Polos (Norte y Sur)
- **Coords**: >80°N/S
- **Interés**: Hielo de agua y CO2
- **Estado**: ✅ SHARAD disponible

### Luna

#### 1. Polo Sur (Artemis)
- **Coords**: >85°S
- **Interés**: Hielo en cráteres sombreados
- **Estado**: ✅ LOLA + Mini-RF

#### 2. Shackleton Crater
- **Coords**: 89.9°S, 0°E
- **Interés**: Hielo confirmado
- **Estado**: ✅ Datos completos

#### 3. Mare Tranquillitatis (Apollo 11)
- **Coords**: 0.67°N, 23.47°E
- **Interés**: Sitio histórico
- **Estado**: ✅ LRO NAC

---

## 🛠️ Arquitectura

```
backend/planetary/
├── mars/
│   ├── ode_connector.py       # Conector ODE (todos los instrumentos)
│   ├── hirise_connector.py    # HiRISE específico
│   ├── ctx_connector.py       # CTX específico
│   └── ...
├── moon/
│   ├── lroc_connector.py      # LRO NAC
│   ├── lola_connector.py      # LOLA altimetría
│   └── ...
├── dem_generator.py           # Generación de DEMs
├── radar_penetration.py       # Análisis radar
├── feature_detection.py       # Detección de cráteres, hielo
├── landing_site_evaluator.py # Evaluación de sitios
└── planetary_etp_generator.py # Perfiles planetarios
```

---

## 📚 APIs de Datos

### NASA PDS (Planetary Data System)
- **URL**: https://pds.nasa.gov/
- **Acceso**: Público, sin autenticación
- **Datos**: Todos los instrumentos NASA

### ODE (Orbital Data Explorer)
- **URL**: https://ode.rsl.wustl.edu/
- **Acceso**: API REST pública
- **Datos**: Marte completo

### LROC QuickMap
- **URL**: https://quickmap.lroc.asu.edu/
- **Acceso**: API pública
- **Datos**: Luna - LRO completo

### USGS Astrogeology
- **URL**: https://astrogeology.usgs.gov/
- **Acceso**: Público
- **Datos**: Mapas procesados, mosaicos

---

## 🎓 Casos de Uso

### Caso 1: Evaluación de Sitio Artemis
```python
from backend.planetary.moon.lola_connector import LOLAConnector
from backend.planetary.landing_site_evaluator import LandingSiteEvaluator

# Analizar Polo Sur Lunar
evaluator = LandingSiteEvaluator()
sites = evaluator.evaluate_region(
    target='moon',
    lat_min=-90,
    lat_max=-85,
    lon_min=0,
    lon_max=360
)

# Ranking de sitios
for site in sites[:5]:
    print(f"{site.name}: PES = {site.pes:.3f}")
```

### Caso 2: Búsqueda de Agua en Marte
```python
from backend.planetary.mars.sharad_connector import SHARADConnector
from backend.planetary.radar_penetration import RadarAnalyzer

# Analizar polos marcianos
analyzer = RadarAnalyzer()
ice_map = analyzer.detect_subsurface_ice(
    lat_min=80,
    lat_max=90,
    lon_min=0,
    lon_max=360
)

# Mapa de probabilidad
ice_map.save('mars_north_pole_ice.tif')
```

---

## 🚀 Roadmap

### Fase 1: Infraestructura (Semanas 1-2) ✅
- [x] Conectores a APIs planetarias
- [x] Test básico Jezero Crater
- [ ] Cache de datos
- [ ] Visualizador 3D

### Fase 2: Análisis Básico (Semanas 3-4)
- [ ] Detección de cráteres (CNN)
- [ ] Análisis de pendientes
- [ ] Clasificación de terreno
- [ ] Mapa de rugosidad

### Fase 3: Análisis Avanzado (Semanas 5-6)
- [ ] Penetración radar (hielo)
- [ ] Fusión multiespectral
- [ ] Evaluador de sitios
- [ ] PES completo

### Fase 4: Casos de Uso (Semanas 7-8)
- [ ] Análisis Jezero completo
- [ ] Polo Sur Lunar
- [ ] Comparación sitios Artemis
- [ ] Detección hielo Shackleton

---

## 📖 Documentación

- [Master Plan](PLANETARY_EXPLORATION_MASTER_PLAN.md) - Plan completo del proyecto
- [API Reference](docs/planetary_api.md) - Referencia de APIs
- [Examples](examples/planetary/) - Ejemplos de uso

---

## 🤝 Contribuir

Este es un proyecto de investigación abierto. Contribuciones bienvenidas:

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añadir nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 🙏 Agradecimientos

- NASA PDS por datos abiertos
- USGS Astrogeology por herramientas
- Comunidad científica planetaria

---

## 📧 Contacto

**ArcheoScope Planetary Team**  
Rama: `planetary-exploration`  
Basado en ArcheoScope v1.0

---

**Estado**: 🚧 En desarrollo activo  
**Última actualización**: 2026-01-28
