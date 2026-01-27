#!/usr/bin/env python3
"""
Verificación de Entorno para Ejecución en Casa
==============================================

Script para verificar que todo esté listo para ejecutar
la captura de 5 candidatos estratégicos en casa.

Verifica:
- Dependencias de Python
- Conexión a PostgreSQL
- Credenciales de instrumentos satelitales
- Integrador robusto V2
- Espacio en disco
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def check_python_dependencies():
    """Verificar dependencias de Python."""
    print("🔍 Verificando dependencias de Python...")
    
    required_modules = [
        ('psycopg2', 'PostgreSQL connector'),
        ('numpy', 'Numerical computing'),
        ('pandas', 'Data analysis (opcional)'),
        ('asyncio', 'Async support'),
        ('dotenv', 'Environment variables')
    ]
    
    missing_modules = []
    
    for module, description in required_modules:
        try:
            if module == 'psycopg2':
                import psycopg2
            elif module == 'numpy':
                import numpy
            elif module == 'pandas':
                import pandas
            elif module == 'asyncio':
                import asyncio
            elif module == 'dotenv':
                from dotenv import load_dotenv
            
            print(f"   ✅ {module}: OK ({description})")
            
        except ImportError:
            print(f"   ❌ {module}: MISSING ({description})")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ Instalar módulos faltantes:")
        for module in missing_modules:
            if module == 'psycopg2':
                print(f"   pip install psycopg2-binary")
            else:
                print(f"   pip install {module}")
        return False
    
    return True

def check_backend_modules():
    """Verificar módulos del backend de ArcheoScope."""
    print("\n🔍 Verificando módulos del backend...")
    
    # Agregar backend al path
    backend_path = Path(__file__).parent / 'backend'
    if backend_path.exists():
        sys.path.insert(0, str(backend_path))
    
    backend_modules = [
        ('satellite_connectors.real_data_integrator_v2', 'RealDataIntegratorV2 - Sistema Robusto'),
        ('data_sanitizer', 'Sanitizador global inf/nan'),
        ('instrument_status', 'Estados explícitos por instrumento'),
        ('credentials_manager', 'Gestor de credenciales cifradas')
    ]
    
    missing_backend = []
    
    for module_path, description in backend_modules:
        try:
            if module_path == 'satellite_connectors.real_data_integrator_v2':
                from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
            elif module_path == 'data_sanitizer':
                from data_sanitizer import sanitize_response
            elif module_path == 'instrument_status':
                from instrument_status import InstrumentResult
            elif module_path == 'credentials_manager':
                from credentials_manager import CredentialsManager
            
            print(f"   ✅ {module_path}: OK ({description})")
            
        except ImportError as e:
            print(f"   ❌ {module_path}: MISSING ({description}) - {e}")
            missing_backend.append(module_path)
    
    if missing_backend:
        print(f"\n⚠️ Módulos del backend faltantes. Verificar estructura de archivos.")
        return False
    
    return True

def check_database_connection():
    """Verificar conexión a PostgreSQL."""
    print("\n🔍 Verificando conexión a PostgreSQL...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv("DATABASE_URL")
        
        if not db_url:
            print("   ❌ DATABASE_URL no configurada en .env")
            return False
        
        print(f"   📍 DATABASE_URL configurada")
        
        # Intentar conexión
        import psycopg2
        conn = psycopg2.connect(db_url)
        
        # Verificar tablas necesarias
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('analysis_candidates', 'raw_measurements');
            """)
            
            tables = [row[0] for row in cur.fetchall()]
            
            if 'analysis_candidates' in tables and 'raw_measurements' in tables:
                print("   ✅ PostgreSQL: Conexión OK, tablas existentes")
            else:
                print("   ⚠️ PostgreSQL: Conexión OK, pero faltan tablas")
                print("      Ejecutar: python setup_database_quick.py")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ PostgreSQL: Error de conexión - {e}")
        return False

def check_instrument_credentials():
    """Verificar credenciales de instrumentos satelitales."""
    print("\n🔍 Verificando credenciales de instrumentos...")
    
    try:
        from credentials_manager import CredentialsManager
        
        creds_manager = CredentialsManager()
        
        # Credenciales esperadas
        expected_credentials = [
            ('earthdata', 'ICESat-2, NSIDC'),
            ('planetary_computer', 'Sentinel-1/2, Landsat (opcional)'),
            ('copernicus_marine', 'SST, hielo marino'),
            ('modis_lst', 'MODIS térmico')
        ]
        
        available_creds = []
        missing_creds = []
        
        for service, description in expected_credentials:
            try:
                username = creds_manager.get_credential(service, "username")
                password = creds_manager.get_credential(service, "password")
                
                if username and password:
                    print(f"   ✅ {service}: OK ({description})")
                    available_creds.append(service)
                else:
                    print(f"   ❌ {service}: MISSING ({description})")
                    missing_creds.append(service)
                    
            except Exception as e:
                print(f"   ❌ {service}: ERROR ({description}) - {e}")
                missing_creds.append(service)
        
        if missing_creds:
            print(f"\n⚠️ Configurar credenciales faltantes:")
            print(f"   python backend/credentials_manager.py")
            return len(available_creds) >= 2  # Mínimo 2 servicios
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando credenciales: {e}")
        return False

def check_disk_space():
    """Verificar espacio en disco disponible."""
    print("\n🔍 Verificando espacio en disco...")
    
    try:
        import shutil
        
        # Verificar espacio en directorio actual
        total, used, free = shutil.disk_usage('.')
        
        free_gb = free / (1024**3)
        
        print(f"   💾 Espacio libre: {free_gb:.1f} GB")
        
        if free_gb >= 5.0:
            print("   ✅ Espacio suficiente (>5GB)")
            return True
        elif free_gb >= 1.0:
            print("   ⚠️ Espacio limitado (1-5GB) - suficiente para test")
            return True
        else:
            print("   ❌ Espacio insuficiente (<1GB)")
            return False
            
    except Exception as e:
        print(f"   ⚠️ No se pudo verificar espacio: {e}")
        return True  # No es crítico

def check_integrator_v2():
    """Verificar que el integrador V2 esté funcional."""
    print("\n🔍 Verificando RealDataIntegratorV2...")
    
    try:
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        
        # Intentar inicializar
        integrator = RealDataIntegratorV2()
        
        # Verificar estado de APIs
        status = integrator.get_availability_status()
        
        available_apis = status['_summary']['available_apis']
        total_apis = status['_summary']['total_apis']
        availability_rate = status['_summary']['availability_rate']
        
        print(f"   📊 APIs disponibles: {available_apis}/{total_apis} ({availability_rate:.1%})")
        
        for api_name, api_status in status.items():
            if api_name.startswith('_'):
                continue
            
            status_icon = "✅" if api_status['available'] else "❌"
            print(f"   {status_icon} {api_name}: {api_status['status']}")
        
        if availability_rate >= 0.5:
            print("   ✅ Integrador V2: Funcional")
            return True
        else:
            print("   ⚠️ Integrador V2: Funcionalidad limitada")
            return False
            
    except Exception as e:
        print(f"   ❌ Error inicializando integrador V2: {e}")
        return False

def generate_verification_report(results):
    """Generar reporte de verificación."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'verificacion_entorno_{timestamp}.json'
    
    report = {
        "verification_timestamp": datetime.now().isoformat(),
        "verification_results": results,
        "overall_status": "READY" if all(results.values()) else "ISSUES",
        "ready_for_execution": all(results.values()),
        "critical_issues": [key for key, value in results.items() if not value],
        "recommendations": []
    }
    
    # Generar recomendaciones
    if not results.get('python_dependencies', True):
        report["recommendations"].append("Instalar dependencias de Python faltantes")
    
    if not results.get('backend_modules', True):
        report["recommendations"].append("Verificar estructura de archivos del backend")
    
    if not results.get('database_connection', True):
        report["recommendations"].append("Configurar conexión a PostgreSQL")
    
    if not results.get('instrument_credentials', True):
        report["recommendations"].append("Configurar credenciales de instrumentos satelitales")
    
    if not results.get('integrator_v2', True):
        report["recommendations"].append("Verificar configuración del integrador V2")
    
    # Guardar reporte
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📁 Reporte guardado: {report_file}")
        
    except Exception as e:
        print(f"\n⚠️ No se pudo guardar reporte: {e}")
    
    return report

def main():
    """Función principal de verificación."""
    
    print("🚀 ArcheoScope - Verificación de Entorno para Ejecución en Casa")
    print("=" * 70)
    print("Verificando que todo esté listo para capturar 5 candidatos estratégicos")
    print("=" * 70)
    
    # Ejecutar verificaciones
    results = {
        'python_dependencies': check_python_dependencies(),
        'backend_modules': check_backend_modules(),
        'database_connection': check_database_connection(),
        'instrument_credentials': check_instrument_credentials(),
        'disk_space': check_disk_space(),
        'integrator_v2': check_integrator_v2()
    }
    
    # Generar reporte
    report = generate_verification_report(results)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    
    for check_name, result in results.items():
        status = "✅ OK" if result else "❌ ISSUE"
        check_display = check_name.replace('_', ' ').title()
        print(f"{check_display:25} {status}")
    
    print(f"\nEstado General: {report['overall_status']}")
    print(f"Listo para Ejecución: {'✅ SÍ' if report['ready_for_execution'] else '❌ NO'}")
    
    if report['critical_issues']:
        print(f"\n⚠️ PROBLEMAS CRÍTICOS:")
        for issue in report['critical_issues']:
            print(f"   • {issue.replace('_', ' ').title()}")
    
    if report['recommendations']:
        print(f"\n💡 RECOMENDACIONES:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
    
    if report['ready_for_execution']:
        print(f"\n🎉 ¡ENTORNO LISTO!")
        print(f"Puedes ejecutar:")
        print(f"   python test_5_candidatos_estrategicos.py")
        print(f"   python analyze_scientific_dataset.py")
    else:
        print(f"\n⚠️ ENTORNO NO LISTO")
        print(f"Resolver problemas antes de continuar")
    
    print("=" * 70)
    
    return report['ready_for_execution']

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Verificación interrumpida por usuario")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error en verificación: {e}")
        exit(1)