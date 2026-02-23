/**
 * Shader de Distorsión Espacial
 * Crea efecto de "espacio vibrando" cerca de anomalías
 */

export const spatialDistortionVertex = `
  uniform float time;
  uniform vec3 anomalyCenter;
  uniform float anomalyRadius;
  uniform float distortionStrength;
  uniform float resonance;
  
  varying vec3 vWorldPosition;
  varying vec3 vNormal;
  varying float vDistortion;
  
  void main() {
    // Posición en espacio mundial
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    vWorldPosition = worldPosition.xyz;
    vNormal = normalize(normalMatrix * normal);
    
    // Calcular distancia a la anomalía
    float dist = distance(vWorldPosition, anomalyCenter);
    
    // Solo distorsionar dentro del radio
    if (dist < anomalyRadius) {
      float factor = 1.0 - (dist / anomalyRadius);
      
      // Ondulación sinusoidal múltiple
      float wave1 = sin(dist * 3.0 - time * 2.0);
      float wave2 = cos(dist * 5.0 + time * 1.5);
      float wave3 = sin(dist * 7.0 - time * 3.0);
      
      float distortion = (wave1 + wave2 * 0.5 + wave3 * 0.3) * distortionStrength * factor * resonance;
      
      // Aplicar distorsión en dirección de la normal
      vec3 distortedPos = vWorldPosition + vNormal * distortion;
      
      vDistortion = distortion;
      
      gl_Position = projectionMatrix * viewMatrix * vec4(distortedPos, 1.0);
    } else {
      vDistortion = 0.0;
      gl_Position = projectionMatrix * viewMatrix * worldPosition;
    }
  }
`

export const spatialDistortionFragment = `
  uniform vec3 baseColor;
  uniform float resonance;
  uniform float time;
  
  varying vec3 vWorldPosition;
  varying vec3 vNormal;
  varying float vDistortion;
  
  void main() {
    // Color base
    vec3 color = baseColor;
    
    // Añadir brillo según distorsión
    float glow = abs(vDistortion) * 2.0;
    color += vec3(0.3, 0.5, 0.8) * glow * resonance;
    
    // Efecto de fresnel sutil
    vec3 viewDirection = normalize(cameraPosition - vWorldPosition);
    float fresnel = pow(1.0 - abs(dot(viewDirection, vNormal)), 2.0);
    color += vec3(0.2, 0.4, 0.6) * fresnel * resonance * 0.5;
    
    // Pulsación temporal
    float pulse = sin(time * 2.0) * 0.5 + 0.5;
    color += vec3(0.1, 0.2, 0.3) * pulse * resonance * 0.3;
    
    gl_FragColor = vec4(color, 1.0);
  }
`
