#!/usr/bin/env python3
"""
Investigar fuentes adicionales de sitios arqueológicos
"""

import requests
import json

print("=" * 80)
print("🔍 INVESTIGACIÓN DE FUENTES ADICIONALES DE SITIOS ARQUEOLÓGICOS")
print("=" * 80)

sources = []

# 1. Pleiades (Mundo Antiguo - Greco-Romano)
print("\n1. 📚 PLEIADES (Mundo Antiguo)")
print("   URL: https://pleiades.stoa.org/")
print("   Cobertura: Mediterráneo, Medio Oriente, Europa")
print("   Período: Antigüedad clásica")
print("   API: https://pleiades.stoa.org/downloads")
try:
    # Verificar disponibilidad
    response = requests.head("https://atlantides.org/downloads/pleiades/json/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: JSON dump completo")
        print("   Estimado: ~35,000 lugares")
        sources.append({
            'name': 'Pleiades',
            'url': 'https://atlantides.org/downloads/pleiades/json/',
            'coverage': 'Mediterranean, Middle East',
            'estimated_sites': 35000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 2. EAMENA (Medio Oriente y Norte de África)
print("\n2. 🏺 EAMENA (Endangered Archaeology)")
print("   URL: https://eamena.org/")
print("   Cobertura: Medio Oriente, Norte de África")
print("   Período: Todos los períodos")
print("   API: Database pública")
try:
    response = requests.head("https://database.eamena.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: Requiere scraping o API request")
        print("   Estimado: ~200,000 sitios")
        sources.append({
            'name': 'EAMENA',
            'url': 'https://database.eamena.org/',
            'coverage': 'Middle East, North Africa',
            'estimated_sites': 200000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 3. ARIADNE (Infraestructura Europea)
print("\n3. 🏛️ ARIADNE (European Archaeological Data)")
print("   URL: https://portal.ariadne-infrastructure.eu/")
print("   Cobertura: Europa principalmente")
print("   Período: Todos los períodos")
print("   API: SPARQL endpoint")
try:
    response = requests.head("https://portal.ariadne-infrastructure.eu/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: SPARQL queries")
        print("   Estimado: ~2,000,000 registros")
        sources.append({
            'name': 'ARIADNE',
            'url': 'https://portal.ariadne-infrastructure.eu/',
            'coverage': 'Europe',
            'estimated_sites': 2000000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 4. Open Context
print("\n4. 📖 OPEN CONTEXT")
print("   URL: https://opencontext.org/")
print("   Cobertura: Global")
print("   Período: Todos los períodos")
print("   API: JSON-LD API")
try:
    response = requests.head("https://opencontext.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: JSON-LD API")
        print("   Estimado: ~50,000 sitios")
        sources.append({
            'name': 'Open Context',
            'url': 'https://opencontext.org/subjects-search/',
            'coverage': 'Global',
            'estimated_sites': 50000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 5. ArchaeoGLOBE
print("\n5. 🌍 ARCHAEOGLOBE")
print("   URL: https://archaeoglobe.org/")
print("   Cobertura: Global")
print("   Período: Holoceno")
print("   API: Dataset público")
try:
    response = requests.head("https://archaeoglobe.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: CSV/Shapefile")
        print("   Estimado: ~10,000 regiones")
        sources.append({
            'name': 'ArchaeoGLOBE',
            'url': 'https://archaeoglobe.org/',
            'coverage': 'Global',
            'estimated_sites': 10000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 6. Digital Atlas of Roman Empire (DARE)
print("\n6. 🏛️ DARE (Digital Atlas of Roman Empire)")
print("   URL: https://dh.gu.se/dare/")
print("   Cobertura: Imperio Romano")
print("   Período: Romano")
print("   API: GeoJSON disponible")
try:
    response = requests.head("https://dh.gu.se/dare/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: GeoJSON")
        print("   Estimado: ~10,000 sitios")
        sources.append({
            'name': 'DARE',
            'url': 'https://dh.gu.se/dare/',
            'coverage': 'Roman Empire',
            'estimated_sites': 10000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 7. Pelagios (Linked Open Data)
print("\n7. 🔗 PELAGIOS")
print("   URL: https://pelagios.org/")
print("   Cobertura: Global (histórico)")
print("   Período: Antigüedad principalmente")
print("   API: Linked Data")
try:
    response = requests.head("https://pelagios.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: RDF/Linked Data")
        print("   Estimado: ~100,000 lugares")
        sources.append({
            'name': 'Pelagios',
            'url': 'https://pelagios.org/',
            'coverage': 'Global historical',
            'estimated_sites': 100000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 8. tDAR (Digital Archaeological Record)
print("\n8. 📚 tDAR (The Digital Archaeological Record)")
print("   URL: https://core.tdar.org/")
print("   Cobertura: Américas principalmente")
print("   Período: Todos los períodos")
print("   API: REST API (requiere registro)")
try:
    response = requests.head("https://core.tdar.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: REST API")
        print("   Estimado: ~500,000 recursos")
        sources.append({
            'name': 'tDAR',
            'url': 'https://core.tdar.org/',
            'coverage': 'Americas',
            'estimated_sites': 500000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 9. Europeana (Patrimonio Cultural Europeo)
print("\n9. 🎨 EUROPEANA")
print("   URL: https://www.europeana.eu/")
print("   Cobertura: Europa")
print("   Período: Todos los períodos")
print("   API: REST API (requiere API key gratuita)")
try:
    response = requests.head("https://www.europeana.eu/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: REST API")
        print("   Estimado: ~50,000 sitios arqueológicos")
        sources.append({
            'name': 'Europeana',
            'url': 'https://www.europeana.eu/',
            'coverage': 'Europe',
            'estimated_sites': 50000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# 10. GeoNames (lugares arqueológicos)
print("\n10. 🌐 GEONAMES (Archaeological features)")
print("   URL: https://www.geonames.org/")
print("   Cobertura: Global")
print("   Período: Todos")
print("   API: REST API gratuita")
try:
    response = requests.head("https://www.geonames.org/", timeout=5)
    if response.status_code == 200:
        print("   Estado: ✅ DISPONIBLE")
        print("   Formato: REST API / Dump")
        print("   Estimado: ~20,000 sitios arqueológicos")
        sources.append({
            'name': 'GeoNames',
            'url': 'https://www.geonames.org/',
            'coverage': 'Global',
            'estimated_sites': 20000,
            'available': True
        })
    else:
        print("   Estado: ⚠️ Verificar manualmente")
except Exception as e:
    print(f"   Estado: ❌ Error: {e}")

# Resumen
print("\n" + "=" * 80)
print("📊 RESUMEN DE FUENTES ADICIONALES")
print("=" * 80)

if sources:
    print(f"\n✅ Fuentes disponibles: {len(sources)}")
    print(f"\n📈 Estimado total de sitios adicionales: {sum(s['estimated_sites'] for s in sources):,}")
    
    print(f"\n🎯 RECOMENDACIONES POR PRIORIDAD:\n")
    
    # Prioridad 1: Más sitios
    print("🔴 PRIORIDAD ALTA (más sitios):")
    high_priority = [s for s in sources if s['estimated_sites'] > 100000]
    for s in sorted(high_priority, key=lambda x: x['estimated_sites'], reverse=True):
        print(f"   • {s['name']}: ~{s['estimated_sites']:,} sitios ({s['coverage']})")
    
    # Prioridad 2: Cobertura específica
    print("\n🟡 PRIORIDAD MEDIA (cobertura específica):")
    medium_priority = [s for s in sources if 10000 < s['estimated_sites'] <= 100000]
    for s in sorted(medium_priority, key=lambda x: x['estimated_sites'], reverse=True):
        print(f"   • {s['name']}: ~{s['estimated_sites']:,} sitios ({s['coverage']})")
    
    # Prioridad 3: Complementarias
    print("\n🟢 PRIORIDAD BAJA (complementarias):")
    low_priority = [s for s in sources if s['estimated_sites'] <= 10000]
    for s in sorted(low_priority, key=lambda x: x['estimated_sites'], reverse=True):
        print(f"   • {s['name']}: ~{s['estimated_sites']:,} sitios ({s['coverage']})")
    
    # Guardar resultados
    with open('additional_sources_research.json', 'w', encoding='utf-8') as f:
        json.dump({
            'research_date': '2026-01-26',
            'total_sources': len(sources),
            'estimated_total_sites': sum(s['estimated_sites'] for s in sources),
            'sources': sources
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: additional_sources_research.json")

else:
    print("\n❌ No se encontraron fuentes adicionales disponibles")

print("\n" + "=" * 80)
print("💡 PRÓXIMOS PASOS SUGERIDOS:")
print("=" * 80)
print("""
1. ARIADNE (2M sitios) - Mayor potencial
   - Requiere: SPARQL queries
   - Tiempo estimado: 2-3 horas de desarrollo
   
2. EAMENA (200K sitios) - Medio Oriente/África
   - Requiere: Web scraping o API
   - Tiempo estimado: 3-4 horas de desarrollo
   
3. tDAR (500K sitios) - Américas
   - Requiere: Registro + API key
   - Tiempo estimado: 2 horas de desarrollo
   
4. Pleiades (35K sitios) - Mundo clásico
   - Requiere: Descargar JSON dump
   - Tiempo estimado: 30 minutos

ALTERNATIVA RÁPIDA:
- Usar Pleiades primero (30 min) para agregar ~35K sitios del mundo antiguo
- Luego evaluar si vale la pena el esfuerzo de ARIADNE/EAMENA
""")

print("=" * 80)
