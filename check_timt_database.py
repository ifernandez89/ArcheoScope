#!/usr/bin/env python3
"""
Verificar qué se guardó en las tablas TIMT.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_timt_data():
    """Verificar datos en tablas TIMT."""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL no configurada")
        return
    
    try:
        pool = await asyncpg.create_pool(database_url)
        
        async with pool.acquire() as conn:
            
            # 1. Verificar timt_analyses
            print("\n" + "="*80)
            print("📊 TIMT ANALYSES")
            print("="*80)
            
            timt_analyses = await conn.fetch("""
                SELECT id, analysis_id, region_name, 
                       territorial_coherence_score, scientific_rigor_score,
                       analysis_timestamp
                FROM timt_analyses
                ORDER BY analysis_timestamp DESC
                LIMIT 5
            """)
            
            if timt_analyses:
                for row in timt_analyses:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   Analysis ID: {row['analysis_id']}")
                    print(f"   Region: {row['region_name']}")
                    print(f"   Coherencia: {row['territorial_coherence_score']:.3f}")
                    print(f"   Rigor: {row['scientific_rigor_score']:.3f}")
                    print(f"   Timestamp: {row['analysis_timestamp']}")
            else:
                print("⚠️ No hay análisis TIMT guardados")
            
            # 2. Verificar tcp_profiles
            print("\n" + "="*80)
            print("🧩 TCP PROFILES")
            print("="*80)
            
            tcp_profiles = await conn.fetch("""
                SELECT id, timt_analysis_id, tcp_id, 
                       dominant_lithology, preservation_potential
                FROM tcp_profiles
                ORDER BY id DESC
                LIMIT 5
            """)
            
            if tcp_profiles:
                for row in tcp_profiles:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   TIMT Analysis ID: {row['timt_analysis_id']}")
                    print(f"   TCP ID: {row['tcp_id']}")
                    print(f"   Litología: {row['dominant_lithology']}")
                    print(f"   Preservación: {row['preservation_potential']}")
            else:
                print("⚠️ No hay TCP profiles guardados")
            
            # 3. Verificar etp_profiles
            print("\n" + "="*80)
            print("🔬 ETP PROFILES")
            print("="*80)
            
            etp_profiles = await conn.fetch("""
                SELECT id, timt_analysis_id, territory_id,
                       ess_superficial, ess_volumetrico, coherencia_3d,
                       confidence_level, recommended_action
                FROM etp_profiles
                ORDER BY id DESC
                LIMIT 5
            """)
            
            if etp_profiles:
                for row in etp_profiles:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   TIMT Analysis ID: {row['timt_analysis_id']}")
                    print(f"   Territory ID: {row['territory_id']}")
                    print(f"   ESS Superficial: {row['ess_superficial']:.3f}")
                    print(f"   ESS Volumétrico: {row['ess_volumetrico']:.3f}")
                    print(f"   Coherencia 3D: {row['coherencia_3d']:.3f}")
                    print(f"   Confianza: {row['confidence_level']}")
                    print(f"   Acción: {row['recommended_action']}")
            else:
                print("⚠️ No hay ETP profiles guardados")
            
            # 4. Verificar territorial_hypotheses
            print("\n" + "="*80)
            print("💡 TERRITORIAL HYPOTHESES")
            print("="*80)
            
            hypotheses = await conn.fetch("""
                SELECT id, tcp_profile_id, hypothesis_type,
                       plausibility_score, validation_status
                FROM territorial_hypotheses
                ORDER BY id DESC
                LIMIT 5
            """)
            
            if hypotheses:
                for row in hypotheses:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   TCP Profile ID: {row['tcp_profile_id']}")
                    print(f"   Tipo: {row['hypothesis_type']}")
                    print(f"   Plausibilidad: {row['plausibility_score']:.3f}")
                    print(f"   Estado: {row['validation_status']}")
            else:
                print("⚠️ No hay hipótesis guardadas")
            
            # 5. Verificar transparency_reports
            print("\n" + "="*80)
            print("📋 TRANSPARENCY REPORTS")
            print("="*80)
            
            reports = await conn.fetch("""
                SELECT id, timt_analysis_id, hypotheses_evaluated,
                       hypotheses_validated, hypotheses_rejected
                FROM transparency_reports
                ORDER BY id DESC
                LIMIT 5
            """)
            
            if reports:
                for row in reports:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   TIMT Analysis ID: {row['timt_analysis_id']}")
                    print(f"   Hipótesis evaluadas: {row['hypotheses_evaluated']}")
                    print(f"   Validadas: {row['hypotheses_validated']}")
                    print(f"   Rechazadas: {row['hypotheses_rejected']}")
            else:
                print("⚠️ No hay reportes de transparencia guardados")
            
            # 6. Comparar con tabla antigua analyses
            print("\n" + "="*80)
            print("📊 COMPARACIÓN CON TABLA ANTIGUA (analyses)")
            print("="*80)
            
            old_analyses = await conn.fetch("""
                SELECT id, candidate_name, region, 
                       archaeological_probability, anomaly_score,
                       created_at
                FROM analyses
                ORDER BY created_at DESC
                LIMIT 5
            """)
            
            if old_analyses:
                for row in old_analyses:
                    print(f"\n✅ ID: {row['id']}")
                    print(f"   Candidato: {row['candidate_name']}")
                    print(f"   Región: {row['region']}")
                    print(f"   Prob. Arqueológica: {row['archaeological_probability']:.3f}")
                    print(f"   Anomaly Score: {row['anomaly_score']:.3f}")
                    print(f"   Creado: {row['created_at']}")
            
            print("\n" + "="*80)
            print("✅ Verificación completada")
            print("="*80)
        
        await pool.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_timt_data())
