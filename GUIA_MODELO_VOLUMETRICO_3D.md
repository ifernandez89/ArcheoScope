# 🎲 Guía del Modelo Volumétrico 3D - ArcheoScope

## 🚨 **¿QUÉ ESTÁS VIENDO?**

### **NO es una reconstrucción arquitectónica**
- ❌ NO son paredes reales
- ❌ NO son estructuras sólidas  
- ❌ NO es un plano arquitectónico

### **SÍ es un campo volumétrico de anomalía**
- ✅ Muestra dónde el terreno se comporta de forma no natural
- ✅ Representa persistencia espacial detectada
- ✅ Indica "aquí ocurre algo que la geología normal no hace"

## 🎮 **CONTROLES EXPLICADOS**

### **Slider de Profundidad (0-100%)**
- **Qué hace:** Corta el volumen verticalmente
- **Cómo funciona:** 50% = muestra hasta la mitad de altura
- **Para qué sirve:** Explorar anomalías por niveles de profundidad

### **Slider de Transparencia (10-90%)**
- **Qué hace:** Cambia la opacidad del volumen completo
- **Cómo funciona:** Más transparente = se ve a través
- **Para qué sirve:** Ver el interior del campo volumétrico

### **Modos de Visualización:**

#### 🎯 **Campo de Probabilidad**
- **Colores:** Azul (baja probabilidad) → Rojo (alta probabilidad)
- **Significado:** Dónde es más probable que haya intervención antrópica
- **Uso:** Vista general de confianza espacial

#### 🏗️ **Gradiente de Densidad**  
- **Colores:** Basados en altura (más denso abajo)
- **Significado:** Distribución vertical de anomalías
- **Uso:** Entender estratificación de la anomalía

#### 📏 **Continuidad Vertical**
- **Colores:** Gradiente de altura (abajo → arriba)
- **Significado:** Persistencia de la anomalía en profundidad
- **Uso:** Ver si la anomalía es superficial o profunda

#### 🧭 **Vectores de Alineación**
- **Colores:** Basados en orientación dominante
- **Significado:** Dirección principal de la anomalía
- **Uso:** Detectar patrones lineales (caminos, muros, etc.)

### **🎬 Animar Campo**
- **Qué hace:** Las partículas "respiran" (crecen y se contraen)
- **Por qué:** Hace más visible la distribución 3D
- **Cuándo usar:** Si el volumen se ve estático o poco claro

### **🔍 Clustering Automático**
- **Qué es:** Separar una anomalía grande en grupos pequeños
- **Por qué es útil:** A veces múltiples estructuras aparecen como una sola
- **Ejemplo:** En lugar de "masa de 300m", ver "3 grupos de 100m cada uno"
- **Colores:** Cada cluster tiene color diferente

### **Escalas:**

#### 🔍 **Lupa Local (≤300m)**
- **Para qué:** Análisis arqueológico detallado
- **Escala:** Edificios, muros, estructuras individuales
- **Precisión:** Alta

#### 🗺️ **Vista Regional (≤1km)**
- **Para qué:** Complejos arqueológicos, asentamientos
- **Escala:** Sitios completos, sistemas de estructuras
- **Precisión:** Media

#### 🌍 **Paisaje Completo (≤5km)**
- **Para qué:** Contexto regional, redes de sitios
- **Escala:** Paisajes culturales completos
- **Precisión:** Baja (solo contexto)

## 🧠 **INTERPRETACIÓN CIENTÍFICA**

### **Lo que SÍ puedes concluir:**
- "Existe un volumen con comportamiento espacial anómalo"
- "La anomalía tiene orientación dominante X°"
- "La persistencia vertical sugiere continuidad estructural"
- "El patrón es inconsistente con procesos naturales"

### **Lo que NO puedes concluir:**
- "Es un edificio de forma rectangular"
- "Tiene habitaciones internas"
- "Es de época romana/maya/etc."
- "Mide exactamente X metros"

## ⚠️ **LIMITACIONES EXPLÍCITAS**

### **Errores de Medición:**
- **Posición horizontal:** ±10-60m (según resolución)
- **Profundidad vertical:** ±2-9m (según penetración)
- **Orientación:** ±15° (según coherencia)

### **Resolución:**
- **Mínimo detectable:** 50m (estructuras muy pequeñas no se ven)
- **Máximo útil:** 300m (estructuras muy grandes se fragmentan)
- **Óptimo:** 100-200m (rango arqueológico típico)

## 🎯 **CASOS DE USO TÍPICOS**

### **Exploración Inicial:**
1. Abrir modelo volumétrico
2. Usar "Lupa Local" 
3. Explorar con slider de profundidad
4. Identificar orientación dominante

### **Análisis Detallado:**
1. Activar "Clustering" si hay múltiples señales
2. Cambiar a "Gradiente de Densidad"
3. Usar slider de transparencia para ver interior
4. Animar campo para mejor visualización

### **Validación:**
1. Comparar orientación con mapas históricos
2. Verificar escala con estructuras conocidas
3. Evaluar coherencia con topografía
4. Considerar limitaciones de resolución

## 🚨 **ERRORES COMUNES**

### **❌ Error:** "Veo un edificio rectangular"
**✅ Correcto:** "Veo un volumen anómalo con orientación dominante"

### **❌ Error:** "Mide exactamente 150m"
**✅ Correcto:** "Extensión aproximada 150±30m"

### **❌ Error:** "Es de época romana"
**✅ Correcto:** "Patrón consistente con intervención antrópica histórica"

### **❌ Error:** "Tiene 3 habitaciones"
**✅ Correcto:** "Clustering detecta 3 grupos de anomalías"

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **"No veo nada"**
- Verificar que el análisis haya detectado anomalías
- Ajustar transparencia (probar 40-60%)
- Cambiar a modo "Campo de Probabilidad"
- Usar "Animar Campo"

### **"Solo veo líneas amarillas"**
- Las líneas son vectores de orientación
- El volumen principal puede estar muy transparente
- Subir opacidad al 70-80%
- Verificar que hay partículas (puntos de colores)

### **"Errores en consola"**
- Normales durante desarrollo
- No afectan funcionalidad principal
- Recargar página si hay problemas graves

### **"El clustering no hace nada"**
- Solo funciona si hay múltiples anomalías
- Cambiar colores para mostrar grupos
- Probar en regiones con varias estructuras

## 📊 **DATOS TÉCNICOS**

### **Componentes del Modelo:**
- **Elipsoide base:** Volumen principal de la anomalía
- **Sistema de partículas:** Distribución interna de anomalías  
- **Wireframe:** Contorno sutil para referencia
- **Vectores:** Orientación dominante (líneas amarillas)
- **Grid:** Referencia espacial (líneas grises)

### **Algoritmos:**
- **Distribución espacial:** Basada en distancia al centro
- **Colores:** HSL dinámico según confianza
- **Transparencia:** Proporcional a certeza
- **Animación:** Función seno para "respiración"

---

**Recuerda:** Este es un **detector de anomalías**, no un **reconstructor de estructuras**. 
Su valor está en mostrar **dónde investigar**, no en **qué vas a encontrar**.