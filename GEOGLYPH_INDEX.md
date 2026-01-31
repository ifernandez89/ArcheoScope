# 📚 Índice de Documentación - Sistema de Detección de Geoglifos

## 🎯 Inicio Rápido

### Para Empezar AHORA
1. **Leer primero**: [`GEOGLYPH_FINAL_SUMMARY.md`](GEOGLYPH_FINAL_SUMMARY.md) (5 min)
2. **Probar**: `python test_geoglyph_detection.py` (2 min)
3. **Ejemplos**: `python ejemplo_geoglyph_practico.py` (5 min)
4. **API**: `python backend/api/main.py` → `http://localhost:8003/docs`

---

## 📖 Documentación Completa

### 1. Resúmenes Ejecutivos

| Archivo | Descripción | Tiempo de Lectura |
|---------|-------------|-------------------|
| [`GEOGLYPH_FINAL_SUMMARY.md`](GEOGLYPH_FINAL_SUMMARY.md) | **EMPEZAR AQUÍ** - Resumen completo de todo | 10 min |
| [`GEOGLYPH_IMPLEMENTATION_SUMMARY.md`](GEOGLYPH_IMPLEMENTATION_SUMMARY.md) | Resumen de implementación técnica | 8 min |

### 2. Guías Detalladas

| Archivo | Descripción | Tiempo de Lectura |
|---------|-------------|-------------------|
| [`GEOGLYPH_DETECTION_GUIDE.md`](GEOGLYPH_DETECTION_GUIDE.md) | **Guía completa** con ejemplos y referencias | 30 min |

### 3. Código

| Archivo | Descripción | Tipo |
|---------|-------------|------|
| [`backend/geoglyph_detector.py`](backend/geoglyph_detector.py) | Detector principal | Core |
| [`backend/api/geoglyph_endpoint.py`](backend/api/geoglyph_endpoint.py) | API REST endpoints | API |
| [`test_geoglyph_detection.py`](test_geoglyph_detection.py) | Suite de tests | Tests |
| [`ejemplo_geoglyph_practico.py`](ejemplo_geoglyph_practico.py) | Ejemplos prácticos | Ejemplos |

---

## 🚀 Flujo de Trabajo Recomendado

### Para Usuarios Nuevos

```
1. GEOGLYPH_FINAL_SUMMARY.md
   ↓
2. python test_geoglyph_detection.py
   ↓
3. python ejemplo_geoglyph_practico.py
   ↓
4. python backend/api/main.py
   ↓
5. http://localhost:8003/docs
   ↓
6. GEOGLYPH_DETECTION_GUIDE.md (para profundizar)
```

### Para Desarrolladores

```
1. GEOGLYPH_IMPLEMENTATION_SUMMARY.md
   ↓
2. backend/geoglyph_detector.py (revisar código)
   ↓
3. backend/api/geoglyph_endpoint.py (revisar API)
   ↓
4. test_geoglyph_detection.py (entender tests)
   ↓
5. GEOGLYPH_DETECTION_GUIDE.md (referencia completa)
```

### Para Investigadores

```
1. GEOGLYPH_FINAL_SUMMARY.md (contexto)
   ↓
2. GEOGLYPH_DETECTION_GUIDE.md (metodología)
   ↓
3. python ejemplo_geoglyph_practico.py (ver ejemplos)
   ↓
4. Adaptar para tus coordenadas específicas
```

---

## 📊 Contenido por Documento

### GEOGLYPH_FINAL_SUMMARY.md
- ✅ Resumen de implementación completa
- ✅ Las 7 especificaciones implementadas
- ✅ Ejemplos de resultados reales
- ✅ Comandos rápidos
- ✅ Próximos pasos

### GEOGLYPH_IMPLEMENTATION_SUMMARY.md
- ✅ Capacidades implementadas
- ✅ Endpoints API
- ✅ Scoring cultural
- ✅ Zonas de exploración
- ✅ Roadmap futuro
- ✅ Checklist de implementación

### GEOGLYPH_DETECTION_GUIDE.md
- ✅ Reglas de resolución espacial
- ✅ Métricas automáticas
- ✅ Análisis volcánico e hidrológico
- ✅ Alineaciones astronómicas
- ✅ Modos operativos
- ✅ Zonas prometedoras
- ✅ Referencias científicas
- ✅ Consideraciones éticas

---

## 🎓 Conceptos Clave

### Resolución Espacial
> **REGLA DE ORO**: Si no ves los extremos con claridad, NO entrenes todavía.

- Óptico: ≤ 0.5-1 m/pixel (ideal: WorldView/Pleiades)
- DEM: ≥ 10-30 m (SRTM/NASADEM)

### Scoring Cultural
```python
cultural_score = (
    form_score * 0.25 +        # Simetría + aspect ratio
    orientation_score * 0.25 + # Orientaciones + alineaciones
    context_score * 0.20 +     # Volcánico
    hydrology_score * 0.30     # Hídrico (ORO - mayor peso)
)
```

### Modos Operativos

| Modo | Min Score | Max FP | Uso |
|------|-----------|--------|-----|
| Científico | 0.75 | 15% | Papers |
| Explorador | 0.50 | 35% | Descubrimientos |
| Cognitivo | 0.30 | 50% | Hipótesis |

---

## 🔍 Búsqueda Rápida

### ¿Cómo...?

| Pregunta | Documento | Sección |
|----------|-----------|---------|
| ¿Cómo empezar? | GEOGLYPH_FINAL_SUMMARY.md | Comandos Rápidos |
| ¿Cómo usar la API? | GEOGLYPH_DETECTION_GUIDE.md | Quick Start |
| ¿Cómo interpretar scores? | GEOGLYPH_IMPLEMENTATION_SUMMARY.md | Scoring Cultural |
| ¿Qué zonas explorar? | GEOGLYPH_DETECTION_GUIDE.md | Zonas No Catalogadas |
| ¿Cómo validar resultados? | GEOGLYPH_DETECTION_GUIDE.md | Modos Operativos |
| ¿Ejemplos de código? | ejemplo_geoglyph_practico.py | Todos los ejemplos |

---

## 📞 Comandos Más Usados

```bash
# Probar sistema
python test_geoglyph_detection.py

# Ejemplos prácticos
python ejemplo_geoglyph_practico.py

# Levantar backend
python backend/api/main.py

# Ver documentación API
http://localhost:8003/docs

# Endpoints principales
curl http://localhost:8003/geoglyph/zones/promising
curl http://localhost:8003/geoglyph/types
curl http://localhost:8003/geoglyph/modes
```

---

## 🗺️ Mapa de Archivos

```
c:\Python\ArcheoScope\
│
├── 📚 DOCUMENTACIÓN
│   ├── GEOGLYPH_FINAL_SUMMARY.md           ← EMPEZAR AQUÍ
│   ├── GEOGLYPH_IMPLEMENTATION_SUMMARY.md
│   ├── GEOGLYPH_DETECTION_GUIDE.md         ← Guía completa
│   └── GEOGLYPH_INDEX.md                   ← Este archivo
│
├── 🧪 TESTS Y EJEMPLOS
│   ├── test_geoglyph_detection.py          ← Tests completos
│   └── ejemplo_geoglyph_practico.py        ← Ejemplos prácticos
│
└── 💻 CÓDIGO
    └── backend/
        ├── geoglyph_detector.py            ← Detector core
        └── api/
            ├── geoglyph_endpoint.py        ← API endpoints
            └── main.py                     ← Actualizado con router
```

---

## ✅ Checklist de Aprendizaje

### Nivel Básico
- [ ] Leer GEOGLYPH_FINAL_SUMMARY.md
- [ ] Ejecutar test_geoglyph_detection.py
- [ ] Ejecutar ejemplo_geoglyph_practico.py
- [ ] Entender los 3 modos operativos
- [ ] Conocer las zonas prometedoras

### Nivel Intermedio
- [ ] Leer GEOGLYPH_DETECTION_GUIDE.md completo
- [ ] Entender el scoring cultural
- [ ] Probar la API REST
- [ ] Adaptar ejemplos a coordenadas propias
- [ ] Entender contexto volcánico e hidrológico

### Nivel Avanzado
- [ ] Revisar código de geoglyph_detector.py
- [ ] Entender alineaciones astronómicas
- [ ] Implementar integración con datos reales
- [ ] Preparar pipeline ML/IA
- [ ] Planificar exploración sistemática

---

## 🎯 Casos de Uso

### 1. Validar Geoglifo Reportado
```python
# Usar modo científico
detector = GeoglyphDetector(mode=DetectionMode.SCIENTIFIC)
result = detector.detect_geoglyph(lat, lon, ...)

if result.cultural_score >= 0.75:
    print("Alta probabilidad - Validar con alta resolución")
```

### 2. Explorar Zona Nueva
```python
# Usar modo explorador
detector = GeoglyphDetector(mode=DetectionMode.EXPLORER)
zones = get_promising_zones()
# Escanear zona prometedora
```

### 3. Investigar Anomalía
```python
# Usar modo cognitivo
detector = GeoglyphDetector(mode=DetectionMode.COGNITIVE)
# Solo señalar, no afirmar
```

---

## 📚 Referencias Adicionales

### Geoglifos de Arabia
- Kennedy, D. (2011). "The 'Works of the Old Men' in Arabia"
- Crassard, R. et al. (2015). "Addressing the Desert Kites Phenomenon"

### Geoglifos de Nazca
- Lambers, K. (2006). "The Geoglyphs of Palpa, Peru"
- Clarkson, P. (1990). "The Archaeology of the Nazca Pampa"

### Alineaciones Astronómicas
- Hawkins, G. (1969). "Ancient Lines in the Peruvian Desert"
- Aveni, A. (1990). "The Lines of Nazca"

---

## 🆘 Solución de Problemas

| Problema | Solución | Documento |
|----------|----------|-----------|
| No arranca el backend | Verificar dependencias | GEOGLYPH_FINAL_SUMMARY.md |
| Score muy bajo | Revisar resolución espacial | GEOGLYPH_DETECTION_GUIDE.md |
| Muchos falsos positivos | Usar modo científico | GEOGLYPH_IMPLEMENTATION_SUMMARY.md |
| No encuentra geoglifos | Usar modo explorador | GEOGLYPH_DETECTION_GUIDE.md |

---

## 🎓 Glosario

| Término | Definición |
|---------|-----------|
| **Cultural Score** | Probabilidad de origen cultural (0-1) |
| **Aspect Ratio** | Relación largo/ancho del geoglifo |
| **NW-SE** | Orientación noroeste-sureste (común en Arabia) |
| **Harrat** | Campo de lava basáltica (Arabia) |
| **Wadi** | Cauce seco de río (agua estacional) |
| **Paper-level** | Descubrimiento con coherencia regional alta |
| **FP** | Falso Positivo |

---

**ArcheoScope - Geoglyph Detection System**  
*Versión 1.0 - Enero 2026*  
*Documentación completa y organizada*
