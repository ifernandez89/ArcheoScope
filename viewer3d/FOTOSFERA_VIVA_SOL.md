# Fotosfera Viva del Sol - Sistema Orgánico

## 🔥 Concepto

Una fotosfera respirando, una piel solar viva, fuego contenido bajo tensión.

No llamaradas explosivas. Sino **presión térmica contenida**. Una **estrella viva**.

## 🎯 Filosofía de Diseño

### Lo que NO es:
- ❌ Animaciones lineales
- ❌ Loops sincronizados
- ❌ Explosiones arcade
- ❌ Efectos predecibles

### Lo que SÍ es:
- ✅ Presión térmica contenida
- ✅ Movimiento orgánico caótico
- ✅ Respiración asíncrona
- ✅ Plasma turbulento
- ✅ Piel energética viva

## 🌊 Sistema de 3 Capas

### Capa 1: Movimiento Líquido (1.02x)
**Posición:** Casi pegada a la superficie del núcleo

**Características:**
- Color: `#ffcc44` (amarillo cálido)
- Opacidad base: 0.15 (respira entre 0.10 - 0.20)
- Escala: Pulsa entre 1.012 - 1.028
- Lado: `FrontSide` (visible desde fuera)

**Rotación Multi-Eje:**
```
X: +0.00003 rad/frame (lenta, hacia adelante)
Y: +0.0001 rad/frame (principal, hacia derecha)
Z: +0.00005 rad/frame (diagonal)
```

**Efecto:** Movimiento líquido lento, como plasma denso fluyendo sobre la superficie.

### Capa 2: Presión Térmica Contenida (1.05x)
**Posición:** Capa media, más separada

**Características:**
- Color: `#ffaa33` (naranja intenso)
- Opacidad base: 0.12 (respira entre 0.08 - 0.16)
- Escala: Pulsa entre 1.038 - 1.062
- Lado: `FrontSide`

**Rotación Multi-Eje (INVERSA):**
```
X: -0.00004 rad/frame (contra-rotación)
Y: -0.00008 rad/frame (inversa a capa 1)
Z: +0.00006 rad/frame (diagonal opuesta)
```

**Efecto:** Contra-rotación crea turbulencia visual, simula corrientes de convección opuestas.

### Capa 3: Piel Energética Exterior (1.08x)
**Posición:** Exterior, más alejada

**Características:**
- Color: `#ff9922` (naranja rojizo)
- Opacidad base: 0.08 (respira entre 0.05 - 0.11)
- Escala: Pulsa entre 1.065 - 1.095
- Lado: `BackSide` (halo exterior)

**Rotación Multi-Eje (DIAGONAL):**
```
X: +0.00007 rad/frame (más rápida)
Y: +0.00012 rad/frame (más rápida que todas)
Z: -0.00004 rad/frame (inversa)
```

**Efecto:** Movimiento diagonal complejo, crea sensación de energía escapando.

## 🎨 Técnicas Implementadas

### 1. Respiración Asíncrona
Cada capa tiene su propio ritmo de expansión/contracción:

```typescript
// Capa 1: Lenta y suave
flow1 = sin(time * 0.15) * 0.008 + 1.0
pulse1 = sin(time * 0.12 + 1.2) * 0.006

// Capa 2: Media, desfasada
flow2 = sin(time * 0.11 + 2.5) * 0.012 + 1.0
pulse2 = cos(time * 0.09) * 0.008

// Capa 3: Más lenta, muy desfasada
flow3 = cos(time * 0.08 + 4.0) * 0.015 + 1.0
pulse3 = sin(time * 0.13 + 3.0) * 0.01
```

**Resultado:** Nunca se sincronizan, movimiento perpetuamente orgánico.

### 2. Rotación Multi-Eje
Cada capa rota en X, Y, Z simultáneamente:

- **Capa 1:** Rotación principal en Y, sutiles en X y Z
- **Capa 2:** Contra-rotación en X e Y, diagonal en Z
- **Capa 3:** Rotación diagonal compleja

**Resultado:** Movimiento tridimensional caótico, como plasma real.

### 3. Opacidad Variable
La opacidad respira independientemente de la escala:

```typescript
// Capa 1: Frecuencia 0.18, amplitud 0.05
opacity1 = 0.15 + sin(time * 0.18) * 0.05

// Capa 2: Frecuencia 0.14, amplitud 0.04, desfasada
opacity2 = 0.12 + cos(time * 0.14 + 1.5) * 0.04

// Capa 3: Frecuencia 0.1, amplitud 0.03, muy desfasada
opacity3 = 0.08 + sin(time * 0.1 + 2.8) * 0.03
```

**Resultado:** Flujo de plasma visible, zonas más densas y menos densas.

### 4. Blending Aditivo
Todas las capas usan `AdditiveBlending`:

```typescript
blending: THREE.AdditiveBlending
depthWrite: false
```

**Resultado:** Las capas se suman visualmente, creando zonas más brillantes donde se superponen.

## 🔬 Física Simulada

### Convección Solar
Las contra-rotaciones simulan las **células de convección** reales del Sol:
- Plasma caliente sube (capa exterior más rápida)
- Plasma frío baja (capa interior más lenta)
- Rotación diferencial (cada capa a diferente velocidad)

### Turbulencia
Rotación multi-eje crea **turbulencia visual**:
- No hay ejes fijos
- Movimiento impredecible
- Caos natural

### Presión Térmica
La respiración simula **presión interna**:
- Expansión = liberación de energía
- Contracción = acumulación de presión
- Ciclo perpetuo

## 📊 Parámetros de Configuración

### Velocidades de Rotación
| Capa | Eje X | Eje Y | Eje Z | Carácter |
|------|-------|-------|-------|----------|
| 1 | +0.00003 | +0.0001 | +0.00005 | Lento, fluido |
| 2 | -0.00004 | -0.00008 | +0.00006 | Inverso, turbulento |
| 3 | +0.00007 | +0.00012 | -0.00004 | Rápido, diagonal |

### Frecuencias de Respiración
| Capa | Escala | Opacidad | Desfase |
|------|--------|----------|---------|
| 1 | 0.15, 0.12 | 0.18 | 1.2 |
| 2 | 0.11, 0.09 | 0.14 | 2.5, 1.5 |
| 3 | 0.08, 0.13 | 0.10 | 4.0, 2.8 |

### Amplitudes
| Capa | Escala Flow | Escala Pulse | Opacidad |
|------|-------------|--------------|----------|
| 1 | 0.008 | 0.006 | 0.05 |
| 2 | 0.012 | 0.008 | 0.04 |
| 3 | 0.015 | 0.010 | 0.03 |

## 🎯 Resultado Visual

### Desde Lejos
- Sol parece "respirar" orgánicamente
- Halo exterior pulsa sutilmente
- Sensación de estrella viva

### Desde Cerca
- Capas visibles moviéndose independientemente
- Turbulencia en la superficie
- Plasma fluyendo en diferentes direcciones
- Zonas más brillantes y menos brillantes cambiando

### En Movimiento
- Nunca se repite exactamente
- Movimiento perpetuamente interesante
- Caos natural, no artificial

## 🔧 Arquitectura Técnica

### Estructura de Capas
```
Sol (group)
├── 1. Núcleo (shader procedural)
├── 2. Fotosfera Capa 1 (líquido)
├── 3. Fotosfera Capa 2 (presión)
├── 4. Fotosfera Capa 3 (piel)
├── 5. Corona (shader)
├── 6. Glow (halo)
├── 7. Luz direccional
└── 8. Luz puntual
```

### Orden de Renderizado
1. Núcleo (opaco, shader)
2. Fotosfera 1-3 (transparentes, aditivas)
3. Corona (transparente, aditiva)
4. Glow (transparente, aditivo)

### Performance
- **Geometrías:** 128, 96, 64 segmentos (optimizado)
- **Materiales:** `meshBasicMaterial` (sin cálculos de luz)
- **Blending:** Aditivo (GPU-acelerado)
- **FPS:** Sin impacto significativo

## 🎨 Paleta de Colores

```
Capa 1: #ffcc44 (amarillo cálido)
Capa 2: #ffaa33 (naranja intenso)
Capa 3: #ff9922 (naranja rojizo)
Corona: (shader procedural)
Glow:   #ff9933 (naranja suave)
```

Gradiente natural: amarillo → naranja → rojo (como fuego real)

## 🚀 Cómo Revertir

Si no te gusta, simplemente elimina las 3 capas de fotosfera:

1. Eliminar refs: `photosphereLayer1Ref`, `photosphereLayer2Ref`, `photosphereLayer3Ref`
2. Eliminar secciones de animación en `useFrame`
3. Eliminar meshes de fotosfera en el JSX
4. Mantener núcleo, corona y glow originales

El sistema es modular, no afecta otras partes.

## 📝 Notas de Diseño

### Por qué 3 capas
- 1 capa: Demasiado simple
- 2 capas: Predecible
- 3 capas: Complejidad orgánica
- 4+ capas: Sobrecarga visual

### Por qué rotación multi-eje
- Solo Y: Movimiento plano, aburrido
- X+Y: Mejor, pero predecible
- X+Y+Z: Caótico, orgánico, vivo

### Por qué contra-rotación
- Todas en misma dirección: Sincronizado, artificial
- Contra-rotación: Turbulencia, realismo
- Velocidades diferentes: Caos natural

### Por qué opacidad variable
- Opacidad fija: Estático
- Opacidad respirando: Flujo de plasma visible
- Desfasada: Nunca sincroniza, perpetuamente interesante

## 🌟 Inspiración

- Imágenes NASA del Sol
- Células de convección solar
- Plasma en movimiento
- Fuego contenido bajo presión
- Estrellas vivas, no bolas estáticas

---

**Estado:** ✅ Implementado  
**Performance:** Excelente  
**Reversible:** Sí (modular)  
**Efecto:** Fotosfera viva y orgánica
