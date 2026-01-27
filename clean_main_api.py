#!/usr/bin/env python3
"""
Limpiar main.py eliminando endpoints rotos y deprecados.
Mantener SOLO endpoints funcionales e importantes.
"""

print("""
🧹 LIMPIEZA DE ENDPOINTS - ArcheoScope

ENDPOINTS A ELIMINAR (rotos/deprecados):
❌ /test-ai - Timeout, no crítico
❌ /known-sites - 503, deprecado (usar /archaeological-sites/known)
❌ /validate-region - 503, deprecado
❌ /comparison-data - 503, deprecado
❌ /instruments/status - 503, deprecado
❌ /archaeological-sites/known - 500, BD no disponible
❌ /archaeological-sites/all - 500, BD no disponible
❌ /archaeological-sites/by-environment - 500, BD no disponible
❌ /archaeological-sites/environments/stats - 500, BD no disponible
❌ /archaeological-sites/recommended-zones-geojson - 500, BD no disponible
❌ /archaeological-sites/enriched-candidates - 501, usa np.random
❌ /archaeological-sites/candidates/priority - 500, BD no disponible
❌ /archaeological-sites/candidates/statistics - 500, BD no disponible
❌ /archaeological-sites/candidates/search - 500, BD no disponible
❌ /falsification-protocol - 500, módulo no existe
❌ /archaeological-sites/cultural-prior-map - 422, parámetros incorrectos
❌ /archaeological-sites/recommended-zones - 422, parámetros incorrectos (DUPLICADO)
❌ /academic/validation/blind-test - 503, no disponible
❌ /academic/explainability/analyze - No probado, probablemente roto

ENDPOINTS A MANTENER (funcionando):
✅ / - Root
✅ /status - System status
✅ /status/detailed - Detailed status
✅ /data-sources - Data sources
✅ /lidar-benchmark - LIDAR benchmark
✅ /instruments/archaeological-value - Archaeological value
✅ /archaeological-sites/candidates - Candidates (funciona)
✅ /volumetric/sites/catalog - Volumetric catalog
✅ /api/scientific/analyses/recent - Recent analyses (NEW)
✅ /api/scientific/analyses/by-region - Analyses by region (NEW)
✅ /api/scientific/analyze - Scientific analysis (NEW, POST)
✅ /test-analyze - Test endpoint (POST)
✅ /analyze - Main analysis endpoint (POST, CRÍTICO)

TOTAL: ~13 endpoints funcionales vs 18 rotos
""")

response = input("\n¿Proceder con la limpieza? (yes/no): ")
if response.lower() != 'yes':
    print("❌ Limpieza cancelada")
    exit(0)

print("\n✅ Limpieza confirmada - proceder manualmente con strReplace")
print("\nPasos:")
print("1. Eliminar endpoints rotos de main.py")
print("2. Mantener solo endpoints funcionales")
print("3. Actualizar documentación Swagger")
print("4. Commit cambios")
