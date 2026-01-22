# 🏺 ARCHEOSCOPE - GUÍA DE DESPLIEGUE Y USO

## 🚀 INICIO RÁPIDO

### **Prerrequisitos**
- Python 3.8+
- Dependencias instaladas: `pip install -r archeoscope/backend/requirements.txt`
- Ollama (opcional, para phi4-mini-reasoning)

### **Iniciar Sistema Completo**

#### **1. Backend ArcheoScope**
```bash
cd archeoscope
python backend/api/main.py
```
**Resultado esperado:**
```
INFO: Sistema arqueológico ArcheoScope inicializado correctamente con módulos académicos y volumétricos
INFO: Uvicorn running on http://0.0.0.0:8003
```

#### **2. Frontend Web**
```bash
cd archeoscope  
python start_frontend.py
```
**Resultado esperado:**
```
🏺 ArcheoScope Archaeological Interface
- Frontend: http://localhost:8080
- API Backend: http://localhost:8003
```

### **3. Verificar Estado del Sistema**
- **Frontend**: http://localhost:8080
- **Indicadores de estado**: Esquina superior derecha
  - 🟢 **Backend**: Verde = Operacional
  - 🟡 **IA**: Amarillo = Determinista (sin Ollama)
  - 🟢 **3D**: Verde = Motor volumétrico activo

## 🎯 COORDENADAS DE TESTING RECOMENDADAS

### **🥇 VÍA APPIA - CALZADA ROMANA** (¡Empezar aquí!)
```
41.87230285419031, 12.504327806909155
```
**Por qué es ideal:**
- Geometría lineal clara y persistente
- Totalmente enterrada (no visible superficialmente)  
- Detectable por NDVI desacoplado, SAR, amplitud térmica
- Validación histórica clara

### **🥈 NAZCA LINES - BENCHMARK GEOMÉTRICO**
```
-14.739503, -75.154533
```
**Por qué es excelente:**
- Geometría extrema conocida
- Test de falsas alarmas
- Validación del paradigma "detecta sin saber qué es"

### **🥉 TEOTIHUACÁN - PLATAFORMAS ENTERRADAS**
```
19.695, -98.845
```
**Por qué es potente:**
- Plataformas de volumen bajo
- Organización urbana enterrada
- Test de volúmenes no monumentales

## 📋 PROCEDIMIENTO DE TESTING

### **Paso 1: Búsqueda de Coordenadas**
1. Acceder a http://localhost:8080
2. Pegar coordenadas en el campo de búsqueda
3. Hacer clic en **🔍 Buscar**
4. Verificar que el mapa se centre correctamente

### **Paso 2: Configurar Análisis**
- **Resolución**: 500m (recomendado para empezar)
- **Incluir Explicabilidad**: ✅ Activar
- **Métricas de Validación**: ✅ Activar

### **Paso 3: Ejecutar Investigación**
1. Hacer clic en **INVESTIGAR**
2. Observar indicador de carga: "🔍 Analizando región arqueológica..."
3. Tiempo esperado: 15-30 segundos

### **Paso 4: Interpretar Resultados**

#### **Panel de Resultados (Derecha)**
- **Área Total**: Superficie analizada en km²
- **Anomalías Detectadas**: Píxeles con probabilidad > 0.3
- **Firmas Arqueológicas**: Píxeles con probabilidad > 0.65
- **Volumen Total Estimado**: Inferencia volumétrica en m³
- **Confianza IA**: Nivel de confianza del análisis

#### **Visualización en Mapa**
- **🟠 Naranja**: Anomalías espaciales (probabilidad moderada)
- **🔴 Rojo**: Firmas arqueológicas (alta probabilidad)
- **Capas toggleables**: Activar/desactivar en panel derecho

#### **Inspección de Píxeles**
- **Hacer clic** en cualquier punto del mapa
- **Panel izquierdo** muestra datos espectrales detallados
- **Información volumétrica** con morfología detectada

## 🔍 QUÉ ESPERAR EN CADA CASO

### **🏛️ Vía Appia (Calzada Romana)**
**Resultados esperados:**
- **Morfología**: `estructura_lineal_compactada`
- **NDVI desacoplado**: Vegetación estresada sobre sustrato compactado
- **Amplitud térmica**: Inercia térmica de base de piedra
- **SAR backscatter**: Rugosidad de piedras enterradas
- **Volumen estimado**: 10,000-15,000 m³
- **Validación**: Score ≥ 70%

### **🏺 Nazca Lines (Benchmark)**
**Resultados esperados:**
- **Morfología**: `estructura_lineal_compactada`
- **Coherencia geométrica**: ≥ 0.9 (geometría extrema)
- **Persistencia temporal**: ≥ 0.95 (muy estable)
- **Anti-pareidolia**: Activo (sin sobre-interpretación)
- **Validación**: Paradigma "detecta sin saber qué es"

### **🏛️ Teotihuacán (Plataformas)**
**Resultados esperados:**
- **Morfología**: `plataforma_escalonada` o `volumen_troncopiramidal`
- **Volúmenes**: 5,000-20,000 m³ (estructuras medianas)
- **Organización**: Patrones urbanos detectables
- **Validación**: Estructuras no monumentales

## ⚠️ SOLUCIÓN DE PROBLEMAS

### **Error: "Failed to fetch"**
**Causa**: Backend no disponible
**Solución**:
1. Verificar que `python backend/api/main.py` esté corriendo
2. Confirmar puerto 8003 libre
3. Revisar logs del backend

### **Indicadores en Rojo**
**Backend Rojo**: 
- Reiniciar `python backend/api/main.py`
- Verificar dependencias instaladas

**IA Rojo**:
- Normal si Ollama no está instalado
- Sistema usa evaluación determinista (funcional)

**3D Rojo**:
- Problema con motor volumétrico
- Revisar logs para errores específicos

### **Sin Resultados Volumétricos**
**Causa**: Probabilidades arqueológicas < 0.65
**Solución**:
1. Probar coordenadas recomendadas
2. Ajustar resolución (probar 300m o 200m)
3. Verificar que la región tenga anomalías detectables

### **Análisis Muy Lento**
**Optimizaciones**:
- Usar resolución 500m o 1000m
- Desactivar explicabilidad para tests rápidos
- Reducir área de análisis

## 📊 MÉTRICAS DE ÉXITO

### **Sistema Operacional**
- ✅ Backend responde en < 2 segundos
- ✅ Frontend carga correctamente
- ✅ Indicadores de estado verdes/amarillos

### **Análisis Exitoso**
- ✅ Detección de anomalías > 0
- ✅ Inferencia volumétrica disponible
- ✅ Morfología clasificada correctamente
- ✅ Score de validación ≥ 50%

### **Paradigma Validado**
- ✅ Detecta geometría sin conocimiento previo
- ✅ Clasifica morfología abstracta (no tipológica)
- ✅ Genera espacios de posibilidad geométrica
- ✅ Mantiene incertidumbre explícita

## 🎓 INTERPRETACIÓN CIENTÍFICA

### **Niveles de Confianza**
- **≥ 0.8**: Muy alta probabilidad antrópica - investigación prioritaria
- **0.65-0.8**: Alta probabilidad - candidato para validación geofísica
- **0.45-0.65**: Probabilidad moderada - análisis adicional
- **0.3-0.45**: Probabilidad baja - monitoreo recomendado
- **< 0.3**: Compatible con procesos naturales

### **Morfologías Detectables**
- **Linear Compact**: Caminos, muros, canales
- **Truncated Pyramidal**: Montículos, tells, pirámides truncadas
- **Stepped Platform**: Terrazas, plataformas escalonadas
- **Embankment Mound**: Terraplenes, montículos funerarios
- **Orthogonal Network**: Trazados urbanos, sistemas de campos
- **Cavity Void**: Cámaras subterráneas, espacios excavados

### **Disclaimer Científico**
> "Las inferencias volumétricas representan espacios de posibilidad geométrica probabilística basados en firmas físicas persistentes. NO constituyen reconstrucciones arqueológicas definitivas y requieren validación independiente mediante métodos geofísicos y prospección controlada."

## 🏆 CASOS DE USO EXITOSOS

1. **Priorización de excavación**: Identificar áreas de alta probabilidad
2. **Planificación geofísica**: Dirigir GPR y magnetometría
3. **Estudios de impacto**: Evaluar patrimonio en desarrollo urbano
4. **Investigación académica**: Generar hipótesis para validación
5. **Pre-LIDAR**: Optimizar adquisición de datos de alta resolución

---

**🎉 ¡Sistema listo para investigación arqueológica real!**

Para soporte técnico o preguntas científicas, consultar la documentación completa en `SISTEMA_COMPLETO_ARCHEOSCOPE.md`.