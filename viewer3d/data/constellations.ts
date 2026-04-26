/**
 * Líneas de constelaciones — pares de índices al catálogo BRIGHT_STARS
 * Cada par [i, j] conecta la estrella i con la estrella j
 * Basado en las 88 constelaciones IAU, subset de las más reconocibles
 */

// Nombres de estrellas por nawal para lookup rápido
export const CONSTELLATION_LINES: Array<{
  name: string
  color: string
  // Pares de nombres de estrellas del catálogo Yale
  stars: [string, string][]
}> = [
  // ─── ORIÓN (la más reconocible) ──────────────────────────────────────────
  {
    name: 'Orión',
    color: '#88aaff',
    stars: [
      ['Betelgeuse', 'Bellatrix'],   // hombros
      ['Betelgeuse', 'Mintaka'],     // hombro izq → cinturón
      ['Bellatrix', 'Mintaka'],      // hombro der → cinturón
      ['Mintaka', 'Alnilam'],        // cinturón
      ['Alnilam', 'Alnitak'],        // cinturón
      ['Alnitak', 'Saiph'],          // cinturón → pie izq
      ['Alnitak', 'Rigel'],          // cinturón → pie der
      ['Saiph', 'Rigel'],            // pies
      ['Mintaka', 'Meissa'],         // cinturón → cabeza
    ]
  },

  // ─── OSA MAYOR ────────────────────────────────────────────────────────────
  {
    name: 'Osa Mayor',
    color: '#ffcc66',
    stars: [
      ['Dubhe', 'Merak'],
      ['Merak', 'Phecda'],
      ['Phecda', 'Megrez'],
      ['Megrez', 'Alioth'],
      ['Alioth', 'Mizar'],
      ['Mizar', 'Alkaid'],
      ['Megrez', 'Dubhe'],
    ]
  },

  // ─── CASIOPEA ─────────────────────────────────────────────────────────────
  {
    name: 'Casiopea',
    color: '#ff88aa',
    stars: [
      ['Caph', 'Schedar'],
      ['Schedar', 'Ruchbah'],
      ['Ruchbah', 'Segin'],
    ]
  },

  // ─── ESCORPIÓN ────────────────────────────────────────────────────────────
  {
    name: 'Escorpión',
    color: '#ff6644',
    stars: [
      ['Graffias', 'Dschubba'],
      ['Dschubba', 'Antares'],
      ['Antares', 'Sargas'],
      ['Sargas', 'Shaula'],
      ['Shaula', 'Lesath'],
    ]
  },

  // ─── CRUZ DEL SUR ─────────────────────────────────────────────────────────
  {
    name: 'Cruz del Sur',
    color: '#44ffcc',
    stars: [
      ['Acrux', 'Gacrux'],    // eje vertical
      ['Mimosa', 'Imai'],     // eje horizontal
    ]
  },

  // ─── LEO ──────────────────────────────────────────────────────────────────
  {
    name: 'Leo',
    color: '#ffaa44',
    stars: [
      ['Régulo', 'Algieba'],
      ['Algieba', 'Zosma'],
      ['Zosma', 'Denébola'],
      ['Régulo', 'Zosma'],
    ]
  },

  // ─── VIRGO ────────────────────────────────────────────────────────────────
  {
    name: 'Virgo',
    color: '#aaffaa',
    stars: [
      ['Espiga', 'Porrima'],
      ['Porrima', 'Auva'],
    ]
  },

  // ─── GÉMINIS ──────────────────────────────────────────────────────────────
  {
    name: 'Géminis',
    color: '#ffff88',
    stars: [
      ['Cástor', 'Pólux'],
      ['Cástor', 'Alhena'],
      ['Pólux', 'Alhena'],
    ]
  },

  // ─── SAGITARIO ────────────────────────────────────────────────────────────
  {
    name: 'Sagitario',
    color: '#ff88ff',
    stars: [
      ['Kaus Australis', 'Kaus Media'],
      ['Kaus Media', 'Kaus Borealis'],
      ['Kaus Australis', 'Nunki'],
    ]
  },

  // ─── ÁGUILA ───────────────────────────────────────────────────────────────
  {
    name: 'Águila',
    color: '#88ccff',
    stars: [
      ['Altair', 'Tarazed'],
      ['Altair', 'Deneb Okab'],
    ]
  },

  // ─── CYGNUS (Cruz del Norte) ──────────────────────────────────────────────
  {
    name: 'Cygnus',
    color: '#ccaaff',
    stars: [
      ['Deneb', 'Sadr'],
      ['Sadr', 'Albireo'],   // eje vertical
      ['Sadr', 'Gienah'],    // eje horizontal
    ]
  },

  // ─── CENTAURO ─────────────────────────────────────────────────────────────
  {
    name: 'Centauro',
    color: '#44ffff',
    stars: [
      ['Rigil Kentaurus', 'Hadar'],
      ['Hadar', 'Menkent'],
    ]
  },

  // ─── BOÖTES ───────────────────────────────────────────────────────────────
  {
    name: 'Boötes',
    color: '#ffaa88',
    stars: [
      ['Arturo', 'Muphrid'],
    ]
  },

  // ─── CORONA BOREALIS ──────────────────────────────────────────────────────
  {
    name: 'Corona Borealis',
    color: '#ffffff',
    stars: [
      ['Alphecca', 'Cor Caroli'],
    ]
  },

  // ─── PISCIS AUSTRINUS ─────────────────────────────────────────────────────
  {
    name: 'Piscis Austrinus',
    color: '#88aaff',
    stars: [
      ['Fomalhaut', 'Sadalsuud'],
    ]
  },

  // ─── PEGASO ───────────────────────────────────────────────────────────────
  {
    name: 'Pegaso',
    color: '#aaccff',
    stars: [
      ['Scheat', 'Markab'],
      ['Markab', 'Algenib'],
      ['Algenib', 'Alpheratz'],
      ['Alpheratz', 'Scheat'],
    ]
  },

  // ─── ANDRÓMEDA ────────────────────────────────────────────────────────────
  {
    name: 'Andrómeda',
    color: '#ffddaa',
    stars: [
      ['Alpheratz', 'Mirach'],
      ['Mirach', 'Almach'],
    ]
  },

  // ─── PERSEO ───────────────────────────────────────────────────────────────
  {
    name: 'Perseo',
    color: '#ffbbcc',
    stars: [
      ['Mirfak', 'Algol'],
    ]
  },

  // ─── TAURO ────────────────────────────────────────────────────────────────
  {
    name: 'Tauro',
    color: '#ffeeaa',
    stars: [
      ['Aldebarán', 'Ain'],
      ['Aldebarán', 'Alcyone (Pléyades)'],
    ]
  },

  // ─── AURIGA ───────────────────────────────────────────────────────────────
  {
    name: 'Auriga',
    color: '#ffffaa',
    stars: [
      ['Capella', 'Menkalinan'],
    ]
  },

  // ─── LYRA ─────────────────────────────────────────────────────────────────
  {
    name: 'Lyra',
    color: '#aaffee',
    stars: [
      ['Vega', 'Sheliak'],
    ]
  },

  // ─── HÉRCULES ─────────────────────────────────────────────────────────────
  {
    name: 'Hércules',
    color: '#ffaa66',
    stars: [
      ['Kornephoros', 'Rasalgethi'],
    ]
  },

  // ─── OPHIUCHUS ────────────────────────────────────────────────────────────
  {
    name: 'Ophiuchus',
    color: '#aaffaa',
    stars: [
      ['Rasalhague', 'Sabik'],
      ['Sabik', 'Unukalhai'],
    ]
  },

  // ─── ERIDANUS ─────────────────────────────────────────────────────────────
  {
    name: 'Eridanus',
    color: '#88ccff',
    stars: [
      ['Achernar', 'Zaurak'],
      ['Zaurak', 'Acamar'],
    ]
  },

  // ─── GRUS ─────────────────────────────────────────────────────────────────
  {
    name: 'Grus',
    color: '#ffccaa',
    stars: [
      ['Alnair', 'Tiaki'],
    ]
  },

  // ─── CARINA ───────────────────────────────────────────────────────────────
  {
    name: 'Carina',
    color: '#aaeeff',
    stars: [
      ['Canopus', 'Avior'],
      ['Avior', 'Aspidiske'],
    ]
  },
]
