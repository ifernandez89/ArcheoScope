# ArcheoScope - Sistema de Análisis Arqueológico Integrado

## 🧠 Arquitectura del Sistema

El sistema ArcheoScope realiza análisis arqueológico remoto mediante una integración inteligente de múltiples fuentes de datos: detección instrumental, análisis temporal y razonamiento con IA.

## 🔄 Flujo de Análisis

### 1. Clasificación de Ambiente
- **Objetivo**: Identificar tipo de terreno (bosque, desierto, mar, glaciar, etc.)
- **Instrumentación**: Clasificador basado en datos geográficos y ambientales
- **Salida**: Sensores primarios y secundarios recomendados para el análisis

### 2. Detección Instrumental (CORE Detector)
- **LIDAR**: Detecta montículos y estructuras bajo vegetación densa
- **SAR (Banda L)**: Penetra nubes y vegetación para identificar patrones geométricos
- **NDVI**: Identifica claros anómalos en la vegetación sobre posibles estructuras enterradas
- **Térmico**: Detecta anomalías térmicas consistentes con estructuras subterráneas

**Cálculo por instrumento**:
```
valor_medido > umbral_predefinido → posible_anomalía_arqueológica
```

### 3. Sensor Temporal (Solo Terrestres)
- **Ventana de análisis**: 5 años de datos satelitales estacionales
- **Métrica clave**: Persistencia temporal de anomalías
- **Lógica**: Patrones que persisten múltiples años tienen mayor probabilidad arqueológica
- **Ambientes aplicables**: Solo análisis terrestres (no acuáticos ni glaciares)

**Cálculo de persistencia**:
```python
CV = std_valores / mean_valores  # Coeficiente de variación
persistencia = años_con_anomalía / total_años
score_temporal = persistencia * (1 - CV/0.3)
```

### 4. Asistente IA Arqueológico (phi:latest)

**Punto de intervención**: Después de obtener mediciones instrumentales y temporales

**Funciones del asistente IA**:
1. **Interpretación contextual**: Analiza patrones detectados desde perspectiva arqueológica profesional
2. **Integración multi-fuente**: Combina información de todos los instrumentos coherentemente
3. **Razonamiento científico**: Proporciona explicaciones paso a paso de los hallazgos
4. **Evaluación de confianza**: Asigna niveles de confianza a las interpretaciones
5. **Identificación de falsos positivos**: Advierte sobre procesos naturales que pueden imitar anomalías arqueológicas
6. **Recomendaciones de validación**: Sugiere próximos pasos para investigación de campo

**Ejemplo de razonamiento IA**:
> "Los patrones geométricos rectangulares detectados por LIDAR, combinados con la persistencia temporal de 5 años observada en NDVI, sugieren estructuras antropogénicas consistentes con terrazas agrícolas prehispánicas. La coherencia espacial y la estabilidad temporal refuerzan la hipótesis arqueológica sobre origen geológico."

## 📊 Cálculo de Probabilidad Arqueológica

**Fórmula integrada**:
```
Probabilidad_Final = 
  Base_CORE (60%) + 
  Persistencia_Temporal × 0.25 + 
  Confianza_IA × 0.15
```

**Componentes**:
- **Base CORE**: Resultado de convergencia instrumental
- **Persistencia Temporal**: Solo para ambientes terrestres con datos ≥3 años
- **Confianza IA**: Basada en coherencia y calidad del razonamiento

## 🎯 Tipos de Análisis por Ambiente

### Terrestres (Bosque, Desierto, Agrícola, etc.)
- **Instrumentos**: LIDAR + SAR + NDVI + Térmico
- **Sensor Temporal**: ✅ Activo (ventana 5 años)
- **IA**: ✅ Integrada para interpretación arqueológica
- **Probabilidades**: Base + Temporal + IA

### Acuáticos (Mar, Agua poco profunda)
- **Instrumentos**: Sonar + Batimetría + SAR
- **Sensor Temporal**: ❌ No aplicable
- **IA**: ✅ Integrada para arqueología submarina
- **Probabilidades**: Base + IA únicamente

### Glaciares/Hielo
- **Instrumentos**: Radar penetrante + Térmico + Óptico
- **Sensor Temporal**: ❌ No aplicable
- **IA**: ✅ Integrada para criocrqueología
- **Probabilidades**: Base + IA únicamente

## 🔍 Proceso de Toma de Decisiones

1. **Detección**: Instrumentos identifican anomalías espaciales
2. **Validación Temporal**: Verifica persistencia (solo terrestres)
3. **Integración IA**: Proporciona contexto arqueológico profesional
4. **Convergencia**: Múltiples líneas de evidencia se cruzan
5. **Clasificación**: Asigna nivel de confianza y tipo de resultado
6. **Explicación**: Genera reporte científico comprensible

## 📈 Salidas del Sistema

### Datos Cuantitativos
- Probabilidad arqueológica (0-1)
- Número de instrumentos convergiendo
- Score de persistencia temporal
- Confianza del análisis IA

### Datos Cualitativos
- Explicación científica completa
- Interpretación arqueológica profesional
- Identificación de posibles falsos positivos
- Recomendaciones para validación de campo

### Metadatos
- Instrumentos utilizados y sus mediciones
- Años analizados (sensor temporal)
- Ambiente clasificado y contexto
- Estado del sistema y disponibilidad de componentes

## 🚀 Ventajas del Enfoque Integrado

1. **Robustez**: Múltiples fuentes independientes validan conclusiones
2. **Especialización**: Cada ambiente usa instrumentos óptimos
3. **Inteligencia**: IA proporciona contexto arqueológico profesional
4. **Persistencia**: Análisis temporal discrimina entre fenómenos temporales y permanentes
5. **Adaptabilidad**: Sistema ajusta probabilidades según disponibilidad de datos
6. **Transparencia**: Cada paso del razonamiento es explicado y justificado

## 🔬 Principios Científicos

- **Convergencia Instrumental**: Múltiples instrumentos deben coincidir
- **Persistencia Temporal**: Evidencia arqueológica resiste el paso del tiempo
- **Razonamiento Experto**: IA entrenada en principios arqueológicos
- **Validación Cruzada**: Ninguna fuente es considerada definitiva
- **Conservativismo**: Prefiere falsos negativos sobre falsos positivos

---

**Resultado**: Sistema de análisis arqueológico remoto que combina la precisión de instrumentos científicos, la persistencia temporal y el razonamiento experto de IA para detectar sitios arqueológicos con alta confianza científica.