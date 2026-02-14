/**
 * CAPA 1 — LEY REAL (OCULTA)
 * Cálculos astronómicos precisos basados en fecha y ubicación
 * No se muestran directamente, pero todo obedece estas leyes
 */

export interface SolarPosition {
  azimuth: number;      // Ángulo horizontal desde el norte (0-360°)
  elevation: number;    // Ángulo vertical sobre el horizonte (-90 a 90°)
  declination: number;  // Declinación solar (-23.44° a 23.44°)
  hourAngle: number;    // Ángulo horario
  distance: number;     // Distancia Tierra-Sol en UA
}

export interface LunarPosition {
  azimuth: number;
  elevation: number;
  phase: number;        // 0-1 (0=nueva, 0.5=llena)
  distance: number;     // Distancia Tierra-Luna en km
  age: number;          // Edad lunar en días (0-29.53)
}

/**
 * Calcula la posición del Sol para una fecha, latitud y longitud dadas
 * Basado en algoritmos astronómicos estándar
 */
export function calculateSolarPosition(
  date: Date,
  latitude: number,
  longitude: number
): SolarPosition {
  // Convertir a tiempo juliano
  const jd = dateToJulianDay(date);
  const jc = (jd - 2451545.0) / 36525.0; // Siglos julianos desde J2000
  
  // Calcular longitud media del Sol
  const L0 = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360;
  
  // Anomalía media
  const M = (357.52911 + jc * (35999.05029 - 0.0001537 * jc)) % 360;
  const Mrad = M * Math.PI / 180;
  
  // Ecuación del centro
  const C = (1.914602 - jc * (0.004817 + 0.000014 * jc)) * Math.sin(Mrad) +
            (0.019993 - 0.000101 * jc) * Math.sin(2 * Mrad) +
            0.000289 * Math.sin(3 * Mrad);
  
  // Longitud verdadera
  const L = (L0 + C) % 360;
  const Lrad = L * Math.PI / 180;
  
  // Oblicuidad de la eclíptica (inclinación axial)
  const epsilon = 23.439291 - 0.0130042 * jc;
  const epsilonRad = epsilon * Math.PI / 180;
  
  // Declinación solar
  const declination = Math.asin(Math.sin(epsilonRad) * Math.sin(Lrad)) * 180 / Math.PI;
  
  // Ecuación del tiempo
  const y = Math.tan(epsilonRad / 2) ** 2;
  const eot = 4 * (y * Math.sin(2 * L0 * Math.PI / 180) -
                   2 * (M * Math.PI / 180) +
                   4 * (M * Math.PI / 180) * y * Math.sin(2 * L0 * Math.PI / 180) -
                   0.5 * y * y * Math.sin(4 * L0 * Math.PI / 180) -
                   1.25 * Mrad * Mrad * Math.sin(2 * Mrad)) * 180 / Math.PI;
  
  // Tiempo solar verdadero
  const timeOffset = eot + 4 * longitude;
  const tst = date.getUTCHours() * 60 + date.getUTCMinutes() + date.getUTCSeconds() / 60 + timeOffset;
  
  // Ángulo horario
  const hourAngle = (tst / 4 - 180);
  const haRad = hourAngle * Math.PI / 180;
  const latRad = latitude * Math.PI / 180;
  const decRad = declination * Math.PI / 180;
  
  // Elevación solar
  const elevation = Math.asin(
    Math.sin(latRad) * Math.sin(decRad) +
    Math.cos(latRad) * Math.cos(decRad) * Math.cos(haRad)
  ) * 180 / Math.PI;
  
  // Azimut solar
  const azimuth = (Math.atan2(
    Math.sin(haRad),
    Math.cos(haRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
  ) * 180 / Math.PI + 180) % 360;
  
  // Distancia Tierra-Sol (órbita elíptica)
  const distance = 1.000001018 * (1 - 0.01671123 * Math.cos(Mrad) - 0.00014 * Math.cos(2 * Mrad));
  
  return {
    azimuth,
    elevation,
    declination,
    hourAngle,
    distance
  };
}

/**
 * Calcula la posición de la Luna
 */
export function calculateLunarPosition(
  date: Date,
  latitude: number,
  longitude: number
): LunarPosition {
  const jd = dateToJulianDay(date);
  const jc = (jd - 2451545.0) / 36525.0;
  
  // Longitud media de la Luna
  const Lm = (218.316 + 13.176396 * (jd - 2451545.0)) % 360;
  
  // Anomalía media de la Luna
  const Mm = (134.963 + 13.064993 * (jd - 2451545.0)) % 360;
  const MmRad = Mm * Math.PI / 180;
  
  // Argumento de latitud
  const F = (93.272 + 13.229350 * (jd - 2451545.0)) % 360;
  
  // Longitud del nodo ascendente
  const omega = (125.045 - 0.052954 * (jd - 2451545.0)) % 360;
  
  // Longitud eclíptica (simplificada)
  const lambda = Lm + 6.289 * Math.sin(MmRad);
  const lambdaRad = lambda * Math.PI / 180;
  
  // Latitud eclíptica
  const beta = 5.128 * Math.sin(F * Math.PI / 180);
  const betaRad = beta * Math.PI / 180;
  
  // Oblicuidad
  const epsilon = 23.439291 - 0.0130042 * jc;
  const epsilonRad = epsilon * Math.PI / 180;
  
  // Conversión a coordenadas ecuatoriales
  const ra = Math.atan2(
    Math.sin(lambdaRad) * Math.cos(epsilonRad) - Math.tan(betaRad) * Math.sin(epsilonRad),
    Math.cos(lambdaRad)
  );
  
  const dec = Math.asin(
    Math.sin(betaRad) * Math.cos(epsilonRad) +
    Math.cos(betaRad) * Math.sin(epsilonRad) * Math.sin(lambdaRad)
  );
  
  // Tiempo sidéreo local
  const gmst = (280.46061837 + 360.98564736629 * (jd - 2451545.0)) % 360;
  const lst = (gmst + longitude) % 360;
  const lstRad = lst * Math.PI / 180;
  
  // Ángulo horario
  const ha = lstRad - ra;
  const latRad = latitude * Math.PI / 180;
  
  // Elevación
  const elevation = Math.asin(
    Math.sin(latRad) * Math.sin(dec) +
    Math.cos(latRad) * Math.cos(dec) * Math.cos(ha)
  ) * 180 / Math.PI;
  
  // Azimut
  const azimuth = (Math.atan2(
    Math.sin(ha),
    Math.cos(ha) * Math.sin(latRad) - Math.tan(dec) * Math.cos(latRad)
  ) * 180 / Math.PI + 180) % 360;
  
  // Fase lunar (simplificada)
  const solarLongitude = (280.46646 + 36000.76983 * jc) % 360;
  const elongation = lambda - solarLongitude;
  const phase = (1 - Math.cos(elongation * Math.PI / 180)) / 2;
  
  // Edad lunar
  const age = ((jd - 2451550.1) % 29.530588853) + 29.530588853;
  
  // Distancia (simplificada)
  const distance = 385000 - 20905 * Math.cos(MmRad);
  
  return {
    azimuth,
    elevation,
    phase,
    distance,
    age: age % 29.530588853
  };
}

/**
 * Convierte fecha a día juliano
 */
function dateToJulianDay(date: Date): number {
  const year = date.getUTCFullYear();
  const month = date.getUTCMonth() + 1;
  const day = date.getUTCDate();
  const hour = date.getUTCHours();
  const minute = date.getUTCMinutes();
  const second = date.getUTCSeconds();
  
  let a = Math.floor((14 - month) / 12);
  let y = year + 4800 - a;
  let m = month + 12 * a - 3;
  
  let jdn = day + Math.floor((153 * m + 2) / 5) + 365 * y + 
            Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
  
  let jd = jdn + (hour - 12) / 24 + minute / 1440 + second / 86400;
  
  return jd;
}

/**
 * Calcula el arco solar para un día completo
 * Útil para visualizar el recorrido del Sol
 */
export function calculateSolarArc(
  date: Date,
  latitude: number,
  longitude: number,
  samples: number = 48
): SolarPosition[] {
  const arc: SolarPosition[] = [];
  const baseDate = new Date(date);
  baseDate.setUTCHours(0, 0, 0, 0);
  
  for (let i = 0; i < samples; i++) {
    const time = new Date(baseDate.getTime() + (i * 24 * 60 * 60 * 1000) / samples);
    arc.push(calculateSolarPosition(time, latitude, longitude));
  }
  
  return arc;
}

/**
 * Calcula el arco solar anual (solsticios y equinoccios)
 */
export function calculateAnnualSolarArcs(
  year: number,
  latitude: number,
  longitude: number
): {
  summerSolstice: SolarPosition[];
  winterSolstice: SolarPosition[];
  equinox: SolarPosition[];
} {
  const summerDate = new Date(Date.UTC(year, 5, 21)); // ~21 junio
  const winterDate = new Date(Date.UTC(year, 11, 21)); // ~21 diciembre
  const equinoxDate = new Date(Date.UTC(year, 2, 20)); // ~20 marzo
  
  return {
    summerSolstice: calculateSolarArc(summerDate, latitude, longitude),
    winterSolstice: calculateSolarArc(winterDate, latitude, longitude),
    equinox: calculateSolarArc(equinoxDate, latitude, longitude)
  };
}
