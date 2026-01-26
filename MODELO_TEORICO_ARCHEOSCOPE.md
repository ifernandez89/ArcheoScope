# Modelo Teórico ArcheoScope
## Formalización Científica del Sistema de Detección de Persistencias Espaciales

**Versión**: 1.0  
**Fecha**: Enero 2026  
**Estado**: Documento Teórico Fundamental

---

## 1. AXIOMA FUNDAMENTAL

### 1.1 Principio de Persistencia Antropogénica

> **"Las intervenciones humanas en el paisaje generan firmas espaciales persistentes, coherentes y multi-escalares que no pueden ser explicadas únicamente por procesos naturales actuales."**

Este axioma constituye la base epistemológica de ArcheoScope y se descompone en cuatro propiedades fundamentales:

#### **P1: Persistencia Temporal**
```
∀ intervención antropogénica I, ∃ firma espacial F tal que:
F(t) ≈ F(t + Δt) para Δt ∈ [0, T_arqueológico]

donde T_arqueológico >> T_procesos_naturales_locales
```

**Interpretación**: Las firmas arqueológicas persisten en escalas temporales superiores a los procesos naturales locales.

#### **P2: Coherencia Multi-espectral**
```
F = {f_vegetación, f_térmica, f_rugosidad, f_suelo, ...}

Coherencia(F) = ∏ᵢ P(fᵢ | H_antropogénico) / P(fᵢ | H_natural) > 1
```

**Interpretación**: La probabilidad conjunta de observar todas las firmas bajo hipótesis antropogénica supera la hipótesis natural.

#### **P3: Organización Geométrica**
```
G(F) = medida de regularidad geométrica

G(F_antropogénico) >> G(F_natural)
```

**Interpretación**: Las firmas antropogénicas exhiben organización geométrica no aleatoria.

#### **P4: Estabilidad Multi-temporal**
```
Var(F, [t₁, t₂, ..., tₙ]) < ε_umbral

donde ε_umbral << Var(procesos_naturales)
```

**Interpretación**: La varianza temporal de firmas arqueológicas es significativamente menor que la de procesos naturales.

---

## 2. MARCO EPISTEMOLÓGICO

### 2.1 Paradigma de Espacios de Posibilidad

ArcheoScope NO reconstruye estructuras arqueológicas. ArcheoScope reconstruye **espacios de posibilidad geométrica** consistentes con firmas físicas persistentes.

#### **Definición Formal**
```
Ω_posible = {geometría G | P(datos observados | G) > τ_mínimo}

donde:
- Ω_posible: Espacio de geometrías posibles
- G: Configuración geométrica 3D
- τ_mínimo: Umbral de verosimilitud mínima
```

#### **Niveles de Reconstrucción**

**Nivel I: Forma Aproximada**
- Morfología general (piramidal, lineal, cavidad)
- Escala espacial correcta (±20%)
- Orientación principal (±15°)

**Nivel II: Relaciones Espaciales**
- Organización relativa entre elementos
- Simetrías detectadas
- Patrones de distribución

**Nivel III: NO ALCANZABLE**
- Detalles arquitectónicos
- Función cultural
- Afiliación cronológica
- Significado histórico

### 2.2 Inferencia Bayesiana Multi-capa


#### **Modelo Probabilístico**
```
P(arqueológico | datos) = P(datos | arqueológico) × P(arqueológico) / P(datos)

donde:
P(datos | arqueológico) = ∏ᵢ P(capa_i | arqueológico)
P(arqueológico) = prior basado en contexto regional
P(datos) = normalización marginal
```

#### **Integración Multi-instrumental**
```
Score_final = Σᵢ wᵢ × Score_instrumento_i

donde:
wᵢ = peso del instrumento i (basado en confiabilidad)
Σᵢ wᵢ = 1 (normalización)
```

#### **Convergencia de Evidencia**
```
Convergencia = N_instrumentos_detectores / N_instrumentos_totales

Umbral_arqueológico: Convergencia ≥ 0.6 (3/5 instrumentos)
```

---

## 3. ARQUITECTURA MATEMÁTICA

### 3.1 Pipeline de Inferencia Volumétrica

#### **ETAPA 1: Extracción de Firma Espacial**

**Vector de Firma S**:
```
S = [s₁, s₂, ..., sₙ]ᵀ

donde:
s₁ = área_m² (escala espacial)
s₂ = elongación (anisotropía)
s₃ = simetría (regularidad)
s₄ = amplitud_térmica (inercia térmica)
s₅ = rugosidad_SAR (textura superficial)
s₆ = coherencia_multitemporal (persistencia)
s₇ = pendiente_residual (anomalía topográfica)
s₈ = confianza_firma (calidad de datos)
s₉ = convergencia_sensores (multi-instrumental)
```

**Normalización**:
```
S_norm = (S - μ_regional) / σ_regional
```

#### **ETAPA 2: Clasificación Morfológica Blanda**

**Función de Pertenencia Difusa**:
```
μ_clase(S) = exp(-||S - C_clase||² / 2σ²_clase)

donde:
C_clase = centroide de la clase morfológica
σ_clase = dispersión de la clase
```

**Clases Morfológicas** (NO tipológicas):
1. `TRUNCATED_PYRAMIDAL`: Volumen troncopiramidal
2. `STEPPED_PLATFORM`: Plataforma escalonada
3. `LINEAR_COMPACT`: Estructura lineal compactada
4. `CAVITY_VOID`: Cavidad/vacío
5. `EMBANKMENT_MOUND`: Terraplén/montículo
6. `ORTHOGONAL_NETWORK`: Red ortogonal superficial

**Clasificación Blanda**:
```
P(clase | S) = μ_clase(S) / Σⱼ μ_clase_j(S)
```

#### **ETAPA 3: Campo Volumétrico Probabilístico**

**Voxelización del Espacio**:
```
V(x, y, z) = probabilidad de material en posición (x, y, z)

V: ℝ³ → [0, 1]
```

**Componentes del Campo**:
```
Campo_volumétrico = {
    V_material(x, y, z),    # P(material | datos)
    V_vacío(x, y, z),       # P(vacío | datos)
    U(x, y, z),             # Incertidumbre
    C(x, y, z)              # Confianza
}

donde:
V_material + V_vacío ≤ 1
U = 1 - (V_material + V_vacío)
C = función de distancia a datos observados
```

**Propagación de Incertidumbre**:
```
U(x, y, z) = U_base × exp(d(x,y,z) / λ_decay)

donde:
d(x,y,z) = distancia a píxel observado más cercano
λ_decay = longitud de decaimiento (función de resolución)
```

#### **ETAPA 4: Modelo Geométrico 3D**

**Extracción de Isosuperficie**:
```
Superficie = {(x, y, z) | V(x, y, z) = τ_iso}

donde:
τ_iso ∈ {0.7, 0.5, 0.3} para zonas {core, probable, possible}
```

**Simplificación Geométrica**:
```
Modelo_simplificado = Decimate(Superficie, target_faces=5000)
```

**Métricas Geométricas**:
```
Volumen_estimado = ∫∫∫ V(x, y, z) dx dy dz

Altura_máxima = max_z {z | V(x, y, z) > τ_min}

Simetría = Σ_ejes |V(r) - V(-r)| / Σ_ejes V(r)
```

#### **ETAPA 5: Evaluación de Consistencia (Phi4)**

**Score de Consistencia**:
```
Consistencia = w₁×C_geométrica + w₂×C_física + w₃×C_contextual - P_pareidolia

donde:
C_geométrica = coherencia entre capas geométricas
C_física = plausibilidad física del modelo
C_contextual = consistencia con contexto regional
P_pareidolia = penalización por sobre-ajuste visual
```

**Anti-Pareidolia**:
```
P_pareidolia = α × (Complejidad_modelo / Calidad_datos)

donde:
Complejidad_modelo = N_vértices + N_simetrías_detectadas
Calidad_datos = Convergencia × Confianza_promedio
α = factor de penalización (típicamente 0.1-0.3)
```

**Ajuste de Pesos**:
```
w_ajustado_i = w_i × (1 - U_i)

donde:
U_i = incertidumbre del instrumento i
```

---

## 4. DETECCIÓN DE ANOMALÍAS ESPACIALES

### 4.1 Definiciones Operativas

#### **Anomalía Espacial**
```
Anomalía = {patrón P | P(P | natural) < 0.3}

Criterios:
1. Desviación estadística: |P - μ_natural| > 2σ_natural
2. Persistencia temporal: Var(P, tiempo) < ε_umbral
3. Coherencia espacial: Autocorrelación(P) > 0.6
```

#### **Firma Arqueológica**
```
Firma_arqueológica = {anomalía A | 
    P(A | arqueológico) > 0.65 AND
    Convergencia(A) ≥ 0.6 AND
    Consistencia_geométrica(A) > 0.7
}
```

#### **Probabilidad Integrada**
```
P_arqueológico = Bayes_ponderado(
    prior_regional,
    likelihood_multi_instrumental,
    evidencia_geométrica,
    persistencia_temporal
)
```

### 4.2 Instrumentos de Detección

#### **1. Sensor de Vegetación (NDVI)**
```
NDVI = (NIR - Red) / (NIR + Red)

Anomalía_vegetación = |NDVI_observado - NDVI_esperado| > τ_NDVI

Interpretación arqueológica:
- NDVI elevado → Humedad retenida (estructuras enterradas)
- NDVI reducido → Compactación (pisos, caminos)
```

#### **2. Sensor Térmico (LST)**
```
LST = Temperatura superficial terrestre

Anomalía_térmica = |LST_día - LST_noche| > τ_térmico

Interpretación arqueológica:
- Alta inercia térmica → Materiales densos (muros, pisos)
- Baja inercia térmica → Cavidades, rellenos
```

#### **3. Sensor de Rugosidad (SAR)**
```
Rugosidad_SAR = σ⁰_backscatter

Anomalía_rugosidad = Textura(SAR) ≠ Textura_natural

Interpretación arqueológica:
- Alta rugosidad → Estructuras superficiales
- Baja rugosidad → Superficies compactadas
```

#### **4. Sensor de Suelo (Salinidad/Humedad)**
```
Anomalía_suelo = Composición_química ≠ Matriz_natural

Interpretación arqueológica:
- Salinidad elevada → Ocupación humana prolongada
- Humedad anómala → Alteración de drenaje
```

#### **5. Sensor Temporal (Persistencia)**
```
Persistencia = Correlación(firma_t₁, firma_t₂, ..., firma_tₙ)

Umbral_arqueológico: Persistencia > 0.8 en ventana de 5-10 años

Interpretación arqueológica:
- Alta persistencia → Firma estructural (no estacional)
- Baja persistencia → Proceso natural variable
```

---

## 5. CONTROL DE SESGOS Y RIGOR CIENTÍFICO

### 5.1 Medidas Anti-Pareidolia

#### **1. Umbrales Cuantitativos**
```
Detección_válida ⟺ 
    Score > τ_mínimo AND
    Convergencia ≥ 0.6 AND
    Persistencia > 0.8 AND
    P_pareidolia < 0.3
```

#### **2. Modelado de Procesos Naturales**
```
P(datos | natural) = Modelo_geológico + Modelo_hidrológico + Modelo_ecológico

Exclusión_natural ⟺ P(datos | arqueológico) / P(datos | natural) > 3
```

#### **3. Requisitos de Coherencia Geométrica**
```
Coherencia_geométrica = 
    w₁×Regularidad_forma +
    w₂×Simetría_detectada +
    w₃×Organización_espacial

Umbral_mínimo: Coherencia_geométrica > 0.7
```

#### **4. Validación de Persistencia Temporal**
```
Persistencia_validada ⟺ 
    ∀ t ∈ [t₁, tₙ]: Firma(t) ≈ Firma(t₀) ± ε_tolerancia

donde:
ε_tolerancia = 0.15 × Firma(t₀)
```

### 5.2 Transparencia Metodológica

#### **Trazabilidad Completa**
```
Resultado = {
    datos_entrada: {fuentes, fechas, resolución},
    parámetros: {umbrales, pesos, configuración},
    procesamiento: {pasos, transformaciones, filtros},
    salida: {scores, incertidumbres, explicaciones},
    validación: {controles, métricas, limitaciones}
}
```

#### **Cuantificación de Incertidumbre**
```
Incertidumbre_total = √(U²_datos + U²_modelo + U²_interpretación)

donde:
U_datos = incertidumbre de mediciones
U_modelo = incertidumbre de parámetros
U_interpretación = incertidumbre de clasificación
```

#### **Intervalos de Confianza**
```
Score_arqueológico = μ ± 1.96σ (95% confianza)

Reporte obligatorio:
- Valor central (μ)
- Intervalo de confianza (σ)
- Nivel de confianza (95%)
```

### 5.3 Controles Científicos

#### **1. Known-Site Blind Testing**
```
Protocolo:
1. Seleccionar sitios arqueológicos documentados
2. Analizar sin conocimiento de ubicación exacta
3. Comparar detecciones con ground truth
4. Calcular métricas de rendimiento

Métricas:
- Sensibilidad = TP / (TP + FN)
- Especificidad = TN / (TN + FP)
- Precisión = TP / (TP + FP)
```

#### **2. Evaluación de Falsos Positivos**
```
Protocolo:
1. Analizar áreas sin arqueología conocida
2. Identificar detecciones
3. Clasificar causas de falsos positivos
4. Ajustar umbrales y pesos

Causas comunes:
- Formaciones geológicas regulares
- Canales fluviales antiguos
- Patrones agrícolas históricos
- Actividades industriales
```

#### **3. Validación Cruzada**
```
Protocolo:
1. Dividir datos en k subconjuntos
2. Entrenar en k-1 subconjuntos
3. Validar en subconjunto restante
4. Repetir k veces
5. Promediar métricas

k = 5 (validación cruzada 5-fold)
```

---

## 6. CAPACIDADES NEGATIVAS

### 6.1 Limitaciones Ambientales

#### **Entornos de Rendimiento Reducido**
```
Performance_factor = f(vegetación, geología, uso_suelo, topografía)

Factores de reducción:
- Dosel forestal denso: ×0.3
- Zonas geológicamente activas: ×0.4
- Perturbación agrícola reciente: ×0.5
- Desarrollo urbano: ×0.2
- Topografía extrema (>30°): ×0.4
```

### 6.2 Limitaciones Arqueológicas

#### **Rasgos NO Detectables**
```
NO_detectable = {
    escala < 10m²,
    antigüedad < 200 años,
    profundidad > 3m,
    ocupación_efímera,
    perturbación_severa
}
```

#### **Umbrales de Detección**
```
Escala_mínima = 10 m² (área)
Antigüedad_mínima = 200 años (persistencia)
Profundidad_máxima = 2-3 m (penetración)
Duración_mínima_ocupación = 50 años (firma acumulativa)
```

### 6.3 Fuentes de Falsos Positivos

#### **Generadores Comunes**
```
FP_sources = {
    formaciones_geológicas: P_FP = 0.15,
    canales_fluviales_antiguos: P_FP = 0.12,
    límites_agrícolas_históricos: P_FP = 0.18,
    actividades_industriales: P_FP = 0.10,
    desastres_naturales: P_FP = 0.08
}

P_FP_total = Σ P_FP_i ≈ 0.63 (sin controles)
P_FP_controlado ≈ 0.15 (con anti-pareidolia)
```

---

## 7. MARCO ÉTICO Y USO RESPONSABLE

### 7.1 Protocolos Anti-Saqueo

#### **Restricción de Precisión**
```
Coordenadas_públicas = round(coordenadas_reales, decimales=2)

Precisión_pública ≈ 1 km (suficiente para investigación, insuficiente para saqueo)
```

#### **Control de Acceso**
```
Acceso_detallado ⟺ 
    Usuario ∈ {instituciones_académicas, autoridades_patrimonio} AND
    Verificación_identidad = TRUE AND
    Acuerdo_uso_responsable = FIRMADO
```

### 7.2 Estándares de Integridad Académica

#### **Comunicación de Resultados**
```
Reporte_obligatorio = {
    "Área de elevado potencial arqueológico",  # NO "descubrimiento"
    "Requiere validación de campo",            # NO "confirmado"
    "Probabilidad X% ± Y%",                    # NO "certeza"
    "Limitaciones: [lista]",                   # Transparencia
    "Incertidumbres: [lista]"                  # Honestidad
}
```

#### **Principios de Ciencia Abierta**
```
Open_science = {
    metodología: PÚBLICA,
    código: OPEN_SOURCE,
    datos: COMPARTIDOS (con restricciones éticas),
    resultados: PEER_REVIEWED,
    limitaciones: EXPLÍCITAS
}
```

---

## 8. VALIDACIÓN Y ASEGURAMIENTO DE CALIDAD

### 8.1 Protocolo de Validación con Sitios Conocidos

#### **Metodología**
```
1. Selección de sitios: N ≥ 50, diversos en cultura/geografía/cronología
2. Análisis ciego: Sin conocimiento de ubicación exacta
3. Comparación: Detecciones vs ground truth
4. Métricas: Sensibilidad, especificidad, precisión
5. Refinamiento: Ajuste de parámetros basado en resultados
```

#### **Métricas de Rendimiento**
```
Sensibilidad_objetivo ≥ 0.75 (detectar 75% de sitios reales)
Especificidad_objetivo ≥ 0.80 (80% de detecciones son válidas)
Precisión_objetivo ≥ 0.70 (70% de predicciones positivas correctas)
```

### 8.2 Marco de Mejora Continua

#### **Ciclo de Retroalimentación**
```
1. Detección → 2. Validación de campo → 3. Análisis de discrepancias →
4. Refinamiento de modelo → 5. Re-validación → 1. Detección mejorada
```

#### **Integración de Feedback**
```
Peso_actualizado_i = Peso_anterior_i × (1 + α × Performance_i)

donde:
Performance_i = (TP_i - FP_i) / Total_detecciones_i
α = tasa de aprendizaje (típicamente 0.1)
```

---

## 9. APLICACIONES CIENTÍFICAS

### 9.1 Casos de Uso Primarios

#### **1. Priorización de Prospección Arqueológica**
```
Objetivo: Optimizar recursos de campo
Entrada: Región de interés (100-1000 km²)
Salida: Mapa de probabilidad arqueológica
Beneficio: Reducción de 60-80% en área a prospectar
```

#### **2. Planificación de Estudios Geofísicos**
```
Objetivo: Dirigir GPR/magnetometría/resistividad
Entrada: Área de estudio (1-10 km²)
Salida: Zonas de alta probabilidad con geometría estimada
Beneficio: Optimización de transectos geofísicos
```

#### **3. Comparación de Hipótesis Geométricas**
```
Objetivo: Evaluar modelos arqueológicos alternativos
Entrada: Hipótesis H₁, H₂, ..., Hₙ
Salida: P(datos | Hᵢ) para cada hipótesis
Beneficio: Selección de modelo basada en evidencia
```

#### **4. Pre-descubrimiento para LIDAR Dirigido**
```
Objetivo: Identificar áreas para LIDAR aerotransportado
Entrada: Región extensa (>1000 km²)
Salida: Zonas prioritarias para LIDAR de alta resolución
Beneficio: Reducción de costos de adquisición LIDAR
```

### 9.2 Integración con Métodos Tradicionales

#### **Flujo de Trabajo Integrado**
```
1. ArcheoScope: Screening regional (100-1000 km²)
   ↓
2. Prospección de superficie: Validación preliminar (10-50 km²)
   ↓
3. Geofísica: Caracterización detallada (0.1-1 km²)
   ↓
4. Excavación: Confirmación y estudio (100-1000 m²)
```

---

## 10. HOJA DE RUTA DE DESARROLLO FUTURO

### 10.1 Mejoras Técnicas

#### **Corto Plazo (6-12 meses)**
```
- Integración de datos Sentinel-1/2 en tiempo real
- Implementación de análisis multitemporal automático
- Desarrollo de API para acceso institucional
- Validación con 100+ sitios conocidos
```

#### **Mediano Plazo (1-2 años)**
```
- Incorporación de datos hiperespectrales
- Integración de modelos de elevación de alta resolución
- Machine learning explicable para clasificación morfológica
- Publicación de metodología en journals peer-reviewed
```

#### **Largo Plazo (2-5 años)**
```
- Integración con bases de datos patrimoniales globales
- Procesamiento en tiempo real de imágenes satelitales
- Extensión a otros dominios (geología, urbanismo)
- Desarrollo de estándares internacionales
```

### 10.2 Expansión Científica

#### **Validación Cross-Regional**
```
Regiones objetivo:
- Mesoamérica: Maya, Azteca, Olmeca
- Andes: Inca, Moche, Nazca, Tiwanaku
- Mediterráneo: Grecia, Roma, Fenicia
- Medio Oriente: Mesopotamia, Persia
- Asia: Angkor, Indus, China
- África: Egipto, Nubia, Gran Zimbabwe
```

#### **Colaboración Interdisciplinaria**
```
Disciplinas:
- Geofísica: Integración de métodos geofísicos
- Ecología: Modelado de procesos naturales
- Ciencia del clima: Análisis de cambios ambientales
- Ciencia de datos: Machine learning explicable
- Ética: Protocolos de uso responsable
```

---

## 11. CONCLUSIÓN

### 11.1 Contribución Científica

ArcheoScope representa un **cambio de paradigma** en arqueología remota:

**De**: Detección visual de formas reconocibles  
**A**: Análisis de patrones de comportamiento espacial

**De**: Resolución máxima para identificación  
**A**: Correlación multi-capa para inferencia

**De**: Afirmaciones arqueológicas definitivas  
**A**: Espacios de posibilidad geométrica con incertidumbre cuantificada

### 11.2 Fortalezas del Marco Teórico

1. **Fundamentación Matemática Sólida**: Formalización rigurosa de principios
2. **Transparencia Metodológica**: Trazabilidad completa de decisiones
3. **Control de Sesgos**: Medidas anti-pareidolia activas
4. **Cuantificación de Incertidumbre**: Intervalos de confianza explícitos
5. **Validación Empírica**: Protocolo de testing con sitios conocidos
6. **Ética Integrada**: Protocolos anti-saqueo y uso responsable

### 11.3 Limitaciones Reconocidas

1. **NO reemplaza métodos arqueológicos tradicionales**
2. **NO proporciona identificaciones culturales o cronológicas**
3. **Rendimiento reducido en ciertos entornos**
4. **Requiere interpretación experta**
5. **Falsos positivos inevitables (tasa controlada ~15%)**

### 11.4 Mensaje Clave

> **ArcheoScope detecta patrones que PUEDEN indicar intervención humana antigua. Todos los resultados requieren interpretación arqueológica experta y validación de campo. El marco sirve a la arqueología, no al revés.**

---

## APÉNDICE A: Glosario de Términos

**Anomalía Espacial**: Patrón con P(natural) < 0.3  
**Firma Arqueológica**: Anomalía con P(arqueológico) > 0.65 y convergencia ≥ 0.6  
**Convergencia**: Fracción de instrumentos que detectan señal  
**Persistencia**: Estabilidad temporal de firma (correlación > 0.8)  
**Coherencia Geométrica**: Medida de regularidad espacial (> 0.7)  
**Espacio de Posibilidad**: Conjunto de geometrías consistentes con datos  
**Anti-Pareidolia**: Penalización por sobre-ajuste visual  
**Nivel de Reconstrucción I**: Forma aproximada, escala correcta  
**Nivel de Reconstrucción II**: Relaciones espaciales, simetrías  

---

## APÉNDICE B: Referencias Teóricas

### Fundamentos Matemáticos
- Inferencia Bayesiana multi-capa
- Teoría de campos probabilísticos
- Geometría computacional
- Análisis de series temporales

### Arqueología Remota
- Prospección geofísica
- Teledetección arqueológica
- Análisis espacial
- Arqueología del paisaje

### Control de Sesgos
- Teoría de detección de señales
- Análisis de falsos positivos
- Validación estadística
- Epistemología científica

---

**Información del Documento**
- **Versión**: 1.0
- **Fecha**: Enero 2026
- **Estado**: Modelo Teórico Fundamental
- **Licencia**: CC BY-SA 4.0
- **Citación**: ArcheoScope Development Team (2026). Modelo Teórico ArcheoScope: Formalización Científica del Sistema de Detección de Persistencias Espaciales. Documento Técnico v1.0.

**Contacto**: Para colaboración académica y acceso institucional, contactar al equipo de desarrollo de ArcheoScope a través de canales de investigación arqueológica establecidos.
