import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import json

async def verify_new_analysis():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    print(f"🔗 Conectando a: {database_url}")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Conexión exitosa")
        
        # Listar tablas relevantes de TIMT
        tables = ['timt_analyses', 'etp_profiles', 'archaeological_candidate_analyses']
        
        for table in tables:
            exists = await conn.fetchval(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
            if exists:
                count = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
                print(f"📊 Tabla '{table}': {count} registros")
                
                if count > 0:
                    # Mostrar el más reciente
                    recent = await conn.fetchrow(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1")
                    print(f"  🆕 Último en '{table}':")
                    if table == 'timt_analyses':
                        print(f"    - ID: {recent['analysis_id']}")
                        print(f"    - Región: {recent['region_name']}")
                        print(f"    - Timestamp: {recent['analysis_timestamp']}")
                    elif table == 'etp_profiles':
                        print(f"    - Territory ID: {recent['territory_id']}")
                        print(f"    - ESS Superficial: {recent['ess_superficial']}")
                        print(f"    - Coherencia 3D: {recent['coherencia_3d']}")
                    elif table == 'archaeological_candidate_analyses':
                        print(f"    - Candidate ID: {recent['candidate_id']}")
                        print(f"    - Region: {recent['region']}")
                        print(f"    - ESS Score: {recent['anomaly_score']}")
            else:
                print(f"❌ Tabla '{table}' no existe")
        
        await conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_new_analysis())
