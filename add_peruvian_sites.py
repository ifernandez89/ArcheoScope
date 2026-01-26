#!/usr/bin/env python3
"""
Agregar sitios arqueológicos peruanos CRÍTICOS a la base de datos
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

# Sitios arqueológicos peruanos CONOCIDOS
PERUVIAN_SITES = [
    # Cusco - Valle Sagrado
    {'name': 'Machu Picchu', 'lat': -13.1631, 'lon': -72.5450, 'type': 'Inca citadel', 'period': 'Inca (1450-1540 CE)', 'confidence': 'HIGH'},
    {'name': 'Ollantaytambo', 'lat': -13.2583, 'lon': -72.2650, 'type': 'Inca fortress', 'period': 'Inca', 'confidence': 'HIGH'},
    {'name': 'Pisac', 'lat': -13.4211, 'lon': -71.8478, 'type': 'Inca citadel', 'period': 'Inca', 'confidence': 'HIGH'},
    {'name': 'Sacsayhuamán', 'lat': -13.5086, 'lon': -71.9819, 'type': 'Inca fortress', 'period': 'Inca', 'confidence': 'HIGH'},
    {'name': 'Qorikancha (Cusco)', 'lat': -13.5186, 'lon': -71.9753, 'type': 'Inca temple', 'period': 'Inca', 'confidence': 'HIGH'},
    {'name': 'Moray', 'lat': -13.3297, 'lon': -72.1942, 'type': 'Inca agricultural terraces', 'period': 'Inca', 'confidence': 'HIGH'},
    {'name': 'Chinchero', 'lat': -13.3933, 'lon': -72.0517, 'type': 'Inca settlement', 'period': 'Inca', 'confidence': 'HIGH'},
    
    # Lima - Costa Central
    {'name': 'Pachacamac', 'lat': -12.2667, 'lon': -76.9000, 'type': 'Pre-Inca temple complex', 'period': 'Lima/Wari/Inca', 'confidence': 'HIGH'},
    {'name': 'Caral', 'lat': -10.8933, 'lon': -77.5200, 'type': 'Ancient city', 'period': 'Caral (3000-1800 BCE)', 'confidence': 'HIGH'},
    {'name': 'Huaca Pucllana', 'lat': -12.1100, 'lon': -77.0300, 'type': 'Pyramid', 'period': 'Lima (200-700 CE)', 'confidence': 'HIGH'},
    {'name': 'Huaca Huallamarca', 'lat': -12.0900, 'lon': -77.0350, 'type': 'Pyramid', 'period': 'Lima', 'confidence': 'HIGH'},
    
    # Nazca
    {'name': 'Nazca Lines', 'lat': -14.7390, 'lon': -75.1300, 'type': 'Geoglyphs', 'period': 'Nazca (500 BCE-500 CE)', 'confidence': 'HIGH'},
    {'name': 'Cahuachi', 'lat': -14.8167, 'lon': -75.1167, 'type': 'Ceremonial center', 'period': 'Nazca', 'confidence': 'HIGH'},
    
    # Arequipa - Sur
    {'name': 'Toro Muerto', 'lat': -16.1500, 'lon': -72.4000, 'type': 'Petroglyphs', 'period': 'Wari/Inca', 'confidence': 'HIGH'},
    {'name': 'Uyo Uyo', 'lat': -15.6300, 'lon': -71.9700, 'type': 'Inca settlement', 'period': 'Inca', 'confidence': 'MEDIUM'},
    
    # Trujillo - Norte
    {'name': 'Chan Chan', 'lat': -8.1067, 'lon': -79.0750, 'type': 'Chimú capital', 'period': 'Chimú (900-1470 CE)', 'confidence': 'HIGH'},
    {'name': 'Huaca del Sol y la Luna', 'lat': -8.1350, 'lon': -79.0050, 'type': 'Moche pyramids', 'period': 'Moche (100-800 CE)', 'confidence': 'HIGH'},
    {'name': 'El Brujo', 'lat': -7.6667, 'lon': -79.4667, 'type': 'Moche complex', 'period': 'Moche', 'confidence': 'HIGH'},
    
    # Cajamarca - Norte
    {'name': 'Cumbemayo', 'lat': -7.1500, 'lon': -78.5000, 'type': 'Aqueduct', 'period': 'Pre-Inca', 'confidence': 'HIGH'},
    {'name': 'Ventanillas de Otuzco', 'lat': -7.1333, 'lon': -78.4833, 'type': 'Necropolis', 'period': 'Cajamarca', 'confidence': 'MEDIUM'},
    
    # Chiclayo - Norte
    {'name': 'Huaca Rajada (Señor de Sipán)', 'lat': -6.7667, 'lon': -79.6167, 'type': 'Moche tomb', 'period': 'Moche', 'confidence': 'HIGH'},
    {'name': 'Túcume', 'lat': -6.5167, 'lon': -79.8500, 'type': 'Pyramid complex', 'period': 'Lambayeque/Chimú', 'confidence': 'HIGH'},
    {'name': 'Batán Grande', 'lat': -6.5500, 'lon': -79.7000, 'type': 'Sicán complex', 'period': 'Sicán (750-1375 CE)', 'confidence': 'HIGH'},
    
    # Puno - Altiplano
    {'name': 'Sillustani', 'lat': -15.7500, 'lon': -70.1667, 'type': 'Chullpas (towers)', 'period': 'Colla/Inca', 'confidence': 'HIGH'},
    {'name': 'Pucará', 'lat': -15.0333, 'lon': -70.3667, 'type': 'Temple complex', 'period': 'Pucará (200 BCE-200 CE)', 'confidence': 'MEDIUM'},
    
    # Ayacucho - Centro
    {'name': 'Wari (Huari)', 'lat': -13.0667, 'lon': -74.1833, 'type': 'Wari capital', 'period': 'Wari (600-1000 CE)', 'confidence': 'HIGH'},
    {'name': 'Pikillacta', 'lat': -13.6333, 'lon': -71.7000, 'type': 'Wari administrative center', 'period': 'Wari', 'confidence': 'HIGH'},
    
    # Amazonía Peruana
    {'name': 'Gran Pajatén', 'lat': -7.9833, 'lon': -77.4167, 'type': 'Cloud forest settlement', 'period': 'Chachapoyas (800-1500 CE)', 'confidence': 'MEDIUM'},
    {'name': 'Kuelap', 'lat': -6.4167, 'lon': -77.9167, 'type': 'Chachapoyas fortress', 'period': 'Chachapoyas', 'confidence': 'HIGH'},
    {'name': 'Revash', 'lat': -6.7500, 'lon': -77.8333, 'type': 'Chachapoyas mausoleums', 'period': 'Chachapoyas', 'confidence': 'MEDIUM'},
    
    # Ica
    {'name': 'Tambo Colorado', 'lat': -13.4167, 'lon': -75.8000, 'type': 'Inca administrative center', 'period': 'Inca', 'confidence': 'HIGH'},
    
    # Ancash
    {'name': 'Chavín de Huántar', 'lat': -9.5933, 'lon': -77.1767, 'type': 'Ceremonial center', 'period': 'Chavín (900-200 BCE)', 'confidence': 'HIGH'},
    {'name': 'Sechín', 'lat': -9.4667, 'lon': -78.2667, 'type': 'Temple', 'period': 'Sechín (1800-900 BCE)', 'confidence': 'HIGH'},
    
    # Lambayeque
    {'name': 'Chotuna-Chornancap', 'lat': -6.6833, 'lon': -79.8667, 'type': 'Lambayeque complex', 'period': 'Lambayeque', 'confidence': 'MEDIUM'},
]

def add_peruvian_sites():
    """Agregar sitios peruanos a la base de datos"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("🇵🇪 AGREGANDO SITIOS ARQUEOLÓGICOS PERUANOS")
    print("=" * 80)
    
    # Verificar cuántos sitios peruanos hay actualmente
    cursor.execute("""
        SELECT COUNT(*) FROM archaeological_sites
        WHERE country = 'Peru' OR country = 'Perú'
    """)
    current_count = cursor.fetchone()[0]
    print(f"\n📊 Sitios peruanos actuales en BD: {current_count}")
    
    # Preparar datos para inserción
    sites_to_insert = []
    
    for site in PERUVIAN_SITES:
        site_id = str(uuid.uuid4())
        
        sites_to_insert.append((
            site_id,
            site['name'],
            site['lat'],
            site['lon'],
            'Peru',
            site['type'],
            site['period'],
            site['confidence'],
            'manual_addition',  # source
            None,  # wikidata_id
            None,  # description
            None,  # image_url
            None   # wikipedia_url
        ))
    
    # Insertar sitios
    insert_query = """
        INSERT INTO archaeological_sites (
            id, name, latitude, longitude, country, site_type, 
            period, confidence, source, wikidata_id, description, 
            image_url, wikipedia_url
        ) VALUES %s
        ON CONFLICT (id) DO NOTHING
    """
    
    execute_values(cursor, insert_query, sites_to_insert)
    conn.commit()
    
    print(f"\n✅ {len(PERUVIAN_SITES)} sitios peruanos agregados exitosamente")
    
    # Verificar inserción
    cursor.execute("""
        SELECT COUNT(*) FROM archaeological_sites
        WHERE country = 'Peru'
    """)
    new_count = cursor.fetchone()[0]
    print(f"📊 Total sitios peruanos en BD ahora: {new_count}")
    
    # Mostrar distribución por región
    print("\n📍 DISTRIBUCIÓN POR REGIÓN:")
    
    regions = [
        ('Cusco - Valle Sagrado', -14, -13, -73, -71),
        ('Lima - Costa Central', -13, -10, -78, -76),
        ('Nazca', -15.5, -14, -76, -74),
        ('Arequipa - Sur', -17, -15, -73, -71),
        ('Trujillo - Norte', -9, -7, -80, -78),
        ('Cajamarca', -8, -6, -79, -77),
        ('Chiclayo', -7, -6, -80, -79),
        ('Puno - Altiplano', -16, -15, -71, -69),
        ('Ayacucho - Centro', -14, -13, -75, -73),
        ('Amazonía Peruana', -8, -6, -78, -77),
    ]
    
    for region_name, lat_min, lat_max, lon_min, lon_max in regions:
        cursor.execute("""
            SELECT COUNT(*) FROM archaeological_sites
            WHERE country = 'Peru'
              AND latitude BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
        """, (lat_min, lat_max, lon_min, lon_max))
        
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"   {region_name}: {count} sitios")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("\n🎯 Ahora puedes generar candidatas en los Andes Peruanos!")
    print("\nEjemplos de regiones para probar:")
    print("   - Cusco: lat -14 a -13, lon -73 a -71")
    print("   - Lima: lat -13 a -10, lon -78 a -76")
    print("   - Nazca: lat -15.5 a -14, lon -76 a -74")
    print("   - Trujillo: lat -9 a -7, lon -80 a -78")

if __name__ == "__main__":
    try:
        add_peruvian_sites()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
