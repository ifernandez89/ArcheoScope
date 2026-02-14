/**
 * Shader del Sol - Plasma turbulento procedural con comportamiento orgánico
 * 
 * CARACTERÍSTICAS MEJORADAS:
 * - FBM (Fractal Brownian Motion) multi-octava
 * - Simplex 3D Noise para turbulencia natural
 * - Distorsión UV dinámica (plasma fluyendo)
 * - Variación térmica con pulsos de calor
 * - Micro displacement radial (vibración térmica)
 * - Flujos tangenciales (movimiento lateral)
 * - Granulación celular (Voronoi)
 * - Alto contraste (zonas oscuras + brillos intensos)
 * - Limb darkening realista
 * - Emisión térmica variable
 * 
 * FILOSOFÍA:
 * No es una textura estática. Es comportamiento matemático.
 * El Sol respira, fluye, pulsa. Como plasma real.
 * 
 * TÉCNICAS:
 * - Vertex Shader: Displacement + flujos tangenciales
 * - Fragment Shader: FBM + distorsión UV + variación térmica
 * - Ruido procedural: Simplex 3D + Voronoi
 * - Colorimetría: Gradiente térmico realista
 */

export const sunVertexShader = `
  varying vec2 vUv;
  varying vec3 vPosition;
  varying vec3 vNormal;
  uniform float time;
  
  // Noise para desplazamiento de vértices (protuberancias)
  float hash(vec3 p) {
    p = fract(p * 0.3183099 + 0.1);
    p *= 17.0;
    return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
  }
  
  float noise(vec3 x) {
    vec3 p = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    
    return mix(
      mix(mix(hash(p + vec3(0,0,0)), hash(p + vec3(1,0,0)), f.x),
          mix(hash(p + vec3(0,1,0)), hash(p + vec3(1,1,0)), f.x), f.y),
      mix(mix(hash(p + vec3(0,0,1)), hash(p + vec3(1,0,1)), f.x),
          mix(hash(p + vec3(0,1,1)), hash(p + vec3(1,1,1)), f.x), f.y),
      f.z);
  }
  
  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    
    // Posición base
    vec3 pos = position;
    
    // 🌊 MICRO DISPLACEMENT RADIAL - Vibración térmica sutil
    vec3 thermalCoord = position * 5.0 + vec3(time * 0.05, time * 0.04, time * 0.03);
    float thermalVibration = noise(thermalCoord) * 0.02;
    
    // 🔥 PROTUBERANCIAS EN EL BORDE - Clave para el efecto de fuego
    vec3 noiseCoord = position * 3.0 + vec3(time * 0.03, time * 0.025, 0.0);
    float displacement = noise(noiseCoord) * 0.5 + noise(noiseCoord * 2.0) * 0.25;
    
    // 🌡️ FLUJOS TANGENCIALES - Movimiento lateral en la superficie
    vec3 flowCoord = position * 4.0 + vec3(time * 0.04, -time * 0.035, 0.0);
    float tangentialFlow = noise(flowCoord) * 0.15;
    
    // Solo en el borde (basado en la normal)
    float edgeFactor = pow(1.0 - abs(dot(normalize(position), vec3(0.0, 1.0, 0.0))), 2.0);
    displacement *= edgeFactor * 0.15; // Protuberancias sutiles
    tangentialFlow *= edgeFactor * 0.08;
    
    // Aplicar desplazamiento combinado
    pos += normal * (displacement + thermalVibration);
    
    // Desplazamiento tangencial (perpendicular a la normal)
    vec3 tangent = normalize(cross(normal, vec3(0.0, 1.0, 0.0)));
    pos += tangent * tangentialFlow;
    
    vPosition = pos;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  }
`

export const sunFragmentShader = `
  uniform sampler2D sunTexture;
  uniform float time;
  uniform float intensity;
  
  varying vec2 vUv;
  varying vec3 vPosition;
  varying vec3 vNormal;
  
  // Simplex 3D Noise
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
  vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
  
  float snoise(vec3 v) {
    const vec2 C = vec2(1.0/6.0, 1.0/3.0);
    const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
    
    vec3 i  = floor(v + dot(v, C.yyy));
    vec3 x0 = v - i + dot(i, C.xxx);
    
    vec3 g = step(x0.yzx, x0.xyz);
    vec3 l = 1.0 - g;
    vec3 i1 = min(g.xyz, l.zxy);
    vec3 i2 = max(g.xyz, l.zxy);
    
    vec3 x1 = x0 - i1 + C.xxx;
    vec3 x2 = x0 - i2 + C.yyy;
    vec3 x3 = x0 - D.yyy;
    
    i = mod289(i);
    vec4 p = permute(permute(permute(
              i.z + vec4(0.0, i1.z, i2.z, 1.0))
            + i.y + vec4(0.0, i1.y, i2.y, 1.0))
            + i.x + vec4(0.0, i1.x, i2.x, 1.0));
    
    float n_ = 0.142857142857;
    vec3 ns = n_ * D.wyz - D.xzx;
    
    vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
    
    vec4 x_ = floor(j * ns.z);
    vec4 y_ = floor(j - 7.0 * x_);
    
    vec4 x = x_ *ns.x + ns.yyyy;
    vec4 y = y_ *ns.x + ns.yyyy;
    vec4 h = 1.0 - abs(x) - abs(y);
    
    vec4 b0 = vec4(x.xy, y.xy);
    vec4 b1 = vec4(x.zw, y.zw);
    
    vec4 s0 = floor(b0)*2.0 + 1.0;
    vec4 s1 = floor(b1)*2.0 + 1.0;
    vec4 sh = -step(h, vec4(0.0));
    
    vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
    vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
    
    vec3 p0 = vec3(a0.xy, h.x);
    vec3 p1 = vec3(a0.zw, h.y);
    vec3 p2 = vec3(a1.xy, h.z);
    vec3 p3 = vec3(a1.zw, h.w);
    
    vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
    p0 *= norm.x;
    p1 *= norm.y;
    p2 *= norm.z;
    p3 *= norm.w;
    
    vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
    m = m * m;
    return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
  }
  
  // Fractal Brownian Motion
  float fbm(vec3 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for(int i = 0; i < 5; i++) {
      value += amplitude * snoise(p * frequency);
      frequency *= 2.0;
      amplitude *= 0.5;
    }
    
    return value;
  }
  
  // Voronoi Noise para granulación celular
  vec2 voronoi(vec2 x) {
    vec2 p = floor(x);
    vec2 f = fract(x);
    
    float minDist = 1.0;
    vec2 minPoint;
    
    for(int j = -1; j <= 1; j++) {
      for(int i = -1; i <= 1; i++) {
        vec2 neighbor = vec2(float(i), float(j));
        vec2 point = neighbor + vec2(
          fract(sin(dot(p + neighbor, vec2(127.1, 311.7))) * 43758.5453),
          fract(sin(dot(p + neighbor, vec2(269.5, 183.3))) * 43758.5453)
        );
        
        vec2 diff = neighbor + point - f;
        float dist = length(diff);
        
        if(dist < minDist) {
          minDist = dist;
          minPoint = point;
        }
      }
    }
    
    return vec2(minDist, 0.0);
  }
  
  void main() {
    // 🌊 DISTORSIÓN UV DINÁMICA - Plasma fluyendo
    vec2 distortedUV = vUv;
    vec3 distortCoord = vPosition * 2.0 + vec3(time * 0.02, time * 0.015, 0.0);
    float distortX = snoise(distortCoord) * 0.03;
    float distortY = snoise(distortCoord + vec3(100.0, 0.0, 0.0)) * 0.03;
    distortedUV += vec2(distortX, distortY);
    
    // Textura base del Sol con UV distorsionada
    vec4 texColor = texture2D(sunTexture, distortedUV);
    
    // Distancia desde el centro (para gradiente radial)
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(vUv, center);
    
    // 1️⃣ MANCHAS SOLARES GRANDES - Zonas oscuras definidas (más lentas)
    vec3 spotCoord = vPosition * 1.5 + vec3(time * 0.005, time * 0.004, 0.0);
    float spots = snoise(spotCoord);
    float darkSpots = smoothstep(0.2, 0.5, spots);
    
    // 2️⃣ FLUJOS TURBULENTOS - Patrones de convección (más complejos)
    vec3 flowCoord = vPosition * 2.5 + vec3(time * 0.012, time * 0.01, time * 0.008);
    float flows = fbm(flowCoord);
    
    // 🔥 FLUJOS SECUNDARIOS - Turbulencia adicional
    vec3 flowCoord2 = vPosition * 3.5 + vec3(time * 0.018, -time * 0.015, 0.0);
    float flows2 = fbm(flowCoord2) * 0.5;
    flows = flows * 0.7 + flows2 * 0.3;
    
    // 3️⃣ GRANULACIÓN CELULAR - Textura fina (más dinámica)
    vec2 cellCoord = vUv * 12.0 + vec2(time * 0.006, time * 0.005);
    vec2 cells = voronoi(cellCoord);
    float cellPattern = smoothstep(0.05, 0.25, cells.x);
    
    // 4️⃣ REGIONES ACTIVAS BRILLANTES - Zonas calientes (más variación)
    vec3 activeCoord = vPosition * 2.0 + vec3(time * 0.008, time * 0.007, 0.0);
    float activeZones = smoothstep(0.4, 0.75, snoise(activeCoord));
    
    // 🌡️ VARIACIÓN TÉRMICA - Pulsos de calor
    vec3 thermalCoord = vPosition * 1.2 + vec3(time * 0.01, 0.0, time * 0.01);
    float thermalPulse = snoise(thermalCoord) * 0.5 + 0.5;
    
    // 5️⃣ COMBINAR CAPAS CON VARIACIÓN TÉRMICA
    float activity = flows * 0.35 + cellPattern * 0.25 + activeZones * 0.4;
    activity *= darkSpots; // Las manchas oscuras reducen la actividad
    activity = mix(activity, activity * thermalPulse, 0.3); // Modulación térmica
    
    // ALTO CONTRASTE
    float brightness = smoothstep(-0.1, 1.0, activity);
    
    // Limb darkening más pronunciado
    float limbDarkening = smoothstep(1.0, 0.15, dist * 2.0);
    brightness *= limbDarkening;
    
    // 6️⃣ COLORIMETRÍA DE FUEGO INTENSO - Gradiente térmico
    vec3 deepShadow = vec3(0.2, 0.08, 0.0);      // Manchas oscuras
    vec3 darkOrange = vec3(0.6, 0.25, 0.05);     // Zonas frías
    vec3 midOrange = vec3(1.0, 0.55, 0.15);      // Temperatura media
    vec3 brightYellow = vec3(1.0, 0.9, 0.4);     // Zonas calientes
    vec3 hotWhite = vec3(1.0, 0.98, 0.9);        // Regiones muy calientes
    
    vec3 solarColor;
    if(brightness < 0.2) {
      solarColor = mix(deepShadow, darkOrange, brightness / 0.2);
    } else if(brightness < 0.5) {
      solarColor = mix(darkOrange, midOrange, (brightness - 0.2) / 0.3);
    } else if(brightness < 0.75) {
      solarColor = mix(midOrange, brightYellow, (brightness - 0.5) / 0.25);
    } else {
      solarColor = mix(brightYellow, hotWhite, (brightness - 0.75) / 0.25);
    }
    
    // Mezclar con textura original (mínimo)
    vec3 finalColor = mix(solarColor, texColor.rgb, 0.15);
    
    // 🔥 EMISIÓN TÉRMICA - Zonas brillantes emiten más
    float emission = pow(brightness, 1.5) * intensity;
    finalColor *= (1.0 + emission * 3.0);
    
    // ✨ VARIACIÓN DE BRILLO - Pulsaciones sutiles
    float brightnessVariation = sin(time * 0.5 + brightness * 10.0) * 0.05 + 1.0;
    finalColor *= brightnessVariation;
    
    gl_FragColor = vec4(finalColor, 1.0);
  }
`

export const coronaFragmentShader = `
  uniform float time;
  uniform float opacity;
  
  varying vec2 vUv;
  varying vec3 vPosition;
  varying vec3 vNormal;
  
  // Simplex noise simplificado
  float hash(vec3 p) {
    p = fract(p * 0.3183099 + 0.1);
    p *= 17.0;
    return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
  }
  
  float noise(vec3 x) {
    vec3 p = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    
    return mix(
      mix(mix(hash(p + vec3(0,0,0)), hash(p + vec3(1,0,0)), f.x),
          mix(hash(p + vec3(0,1,0)), hash(p + vec3(1,1,0)), f.x), f.y),
      mix(mix(hash(p + vec3(0,0,1)), hash(p + vec3(1,0,1)), f.x),
          mix(hash(p + vec3(0,1,1)), hash(p + vec3(1,1,1)), f.x), f.y),
      f.z);
  }
  
  // FBM para borde más complejo
  float fbm(vec3 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for(int i = 0; i < 3; i++) {
      value += amplitude * noise(p);
      p *= 2.0;
      amplitude *= 0.5;
    }
    return value;
  }
  
  void main() {
    // Distancia desde el centro
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(vUv, center);
    
    // Gradiente radial suave
    float radialGradient = smoothstep(0.5, 0.0, dist);
    
    // BORDE VIOLENTO - Irregular con erupciones
    vec3 noiseCoord = vPosition * 6.0 + vec3(time * 0.015, time * 0.012, 0.0);
    float edgeNoise = fbm(noiseCoord);
    
    // Erupciones ocasionales que salen y se retraen
    vec3 eruptionCoord = vPosition * 3.0 + vec3(time * 0.02, 0.0, 0.0);
    float eruptions = smoothstep(0.4, 0.8, noise(eruptionCoord));
    
    // Combinar irregularidad
    float irregularity = edgeNoise * 0.7 + eruptions * 0.3;
    
    // Alpha irregular (borde desgarrado)
    float alpha = radialGradient * irregularity * opacity;
    
    // Color naranja profundo (menos saturado)
    vec3 coronaColor = vec3(0.9, 0.5, 0.15);
    
    gl_FragColor = vec4(coronaColor, alpha);
  }
`
