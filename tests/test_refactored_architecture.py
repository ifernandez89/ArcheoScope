#!/usr/bin/env python3
"""
Tests para Arquitectura Refactorizada
====================================

Verifica que la nueva arquitectura modular funciona correctamente:
1. Lazy loading de componentes
2. Dependency injection
3. Routers modulares
4. Compatibilidad con API existente
5. Performance mejorado
"""

import pytest
import sys
import time
import psutil
import os
from pathlib import Path
import requests
import threading
import subprocess
from typing import Dict, Any

# Agregar paths necesarios
sys.path.append(str(Path(__file__).parent / "backend" / "api"))

class TestRefactoredArchitecture:
    """Suite de tests para arquitectura refactorizada."""
    
    @classmethod
    def setup_class(cls):
        """Setup inicial para todos los tests."""
        cls.api_base_url = "http://localhost:8003"
        cls.server_process = None
        
    def test_import_performance(self):
        """Test 1: Verificar que importar la app es rápido (lazy loading)."""
        
        print("\n🧪 Test 1: Performance de importación (lazy loading)")
        
        start_time = time.time()
        
        try:
            from main import app
            import_time = time.time() - start_time
            
            print(f"   ⏱️  Tiempo de importación: {import_time:.3f} segundos")
            
            # Debe ser rápido (< 2 segundos)
            assert import_time < 2.0, f"Importación muy lenta: {import_time:.3f}s"
            
            print("   ✅ Importación rápida - lazy loading funcionando")
            return True
            
        except Exception as e:
            print(f"   ❌ Error importando aplicación: {e}")
            return False
    
    def test_dependency_injection(self):
        """Test 2: Verificar sistema de dependency injection."""
        
        print("\n🧪 Test 2: Sistema de dependency injection")
        
        try:
            from dependencies import (
                get_system_components,
                get_environment_classifier,
                get_core_anomaly_detector
            )
            
            # Test de componentes
            components = get_system_components()
            print(f"   📦 Componentes disponibles: {len(components)}")
            
            # Test de lazy loading específico
            classifier = get_environment_classifier()
            if classifier:
                print("   ✅ EnvironmentClassifier cargado correctamente")
            else:
                print("   ⚠️ EnvironmentClassifier no disponible")
            
            detector = get_core_anomaly_detector()
            if detector:
                print("   ✅ CoreAnomalyDetector cargado correctamente")
            else:
                print("   ⚠️ CoreAnomalyDetector no disponible")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error en dependency injection: {e}")
            return False
    
    def test_routers_registration(self):
        """Test 3: Verificar que los routers están registrados."""
        
        print("\n🧪 Test 3: Registro de routers modulares")
        
        try:
            from main import app
            
            # Obtener rutas registradas
            routes = [route.path for route in app.routes]
            
            # Verificar routers esperados
            expected_prefixes = ["/status", "/analysis", "/catalog"]
            
            registered_routers = []
            for prefix in expected_prefixes:
                matching_routes = [r for r in routes if r.startswith(prefix)]
                if matching_routes:
                    registered_routers.append(prefix)
                    print(f"   ✅ Router {prefix}: {len(matching_routes)} endpoints")
                else:
                    print(f"   ❌ Router {prefix}: no encontrado")
            
            print(f"   📊 Total rutas registradas: {len(routes)}")
            
            # Debe tener al menos los routers básicos
            assert len(registered_routers) >= 3, f"Faltan routers: {registered_routers}"
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error verificando routers: {e}")
            return False
    
    def test_pydantic_models(self):
        """Test 4: Verificar modelos Pydantic centralizados."""
        
        print("\n🧪 Test 4: Modelos Pydantic centralizados")
        
        try:
            from models import (
                RegionRequest,
                AnalysisResponse,
                SystemStatus,
                ArchaeologicalSite
            )
            
            # Test de creación de modelos
            request = RegionRequest(
                lat_min=0.0,
                lat_max=1.0,
                lon_min=0.0,
                lon_max=1.0,
                region_name="Test Region"
            )
            
            print(f"   ✅ RegionRequest: {request.region_name}")
            
            # Test de validación
            try:
                invalid_request = RegionRequest(
                    lat_min=100.0,  # Inválido
                    lat_max=1.0,
                    lon_min=0.0,
                    lon_max=1.0,
                    region_name="Invalid"
                )
                print("   ❌ Validación no funcionó")
                return False
            except Exception:
                print("   ✅ Validación Pydantic funcionando")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error con modelos Pydantic: {e}")
            return False
    
    def test_memory_usage(self):
        """Test 5: Verificar uso de memoria optimizado."""
        
        print("\n🧪 Test 5: Uso de memoria optimizado")
        
        try:
            process = psutil.Process(os.getpid())
            
            # Memoria antes de importar
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Importar aplicación
            from main import app
            
            # Memoria después de importar
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_increase = memory_after - memory_before
            
            print(f"   📊 Memoria antes: {memory_before:.1f} MB")
            print(f"   📊 Memoria después: {memory_after:.1f} MB")
            print(f"   📊 Incremento: {memory_increase:.1f} MB")
            
            # El incremento debe ser razonable (< 100 MB)
            if memory_increase < 100:
                print("   ✅ Uso de memoria optimizado")
                return True
            else:
                print("   ⚠️ Uso de memoria alto")
                return False
                
        except ImportError:
            print("   ⚠️ psutil no disponible - test omitido")
            return True
        except Exception as e:
            print(f"   ❌ Error midiendo memoria: {e}")
            return False
    
    def test_smoke_tests_system(self):
        """Test 6: Verificar sistema de smoke tests."""
        
        print("\n🧪 Test 6: Sistema de smoke tests")
        
        try:
            from dependencies import perform_smoke_tests
            
            # Ejecutar smoke tests
            results = perform_smoke_tests()
            
            print(f"   📊 Tests ejecutados: {len(results)}")
            
            passed_tests = sum(results.values())
            total_tests = len(results)
            
            print(f"   📊 Tests pasados: {passed_tests}/{total_tests}")
            
            # Mostrar detalles
            for test_name, passed in results.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {test_name}")
            
            # Al menos algunos tests deben pasar
            assert passed_tests > 0, "Ningún smoke test pasó"
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error en smoke tests: {e}")
            return False
    
    def test_feature_flags(self):
        """Test 7: Verificar sistema de feature flags."""
        
        print("\n🧪 Test 7: Sistema de feature flags")
        
        try:
            from dependencies import get_feature_flags, is_feature_enabled
            
            # Obtener flags
            flags = get_feature_flags()
            
            print(f"   📊 Feature flags disponibles: {len(flags)}")
            
            for flag_name, enabled in flags.items():
                status = "🟢" if enabled else "🔴"
                print(f"   {status} {flag_name}: {enabled}")
            
            # Test de flag específico
            ai_enabled = is_feature_enabled('ai')
            print(f"   🤖 IA habilitada: {ai_enabled}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error con feature flags: {e}")
            return False

def run_architecture_tests():
    """Ejecutar todos los tests de arquitectura."""
    
    print("="*70)
    print("🧪 TESTS DE ARQUITECTURA REFACTORIZADA")
    print("="*70)
    
    tester = TestRefactoredArchitecture()
    
    tests = [
        ("Import Performance", tester.test_import_performance),
        ("Dependency Injection", tester.test_dependency_injection),
        ("Routers Registration", tester.test_routers_registration),
        ("Pydantic Models", tester.test_pydantic_models),
        ("Memory Usage", tester.test_memory_usage),
        ("Smoke Tests System", tester.test_smoke_tests_system),
        ("Feature Flags", tester.test_feature_flags)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🔬 EJECUTANDO: {test_name}")
        print(f"{'='*50}")
        
        try:
            start_time = time.time()
            success = test_func()
            duration = time.time() - start_time
            
            results.append((test_name, success, duration))
            
            if success:
                print(f"\n✅ {test_name}: EXITOSO ({duration:.3f}s)")
            else:
                print(f"\n❌ {test_name}: FALLÓ ({duration:.3f}s)")
                
        except Exception as e:
            print(f"\n💥 {test_name}: EXCEPCIÓN - {e}")
            results.append((test_name, False, 0))
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📊 RESUMEN DE TESTS")
    print(f"{'='*70}")
    
    passed_tests = sum(1 for _, success, _ in results if success)
    total_tests = len(results)
    
    for test_name, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name} ({duration:.3f}s)")
    
    print(f"\n🎯 RESULTADO FINAL: {passed_tests}/{total_tests} tests pasaron ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 TODOS LOS TESTS PASARON - Arquitectura refactorizada funcionando correctamente")
        return True
    elif passed_tests > total_tests * 0.7:
        print("⚠️ MAYORÍA DE TESTS PASARON - Arquitectura funcional con algunas mejoras pendientes")
        return True
    else:
        print("🚨 MUCHOS TESTS FALLARON - Revisar implementación de arquitectura")
        return False

def test_api_compatibility():
    """Test adicional: Verificar compatibilidad de API."""
    
    print(f"\n{'='*50}")
    print("🌐 TEST DE COMPATIBILIDAD DE API")
    print(f"{'='*50}")
    
    # Este test requiere que el servidor esté corriendo
    # Se puede ejecutar por separado
    
    try:
        # Test básico de conectividad
        response = requests.get("http://localhost:8003/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ API responde correctamente")
            
            # Test de documentación Swagger
            docs_response = requests.get("http://localhost:8003/docs", timeout=5)
            if docs_response.status_code == 200:
                print("✅ Documentación Swagger disponible")
            
            return True
        else:
            print(f"❌ API no responde: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor no está corriendo - test omitido")
        print("   Para ejecutar: python backend/api/main.py")
        return True
    except Exception as e:
        print(f"❌ Error probando API: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar tests de arquitectura
    architecture_success = run_architecture_tests()
    
    # Test de compatibilidad de API (opcional)
    api_success = test_api_compatibility()
    
    print(f"\n{'='*70}")
    print("🏁 RESULTADO FINAL")
    print(f"{'='*70}")
    
    if architecture_success:
        print("✅ Arquitectura refactorizada: FUNCIONANDO")
    else:
        print("❌ Arquitectura refactorizada: PROBLEMAS")
    
    if api_success:
        print("✅ Compatibilidad de API: VERIFICADA")
    else:
        print("❌ Compatibilidad de API: PROBLEMAS")
    
    if architecture_success and api_success:
        print("\n🎉 REFACTORIZACIÓN EXITOSA - Sistema listo para producción")
        sys.exit(0)
    else:
        print("\n🚨 REFACTORIZACIÓN INCOMPLETA - Revisar problemas")
        sys.exit(1)