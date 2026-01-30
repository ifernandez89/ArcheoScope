#!/usr/bin/env python3
"""
Migración: Agregar columna scientific_output a timt_analyses
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def add_column():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("❌ DATABASE_URL no configurada")
        return

    try:
        pool = await asyncpg.create_pool(database_url)
        async with pool.acquire() as conn:
            # Verificar si la columna ya existe
            column_exists = await conn.fetchval("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'timt_analyses'
                    AND column_name = 'scientific_output'
                );
            """)

            if not column_exists:
                logger.info("🔧 Agregando columna scientific_output a timt_analyses...")
                await conn.execute("""
                    ALTER TABLE timt_analyses
                    ADD COLUMN scientific_output JSONB;
                """)
                logger.info("✅ Columna agregada exitosamente.")
            else:
                logger.info("ℹ️ La columna scientific_output ya existe.")

        await pool.close()

    except Exception as e:
        logger.error(f"❌ Error en migración: {e}")

if __name__ == "__main__":
    asyncio.run(add_column())
