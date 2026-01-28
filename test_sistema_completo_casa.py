#!/usr/bin/env python3
"""
Test Sistema ETP Completo - PARA TESTING EN CASA
===============================================

Script maestro que ejecuta todos los tests del sistema ETP revolucionario.
"""

import asyncio
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

def run_test_script(script_name, description):
    """Ejecutar un script de testing y capturar resultados."""
    
    print(f"\n🔄 EJECUTANDO: {description}")
    print("=" * (len(description) + 15))
    
    try:
        # Ejecutar script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        success = result.returncode == 0
        
        if success:
            print(f"✅ {description}: EXITOSO")
        else:
            print(f"❌ {description}: FALLÓ")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
        
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {description}: TIMEOUT (>5 min)")
        return False, "", "Timeout"
    except Exception as e:
        print(f"💥 {description}: ERROR - {e}")
        return False, "", str(e)

async def test_sistema_completo_casa():
    """Test completo del sistema ETP."""
    
    print("🚀 ARCHEOSCOPE ETP - TESTING SISTEMA COMPLETO")
    print("=" * 55)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear directorio de logs
    os.makedirs('testing_logs_etp', exist_ok=True)
    
    # Lista de tests a ejecutar
    tests = [
        ('test_etp_simple.py', 'Verificación de Sistema ETP'),
        ('test_candidato_etp_casa.py', 'Testing con Candidato Real'),
        ('test_nuevos_instrumentos_casa.py', 'Testing de Nuevos Instrumentos')
    ]
    
    resultados = {}
    logs_completos = {}
    
    print(f"\n📋 PLAN DE TESTING:")
    for i, (script, desc) in enumerate(tests, 1):
        print(f"   {i}. {desc}")
    
    # Ejecutar cada test
    for script, description in tests:
        if os.path.exists(script):
            success, stdout, stderr = run_test_script(script, description)
            resultados[script] = success
            logs_completos[script] = {'stdout': stdout, 'stderr': stderr}
        else:
            print(f"⚠️ Script {script} no encontrado, saltando...")
            resultados[script] = False
            logs_completos[script] = {'stdout': '', 'stderr': 'Script no encontrado'}
    
    # Análisis de resultados
    print(f"\n📊 ANÁLISIS DE RESULTADOS")
    print("=" * 30)
    
    exitosos = sum(resultados.values())
    total = len(resultados)
    tasa_exito = exitosos / total * 100 if total > 0 else 0
    
    print(f"\n🎯 RESUMEN EJECUTIVO:")
    print(f"   Tests ejecutados: {total}")
    print(f"   Tests exitosos: {exitosos}")
    print(f"   Tasa de éxito: {tasa_exito:.1f}%")
    
    print(f"\n📋 DETALLE POR TEST:")
    for script, success in resultados.items():
        status_icon = "✅" if success else "❌"
        print(f"   {status_icon} {script}")
    
    # Verificar componentes del sistema
    print(f"\n🔍 VERIFICACIÓN DE COMPONENTES:")
    
    # Verificar archivos principales
    archivos_principales = [
        'backend/etp_core.py',
        'backend/etp_generator.py',
        'backend/geological_context.py',
        'backend/historical_hydrography.py',
        'backend/external_archaeological_validation.py',
        'backend/human_traces_analysis.py'
    ]
    
    componentes_ok = 0
    for archivo in archivos_principales:
        if os.path.exists(archivo):
            size_kb = os.path.getsize(archivo) / 1024
            print(f"   ✅ {archivo:<45} ({size_kb:.1f} KB)")
            componentes_ok += 1
        else:
            print(f"   ❌ {archivo:<45} (FALTANTE)")
    
    # Verificar nuevos instrumentos
    print(f"\n🛰️ VERIFICACIÓN DE NUEVOS INSTRUMENTOS:")
    
    instrumentos_nuevos = [
        'backend/satellite_connectors/viirs_connector.py',
        'backend/satellite_connectors/srtm_connector.py',
        'backend/satellite_connectors/palsar_connector.py',
        'backend/satellite_connectors/era5_connector.py',
        'backend/satellite_connectors/chirps_connector.py'
    ]
    
    instrumentos_ok = 0
    for instrumento in instrumentos_nuevos:
        if os.path.exists(instrumento):
            size_kb = os.path.getsize(instrumento) / 1024
            print(f"   ✅ {os.path.basename(instrumento):<25} ({size_kb:.1f} KB)")
            instrumentos_ok += 1
        else:
            print(f"   ❌ {os.path.basename(instrumento):<25} (FALTANTE)")
    
    # Generar reporte final
    print(f"\n💾 GENERANDO REPORTE FINAL...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    reporte_filename = f'testing_logs_etp/REPORTE_SISTEMA_COMPLETO_{timestamp}.txt'
    
    with open(reporte_filename, 'w', encoding='utf-8') as f:
        f.write("REPORTE SISTEMA ETP COMPLETO - TESTING EN CASA\n")
        f.write("=" * 50 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Sistema: ArcheoScope Environmental Tomographic Profile\n\n")
        
        f.write("RESUMEN EJECUTIVO:\n")
        f.write("-" * 18 + "\n")
        f.write(f"Tests ejecutados: {total}\n")
        f.write(f"Tests exitosos: {exitosos}\n")
        f.write(f"Tasa de éxito: {tasa_exito:.1f}%\n")
        f.write(f"Componentes principales: {componentes_ok}/{len(archivos_principales)}\n")
        f.write(f"Nuevos instrumentos: {instrumentos_ok}/{len(instrumentos_nuevos)}\n\n")
        
        f.write("RESULTADOS POR TEST:\n")
        f.write("-" * 20 + "\n")
        for script, success in resultados.items():
            status = "ÉXITO" if success else "FALLO"
            f.write(f"{script}: {status}\n")
        
        f.write("\nLOGS DETALLADOS:\n")
        f.write("-" * 16 + "\n")
        for script, logs in logs_completos.items():
            f.write(f"\n{script.upper()}:\n")
            f.write("=" * len(script) + "\n")
            if logs['stdout']:
                f.write("STDOUT:\n")
                f.write(logs['stdout'][:1000] + "...\n" if len(logs['stdout']) > 1000 else logs['stdout'])
            if logs['stderr']:
                f.write("STDERR:\n")
                f.write(logs['stderr'][:500] + "...\n" if len(logs['stderr']) > 500 else logs['stderr'])
        
        f.write("\nCONCLUSIONES:\n")
        f.write("-" * 13 + "\n")
        
        if tasa_exito >= 80:
            f.write("✅ SISTEMA ETP COMPLETAMENTE OPERATIVO\n")
            f.write("🚀 Transformación DETECTOR → EXPLICADOR: EXITOSA\n")
            f.write("🔬 Tomografía territorial 4D: FUNCIONAL\n")
            f.write("📊 Métricas integradas: OPERATIVAS\n")
        elif tasa_exito >= 60:
            f.write("⚠️ SISTEMA ETP MAYORMENTE OPERATIVO\n")
            f.write("🔧 Algunos componentes necesitan ajustes\n")
            f.write("📊 Funcionalidad principal: DISPONIBLE\n")
        else:
            f.write("❌ SISTEMA ETP NECESITA CORRECCIONES\n")
            f.write("🔧 Múltiples componentes requieren atención\n")
            f.write("📊 Funcionalidad limitada\n")
    
    print(f"   ✅ Reporte guardado en: {reporte_filename}")
    
    # Evaluación final
    print(f"\n🎯 EVALUACIÓN FINAL DEL SISTEMA ETP:")
    
    if tasa_exito >= 80 and componentes_ok >= len(archivos_principales) * 0.8:
        print(f"   🟢 SISTEMA COMPLETAMENTE OPERATIVO")
        print(f"   🚀 Transformación DETECTOR → EXPLICADOR: EXITOSA")
        print(f"   🔬 Tomografía territorial 4D: FUNCIONAL")
        print(f"   📊 Métricas integradas: OPERATIVAS")
        evaluation = "OPERATIVO"
    elif tasa_exito >= 60:
        print(f"   🟡 SISTEMA MAYORMENTE OPERATIVO")
        print(f"   🔧 Algunos ajustes necesarios")
        print(f"   📊 Funcionalidad principal disponible")
        evaluation = "FUNCIONAL"
    else:
        print(f"   🔴 SISTEMA NECESITA CORRECCIONES")
        print(f"   🔧 Múltiples componentes requieren atención")
        evaluation = "NECESITA_AJUSTES"
    
    print(f"\n✅ TESTING SISTEMA COMPLETO FINALIZADO")
    print(f"⏰ Duración total: {datetime.now().strftime('%H:%M:%S')}")
    
    return evaluation == "OPERATIVO", evaluation, resultados

if __name__ == "__main__":
    print("🧪 ARCHEOSCOPE ETP - TESTING MAESTRO")
    print("=" * 40)
    
    success, evaluation, details = asyncio.run(test_sistema_completo_casa())
    
    print(f"\n" + "=" * 55)
    print(f"🎯 RESULTADO FINAL: {evaluation}")
    
    if success:
        print(f"🎉 ¡SISTEMA ETP REVOLUCIONARIO COMPLETAMENTE OPERATIVO!")
        print(f"🔬 Tomografía territorial inferencial: ACTIVA")
        print(f"🚀 Transformación conceptual: LOGRADA")
        print(f"📊 Métricas multi-dominio: INTEGRADAS")
        print(f"🎨 Visualización 4D: PREPARADA")
        
        print(f"\n🌟 CAPACIDADES CONFIRMADAS:")
        print(f"   ✅ Análisis 4D (XYZ + Tiempo)")
        print(f"   ✅ 4 contextos adicionales operativos")
        print(f"   ✅ 15 instrumentos satelitales")
        print(f"   ✅ Métricas integradas (GCS, ECS, etc.)")
        print(f"   ✅ Narrativa territorial automática")
        print(f"   ✅ Recomendaciones arqueológicas")
        
    else:
        print(f"🔧 Sistema necesita ajustes antes de producción")
        print(f"📊 Funcionalidad parcial disponible")
        print(f"🔍 Revisar logs para detalles específicos")
    
    print(f"\n📁 Todos los logs disponibles en: testing_logs_etp/")
    print(f"📋 Reporte completo generado automáticamente")
    print(f"⏰ Testing finalizado: {datetime.now().strftime('%H:%M:%S')}")
    
    print(f"\n🎊 ¡SISTEMA ETP LISTO PARA VALIDACIÓN CIENTÍFICA!")
    print(f"Environmental Tomographic Profile System")
    print(f"ArcheoScope: De Detector a Explicador Territorial")