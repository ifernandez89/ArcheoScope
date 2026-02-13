# Changelog - ArcheoScope 3D Viewer

## [2024-02-13] - Sistema Astronómico-Sonoro Completo + Mejoras Visuales

### ✨ Nuevas Características

#### Sistema Astronómico Vivo
- **Motor Solar Real**: Cálculo astronómico preciso basado en fecha, hora y ubicación GPS
  - Usa UTC + ajuste de longitud para tiempo solar local
  - Calcula declinación solar, altura y azimut en tiempo real
  - Transiciones suaves entre día y noche

- **Trayectoria Solar Visualizada**:
  - Arco dorado mostrando el recorrido completo del sol durante el día
  - Posición actual del sol con esfera pulsante
  - Ejes cardinales (Norte-Sur, Este-Oeste) en azul sutil
  - Eje axial terrestre inclinado 23.44° en verde
  - Todos los elementos en capa 1 (no interfieren con movimiento)

- **Iluminación Estacional**:
  - Color de luz cambia según hora del día (amanecer naranja → mediodía blanco → atardecer naranja)
  - Intensidad dinámica basada en altura solar
  - Niebla volumétrica que responde al ciclo día/noche

- **Cielo Dinámico Mejorado**:
  - Estrellas con textura circular suave (no más cuadrados pixelados)
  - Tamaños variables (90% pequeñas, 10% grandes)
  - Colores sutiles azul-blanco con bajo saturación
  - Efecto de brillo suave con gradiente radial

- **Sistema de Sonido Atmosférico**:
  - Dron armónico procedural que cambia con la altura solar (80Hz noche → 240Hz día)
  - Viento ambiental dinámico con variación lenta
  - Sin melodías reconocibles - solo textura sonora espacial
  - El mundo "respira" con el cosmos

- **Efectos Cósmicos en Avatares**:
  - Aura dorada sutil que pulsa alrededor de cada entidad
  - Eje visual conectando avatar con el sol
  - Efectos en capa 1 (invisibles para raycaster)

#### Mejoras de Movimiento
- **Sistema de Capas Three.js**:
  - Capa 0: Terreno (detectado por raycaster)
  - Capa 1: Efectos visuales (ignorados por raycaster)
  - Movimiento fluido sin bloqueos por efectos visuales

- **Avatares Mejorados**:
  - Warrior: Animaciones de rig si están disponibles
  - Moai: Deslizamiento místico con oscilación vertical
  - Sphinx: Movimiento majestuoso con peso
  - OVNI: Vuelo flotante a 5m de altura con inclinación sutil (reducida 70%)

#### Detección Inteligente de Océano
- **Terreno Volcánico Condicional**:
  - Detecta automáticamente si las coordenadas están en océano abierto
  - Océano Pacífico (lon < -70 y lon > 100)
  - Océano Atlántico central
  - Océano Índico
  - Excluye costas de continentes e islas principales
  - Solo muestra agua en ubicaciones oceánicas

#### Sitios Arqueológicos Expandidos
- **10 Sitios Famosos**:
  - Machu Picchu, Pirámides de Giza, Stonehenge, Petra, Angkor Wat
  - Chichén Itzá, Coliseo Romano, Acrópolis, Teotihuacán, Moai (Isla de Pascua)

- **Descubrimientos ArcheoScope**:
  - Anomalía Patagonia (-45.2°, -71.5°)
  - Estructura Anatolia (37.2°, 38.9°)
  - Anomalía Puerto Rico (18.3°, -66.5°)
  - Formación Amazonas (-3.1°, -60.0°)

- **Panel Scrolleable**: Barra lateral para acceder a todos los sitios

### 🐛 Correcciones

#### Coordenadas y Navegación
- **Longitud Corregida en Argentina**: Ahora muestra correctamente -60° (antes mostraba positivo)
  - Usa transformación de matriz inversa para cálculo preciso
  - Click en globo devuelve coordenadas GPS reales

#### Interfaz Visual
- **Círculo de Horizonte Invisible**: Opacidad 0 (antes 0.15)
- **Proyección de Sombra Invisible**: Forzada a opacidad 0 en todo momento
- **Terreno Volcánico Mejorado**:
  - Amplitud base aumentada 50% (1.0 → 1.5)
  - Rugosidad aumentada 20% (1.0 → 1.2)
  - Zonas tropicales ahora tienen relieve visible (0.6 → 1.2)

#### Rotación de OVNI
- **Inclinación Reducida**: De 0.15 a 0.05 (70% menos)
- **Balanceo Lateral Reducido**: De 0.08 a 0.03 (62% menos)
- **Interpolación Suave**: Cambio de asignación directa a lerp
- **Reset Agresivo**: Factor 0.85 en lugar de 0.95

#### Problemas Técnicos Resueltos
- **Error de Serialización Next.js**: 
  - Cambio de `THREE.Vector3` a objetos planos `{ x, y, z }` en estado
  - Conversión a Vector3 solo dentro de componentes que lo necesitan
  
- **Error de TypeScript con Refs**:
  - Cambio de `useRef` a `useState` para objetos 3D mutables
  - Soluciona "Cannot assign to 'current' because it is a read-only property"

- **Loop Infinito de Re-renders**:
  - Eliminado callback `onModelChange` que causaba renders infinitos
  - Logs de debug removidos para mejor performance

### 🎨 Mejoras de Experiencia

#### Controles
- W/A/S/D: Movimiento del avatar
- Q/E: Rotación del avatar
- Espacio: Salto (avatares terrestres)
- Cámara tercera persona con seguimiento suave

#### Visual
- Post-processing sutil (bloom + viñeta)
- Partículas ambientales flotantes
- Agua minimalista siempre visible
- Grid sutil para referencia de movimiento

#### Performance
- Raycaster optimizado (solo capa 0)
- Efectos visuales en capa separada
- Geometrías con LOD apropiado
- Materiales optimizados para reaccionar a luz

### 🔧 Cambios Técnicos

#### Arquitectura
- `AstronomicalWorld.tsx`: Sistema astronómico integrado
- `SolarEngine.ts`: Cálculos solares precisos
- `SeasonalLight.ts`: Iluminación dinámica
- `SkyEngine.ts`: Cielo procedural
- `AtmosphericSound.ts`: Sistema de audio espacial
- `SolarTrajectory.tsx`: Visualización de trayectoria solar
- `CosmicEntity.tsx`: Efectos cósmicos en avatares

#### Optimizaciones
- Sistema de capas para raycasting selectivo
- Estado serializable para Next.js SSR
- Refs mutables con useState para objetos 3D
- Detección de océano con memoización

### 📝 Notas

- El sistema astronómico usa la fecha/hora/ubicación real del usuario
- Los efectos cósmicos son sutiles y contemplativos, no intrusivos
- El sonido atmosférico es procedural, sin loops reconocibles
- La detección de océano es aproximada, puede requerir ajustes para islas pequeñas

---

**Versión**: 0.2.0  
**Fecha**: 13 de Febrero, 2026  
**Build**: Producción optimizada  
**Estado**: ✅ Estable
