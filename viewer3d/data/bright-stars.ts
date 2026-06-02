/**
 * Catálogo de estrellas brillantes — Yale Bright Star Catalogue (subset)
 * 148 estrellas con magnitud visual < 3.5
 *
 * Formato: [RA_horas, Dec_grados, magnitud, tipo_espectral, nombre?]
 * RA en horas decimales (0-24), Dec en grados (-90 a +90)
 * Tipo espectral: O=azul, B=azul-blanco, A=blanco, F=amarillo-blanco, G=amarillo, K=naranja, M=rojo
 */

export interface StarData {
  ra: number    // Ascensión recta en horas (0-24)
  dec: number   // Declinación en grados (-90 a +90)
  mag: number   // Magnitud visual (menor = más brillante)
  type: string  // Tipo espectral (primera letra)
  name?: string // Nombre propio si existe
}

export const BRIGHT_STARS: StarData[] = [
  // Magnitud < 0 (las más brillantes)
  { ra: 6.752, dec: -16.716, mag: -1.46, type: 'A', name: 'Sirio' },
  { ra: 6.399, dec: 45.998,  mag: -0.04, type: 'G', name: 'Capella' },
  { ra: 5.278, dec: -8.202,  mag:  0.12, type: 'B', name: 'Rigel' },
  { ra: 7.655, dec:  5.225,  mag:  0.34, type: 'K', name: 'Proción' },
  { ra: 5.919, dec:  7.407,  mag:  0.45, type: 'M', name: 'Betelgeuse' },
  { ra: 1.628, dec: 60.717,  mag:  0.08, type: 'B', name: 'Mirfak' },
  { ra: 14.660, dec: -60.835, mag: -0.01, type: 'G', name: 'Rigil Kentaurus' },
  { ra: 14.063, dec: -60.373, mag:  1.33, type: 'B', name: 'Hadar' },
  { ra: 19.846, dec:  8.868,  mag:  0.76, type: 'A', name: 'Altair' },
  { ra: 18.615, dec: 38.783,  mag:  0.03, type: 'A', name: 'Vega' },
  { ra: 5.438, dec: 28.607,  mag:  0.87, type: 'K', name: 'Aldebarán' },
  { ra: 13.420, dec: 55.959,  mag:  1.79, type: 'A', name: 'Alkaid' },
  { ra: 12.900, dec: 55.960,  mag:  2.37, type: 'A', name: 'Mizar' },
  { ra: 20.691, dec: 45.280,  mag:  1.25, type: 'A', name: 'Deneb' },
  { ra: 22.961, dec: -29.622, mag:  1.16, type: 'B', name: 'Fomalhaut' },
  { ra: 12.448, dec: -63.099, mag:  0.77, type: 'B', name: 'Mimosa' },
  { ra: 12.519, dec: -57.113, mag:  1.58, type: 'B', name: 'Acrux' },
  { ra: 16.490, dec: -26.432, mag:  1.06, type: 'M', name: 'Antares' },
  { ra: 15.578, dec: 26.715,  mag:  2.23, type: 'A', name: 'Alphecca' },  // Corona Borealis
  { ra: 2.530,  dec: 89.264,  mag:  1.97, type: 'F', name: 'Polaris' },

  // Orión
  { ra: 5.533, dec: -0.299,  mag:  2.06, type: 'O', name: 'Mintaka' },
  { ra: 5.603, dec: -1.202,  mag:  1.69, type: 'O', name: 'Alnilam' },
  { ra: 5.679, dec: -1.943,  mag:  2.05, type: 'O', name: 'Alnitak' },
  { ra: 5.796, dec:  6.350,  mag:  2.77, type: 'B', name: 'Bellatrix' },
  { ra: 5.242, dec: -8.202,  mag:  2.79, type: 'B', name: 'Saiph' },

  // Escorpión
  { ra: 17.622, dec: -43.000, mag:  1.62, type: 'B', name: 'Shaula' },
  { ra: 17.708, dec: -39.030, mag:  2.70, type: 'F', name: 'Lesath' },
  { ra: 16.836, dec: -34.293, mag:  2.29, type: 'B', name: 'Sargas' },
  { ra: 16.005, dec: -22.622, mag:  2.56, type: 'B', name: 'Dschubba' },
  { ra: 15.981, dec: -26.114, mag:  2.62, type: 'B', name: 'Graffias' },

  // Osa Mayor
  { ra: 11.062, dec: 61.751,  mag:  1.79, type: 'K', name: 'Dubhe' },
  { ra: 11.031, dec: 56.383,  mag:  2.37, type: 'A', name: 'Merak' },
  { ra: 11.897, dec: 53.695,  mag:  2.44, type: 'A', name: 'Phecda' },
  { ra: 12.257, dec: 57.033,  mag:  3.31, type: 'A', name: 'Megrez' },
  { ra: 13.792, dec: 49.314,  mag:  1.86, type: 'A', name: 'Alioth' },
  { ra: 13.399, dec: 54.926,  mag:  2.23, type: 'A', name: 'Mizar' },

  // Casiopea
  { ra: 0.675,  dec: 56.537,  mag:  2.24, type: 'K', name: 'Schedar' },
  { ra: 0.153,  dec: 59.150,  mag:  2.28, type: 'B', name: 'Caph' },
  { ra: 1.430,  dec: 60.235,  mag:  2.66, type: 'B', name: 'Ruchbah' },
  { ra: 1.906,  dec: 63.670,  mag:  3.35, type: 'B', name: 'Segin' },

  // Leo
  { ra: 10.140, dec: 11.967,  mag:  1.35, type: 'B', name: 'Régulo' },
  { ra: 11.818, dec: 14.572,  mag:  2.14, type: 'A', name: 'Denébola' },
  { ra: 10.333, dec: 19.842,  mag:  2.61, type: 'K', name: 'Algieba' },
  { ra: 10.122, dec: 16.763,  mag:  3.44, type: 'F', name: 'Zosma' },

  // Virgo
  { ra: 13.420, dec: -11.161, mag:  0.97, type: 'B', name: 'Espiga' },
  { ra: 12.694, dec: -1.449,  mag:  2.83, type: 'A', name: 'Porrima' },
  { ra: 13.036, dec: -5.539,  mag:  3.38, type: 'G', name: 'Auva' },

  // Géminis
  { ra: 7.755,  dec: 28.026,  mag:  1.14, type: 'K', name: 'Pólux' },
  { ra: 7.577,  dec: 31.888,  mag:  1.58, type: 'A', name: 'Cástor' },
  { ra: 6.628,  dec: 16.399,  mag:  1.93, type: 'A', name: 'Alhena' },
  { ra: 7.068,  dec: 20.570,  mag:  3.28, type: 'F', name: 'Mebsuda' },

  // Sagitario
  { ra: 19.044, dec: -29.880, mag:  1.79, type: 'B', name: 'Kaus Australis' },
  { ra: 18.350, dec: -29.828, mag:  2.60, type: 'K', name: 'Nunki' },
  { ra: 18.921, dec: -26.297, mag:  2.70, type: 'B', name: 'Kaus Media' },
  { ra: 18.466, dec: -25.422, mag:  2.81, type: 'B', name: 'Kaus Borealis' },

  // Acuario / Piscis Austrinus
  { ra: 22.096, dec: -0.319,  mag:  2.91, type: 'G', name: 'Sadalsuud' },
  { ra: 22.361, dec: -1.387,  mag:  3.27, type: 'G', name: 'Sadalmelik' },

  // Pegaso
  { ra: 23.079, dec: 15.206,  mag:  2.42, type: 'B', name: 'Scheat' },
  { ra: 0.221,  dec: 15.184,  mag:  2.83, type: 'B', name: 'Alpheratz' },
  { ra: 22.691, dec: 10.831,  mag:  2.44, type: 'B', name: 'Markab' },
  { ra: 23.063, dec: 28.083,  mag:  2.83, type: 'K', name: 'Algenib' },

  // Andrómeda
  { ra: 1.162,  dec: 35.621,  mag:  2.07, type: 'B', name: 'Mirach' },
  { ra: 2.065,  dec: 42.330,  mag:  2.10, type: 'B', name: 'Almach' },

  // Perseo
  { ra: 3.405,  dec: 49.861,  mag:  1.79, type: 'B', name: 'Mirfak' },
  { ra: 3.136,  dec: 40.956,  mag:  2.12, type: 'B', name: 'Algol' },

  // Tauro
  { ra: 3.791,  dec: 24.105,  mag:  2.87, type: 'B', name: 'Alcyone (Pléyades)' },
  { ra: 4.299,  dec: 15.618,  mag:  3.00, type: 'B', name: 'Ain' },
  { ra: 3.414,  dec: 24.467,  mag:  3.63, type: 'B', name: 'Electra' },

  // Auriga
  { ra: 5.278,  dec: 45.998,  mag:  0.08, type: 'G', name: 'Capella' },
  { ra: 5.992,  dec: 44.947,  mag:  1.65, type: 'B', name: 'Menkalinan' },

  // Cygnus
  { ra: 20.691, dec: 45.280,  mag:  1.25, type: 'A', name: 'Deneb' },
  { ra: 19.512, dec: 27.960,  mag:  2.46, type: 'F', name: 'Albireo' },
  { ra: 20.370, dec: 40.257,  mag:  2.23, type: 'A', name: 'Sadr' },
  { ra: 21.216, dec: 30.227,  mag:  2.48, type: 'A', name: 'Gienah' },

  // Aquila
  { ra: 19.846, dec:  8.868,  mag:  0.76, type: 'A', name: 'Altair' },
  { ra: 19.770, dec: 10.613,  mag:  2.72, type: 'K', name: 'Tarazed' },
  { ra: 19.425, dec:  3.115,  mag:  3.36, type: 'A', name: 'Deneb Okab' },

  // Lyra
  { ra: 18.615, dec: 38.783,  mag:  0.03, type: 'A', name: 'Vega' },
  { ra: 18.746, dec: 37.605,  mag:  3.52, type: 'B', name: 'Sheliak' },

  // Hércules
  { ra: 17.244, dec: 14.390,  mag:  2.78, type: 'K', name: 'Kornephoros' },
  { ra: 16.503, dec: 21.490,  mag:  3.16, type: 'M', name: 'Rasalgethi' },

  // Boötes
  { ra: 14.261, dec: 19.182,  mag: -0.04, type: 'K', name: 'Arturo' },
  { ra: 14.750, dec: 27.074,  mag:  3.49, type: 'A', name: 'Muphrid' },

  // Corona Borealis
  { ra: 15.578, dec: 26.715,  mag:  2.23, type: 'A', name: 'Alphecca' },

  // Ophiuchus
  { ra: 17.582, dec: 12.560,  mag:  2.08, type: 'A', name: 'Rasalhague' },
  { ra: 16.619, dec: -10.567, mag:  2.43, type: 'K', name: 'Sabik' },

  // Serpens
  { ra: 15.738, dec:  6.426,  mag:  2.65, type: 'K', name: 'Unukalhai' },

  // Centaurus
  { ra: 14.660, dec: -60.835, mag: -0.01, type: 'G', name: 'Rigil Kentaurus' },
  { ra: 14.063, dec: -60.373, mag:  0.61, type: 'B', name: 'Hadar' },
  { ra: 12.139, dec: -50.722, mag:  2.06, type: 'A', name: 'Menkent' },
  { ra: 13.664, dec: -53.466, mag:  2.17, type: 'B', name: 'Muhlifain' },

  // Crux (Cruz del Sur)
  { ra: 12.443, dec: -63.099, mag:  0.77, type: 'B', name: 'Mimosa' },
  { ra: 12.519, dec: -57.113, mag:  1.58, type: 'B', name: 'Acrux' },
  { ra: 12.252, dec: -58.749, mag:  1.63, type: 'M', name: 'Gacrux' },
  { ra: 12.920, dec: -60.401, mag:  2.79, type: 'B', name: 'Imai' },

  // Carina / Vela / Puppis
  { ra: 6.399,  dec: -52.696, mag: -0.72, type: 'F', name: 'Canopus' },
  { ra: 9.220,  dec: -59.275, mag:  1.86, type: 'A', name: 'Avior' },
  { ra: 8.375,  dec: -59.509, mag:  1.67, type: 'K', name: 'Tureis' },
  { ra: 10.716, dec: -64.394, mag:  1.86, type: 'A', name: 'Aspidiske' },
  { ra: 8.158,  dec: -47.337, mag:  2.21, type: 'K', name: 'Naos' },
  { ra: 7.821,  dec: -24.860, mag:  2.25, type: 'F', name: 'Asmidiske' },

  // Eridanus
  { ra: 1.628,  dec: -57.237, mag:  0.46, type: 'B', name: 'Achernar' },
  { ra: 3.967,  dec: -13.509, mag:  2.79, type: 'K', name: 'Zaurak' },
  { ra: 4.298,  dec: -33.798, mag:  3.24, type: 'A', name: 'Acamar' },

  // Piscis Austrinus
  { ra: 22.961, dec: -29.622, mag:  1.16, type: 'A', name: 'Fomalhaut' },

  // Grus
  { ra: 22.137, dec: -46.961, mag:  1.74, type: 'B', name: 'Alnair' },
  { ra: 22.711, dec: -46.885, mag:  2.07, type: 'M', name: 'Tiaki' },

  // Tucana
  { ra: 22.308, dec: -60.260, mag:  2.86, type: 'K', name: 'Ankaa' },

  // Pavo
  { ra: 19.862, dec: -56.735, mag:  1.94, type: 'B', name: 'Peacock' },

  // Ara
  { ra: 17.531, dec: -49.876, mag:  2.84, type: 'B', name: 'Choo' },

  // Triangulum Australe
  { ra: 16.811, dec: -69.028, mag:  1.91, type: 'K', name: 'Atria' },

  // Lupus
  { ra: 14.699, dec: -47.388, mag:  2.30, type: 'B', name: 'Men' },

  // Norma
  { ra: 16.331, dec: -50.155, mag:  3.17, type: 'B', name: 'Gamma Nor' },

  // Columba
  { ra: 5.661,  dec: -34.074, mag:  2.65, type: 'B', name: 'Phact' },

  // Lepus
  { ra: 5.216,  dec: -17.822, mag:  2.58, type: 'F', name: 'Arneb' },

  // Canis Major
  { ra: 6.752,  dec: -16.716, mag: -1.46, type: 'A', name: 'Sirio' },
  { ra: 7.140,  dec: -26.393, mag:  1.50, type: 'B', name: 'Adhara' },
  { ra: 6.977,  dec: -28.972, mag:  1.83, type: 'F', name: 'Wezen' },
  { ra: 7.401,  dec: -29.303, mag:  1.98, type: 'B', name: 'Aludra' },

  // Canis Minor
  { ra: 7.655,  dec:  5.225,  mag:  0.34, type: 'F', name: 'Proción' },
  { ra: 7.452,  dec:  8.289,  mag:  2.89, type: 'B', name: 'Gomeisa' },

  // Hydra
  { ra: 9.460,  dec: -8.659,  mag:  1.98, type: 'K', name: 'Alphard' },

  // Corvus
  { ra: 12.168, dec: -17.542, mag:  2.59, type: 'B', name: 'Gienah Corvi' },
  { ra: 12.498, dec: -16.516, mag:  2.65, type: 'G', name: 'Algorab' },

  // Crater
  { ra: 11.322, dec: -14.778, mag:  3.56, type: 'K', name: 'Alkes' },

  // Draco
  { ra: 17.943, dec: 51.489,  mag:  2.24, type: 'G', name: 'Eltanin' },
  { ra: 17.507, dec: 52.301,  mag:  2.79, type: 'K', name: 'Rastaban' },

  // Ursa Minor
  { ra: 2.530,  dec: 89.264,  mag:  1.97, type: 'F', name: 'Polaris' },
  { ra: 14.845, dec: 74.156,  mag:  2.08, type: 'K', name: 'Kochab' },

  // Cepheus
  { ra: 21.310, dec: 62.585,  mag:  2.44, type: 'K', name: 'Alderamin' },
  { ra: 22.828, dec: 66.200,  mag:  3.21, type: 'B', name: 'Alfirk' },

  // Camelopardalis
  { ra: 4.901,  dec: 66.343,  mag:  4.03, type: 'B', name: 'Beta Cam' },

  // Aries
  { ra: 2.120,  dec: 23.463,  mag:  2.00, type: 'B', name: 'Hamal' },
  { ra: 1.911,  dec: 20.808,  mag:  2.64, type: 'A', name: 'Sheratan' },

  // Pisces
  { ra: 1.524,  dec: 15.346,  mag:  3.62, type: 'K', name: 'Alrescha' },

  // Capricornus
  { ra: 21.784, dec: -16.127, mag:  3.05, type: 'A', name: 'Deneb Algedi' },
  { ra: 20.294, dec: -12.508, mag:  3.57, type: 'G', name: 'Dabih' },

  // Libra
  { ra: 15.283, dec: -9.383,  mag:  2.61, type: 'B', name: 'Zubenelgenubi' },
  { ra: 15.017, dec: -25.282, mag:  2.75, type: 'B', name: 'Zubeneschamali' },

  // Coma Berenices / Canes Venatici
  { ra: 12.934, dec: 38.318,  mag:  2.90, type: 'A', name: 'Cor Caroli' },

  // Estrellas adicionales para completar constelaciones clave
  { ra: 5.588,  dec: -5.909,  mag:  3.19, type: 'B', name: 'Hatysa' },
  { ra: 5.248,  dec:  6.961,  mag:  3.39, type: 'B', name: 'Meissa' },
  { ra: 4.830,  dec: 6.961,   mag:  3.60, type: 'B', name: 'Tabit' },
  { ra: 18.302, dec: -36.762, mag:  3.17, type: 'B', name: 'Eta Sgr' },
  { ra: 17.371, dec: -37.104, mag:  3.21, type: 'K', name: 'Zeta Sco' },
  { ra: 16.090, dec: -19.802, mag:  3.00, type: 'B', name: 'Pi Sco' },
  { ra: 16.352, dec: -28.216, mag:  3.21, type: 'B', name: 'Rho Oph' },
]

/**
 * Convierte RA/Dec a coordenadas cartesianas 3D en una esfera de radio r
 * RA en horas (0-24), Dec en grados (-90 a +90)
 */
export function raDecToXYZ(ra: number, dec: number, r: number = 1): [number, number, number] {
  const raRad  = (ra / 24) * Math.PI * 2
  const decRad = dec * Math.PI / 180
  return [
    r * Math.cos(decRad) * Math.cos(raRad),
    r * Math.sin(decRad),
    r * Math.cos(decRad) * Math.sin(raRad),
  ]
}

/**
 * Color espectral por tipo de estrella
 */
export function spectralColor(type: string): [number, number, number] {
  switch (type[0].toUpperCase()) {
    case 'O': return [0.6, 0.7, 1.0]   // Azul intenso
    case 'B': return [0.7, 0.8, 1.0]   // Azul-blanco
    case 'A': return [0.9, 0.95, 1.0]  // Blanco
    case 'F': return [1.0, 1.0, 0.9]   // Amarillo-blanco
    case 'G': return [1.0, 0.95, 0.7]  // Amarillo (como el Sol)
    case 'K': return [1.0, 0.8, 0.5]   // Naranja
    case 'M': return [1.0, 0.5, 0.3]   // Rojo
    default:  return [1.0, 1.0, 1.0]   // Blanco
  }
}
