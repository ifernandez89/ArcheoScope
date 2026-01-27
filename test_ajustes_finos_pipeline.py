#!/usr/bin/env python3
"""
Test de los 3 ajustes finos implementados en el pipeline científico.

AJUSTES FINOS:
1. Baseline profiles por ambiente (glacial, desert, coastal, mountain)
2. Diferenciar discard_operational vs archive_scientific_negative
3. Scientific confidence (certeza del descarte)
"""

import asyncio
import asyncpg
import requests
import json

API_BASE = "http://localhost:8002"

async def test_ajustes_finos():
    """Test de ajustes finos con segundo candidato."""
    
    conn = await asyncpg.connect(
        host='localhost', port=5433, user='postgres',
        password='1464', database='archeoscope_db'
    )
    
    print("="*80, flush=True)
    print("TEST AJUSTES FINOS - PIPELINE CIENTÍFICO", flush=True)
    print("="*80, flush=True)
    
    # Obtener segundo candidato (Nuuk SW Groenlandia)
    candidato = await conn.fetchrow("""
        SELECT 
            analysis_id,
            region_name,
            latitude,
            longitude
        FROM measurements
        ORDER BY measurement_timestamp
        LIMIT 1 OFFSET 1
    """)
    
    if not candidato:
        print("\nNo hay segundo candidato en BD", flush=True)
        await conn.close()
        return
    
    analysis_id = candidato['analysis_id']
    region_name = candidato['region_name']
    lat = float(candidato['latitude'])
    lon = float(candidato['longitude'])
    
    print(f"\nCANDIDATO: {region_name}", flush=True)
    print(f"Coordenadas: {lat:.4f}, {lon:.4f}", flush=True)
    print(f"Ambiente esperado: polar_ice (glacial baseline)", flush=True)
    
    lat_min = lat - 0.05
    lat_max = lat + 0.05
    lon_min = lon - 0.05
    lon_max = lon + 0.05
    
    try:
        print(f"\n[ANALISIS] Ejecutando pipeline con ajustes finos...", flush=True)
        
        payload = {
            "lat_min": lat_min,
            "lat_max": lat_max,
            "lon_min": lon_min,
            "lon_max": lon_max,
            "region_name": region_name,
            "candidate_id": str(analysis_id)
        }
        
        response = requests.post(
            f"{API_BASE}/analyze-scientific",
            json=payload,
            timeout=180
        )
        
        if response.status_code != 200:
            print(f"[ERROR] Error en API: {response.status_code}", flush=True)
            await conn.close()
            return
        
        resultado = response.json()
        scientific_output = resultado.get('scientific_output', {})
        
        print(f"\n{'='*80}", flush=True)
        print("VERIFICACIÓN DE AJUSTES FINOS", flush=True)
        print(f"{'='*80}", flush=True)
        
        # AJUSTE FINO 1: Baseline Profile
        print(f"\n🔵 AJUSTE FINO 1: BASELINE PROFILE", flush=True)
        print(f"  Ambiente: {resultado.get('environment_context', {}).get('environment_type', 'unknown')}", flush=True)
        print(f"  Geomorfología: {resultado.get('phase_c_morphology', {}).get('geomorphology_hint', 'unknown')}", flush=True)
        print(f"  ✅ Debería coincidir con baseline 'glacial'", flush=True)
        
        # AJUSTE FINO 2: Tipo de descarte
        print(f"\n🟡 AJUSTE FINO 2: TIPO DE DESCARTE", flush=True)
        discard_type = scientific_output.get('discard_type', 'none')
        print(f"  Discard type: {discard_type}", flush=True)
        if discard_type == "archive_scientific_negative":
            print(f"  ✅ CORRECTO: Archivado como referencia científica negativa", flush=True)
            print(f"  📚 Este candidato vale para entrenar anti-patrones glaciares", flush=True)
        elif discard_type == "discard_operational":
            print(f"  ⚠️ Descarte operacional simple (sin valor científico)", flush=True)
        else:
            print(f"  ℹ️ No es un descarte (candidato positivo o incierto)", flush=True)
        
        # AJUSTE FINO 3: Confianza científica
        print(f"\n🟢 AJUSTE FINO 3: CONFIANZA CIENTÍFICA", flush=True)
        scientific_confidence = scientific_output.get('scientific_confidence', 'unknown')
        anthropic_prob = scientific_output.get('anthropic_probability', 0)
        print(f"  Probabilidad antropogénica: {anthropic_prob:.3f}", flush=True)
        print(f"  Confianza científica del descarte: {scientific_confidence}", flush=True)
        
        if scientific_confidence == "high":
            print(f"  ✅ ALTA confianza en que NO es arqueológico", flush=True)
            print(f"  📌 Inferencia baja + contexto geológico claro", flush=True)
        elif scientific_confidence == "medium_high":
            print(f"  ✅ MEDIA-ALTA confianza en el descarte", flush=True)
        elif scientific_confidence == "medium":
            print(f"  ⚠️ MEDIA confianza en el descarte", flush=True)
        else:
            print(f"  ⚠️ BAJA confianza en el descarte", flush=True)
        
        print(f"\n{'='*80}", flush=True)
        print("RESUMEN DE SALIDA CIENTÍFICA", flush=True)
        print(f"{'='*80}", flush=True)
        
        print(f"\n📊 Métricas:", flush=True)
        print(f"  - Anomaly score: {scientific_output.get('anomaly_score', 0):.3f}", flush=True)
        print(f"  - Anthropic probability: {anthropic_prob:.3f}", flush=True)
        print(f"  - Confidence interval: {scientific_output.get('confidence_interval', [0, 0])}", flush=True)
        
        print(f"\n🏷️ Clasificación:", flush=True)
        print(f"  - Candidate type: {scientific_output.get('candidate_type', 'unknown')}", flush=True)
        print(f"  - Negative reason: {scientific_output.get('negative_reason', 'N/A')}", flush=True)
        print(f"  - Reuse for training: {scientific_output.get('reuse_for_training', False)}", flush=True)
        
        print(f"\n🎯 Decisión:", flush=True)
        print(f"  - Recommended action: {scientific_output.get('recommended_action', 'unknown')}", flush=True)
        print(f"  - Discard type: {discard_type}", flush=True)
        print(f"  - Scientific confidence: {scientific_confidence}", flush=True)
        
        print(f"\n📝 Notas:", flush=True)
        print(f"  {scientific_output.get('notes', 'N/A')}", flush=True)
        
        # Verificación conceptual
        print(f"\n{'='*80}", flush=True)
        print("VERIFICACIÓN CONCEPTUAL", flush=True)
        print(f"{'='*80}", flush=True)
        
        checks_passed = 0
        checks_total = 3
        
        # Check 1: Baseline profile
        if resultado.get('environment_context', {}).get('environment_type') in ['polar_ice', 'glacier']:
            print(f"✅ Check 1: Ambiente glaciar detectado correctamente", flush=True)
            checks_passed += 1
        else:
            print(f"❌ Check 1: Ambiente no es glaciar", flush=True)
        
        # Check 2: Tipo de descarte apropiado
        if discard_type == "archive_scientific_negative" and anthropic_prob < 0.3:
            print(f"✅ Check 2: Descarte científico apropiado (baja prob + alta certeza)", flush=True)
            checks_passed += 1
        elif discard_type == "none" and anthropic_prob >= 0.5:
            print(f"✅ Check 2: No es descarte (candidato positivo)", flush=True)
            checks_passed += 1
        else:
            print(f"⚠️ Check 2: Tipo de descarte: {discard_type}", flush=True)
        
        # Check 3: Confianza científica coherente
        if scientific_confidence in ["high", "medium_high"] and anthropic_prob < 0.3:
            print(f"✅ Check 3: Alta confianza científica coherente con baja probabilidad", flush=True)
            checks_passed += 1
        elif scientific_confidence == "low" and anthropic_prob > 0.4:
            print(f"✅ Check 3: Baja confianza coherente con probabilidad media", flush=True)
            checks_passed += 1
        else:
            print(f"⚠️ Check 3: Confianza científica: {scientific_confidence}", flush=True)
        
        print(f"\n{'='*80}", flush=True)
        print(f"RESULTADO: {checks_passed}/{checks_total} checks pasados", flush=True)
        print(f"{'='*80}", flush=True)
        
        if checks_passed == checks_total:
            print(f"\n✅ [SUCCESS] Todos los ajustes finos funcionan correctamente", flush=True)
        else:
            print(f"\n⚠️ [PARTIAL] {checks_passed}/{checks_total} ajustes verificados", flush=True)
        
    except Exception as e:
        print(f"\n[ERROR] Error en test: {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(test_ajustes_finos())
