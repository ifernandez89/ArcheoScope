# 🏺 ARCHEOSCOPE - MANUAL DE USUARIO

**Sistema de Detección Arqueológica por Teledetección**  
*Versión 2.1 - Enero 2026*

---

## 📋 ÍNDICE

1. [¿Qué es ArcheoScope?](#qué-es-archeoscope)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Interfaz Principal](#interfaz-principal)
4. [Cómo Realizar un Análisis](#cómo-realizar-un-análisis)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Lupa Arqueológica](#lupa-arqueológica)
7. [Validación Científica](#validación-científica)
8. [Casos de Uso Prácticos](#casos-de-uso-prácticos)
9. [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
10. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🔍 ¿Qué es ArcheoScope?

ArcheoScope es un **sistema de detección arqueológica remota** que utiliza datos satelitales multiespectrales para identificar **persistencias espaciales no explicables por procesos naturales actuales**.

### 🎯 Paradigma Científico

**"ArcheoScope no busca estructuras arqueológicas específicas, sino patrones de persistencia espacial que sugieren intervención humana antigua"**

### 🛰️ Tecnología Utilizada

- **15 instrumentos satelitales** integrados (Sentinel-2, Landsat, MODIS, ICESat-2, GEDI, etc.)
- **Análisis multitemporal** (3-5 años de datos estacionales)
- **Motor de reglas arqueológicas** con validación científica
- **Inferencia volumétrica 3D** para reconstrucción geométrica
- **Filtros anti-modernos** para excluir estructuras contemporáneas

### 🌍 Aplicaciones

- **Prospección arqueológica** no invasiva
- **Validación de sitios conocidos** con nuevas perspectivas
- **Detección de paisajes culturales** invisibles
- **Investigación de civilizaciones perdidas**
- **Análisis de modificación antrópica del paisaje**

---

## 🚀 Acceso al Sistema

### Requisitos Previos
- Navegador web moderno (Chrome, Firefox, Edge)
- Conexión a internet estable
- Conocimientos básicos de coordenadas geográficas

### URLs de Acceso
- **Interfaz Principal**: http://localhost:8001
- **API Backend**: http://localhost:8003 (solo para desarrolladores)

### Verificación del Sistema
Al acceder, verifica que veas:
- ✅ Mapa interactivo cargado
- ✅ Paneles de control visibles
- ✅ Indicadores de estado en verde

---

## 🖥️ Interfaz Principal

### Layout de 3 Paneles

```
┌─────────────┬──────────────────┬─────────────────┐
│   CONTROLES │       MAPA       │    ANÁLISIS     │
│             │    INTERACTIVO   │   RESULTADOS    │
│  • Capas    │                  │  • Instrumentos │
│  • Reglas   │   🗺️ Leaflet    │  • Anomalías    │
│  • Config   │                  │  • Validación   │
└─────────────┴──────────────────┴─────────────────┘
```

### 🎛️ Panel de Controles (Izquierda)

#### Capas Espectrales
- **📡 Anomalías Espaciales**: Patrones geométricos no naturales
- **🏛️ Firmas Arqueológicas**: Indicadores de intervención humana
- **🌿 Procesos Naturales**: Patrones explicables naturalmente
- **📊 Inferencia Volumétrica**: Reconstrucción 3D probabilística

#### Reglas Arqueológicas
- **🌱 Desacople Vegetación-Topografía**: Vegetación anómala vs. condiciones esperadas
- **🌡️ Patrones Térmicos Residuales**: Inercia térmica de estructuras enterradas

#### Utilidades
- **🧪 Test de Lupa**: Probar detección de anomalías
- **🗑️ Limpiar Caché**: Reiniciar análisis

### 🗺️ Mapa Central

#### Funcionalidades Interactivas
- **Zoom**: Rueda del ratón o controles
- **Pan**: Arrastrar para mover
- **Selección de Región**: Ctrl + arrastrar para seleccionar área
- **Inspección de Píxel**: Click para ver datos específicos

#### Modos de Selección
1. **📍 Click**: Colocar pin en ubicación específica
2. **🔲 Área**: Dibujar rectángulo de análisis
3. **📍 Múltiple**: Colocar varios pins para comparación

### 📊 Panel de Análisis (Derecha)

#### Secciones Principales
- **🔍 Inspección de Píxel**: Datos del punto seleccionado
