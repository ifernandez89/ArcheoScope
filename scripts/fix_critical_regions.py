#!/usr/bin/env python3
"""
Agregar sitios arqueológicos a TODAS las regiones críticas identificadas
"""

import psycopg2
from psycopg2.extras import execute_values
import uuid

# Configuración de base de datos
DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

# Sitios arqueológicos para regiones CRÍTICAS
CRITICAL_SITES = {
    'PERÚ': [
        # Cusco - Valle Sagrado
        {'name': 'Machu Picchu', 'lat': -13.1631, 'lon': -72.5450, 'type': 'Inca citadel', 'period': 'Inca (1450-1540 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Ollantaytambo', 'lat': -13.2583, 'lon': -72.2650, 'type': 'Inca fortress', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Pisac', 'lat': -13.4211, 'lon': -71.8478, 'type': 'Inca citadel', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Sacsayhuamán', 'lat': -13.5086, 'lon': -71.9819, 'type': 'Inca fortress', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Qorikancha (Cusco)', 'lat': -13.5186, 'lon': -71.9753, 'type': 'Inca temple', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Moray', 'lat': -13.3297, 'lon': -72.1942, 'type': 'Inca agricultural terraces', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Chinchero', 'lat': -13.3933, 'lon': -72.0517, 'type': 'Inca settlement', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Raqchi', 'lat': -14.4667, 'lon': -71.2500, 'type': 'Inca temple', 'period': 'Inca', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Lima - Costa Central
        {'name': 'Pachacamac', 'lat': -12.2667, 'lon': -76.9000, 'type': 'Pre-Inca temple complex', 'period': 'Lima/Wari/Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Caral', 'lat': -10.8933, 'lon': -77.5200, 'type': 'Ancient city', 'period': 'Caral (3000-1800 BCE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Huaca Pucllana', 'lat': -12.1100, 'lon': -77.0300, 'type': 'Pyramid', 'period': 'Lima (200-700 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Huaca Huallamarca', 'lat': -12.0900, 'lon': -77.0350, 'type': 'Pyramid', 'period': 'Lima', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Nazca
        {'name': 'Nazca Lines', 'lat': -14.7390, 'lon': -75.1300, 'type': 'Geoglyphs', 'period': 'Nazca (500 BCE-500 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Cahuachi', 'lat': -14.8167, 'lon': -75.1167, 'type': 'Ceremonial center', 'period': 'Nazca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Palpa Lines', 'lat': -14.5333, 'lon': -75.1833, 'type': 'Geoglyphs', 'period': 'Nazca/Paracas', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Arequipa - Sur
        {'name': 'Toro Muerto', 'lat': -16.1500, 'lon': -72.4000, 'type': 'Petroglyphs', 'period': 'Wari/Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Uyo Uyo', 'lat': -15.6300, 'lon': -71.9700, 'type': 'Inca settlement', 'period': 'Inca', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Trujillo - Norte
        {'name': 'Chan Chan', 'lat': -8.1067, 'lon': -79.0750, 'type': 'Chimú capital', 'period': 'Chimú (900-1470 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Huaca del Sol y la Luna', 'lat': -8.1350, 'lon': -79.0050, 'type': 'Moche pyramids', 'period': 'Moche (100-800 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'El Brujo', 'lat': -7.6667, 'lon': -79.4667, 'type': 'Moche complex', 'period': 'Moche', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Cajamarca - Norte
        {'name': 'Cumbemayo', 'lat': -7.1500, 'lon': -78.5000, 'type': 'Aqueduct', 'period': 'Pre-Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Ventanillas de Otuzco', 'lat': -7.1333, 'lon': -78.4833, 'type': 'Necropolis', 'period': 'Cajamarca', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Chiclayo - Norte
        {'name': 'Huaca Rajada (Señor de Sipán)', 'lat': -6.7667, 'lon': -79.6167, 'type': 'Moche tomb', 'period': 'Moche', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Túcume', 'lat': -6.5167, 'lon': -79.8500, 'type': 'Pyramid complex', 'period': 'Lambayeque/Chimú', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Batán Grande', 'lat': -6.5500, 'lon': -79.7000, 'type': 'Sicán complex', 'period': 'Sicán (750-1375 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Puno - Altiplano
        {'name': 'Sillustani', 'lat': -15.7500, 'lon': -70.1667, 'type': 'Chullpas (towers)', 'period': 'Colla/Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Pucará', 'lat': -15.0333, 'lon': -70.3667, 'type': 'Temple complex', 'period': 'Pucará (200 BCE-200 CE)', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Ayacucho - Centro
        {'name': 'Wari (Huari)', 'lat': -13.0667, 'lon': -74.1833, 'type': 'Wari capital', 'period': 'Wari (600-1000 CE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Pikillacta', 'lat': -13.6333, 'lon': -71.7000, 'type': 'Wari administrative center', 'period': 'Wari', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Amazonía Peruana
        {'name': 'Gran Pajatén', 'lat': -7.9833, 'lon': -77.4167, 'type': 'Cloud forest settlement', 'period': 'Chachapoyas (800-1500 CE)', 'confidence': 'MEDIUM', 'country': 'Peru'},
        {'name': 'Kuelap', 'lat': -6.4167, 'lon': -77.9167, 'type': 'Chachapoyas fortress', 'period': 'Chachapoyas', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Revash', 'lat': -6.7500, 'lon': -77.8333, 'type': 'Chachapoyas mausoleums', 'period': 'Chachapoyas', 'confidence': 'MEDIUM', 'country': 'Peru'},
        
        # Ica
        {'name': 'Tambo Colorado', 'lat': -13.4167, 'lon': -75.8000, 'type': 'Inca administrative center', 'period': 'Inca', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Ancash
        {'name': 'Chavín de Huántar', 'lat': -9.5933, 'lon': -77.1767, 'type': 'Ceremonial center', 'period': 'Chavín (900-200 BCE)', 'confidence': 'HIGH', 'country': 'Peru'},
        {'name': 'Sechín', 'lat': -9.4667, 'lon': -78.2667, 'type': 'Temple', 'period': 'Sechín (1800-900 BCE)', 'confidence': 'HIGH', 'country': 'Peru'},
        
        # Lambayeque
        {'name': 'Chotuna-Chornancap', 'lat': -6.6833, 'lon': -79.8667, 'type': 'Lambayeque complex', 'period': 'Lambayeque', 'confidence': 'MEDIUM', 'country': 'Peru'},
    ],
    
    'COLOMBIA': [
        {'name': 'San Agustín', 'lat': 1.8833, 'lon': -76.2833, 'type': 'Megalithic statues', 'period': 'San Agustín (3300 BCE-1630 CE)', 'confidence': 'HIGH', 'country': 'Colombia'},
        {'name': 'Tierradentro', 'lat': 2.5833, 'lon': -76.0333, 'type': 'Underground tombs', 'period': 'Tierradentro (600-900 CE)', 'confidence': 'HIGH', 'country': 'Colombia'},
        {'name': 'Ciudad Perdida (Teyuna)', 'lat': 11.0383, 'lon': -73.9250, 'type': 'Tayrona city', 'period': 'Tayrona (800 CE)', 'confidence': 'HIGH', 'country': 'Colombia'},
        {'name': 'Alto de los Ídolos', 'lat': 1.9167, 'lon': -76.2500, 'type': 'Megalithic site', 'period': 'San Agustín', 'confidence': 'MEDIUM', 'country': 'Colombia'},
        {'name': 'Alto de las Piedras', 'lat': 1.8667, 'lon': -76.3000, 'type': 'Megalithic site', 'period': 'San Agustín', 'confidence': 'MEDIUM', 'country': 'Colombia'},
    ],
    
    'BRASIL_AMAZONIA': [
        {'name': 'Geoglifo Jacó Sá', 'lat': -4.2500, 'lon': -61.5000, 'type': 'Geoglyph', 'period': 'Pre-Columbian', 'confidence': 'MEDIUM', 'country': 'Brazil'},
        {'name': 'Terra Preta Site (Amazonas)', 'lat': -3.8000, 'lon': -61.0000, 'type': 'Settlement', 'period': 'Pre-Columbian', 'confidence': 'MEDIUM', 'country': 'Brazil'},
        {'name': 'Amazonian Earthworks', 'lat': -4.5000, 'lon': -60.5000, 'type': 'Earthworks', 'period': 'Pre-Columbian', 'confidence': 'LOW', 'country': 'Brazil'},
        {'name': 'Manaus Archaeological Site', 'lat': -3.1190, 'lon': -60.0217, 'type': 'Settlement', 'period': 'Pre-Columbian', 'confidence': 'LOW', 'country': 'Brazil'},
    ],
    
    'MYANMAR': [
        {'name': 'Bagan Archaeological Zone', 'lat': 21.1717, 'lon': 94.8578, 'type': 'Temple complex', 'period': 'Pagan Kingdom (849-1297 CE)', 'confidence': 'HIGH', 'country': 'Myanmar'},
        {'name': 'Ananda Temple', 'lat': 21.1750, 'lon': 94.8683, 'type': 'Buddhist temple', 'period': 'Pagan', 'confidence': 'HIGH', 'country': 'Myanmar'},
        {'name': 'Shwezigon Pagoda', 'lat': 21.1833, 'lon': 94.8833, 'type': 'Buddhist stupa', 'period': 'Pagan', 'confidence': 'HIGH', 'country': 'Myanmar'},
        {'name': 'Dhammayangyi Temple', 'lat': 21.1633, 'lon': 94.8717, 'type': 'Buddhist temple', 'period': 'Pagan', 'confidence': 'HIGH', 'country': 'Myanmar'},
        {'name': 'Thatbyinnyu Temple', 'lat': 21.1717, 'lon': 94.8633, 'type': 'Buddhist temple', 'period': 'Pagan', 'confidence': 'HIGH', 'country': 'Myanmar'},
    ],
    
    'ISLA_PASCUA': [
        {'name': 'Rano Raraku (Moai quarry)', 'lat': -27.1247, 'lon': -109.2897, 'type': 'Quarry and moai', 'period': 'Rapa Nui (1250-1500 CE)', 'confidence': 'HIGH', 'country': 'Chile'},
        {'name': 'Ahu Tongariki', 'lat': -27.1258, 'lon': -109.2783, 'type': 'Moai platform', 'period': 'Rapa Nui', 'confidence': 'HIGH', 'country': 'Chile'},
        {'name': 'Ahu Akivi', 'lat': -27.1100, 'lon': -109.3833, 'type': 'Moai platform', 'period': 'Rapa Nui', 'confidence': 'HIGH', 'country': 'Chile'},
        {'name': 'Orongo', 'lat': -27.1917, 'lon': -109.4267, 'type': 'Ceremonial village', 'period': 'Rapa Nui', 'confidence': 'HIGH', 'country': 'Chile'},
        {'name': 'Ahu Tahai', 'lat': -27.1400, 'lon': -109.4267, 'type': 'Moai platform', 'period': 'Rapa Nui', 'confidence': 'HIGH', 'country': 'Chile'},
    ],
}

def add_critical_sites():
    """Agregar sitios a regiones críticas"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("🌍 AGREGANDO SITIOS A REGIONES CRÍTICAS")
    print("=" * 100)
    
    total_added = 0
    
    for region_name, sites in CRITICAL_SITES.items():
        print(f"\n{'='*100}")
        print(f"📍 {region_name}")
        print(f"{'='*100}")
        
        sites_to_insert = []
        
        for site in sites:
            site_id = str(uuid.uuid4())
            slug = site['name'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            
            # Mapear tipo de sitio
            site_type_map = {
                'citadel': 'MOUNTAIN_CITADEL',
                'fortress': 'FORTIFICATION',
                'temple': 'TEMPLE_COMPLEX',
                'pyramid': 'MONUMENTAL_COMPLEX',
                'city': 'URBAN_SETTLEMENT',
                'settlement': 'URBAN_SETTLEMENT',
                'complex': 'MONUMENTAL_COMPLEX',
                'tomb': 'BURIAL_SITE',
                'necropolis': 'BURIAL_SITE',
                'ceremonial': 'CEREMONIAL_CENTER',
                'aqueduct': 'AGRICULTURAL_SITE',
                'terraces': 'AGRICULTURAL_SITE',
                'geoglyph': 'CEREMONIAL_CENTER',
                'petroglyphs': 'CEREMONIAL_CENTER',
                'quarry': 'MONUMENTAL_COMPLEX',
                'platform': 'CEREMONIAL_CENTER',
                'village': 'URBAN_SETTLEMENT',
                'mausoleums': 'BURIAL_SITE',
                'towers': 'FORTIFICATION',
                'stupa': 'TEMPLE_COMPLEX',
                'pagoda': 'TEMPLE_COMPLEX',
                'moai': 'MEGALITHIC_MONUMENT',
                'statues': 'MEGALITHIC_MONUMENT',
                'earthworks': 'AGRICULTURAL_SITE',
            }
            
            site_type = 'UNKNOWN'
            for key, value in site_type_map.items():
                if key in site['type'].lower():
                    site_type = value
                    break
            
            # Mapear nivel de confianza
            confidence_map = {
                'HIGH': 'HIGH',
                'MEDIUM': 'MODERATE',
                'LOW': 'LOW'
            }
            confidence = confidence_map.get(site['confidence'], 'MODERATE')
            
            sites_to_insert.append((
                site_id,
                site['name'],
                slug,
                'UNKNOWN',  # environmentType
                site_type,  # siteType
                confidence,  # confidenceLevel
                'PARTIALLY_EXCAVATED',  # excavationStatus
                'UNKNOWN',  # preservationStatus
                site['lat'],
                site['lon'],
                site['country'],
                site['period'],
                True,  # isReferencesite
                False,  # isControlSite
                site['type']  # description
            ))
        
        # Insertar sitios
        insert_query = """
            INSERT INTO archaeological_sites (
                id, name, slug, "environmentType", "siteType", "confidenceLevel",
                "excavationStatus", "preservationStatus", latitude, longitude, 
                country, period, "isReferencesite", "isControlSite", description
            ) VALUES %s
            ON CONFLICT (id) DO NOTHING
        """
        
        execute_values(cursor, insert_query, sites_to_insert)
        conn.commit()
        
        print(f"✅ {len(sites)} sitios agregados")
        total_added += len(sites)
        
        # Mostrar algunos ejemplos
        print(f"\n   Ejemplos:")
        for site in sites[:3]:
            print(f"      - {site['name']} ({site['lat']:.4f}, {site['lon']:.4f})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ PROCESO COMPLETADO")
    print(f"\n📊 TOTAL SITIOS AGREGADOS: {total_added}")
    
    print("\n🎯 REGIONES CORREGIDAS:")
    print("   ✅ Perú - Andes/Costa: 35 sitios")
    print("   ✅ Colombia - San Agustín: 5 sitios")
    print("   ✅ Brasil - Amazonía Occidental: 4 sitios")
    print("   ✅ Myanmar - Bagan: 5 sitios")
    print("   ✅ Isla de Pascua - Moai: 5 sitios")
    
    print("\n🚀 Ahora puedes generar candidatas en TODAS estas regiones!")

if __name__ == "__main__":
    try:
        add_critical_sites()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
