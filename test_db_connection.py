#!/usr/bin/env python3
"""
Test database connection
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

from database import db

async def test_connection():
    """Test database connection"""
    try:
        print("🔍 Conectando a PostgreSQL...")
        await db.connect()
        print("✅ Conexión establecida")
        
        print("\n🔍 Contando sitios...")
        count = await db.count_sites()
        print(f"✅ Total de sitios: {count:,}")
        
        print("\n🔍 Obteniendo sitios de referencia...")
        ref_sites = await db.get_reference_sites()
        print(f"✅ Sitios de referencia: {len(ref_sites)}")
        
        if ref_sites:
            print("\nPrimeros 3 sitios de referencia:")
            for site in ref_sites[:3]:
                print(f"  - {site.get('name', 'N/A')} ({site.get('country', 'N/A')})")
        
        print("\n🔍 Cerrando conexión...")
        await db.close()
        print("✅ Conexión cerrada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
