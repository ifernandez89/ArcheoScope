#!/usr/bin/env python3
"""Verificar que los registros están en la BD."""

import asyncio
import asyncpg
import json


async def verify_records():
    """Verificar registros en detection_history."""
    
    try:
        conn = await asyncpg.connect(
            'postgresql://postgres:1464@localhost:5433/archeoscope_db'
        )
        print("✅ Conectado a BD")
        print()
        
        # Contar registros totales
        count = await conn.fetchval('SELECT COUNT(*) FROM detection_history')
        print(f"📊 Total registros en detection_history: {count}")
        print()
        
        # Obtener últimos 5 registros
        records = await conn.fetch("""
            SELECT 
                id,
                "regionName",
                "environmentDetected",
                "archaeologicalProbability",
                "confidenceLevel",
                "instrumentsConverging",
                "detectionDate"
            FROM detection_history
            ORDER BY "detectionDate" DESC
            LIMIT 5
        """)
        
        print("🔍 ÚLTIMOS 5 REGISTROS:")
        print("="*100)
        for i, rec in enumerate(records, 1):
            print(f"\n{i}. {rec['regionName']}")
            print(f"   ID: {rec['id']}")
            print(f"   Ambiente: {rec['environmentDetected']}")
            print(f"   Prob. Arqueológica: {rec['archaeologicalProbability']:.3f}")
            print(f"   Confianza: {rec['confidenceLevel']}")
            print(f"   Instrumentos: {rec['instrumentsConverging']}")
            print(f"   Fecha: {rec['detectionDate']}")
        
        print()
        print("="*100)
        
        # Verificar los dos específicos
        print()
        print("🎯 VERIFICANDO REGISTROS ESPECÍFICOS:")
        print()
        
        atacama_id = '109951be-919f-4c13-9f37-c4db914c70ba'
        altiplano_id = 'e028f0d2-c2e4-4072-a658-eb0b0d86ea14'
        
        atacama = await conn.fetchrow(
            'SELECT * FROM detection_history WHERE id = $1',
            atacama_id
        )
        
        if atacama:
            print("✅ ATACAMA INTERIOR encontrado:")
            print(f"   Región: {atacama['regionName']}")
            print(f"   ESS Vol: {atacama['archaeologicalProbability']:.3f}")
            print(f"   Ambiente: {atacama['environmentDetected']}")
            
            # Mostrar measurements
            measurements = json.loads(atacama['measurements'])
            print(f"   TAS Score: {measurements['tas']['tas_score']:.3f}")
            print(f"   Thermal Stability: {measurements['tas']['thermal_stability']:.3f}")
        else:
            print("❌ ATACAMA INTERIOR NO encontrado")
        
        print()
        
        altiplano = await conn.fetchrow(
            'SELECT * FROM detection_history WHERE id = $1',
            altiplano_id
        )
        
        if altiplano:
            print("✅ ALTIPLANO ANDINO encontrado:")
            print(f"   Región: {altiplano['regionName']}")
            print(f"   ESS Vol: {altiplano['archaeologicalProbability']:.3f}")
            print(f"   Ambiente: {altiplano['environmentDetected']}")
            
            # Mostrar measurements
            measurements = json.loads(altiplano['measurements'])
            print(f"   TAS Score: {measurements['tas']['tas_score']:.3f}")
            print(f"   Thermal Stability: {measurements['tas']['thermal_stability']:.3f}")
        else:
            print("❌ ALTIPLANO ANDINO NO encontrado")
        
        await conn.close()
        print()
        print("="*100)
        print("✅ VERIFICACIÓN COMPLETADA")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(verify_records())
