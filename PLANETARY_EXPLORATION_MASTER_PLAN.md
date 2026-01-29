# 🚀 ArcheoScope Planetary - Master Plan
**Rama**: planetary-exploration  
**Objetivo**: Transformar ArcheoScope en sistema de exploración planetaria para Marte y Luna  
**Fecha**: 2026-01-28

---

## 🎯 VISIÓN

**ArcheoScope Planetary** es la evolución natural del sistema:
- De detectar paisajes antropizados → a detectar paisajes habitables
- De Tierra → a Marte y Luna
- De arqueología → a exploración planetaria

**Ventaja competitiva**: El sistema ya está diseñado para ambientes extremos sin vida biológica.

---

## 📡 INSTRUMENTOS CLAVE

### Tabla de Instrumentos Planetarios

| Instrumento | Función | Ventaja para Marte/Luna | Disponibilidad |
|-------------|---------|-------------------------|----------------|
| **SAR (Radar)** | Penetración del suelo | Detecta capas subsuperficiales, hielo oculto, estructuras geológicas | ✅ SHARAD (Marte), Mini-RF (Luna) |
| **Altimetría** | Topografía precisa | Mapas de cráteres, llanuras, pendientes, zonas de aterrizaje | ✅ MOLA (Marte), LOLA (Luna) |
| **Óptico Multiespectral** | Imagen de superficie | Diferencia rocas, regolito, minerales | ✅ HiRISE, CTX (Marte), LRO NAC (Luna) |
| **Térmico** | Composición de rocas | Identifica materiales que retienen calor o hielo superficial | ✅ THEMIS (Marte), Diviner (Luna) |
| **Espectrómetro** | Composición química | Minerales, agua, hielo | ✅ CRISM (Marte), M³ (Luna) |

### Resoluciones Disponibles

#### Marte
- **HiRISE**: 25-50 cm/pixel (áreas limitadas)
- **CTX**: 6 m/pixel (cobertura amplia)
- **THEMIS**: 100 m/pixel (térmico)
- **MOLA**: 463 m/pixel (altimetría)
- **SHARAD**: 15 m penetración vertical

#### Luna
- **LRO NAC**: 0.5-2 m/pixel
- **LOLA**: 5 m/pixel (altimetría)
- **Diviner**: 200 m/pixel (térmico)
- **Mini-RF**: 30 m/pixel (radar)

---

## 🎯 APLICACIONES CON ALTO RETORNO CIENTÍFICO

### 1. Mapeo de Cráteres y Llanuras
**Técnica**: SAR + Altimetría → Relieve 3D preciso
- Detectar cráteres ocultos bajo regolito o polvo
- Mapear llanuras de impacto
- Identificar cuencas antiguas

**Valor**: Entender historia geológica

### 2. Detección de Recursos Potenciales
**Técnica**: Radar penetrante + Térmico + Espectral
- Hielo en polos o capas subsuperficiales
- Zonas de roca expuesta con minerales valiosos
- Agua congelada en cráteres permanentemente sombreados

**Valor**: Soporte a misiones tripuladas (ISRU - In-Situ Resource Utilization)

### 3. Selección de Sitios de Aterrizaje
**Técnica**: Pendientes + Rocas + Cráteres → Zonas planas y seguras
- Análisis de rugosidad del terreno
- Detección de rocas peligrosas
- Evaluación de pendientes

**Valor**: Seguridad de misiones

### 4. Análisis Geológico
**Técnica**: Estructura de capas + Sedimentación
- Entender historia del planeta/satélite
- Detectar paleolacustres (Marte)
- Mapear flujos de lava antiguos

**Valor**: Ciencia planetaria

### 5. Seguimiento de Cambios
**Técnica**: Observaciones periódicas
- Erosión por viento (Marte)
- Desplazamiento de regolito
- Cambios térmicos estacionales
- Nuevos impactos

**Valor**: Dinámica planetaria

---

## 🔬 METODOLOGÍA RECOMENDADA

### Pipeline de Procesamiento

```
1. ALTIMETRÍA (DEM Base)
   ↓
2. RADAR SAR (Penetración + Textura)
   ↓
3. MULTIESPECTRAL (Composición)
   ↓
4. TÉRMICO (Propiedades físicas)
   ↓
5. FUSIÓN MULTIMODAL
   ↓
6. ANÁLISIS COMBINADO
```

### Módulos a Desarrollar

#### 1. Generación de DEMs y Mapas 3D
```python
# backend/planetary/dem_generator.py
- Tomar altimetría de MOLA/LOLA
- Fusionar con radar SAR para mejorar precisión
- Generar modelos 3D de cráteres y llanuras
```

#### 2. Análisis de Penetración Radar
```python
# backend/planetary/radar_penetration.py
- Detectar hielo o capas densas bajo regolito
- Mapear capas geológicas no visibles ópticamente
- Estimar profundidad de penetración
```

#### 3. Fusión Multiespectral/Térmico
```python
# backend/planetary/spectral_fusion.py
- Diferenciar tipos de rocas y materiales
- Identificar zonas con interés mineral
- Clasificar composición superficial
```

#### 4. Detección Automática
```python
# backend/planetary/feature_detection.py
- Cráteres (CNN-based)
- Hielo superficial/subsuperficial
- Pendientes peligrosas
- Rocas expuestas
```

#### 5. Evaluación de Sitios de Aterrizaje
```python
# backend/planetary/landing_site_evaluator.py
- Análisis de rugosidad
- Mapa de riesgos
- Score de habitabilidad
```

---

## 🌍 ZONAS PRIORITARIAS

### Marte

#### 1. Jezero Crater (Perseverance)
- **Coords**: 18.38°N, 77.58°E
- **Interés**: Paleolacustre, delta antiguo
- **Datos**: HiRISE, CRISM, THEMIS, MOLA

#### 2. Gale Crater (Curiosity)
- **Coords**: 5.4°S, 137.8°E
- **Interés**: Monte Sharp, capas sedimentarias
- **Datos**: Cobertura completa

#### 3. Valles Marineris
- **Coords**: 14°S, 59°W
- **Interés**: Cañón gigante, estratigrafía expuesta
- **Datos**: CTX, THEMIS

#### 4. Polos (Norte y Sur)
- **Coords**: >80°N/S
- **Interés**: Hielo de agua, CO2
- **Datos**: SHARAD, THEMIS

#### 5. Hellas Planitia
- **Coords**: 42.4°S, 70.5°E
- **Interés**: Cuenca de impacto más profunda
- **Datos**: MOLA, CTX

### Luna

#### 1. Polo Sur (Artemis)
- **Coords**: >85°S
- **Interés**: Hielo en cráteres permanentemente sombreados
- **Datos**: LOLA, Mini-RF, Diviner

#### 2. Mare Tranquillitatis (Apollo 11)
- **Coords**: 0.67°N, 23.47°E
- **Interés**: Sitio histórico, llanura basáltica
- **Datos**: LRO NAC, LOLA

#### 3. Shackleton Crater
- **Coords**: 89.9°S, 0°E
- **Interés**: Hielo confirmado, sitio Artemis
- **Datos**: Mini-RF, LOLA

#### 4. Oceanus Procellarum
- **Coords**: 18.4°N, 57.4°W
- **Interés**: Mayor mare lunar, anomalías magnéticas
- **Datos**: Cobertura completa

#### 5. Tycho Crater
- **Coords**: 43.3°S, 11.2°W
- **Interés**: Cráter joven, rayos brillantes
- **Datos**: LRO NAC

---

## 🛠️ ARQUITECTURA TÉCNICA

### Estructura de Directorios

```
backend/
├── planetary/
│   ├── __init__.py
│   ├── mars/
│   │   ├── __init__.py
│   │   ├── hirise_connector.py
│   │   ├── ctx_connector.py
│   │   ├── themis_connector.py
│   │   ├── mola_connector.py
│   │   └── sharad_connector.py
│   ├── moon/
│   │   ├── __init__.py
│   │   ├── lro_nac_connector.py
│   │   ├── lola_connector.py
│   │   ├── diviner_connector.py
│   │   └── minirf_connector.py
│   ├── dem_generator.py
│   ├── radar_penetration.py
│   ├── spectral_fusion.py
│   ├── feature_detection.py
│   ├── landing_site_evaluator.py
│   └── planetary_etp_generator.py
├── api/
│   └── planetary_endpoint.py
└── ...

frontend/
├── planetary/
│   ├── mars_viewer.html
│   ├── moon_viewer.html
│   ├── planetary_map.js
│   └── 3d_terrain_viewer.js
└── ...
```

### APIs de Datos Disponibles

#### NASA PDS (Planetary Data System)
- **URL**: https://pds.nasa.gov/
- **Datos**: Todos los instrumentos de misiones NASA
- **Acceso**: Público, sin autenticación

#### USGS Astrogeology
- **URL**: https://astrogeology.usgs.gov/
- **Datos**: Mapas procesados, mosaicos
- **Acceso**: Público

#### ESA PSA (Planetary Science Archive)
- **URL**: https://archives.esac.esa.int/psa/
- **Datos**: Misiones ESA (Mars Express, etc.)
- **Acceso**: Público

#### ODE (Orbital Data Explorer)
- **URL**: https://ode.rsl.wustl.edu/
- **Datos**: Marte - todos los instrumentos
- **Acceso**: API REST pública

#### LROC QuickMap
- **URL**: https://quickmap.lroc.asu.edu/
- **Datos**: Luna - LRO completo
- **Acceso**: API pública

---

## 🤖 ALGORITMOS DE DETECCIÓN

### 1. Detección de Cráteres
**Método**: CNN (Convolutional Neural Network)
- Entrenamiento con dataset de cráteres conocidos
- Detección automática en imágenes nuevas
- Clasificación por tamaño y edad

**Dataset**: Robbins Crater Database (385,000 cráteres en Marte)

### 2. Detección de Hielo
**Método**: Fusión Radar + Térmico + Espectral
- Radar: Alta reflectividad subsuperficial
- Térmico: Baja temperatura persistente
- Espectral: Firma de agua/hielo

**Umbral**: Combinación de 3 señales

### 3. Evaluación de Pendientes
**Método**: Análisis de DEM
- Cálculo de gradiente en 8 direcciones
- Clasificación: <5° (seguro), 5-15° (moderado), >15° (peligroso)
- Mapa de rugosidad

### 4. Clasificación de Terreno
**Método**: Machine Learning (Random Forest)
- Features: Altimetría, textura SAR, espectral, térmico
- Clases: Llanura, cráter, roca expuesta, regolito, hielo
- Entrenamiento supervisado

---

## 📊 MÉTRICAS PLANETARIAS

### Planetary Exploration Score (PES)

Similar a ESS, pero adaptado:

```python
PES = (
    0.30 * habitability_score +      # Recursos (agua, minerales)
    0.25 * accessibility_score +     # Pendientes, rugosidad
    0.20 * scientific_interest +     # Geología, historia
    0.15 * safety_score +            # Riesgos de aterrizaje
    0.10 * coverage_score            # Disponibilidad de datos
)
```

### Habitability Score
- Presencia de agua/hielo
- Minerales útiles (ISRU)
- Protección contra radiación
- Temperatura moderada

### Accessibility Score
- Pendientes bajas
- Superficie lisa
- Sin rocas grandes
- Latitud favorable

### Scientific Interest
- Diversidad geológica
- Capas expuestas
- Características únicas
- Potencial astrobiológico (Marte)

### Safety Score
- Sin cráteres cercanos
- Terreno estable
- Visibilidad
- Comunicación con Tierra

---

## 🚀 ROADMAP DE IMPLEMENTACIÓN

### Fase 1: Infraestructura Base (Semana 1-2)
- [ ] Conectores a APIs planetarias (PDS, ODE, LROC)
- [ ] Descarga y cache de datos
- [ ] Generador de DEMs básico
- [ ] Visualizador 3D simple

### Fase 2: Análisis Básico (Semana 3-4)
- [ ] Detección de cráteres (CNN)
- [ ] Análisis de pendientes
- [ ] Clasificación de terreno
- [ ] Mapa de rugosidad

### Fase 3: Análisis Avanzado (Semana 5-6)
- [ ] Penetración radar (hielo)
- [ ] Fusión multiespectral
- [ ] Evaluador de sitios de aterrizaje
- [ ] PES (Planetary Exploration Score)

### Fase 4: Casos de Uso (Semana 7-8)
- [ ] Análisis de Jezero Crater
- [ ] Análisis de Polo Sur Lunar
- [ ] Comparación de sitios Artemis
- [ ] Detección de hielo en Shackleton

### Fase 5: Interfaz y Documentación (Semana 9-10)
- [ ] Frontend interactivo
- [ ] Visualización 3D avanzada
- [ ] Documentación científica
- [ ] Paper draft

---

## 🎓 CASOS DE USO INICIALES

### Caso 1: Evaluación de Sitio Artemis (Luna)
**Objetivo**: Evaluar candidatos para base lunar
**Zona**: Polo Sur Lunar (85-90°S)
**Análisis**:
- Detección de hielo (Mini-RF + Diviner)
- Pendientes y rugosidad (LOLA)
- Iluminación solar (LOLA + geometría)
- Accesibilidad desde órbita

**Output**: Ranking de sitios con PES

### Caso 2: Búsqueda de Agua en Marte
**Objetivo**: Mapear recursos hídricos
**Zona**: Polos + Latitudes medias
**Análisis**:
- SHARAD (penetración radar)
- THEMIS (temperatura)
- CRISM (espectral - minerales hidratados)
- MOLA (topografía - cuencas)

**Output**: Mapa de probabilidad de hielo

### Caso 3: Análisis de Jezero Crater
**Objetivo**: Entender contexto geológico de Perseverance
**Zona**: Jezero Crater (18.38°N, 77.58°E)
**Análisis**:
- HiRISE (morfología detallada)
- CRISM (mineralogía)
- CTX (contexto regional)
- MOLA (paleotopografía)

**Output**: Reconstrucción del paleolago

---

## 💡 VENTAJAS COMPETITIVAS

### 1. Stack Ya Probado
ArcheoScope ya maneja:
- Ambientes extremos sin vida
- Fusión multimodal
- Análisis temporal
- Inferencia de profundidad

### 2. Honestidad Estadística
El sistema no inventa señales → crítico para exploración planetaria

### 3. Escalabilidad
Diseñado para grandes áreas → perfecto para planetas enteros

### 4. Open Source
Transparencia científica total

---

## 📚 REFERENCIAS CIENTÍFICAS

### Datasets
- Robbins Crater Database (Marte)
- LRO Diviner Polar Maps (Luna)
- SHARAD Radargrams (Marte)
- CRISM Spectral Library (Marte)

### Papers Clave
- Bandfield et al. (2018) - THEMIS Mars
- Smith et al. (2010) - LOLA Lunar Topography
- Seu et al. (2007) - SHARAD Subsurface
- Paige et al. (2010) - Diviner Lunar Ice

### Herramientas
- ISIS (Integrated Software for Imagers and Spectrometers)
- GDAL (Geospatial Data Abstraction Library)
- PyPDS (Python PDS parser)

---

## 🎯 OBJETIVOS INMEDIATOS

### Sprint 1 (Esta semana)
1. Crear conectores básicos a PDS/ODE
2. Descargar datos de prueba (Jezero + Polo Sur Lunar)
3. Generar primer DEM
4. Visualización 3D básica

### Sprint 2 (Próxima semana)
1. Implementar detección de cráteres
2. Análisis de pendientes
3. Primer PES calculado
4. Comparación de 3 sitios

---

## 🚀 VISIÓN A LARGO PLAZO

**ArcheoScope Planetary** puede convertirse en:
- Herramienta estándar para selección de sitios de aterrizaje
- Sistema de evaluación de recursos planetarios
- Plataforma de análisis geológico automatizado
- Soporte a misiones tripuladas (Artemis, Mars)

**Potencial de impacto**: NASA, ESA, agencias espaciales privadas

---

**Rama**: planetary-exploration  
**Estado**: Iniciando  
**Próximo paso**: Implementar conectores a APIs planetarias

---

## 📝 NOTAS TÉCNICAS

### Diferencias con ArcheoScope Terrestre

| Aspecto | Tierra | Marte/Luna |
|---------|--------|------------|
| Atmósfera | Densa | Tenue/Nula |
| Vida | Presente | Ausente |
| Agua | Abundante | Escasa/Congelada |
| Erosión | Rápida | Lenta |
| Resolución | Alta | Variable |
| Cobertura | Completa | Parcial |
| Objetivo | Arqueología | Exploración |

### Adaptaciones Necesarias

1. **Sin señales biológicas**: NDVI no aplica
2. **Térmico diferente**: Rangos extremos (-180°C a +120°C)
3. **Radar más importante**: Penetración crítica
4. **Altimetría esencial**: Sin referencias terrestres
5. **Temporal limitado**: Menos observaciones históricas

---

**Generado por**: ArcheoScope Planetary Team  
**Versión**: 1.0 (Master Plan)  
**Fecha**: 2026-01-28
