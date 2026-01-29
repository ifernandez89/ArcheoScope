"""
Migración: Agregar soporte para detección de subestructuras huecas
===================================================================

EJECUTAR EN CASA con PostgreSQL real:
python apply_void_detection_migration.py

Esta migración agrega columnas a timt_analysis_results para almacenar
resultados de detección de vacíos subsuperficiales.
"""

import os
import sys
from datetime import datetime

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def apply_migration():
    """Aplicar migración de BD para void detection"""
    
    print("=" * 80)
    print("MIGRACIÓN: Soporte para Detección de Subestructuras Huecas")
    print("=" * 80)
    print(f"Timestamp: {datetime.utcnow().isoformat()}\n")
    
    try:
        from database import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("✅ Conectado a PostgreSQL\n")
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'timt_analysis_results'
            )
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("⚠️ Tabla timt_analysis_results no existe. Creándola...\n")
            
            create_table_sql = """
            CREATE TABLE timt_analysis_results (
                id SERIAL PRIMARY KEY,
                lat DOUBLE PRECISION NOT NULL,
                lon DOUBLE PRECISION NOT NULL,
                analysis_type VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Índices geográficos
                CONSTRAINT unique_analysis UNIQUE (lat, lon, analysis_type, created_at)
            )
            """
            
            cursor.execute(create_table_sql)
            print("✅ Tabla timt_analysis_results creada\n")
        
        # Agregar columnas para void detection
        print("Agregando columnas para void detection...\n")
        
        columns_to_add = [
            ("void_probability_score", "DOUBLE PRECISION"),
            ("void_probability_level", "VARCHAR(50)"),
            ("void_classification", "VARCHAR(50)"),
            ("sar_score", "DOUBLE PRECISION"),
            ("thermal_score", "DOUBLE PRECISION"),
            ("humidity_score", "DOUBLE PRECISION"),
            ("subsidence_score", "DOUBLE PRECISION"),
            ("geometric_symmetry", "DOUBLE PRECISION"),
            ("scientific_conclusion", "TEXT"),
            ("confidence", "DOUBLE PRECISION"),
            ("is_stable_terrain", "BOOLEAN"),
            ("rejection_reason", "TEXT"),
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                alter_sql = f"""
                ALTER TABLE timt_analysis_results 
                ADD COLUMN IF NOT EXISTS {column_name} {column_type}
                """
                cursor.execute(alter_sql)
                print(f"  ✓ Columna '{column_name}' agregada")
            except Exception as e:
                print(f"  ⚠️ Columna '{column_name}': {e}")
        
        # Crear índices para búsquedas eficientes
        print("\nCreando índices...\n")
        
        indices = [
            ("idx_void_score", "void_probability_score"),
            ("idx_void_level", "void_probability_level"),
            ("idx_analysis_type", "analysis_type"),
            ("idx_coordinates", "lat, lon"),
        ]
        
        for index_name, columns in indices:
            try:
                create_index_sql = f"""
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON timt_analysis_results ({columns})
                """
                cursor.execute(create_index_sql)
                print(f"  ✓ Índice '{index_name}' creado")
            except Exception as e:
                print(f"  ⚠️ Índice '{index_name}': {e}")
        
        # Commit cambios
        conn.commit()
        
        print("\n" + "=" * 80)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        
        # Mostrar estructura final
        print("\nEstructura de tabla timt_analysis_results:")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'timt_analysis_results'
            ORDER BY ordinal_position
        """)
        
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("  1. Ejecutar: python test_void_detection_with_db.py --lat 30.0 --lon 31.0")
        print("  2. Verificar resultados en BD")
        print("  3. Integrar con pipeline principal\n")
        
        return 0
        
    except ImportError:
        print("❌ Error: No se pudo importar database module")
        print("\nVerifica que:")
        print("  1. El archivo backend/database.py exista")
        print("  2. Las credenciales de BD estén en .env")
        print("  3. PostgreSQL esté corriendo\n")
        return 1
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(apply_migration())
