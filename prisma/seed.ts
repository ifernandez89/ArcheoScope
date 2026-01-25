/**
 * ArcheoScope Database Seed Script
 * Pobla la base de datos con sitios arqueológicos de referencia
 */

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Iniciando seed de base de datos ArcheoScope...\n');

  // ============================================================================
  // SITIOS DE REFERENCIA ARQUEOLÓGICOS
  // ============================================================================

  console.log('📍 Creando sitios de referencia arqueológicos...');

  // 1. GIZA PYRAMIDS (Egypt) - DESERT
  const giza = await prisma.archaeologicalSite.upsert({
    where: { slug: 'giza-pyramids' },
    update: {},
    create: {
      name: 'Giza Pyramids Complex',
      alternateNames: ['Great Pyramid of Khufu', 'Pyramid of Cheops', 'Giza Necropolis'],
      slug: 'giza-pyramids',
      environmentType: 'DESERT',
      siteType: 'MONUMENTAL_COMPLEX',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'EXTENSIVELY_EXCAVATED',
      preservationStatus: 'GOOD',
      latitude: 29.9792,
      longitude: 31.1342,
      elevation: 60,
      areaKm2: 2.5,
      country: 'Egypt',
      region: 'Giza Governorate',
      period: 'Old Kingdom Egypt',
      dateRangeStart: -2580,
      dateRangeEnd: -2560,
      dateUnit: 'BCE',
      unescoId: 86,
      unescoStatus: 'World Heritage Site',
      unescoYear: 1979,
      description: 'The Giza pyramid complex is an archaeological site on the Giza Plateau, on the outskirts of Cairo, Egypt.',
      scientificSignificance: 'One of the Seven Wonders of the Ancient World. Demonstrates advanced engineering and astronomical knowledge of Old Kingdom Egypt.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Great Pyramid of Khufu', featureType: 'pyramid' },
          { name: 'Pyramid of Khafre', featureType: 'pyramid' },
          { name: 'Pyramid of Menkaure', featureType: 'pyramid' },
          { name: 'Great Sphinx', featureType: 'monument' },
          { name: 'Valley temples', featureType: 'temple' },
          { name: 'Mastaba tombs', featureType: 'burial' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'UNESCO World Heritage Centre',
            sourceUrl: 'https://whc.unesco.org/en/list/86',
          },
          {
            sourceType: 'lidar_source',
            sourceName: 'Giza Plateau Mapping Project (Harvard University)',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'LIDAR', available: true, quality: 'high' },
          { dataType: 'SATELLITE_MULTISPECTRAL', available: true, quality: 'high' },
          { dataType: 'SATELLITE_THERMAL', available: true, quality: 'high' },
          { dataType: 'SAR', available: true, quality: 'high' },
          { dataType: 'PHOTOGRAMMETRY', available: true, quality: 'high' },
          { dataType: 'GROUND_PENETRATING_RADAR', available: true, quality: 'medium' },
        ],
      },
      threats: {
        create: [
          { threatType: 'urban_encroachment', severity: 'high' },
          { threatType: 'air_pollution', severity: 'medium' },
          { threatType: 'tourism_pressure', severity: 'high' },
          { threatType: 'groundwater', severity: 'medium' },
        ],
      },
      calibrationData: {
        create: {
          thermalDeltaK: 12.0,
          sarBackscatterDb: -8.0,
          ndviDelta: 0.15,
          calibrationNotes: 'Reference site for DESERT environment detection',
          calibrationConfidence: 0.95,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Giza Pyramids Complex');

  // 2. ANGKOR WAT (Cambodia) - FOREST
  const angkor = await prisma.archaeologicalSite.upsert({
    where: { slug: 'angkor-wat' },
    update: {},
    create: {
      name: 'Angkor Wat Temple Complex',
      alternateNames: ['Angkor Archaeological Park', 'Angkor Thom'],
      slug: 'angkor-wat',
      environmentType: 'FOREST',
      siteType: 'TEMPLE_COMPLEX',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'ONGOING_RESEARCH',
      preservationStatus: 'FAIR',
      latitude: 13.4125,
      longitude: 103.8670,
      elevation: 65,
      areaKm2: 162.6,
      country: 'Cambodia',
      region: 'Siem Reap Province',
      period: 'Khmer Empire',
      dateRangeStart: 1113,
      dateRangeEnd: 1150,
      dateUnit: 'CE',
      unescoId: 668,
      unescoStatus: 'World Heritage Site',
      unescoYear: 1992,
      description: 'Angkor Wat is a temple complex in Cambodia and one of the largest religious monuments in the world.',
      scientificSignificance: 'Largest religious monument in the world. Revolutionary LiDAR discoveries revealed extensive urban infrastructure and water management systems.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Angkor Wat temple', featureType: 'temple' },
          { name: 'Angkor Thom city', featureType: 'urban' },
          { name: 'Bayon temple', featureType: 'temple' },
          { name: 'Ta Prohm temple', featureType: 'temple' },
          { name: 'Hydraulic network', featureType: 'infrastructure' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'APSARA Authority',
          },
          {
            sourceType: 'lidar_source',
            sourceName: 'Khmer Archaeology LiDAR Consortium (University of Sydney)',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'LIDAR', available: true, quality: 'high' },
          { dataType: 'SATELLITE_MULTISPECTRAL', available: true, quality: 'high' },
          { dataType: 'SAR', available: true, quality: 'high' },
        ],
      },
      threats: {
        create: [
          { threatType: 'vegetation_damage', severity: 'high' },
          { threatType: 'tourism_pressure', severity: 'high' },
          { threatType: 'climate_change', severity: 'medium' },
        ],
      },
      calibrationData: {
        create: {
          lidarHeightM: 15.0,
          ndviDelta: 0.35,
          sarCoherence: 0.85,
          calibrationNotes: 'Reference site for FOREST environment - LiDAR penetration through canopy',
          calibrationConfidence: 0.90,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Angkor Wat Temple Complex');

  // 3. ÖTZI THE ICEMAN (Alps) - GLACIER
  const otzi = await prisma.archaeologicalSite.upsert({
    where: { slug: 'otzi-iceman' },
    update: {},
    create: {
      name: 'Ötzi the Iceman Discovery Site',
      alternateNames: ['Similaun Man', 'Hauslabjoch', 'Tisenjoch Iceman'],
      slug: 'otzi-iceman',
      environmentType: 'GLACIER',
      siteType: 'GLACIER_MUMMY',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'FULLY_EXCAVATED',
      preservationStatus: 'EXCELLENT',
      latitude: 46.7789,
      longitude: 10.8494,
      elevation: 3210,
      areaKm2: 0.001,
      country: 'Italy/Austria',
      region: 'Ötztal Alps, South Tyrol',
      period: 'Copper Age (Chalcolithic)',
      dateRangeStart: -3350,
      dateRangeEnd: -3105,
      dateUnit: 'BCE',
      description: 'Discovery site of a well-preserved natural mummy of a man from the Copper Age.',
      scientificSignificance: "Europe's oldest known natural human mummy. Provides unprecedented insight into Copper Age life, technology, health, and diet.",
      isReferencesite: true,
      discoveryDate: new Date('1991-09-19'),
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Natural mummy', featureType: 'burial' },
          { name: 'Copper axe', featureType: 'artifact' },
          { name: 'Bow and arrows', featureType: 'artifact' },
          { name: 'Clothing and equipment', featureType: 'artifact' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'South Tyrol Museum of Archaeology',
            sourceUrl: 'https://www.iceman.it/en/',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'SATELLITE_MULTISPECTRAL', available: true, quality: 'medium' },
          { dataType: 'SAR', available: true, quality: 'medium' },
          { dataType: 'ICESAT2', available: true, quality: 'high' },
        ],
      },
      threats: {
        create: [
          { threatType: 'glacier_melting', severity: 'critical' },
          { threatType: 'climate_change', severity: 'critical' },
        ],
      },
      calibrationData: {
        create: {
          thermalDeltaK: 3.0,
          sarCoherence: 0.4,
          calibrationNotes: 'Reference site for ICE/GLACIER environment',
          calibrationConfidence: 0.85,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Ötzi the Iceman Discovery Site');

  // 4. PORT ROYAL (Jamaica) - SHALLOW_SEA
  const portRoyal = await prisma.archaeologicalSite.upsert({
    where: { slug: 'port-royal' },
    update: {},
    create: {
      name: 'Port Royal Submerged City',
      alternateNames: ['Sunken Pirate City', 'Wickedest City on Earth'],
      slug: 'port-royal',
      environmentType: 'SHALLOW_SEA',
      siteType: 'SUBMERGED_CITY',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'ONGOING_UNDERWATER',
      preservationStatus: 'GOOD',
      latitude: 17.9364,
      longitude: -76.8408,
      elevation: -12,
      areaKm2: 0.13,
      country: 'Jamaica',
      region: 'Kingston Harbour',
      period: 'Colonial Era',
      dateRangeStart: 1518,
      dateRangeEnd: 1692,
      dateUnit: 'CE',
      description: 'Submerged city that sank during an earthquake on June 7, 1692.',
      scientificSignificance: 'One of the best-preserved underwater archaeological sites. Complete time capsule of colonial Caribbean life.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Submerged 17th century buildings', featureType: 'urban' },
          { name: 'Shipwrecks in harbor', featureType: 'shipwreck' },
          { name: 'Fort structures', featureType: 'fortification' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'Texas A&M University Nautical Archaeology Program',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'MULTIBEAM_SONAR', available: true, quality: 'high' },
          { dataType: 'SIDE_SCAN_SONAR', available: true, quality: 'high' },
          { dataType: 'MAGNETOMETRY', available: true, quality: 'high' },
          { dataType: 'SUB_BOTTOM_PROFILER', available: true, quality: 'medium' },
        ],
      },
      threats: {
        create: [
          { threatType: 'marine_erosion', severity: 'medium' },
          { threatType: 'looting', severity: 'high' },
          { threatType: 'hurricanes', severity: 'high' },
        ],
      },
      calibrationData: {
        create: {
          bathymetricHeightM: 4.0,
          acousticReflectance: 0.7,
          magneticAnomalyNt: 150.0,
          calibrationNotes: 'Reference site for WATER/SUBMARINE environment',
          calibrationConfidence: 0.90,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Port Royal Submerged City');

  // 5. MACHU PICCHU (Peru) - MOUNTAIN
  const machuPicchu = await prisma.archaeologicalSite.upsert({
    where: { slug: 'machu-picchu' },
    update: {},
    create: {
      name: 'Machu Picchu',
      alternateNames: ['Lost City of the Incas', 'Machu Pikchu'],
      slug: 'machu-picchu',
      environmentType: 'MOUNTAIN',
      siteType: 'MOUNTAIN_CITADEL',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'ONGOING_RESEARCH',
      preservationStatus: 'GOOD',
      latitude: -13.1631,
      longitude: -72.5450,
      elevation: 2430,
      areaKm2: 0.326,
      country: 'Peru',
      region: 'Cusco Region',
      period: 'Inca Empire',
      dateRangeStart: 1450,
      dateRangeEnd: 1572,
      dateUnit: 'CE',
      unescoId: 274,
      unescoStatus: 'World Heritage Site',
      unescoYear: 1983,
      description: 'Iconic Inca citadel set high in the Andes Mountains.',
      scientificSignificance: 'Demonstrates advanced engineering and agricultural terracing in extreme mountain environment.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Agricultural terraces', featureType: 'agricultural' },
          { name: 'Temple of the Sun', featureType: 'temple' },
          { name: 'Intihuatana stone', featureType: 'ceremonial' },
          { name: 'Water management system', featureType: 'infrastructure' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'UNESCO World Heritage Centre',
            sourceUrl: 'https://whc.unesco.org/en/list/274',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'LIDAR', available: true, quality: 'high' },
          { dataType: 'SATELLITE_MULTISPECTRAL', available: true, quality: 'high' },
          { dataType: 'SAR', available: true, quality: 'medium' },
        ],
      },
      threats: {
        create: [
          { threatType: 'tourism_pressure', severity: 'critical' },
          { threatType: 'landslides', severity: 'high' },
          { threatType: 'earthquakes', severity: 'medium' },
        ],
      },
      calibrationData: {
        create: {
          elevationTerracingM: 8.0,
          slopeDeltaDegrees: 25.0,
          sarCoherence: 0.75,
          calibrationNotes: 'Reference site for MOUNTAIN environment',
          calibrationConfidence: 0.90,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Machu Picchu');

  // 6. PETRA (Jordan) - DESERT
  const petra = await prisma.archaeologicalSite.upsert({
    where: { slug: 'petra' },
    update: {},
    create: {
      name: 'Petra',
      alternateNames: ['Rose City', 'Raqmu'],
      slug: 'petra',
      environmentType: 'DESERT',
      siteType: 'ROCK_CUT_CITY',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'ONGOING_RESEARCH',
      preservationStatus: 'FAIR',
      latitude: 30.3285,
      longitude: 35.4444,
      elevation: 810,
      areaKm2: 264.0,
      country: 'Jordan',
      region: "Ma'an Governorate",
      period: 'Nabataean Kingdom',
      dateRangeStart: -300,
      dateRangeEnd: 106,
      dateUnit: 'BCE/CE',
      unescoId: 326,
      unescoStatus: 'World Heritage Site',
      unescoYear: 1985,
      description: 'Famous archaeological site with rock-cut architecture.',
      scientificSignificance: 'Spectacular rock-cut architecture demonstrating Nabataean engineering and water management in desert environment.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Al-Khazneh (Treasury)', featureType: 'monument' },
          { name: 'Monastery (Ad Deir)', featureType: 'temple' },
          { name: 'Royal tombs', featureType: 'burial' },
          { name: 'Water conduit system', featureType: 'infrastructure' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'UNESCO World Heritage Centre',
            sourceUrl: 'https://whc.unesco.org/en/list/326',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'LIDAR', available: true, quality: 'high' },
          { dataType: 'SATELLITE_THERMAL', available: true, quality: 'high' },
          { dataType: 'SAR', available: true, quality: 'high' },
        ],
      },
      threats: {
        create: [
          { threatType: 'erosion', severity: 'high' },
          { threatType: 'tourism_pressure', severity: 'high' },
          { threatType: 'flash_floods', severity: 'medium' },
        ],
      },
      calibrationData: {
        create: {
          thermalDeltaK: 8.0,
          sarBackscatterDb: -6.0,
          ndviDelta: 0.2,
          calibrationNotes: 'Reference site for DESERT environment',
          calibrationConfidence: 0.90,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Petra');

  // 7. STONEHENGE (UK) - GRASSLAND
  const stonehenge = await prisma.archaeologicalSite.upsert({
    where: { slug: 'stonehenge' },
    update: {},
    create: {
      name: 'Stonehenge',
      alternateNames: ['Stonehenge Stone Circle'],
      slug: 'stonehenge',
      environmentType: 'GRASSLAND',
      siteType: 'MEGALITHIC_MONUMENT',
      confidenceLevel: 'CONFIRMED',
      excavationStatus: 'EXTENSIVELY_EXCAVATED',
      preservationStatus: 'GOOD',
      latitude: 51.1789,
      longitude: -1.8262,
      elevation: 104,
      areaKm2: 0.011,
      country: 'United Kingdom',
      region: 'Wiltshire, England',
      period: 'Neolithic to Bronze Age',
      dateRangeStart: -3000,
      dateRangeEnd: -2000,
      dateUnit: 'BCE',
      unescoId: 373,
      unescoStatus: 'World Heritage Site',
      unescoYear: 1986,
      description: 'Iconic prehistoric monument consisting of a ring of standing stones.',
      scientificSignificance: 'Iconic prehistoric monument with astronomical alignments. Recent discoveries show extensive surrounding landscape of monuments.',
      isReferencesite: true,
      lastVerified: new Date('2026-01-25'),
      features: {
        create: [
          { name: 'Stone circle', featureType: 'monument' },
          { name: 'Trilithons', featureType: 'monument' },
          { name: 'Aubrey holes', featureType: 'ceremonial' },
          { name: 'Avenue', featureType: 'infrastructure' },
        ],
      },
      dataSources: {
        create: [
          {
            sourceType: 'primary',
            sourceName: 'UNESCO World Heritage Centre',
            sourceUrl: 'https://whc.unesco.org/en/list/373',
          },
          {
            sourceType: 'lidar_source',
            sourceName: 'English Heritage',
          },
        ],
      },
      dataAvailability: {
        create: [
          { dataType: 'LIDAR', available: true, quality: 'high' },
          { dataType: 'SATELLITE_MULTISPECTRAL', available: true, quality: 'high' },
          { dataType: 'GROUND_PENETRATING_RADAR', available: true, quality: 'high' },
        ],
      },
      threats: {
        create: [
          { threatType: 'tourism_pressure', severity: 'high' },
          { threatType: 'road_vibrations', severity: 'medium' },
          { threatType: 'weathering', severity: 'low' },
        ],
      },
      calibrationData: {
        create: {
          sarCoherence: 0.7,
          calibrationNotes: 'Reference site for GRASSLAND environment',
          calibrationConfidence: 0.85,
          lastCalibrated: new Date('2026-01-25'),
        },
      },
    },
  });
  console.log('  ✅ Stonehenge');

  // ============================================================================
  // SITIOS DE CONTROL (NEGATIVOS)
  // ============================================================================

  console.log('\n🌿 Creando sitios de control (negativos)...');

  // Control 1: Atacama Desert
  await prisma.archaeologicalSite.upsert({
    where: { slug: 'atacama-desert-control' },
    update: {},
    create: {
      name: 'Atacama Desert Natural Control',
      alternateNames: [],
      slug: 'atacama-desert-control',
      environmentType: 'DESERT',
      siteType: 'NATURAL_CONTROL',
      confidenceLevel: 'NEGATIVE_CONTROL',
      excavationStatus: 'NOT_APPLICABLE',
      preservationStatus: 'EXCELLENT',
      latitude: -24.0000,
      longitude: -69.0000,
      country: 'Chile',
      region: 'Atacama Desert',
      description: 'Natural desert with NO archaeological features - used to calibrate false positive rates',
      isControlSite: true,
      lastVerified: new Date('2026-01-25'),
    },
  });
  console.log('  ✅ Atacama Desert Control');

  // Control 2: Amazon Rainforest
  await prisma.archaeologicalSite.upsert({
    where: { slug: 'amazon-rainforest-control' },
    update: {},
    create: {
      name: 'Amazon Rainforest Natural Control',
      alternateNames: [],
      slug: 'amazon-rainforest-control',
      environmentType: 'FOREST',
      siteType: 'NATURAL_CONTROL',
      confidenceLevel: 'NEGATIVE_CONTROL',
      excavationStatus: 'NOT_APPLICABLE',
      preservationStatus: 'EXCELLENT',
      latitude: -3.4653,
      longitude: -62.2159,
      country: 'Brazil',
      region: 'Amazon Rainforest',
      description: 'Pristine rainforest with NO known archaeological features - used to calibrate false positive rates',
      isControlSite: true,
      lastVerified: new Date('2026-01-25'),
    },
  });
  console.log('  ✅ Amazon Rainforest Control');

  // Control 3: Greenland Ice Sheet
  await prisma.archaeologicalSite.upsert({
    where: { slug: 'greenland-ice-control' },
    update: {},
    create: {
      name: 'Greenland Ice Sheet Natural Control',
      alternateNames: [],
      slug: 'greenland-ice-control',
      environmentType: 'POLAR_ICE',
      siteType: 'NATURAL_CONTROL',
      confidenceLevel: 'NEGATIVE_CONTROL',
      excavationStatus: 'NOT_APPLICABLE',
      preservationStatus: 'EXCELLENT',
      latitude: 72.5796,
      longitude: -38.4592,
      country: 'Greenland',
      region: 'Greenland Ice Sheet',
      description: 'Pristine ice sheet with NO archaeological features - used to calibrate false positive rates',
      isControlSite: true,
      lastVerified: new Date('2026-01-25'),
    },
  });
  console.log('  ✅ Greenland Ice Sheet Control');

  // Control 4: Pacific Ocean
  await prisma.archaeologicalSite.upsert({
    where: { slug: 'pacific-ocean-control' },
    update: {},
    create: {
      name: 'Pacific Ocean Natural Control',
      alternateNames: [],
      slug: 'pacific-ocean-control',
      environmentType: 'DEEP_OCEAN',
      siteType: 'NATURAL_CONTROL',
      confidenceLevel: 'NEGATIVE_CONTROL',
      excavationStatus: 'NOT_APPLICABLE',
      preservationStatus: 'EXCELLENT',
      latitude: 0.0000,
      longitude: -140.0000,
      elevation: -4000,
      country: 'International Waters',
      region: 'Pacific Ocean',
      description: 'Deep ocean with NO known archaeological features - used to calibrate false positive rates',
      isControlSite: true,
      lastVerified: new Date('2026-01-25'),
    },
  });
  console.log('  ✅ Pacific Ocean Control');

  // ============================================================================
  // FIRMAS DE ANOMALÍAS POR AMBIENTE
  // ============================================================================

  console.log('\n🔬 Creando firmas de anomalías por ambiente...');

  const environments = [
    'DESERT',
    'FOREST',
    'GLACIER',
    'SHALLOW_SEA',
    'MOUNTAIN',
    'GRASSLAND',
    'POLAR_ICE',
    'UNKNOWN',
  ];

  for (const env of environments) {
    await prisma.anomalySignature.upsert({
      where: { environmentType: env as any },
      update: {},
      create: {
        environmentType: env as any,
        description: `Anomaly signatures for ${env} environment`,
        primaryInstruments: ['sentinel2', 'landsat', 'sar'],
        secondaryInstruments: ['modis'],
        minimumConvergence: 2,
        indicators: {
          // Placeholder - se llenará con datos reales
          placeholder: true,
        },
      },
    });
  }
  console.log(`  ✅ ${environments.length} firmas de anomalías creadas`);

  // ============================================================================
  // RESUMEN
  // ============================================================================

  const totalSites = await prisma.archaeologicalSite.count();
  const referenceSites = await prisma.archaeologicalSite.count({
    where: { isReferencesite: true },
  });
  const controlSites = await prisma.archaeologicalSite.count({
    where: { isControlSite: true },
  });

  console.log('\n✅ Seed completado exitosamente!');
  console.log(`\n📊 Resumen:`);
  console.log(`   Total de sitios: ${totalSites}`);
  console.log(`   Sitios de referencia: ${referenceSites}`);
  console.log(`   Sitios de control: ${controlSites}`);
  console.log(`   Firmas de anomalías: ${environments.length}`);
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error('❌ Error en seed:', e);
    await prisma.$disconnect();
    process.exit(1);
  });
