# 🌍 Release Notes - Sistema de Biomas v1.0

## Fecha: 13 de Febrero, 2026

## 🎉 Nuevas Características

### Sistema de Detección de Biomas
- **Detección automática** de biomas basada en coordenadas geográficas
- **6 tipos de biomas**: Ice (Hielo), Volcanic (Volcánico), Desert (Desierto), Ocean (Océano), Forest (Bosque), Default (Genérico)
- **Información contextual** con temperatura y humedad por bioma

### Ambientación Completa para Regiones Heladas ❄️

#### Visual
- Terreno helado con grietas y formaciones de hielo (seracs)
- Material blanco-azulado con reflejos realistas
- 2000 partículas de nieve cayendo constantemente
- Cielo azul pálido característico de regiones polares
- Niebla blanca-azulada más densa

#### Iluminación
- Sistema de iluminación especializado para hielo
- Tonos fríos azulados (#f0f8ff, #d0e8f2, #c8e0f0)
- Mayor intensidad para simular reflejos en hielo
- Luz de reflejo desde el suelo
- Animación sutil de intensidad

#### Interfaz
- Panel de información mostrando datos del bioma
- Icono distintivo por tipo de bioma (❄️ para hielo)
- Temperatura y humedad del ambiente
- Descripción contextual de la región

### Regiones Heladas Detectadas
- **Ártico**: Latitud > 66.5°
- **Antártico**: Latitud < -66.5°
- **Groenlandia**: lat > 60, lon -73 a -12
- **Islandia**: lat 63-67, lon -25 a -13
- **Patagonia Glaciar**: lat < -45, lon -75 a -65
- **Himalaya y Tibet**: lat 27-36, lon 75-105
- **Alaska Glaciar**: lat > 58, lon -170 a -130

### Integración con Ollama (Bonus) 🦙
- Soporte para LLM local con Ollama
- Compatible con gemma2:2b y otros modelos
- Configuración mediante variables de entorno
- Intercambio fácil entre OpenRouter y Ollama

## 🔧 Mejoras Técnicas

### Archivos Nuevos
- `viewer3d/utils/biome-detector.ts` - Detector de biomas
- `viewer3d/components/IceTerrain.tsx` - Terreno helado
- `viewer3d/components/SnowParticles.tsx` - Sistema de nieve
- `viewer3d/components/IceLighting.tsx` - Iluminación para hielo
- `viewer3d/ai/ollama-integration.ts` - Integración con Ollama

### Archivos Modificados
- `viewer3d/components/ImmersiveScene.tsx` - Detección y renderizado condicional
- `viewer3d/components/DynamicSky.tsx` - Color personalizable
- `viewer3d/components/LocationInfo.tsx` - Información de bioma
- `viewer3d/components/ConversationalAvatar.tsx` - Soporte Ollama
- `viewer3d/.env.local` - Configuración de providers

### Optimizaciones
- Agua solo visible en biomas no helados
- Renderizado condicional según tipo de bioma
- Colores dinámicos de cielo y niebla
- Log automático de bioma detectado

## 📍 Coordenadas de Prueba

### Regiones Heladas
- **Polo Norte**: 90, 0
- **Polo Sur**: -90, 0
- **Groenlandia**: 72, -40
- **Monte Everest**: 27.9881, 86.9250
- **Glaciar Perito Moreno**: -50.4950, -73.1400
- **Antártica**: -80.4, -97.7234

### Otras Regiones (Comparación)
- **Hawái (Volcánico)**: 19.4194, -155.2885
- **Sahara (Desierto)**: 25, 5
- **Pacífico (Océano)**: 0, -160

## 🚀 Cómo Usar

1. Visita https://tu-usuario.github.io/ArcheoScope/
2. Ingresa coordenadas en el input superior izquierdo
3. Observa la transición cinematográfica
4. Explora la ambientación del bioma
5. Revisa el panel de información (botón "📍 Mostrar Info")

## 🎯 Próximas Mejoras

- Más tipos de biomas (selva tropical, tundra, sabana)
- Efectos climáticos adicionales (lluvia, tormenta, aurora boreal)
- Fauna y flora según bioma
- Sonidos ambientales contextuales
- Transiciones graduales de temperatura

## 🐛 Correcciones

- Agua ahora se oculta correctamente en regiones heladas
- Detección precisa de regiones polares
- Iluminación adaptada a cada tipo de bioma

## 📚 Documentación

Ver archivos:
- `IMPLEMENTACION_BIOMAS.md` - Detalles técnicos completos
- `COORDENADAS_HIELO_TEST.md` - Lista de coordenadas para testing

---

**Versión**: 1.0.0
**Fecha**: 13 de Febrero, 2026
**Autor**: ArcheoScope Team
