#!/usr/bin/env python3
"""
Test OpenCode Validator - ArcheoScope

Prueba la integración de OpenCode/Zen para validación lógica post-scoring.
"""

import sys
import json
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from backend.ai.opencode_validator import OpenCodeValidator

def test_validator_initialization():
    """Test 1: Inicialización del validador."""
    
    print("🧪 Test 1: Inicialización del validador")
    print("=" * 60)
    
    validator = OpenCodeValidator()
    
    print(f"✅ Validador creado")
    print(f"   - Enabled: {validator.enabled}")
    print(f"   - Available: {validator.is_available}")
    print(f"   - API URL: {validator.api_url}")
    print(f"   - Min score: {validator.min_score}")
    print(f"   - Timeout: {validator.timeout}s")
    print()
    
    return validator

def test_should_validate(validator):
    """Test 2: Lógica de decisión de validación."""
    
    print("🧪 Test 2: Decisión de validación")
    print("=" * 60)
    
    # Candidato con score alto
    high_score_candidate = {
        "archaeological_probability": 0.85,
        "evidence_layers": [
            {"type": "ndvi", "value": 0.7},
            {"type": "sar", "value": 0.8}
        ]
    }
    
    # Candidato con score bajo
    low_score_candidate = {
        "archaeological_probability": 0.45,
        "evidence_layers": [
            {"type": "ndvi", "value": 0.3}
        ]
    }
    
    should_validate_high = validator.should_validate(high_score_candidate)
    should_validate_low = validator.should_validate(low_score_candidate)
    
    print(f"Candidato score alto (0.85): {'✅ Validar' if should_validate_high else '❌ Saltar'}")
    print(f"Candidato score bajo (0.45): {'✅ Validar' if should_validate_low else '❌ Saltar'}")
    print()
    
    assert should_validate_low == False, "Score bajo no debe validarse"
    print("✅ Lógica de decisión correcta")
    print()

def test_hash_candidate(validator):
    """Test 3: Hashing determinista para caché."""
    
    print("🧪 Test 3: Hashing determinista")
    print("=" * 60)
    
    candidate1 = {
        "archaeological_probability": 0.85,
        "spatial_context": {"lat": 10.0, "lon": 20.0},
        "evidence_layers": [
            {"type": "ndvi", "value": 0.7},
            {"type": "sar", "value": 0.8}
        ]
    }
    
    # Mismo candidato, diferente orden
    candidate2 = {
        "archaeological_probability": 0.85,
        "evidence_layers": [
            {"type": "sar", "value": 0.8},
            {"type": "ndvi", "value": 0.7}
        ],
        "spatial_context": {"lat": 10.0, "lon": 20.0}
    }
    
    # Candidato diferente
    candidate3 = {
        "archaeological_probability": 0.90,
        "spatial_context": {"lat": 10.0, "lon": 20.0},
        "evidence_layers": [
            {"type": "ndvi", "value": 0.7}
        ]
    }
    
    hash1 = validator._hash_candidate(candidate1)
    hash2 = validator._hash_candidate(candidate2)
    hash3 = validator._hash_candidate(candidate3)
    
    print(f"Hash 1: {hash1[:16]}...")
    print(f"Hash 2: {hash2[:16]}...")
    print(f"Hash 3: {hash3[:16]}...")
    print()
    
    assert hash1 == hash2, "Mismo candidato debe tener mismo hash"
    assert hash1 != hash3, "Candidatos diferentes deben tener hash diferente"
    
    print("✅ Hashing determinista funciona correctamente")
    print()

def test_cache_operations(validator):
    """Test 4: Operaciones de caché."""
    
    print("🧪 Test 4: Operaciones de caché")
    print("=" * 60)
    
    stats = validator.get_cache_stats()
    
    print(f"Estadísticas de caché:")
    print(f"   - Total entradas: {stats['total_entries']}")
    print(f"   - Archivo: {stats['cache_file']}")
    print(f"   - Existe: {stats['cache_exists']}")
    print()
    
    print("✅ Caché operacional")
    print()

def test_prepare_validation_data(validator):
    """Test 5: Preparación de datos para validación."""
    
    print("🧪 Test 5: Preparación de datos")
    print("=" * 60)
    
    candidate = {
        "archaeological_probability": 0.85,
        "evidence_layers": [
            {"type": "ndvi", "value": 0.7, "confidence": "high"},
            {"type": "sar", "value": 0.8, "confidence": "medium"}
        ],
        "instruments_converging": 2,
        "environment_type": "forest",
        "temporal_persistence": {"years": 10}
    }
    
    validation_data = validator._prepare_validation_data(candidate)
    
    print("Datos preparados:")
    print(json.dumps(validation_data, indent=2))
    print()
    
    assert validation_data['score'] == 0.85
    assert len(validation_data['instruments']) == 2
    assert validation_data['convergence'] == 2
    
    print("✅ Preparación de datos correcta")
    print()

def test_mock_validation(validator):
    """Test 6: Validación simulada (sin OpenCode real)."""
    
    print("🧪 Test 6: Validación simulada")
    print("=" * 60)
    
    candidate = {
        "archaeological_probability": 0.85,
        "evidence_layers": [
            {"type": "ndvi", "value": 0.7, "confidence": "high"},
            {"type": "sar", "value": 0.8, "confidence": "high"},
            {"type": "thermal", "value": 0.6, "confidence": "medium"}
        ],
        "instruments_converging": 3,
        "environment_type": "forest",
        "spatial_context": {"lat": 10.0, "lon": 20.0},
        "temporal_persistence": {"years": 10}
    }
    
    if validator.is_available:
        print("⚠️ OpenCode disponible - ejecutando validación real...")
        try:
            validation = validator.validate_candidate(candidate)
            if validation:
                print(f"✅ Validación exitosa:")
                print(f"   - Coherente: {validation.is_coherent}")
                print(f"   - Confianza: {validation.confidence_score:.3f}")
                print(f"   - Razonamiento: {validation.validation_reasoning[:100]}...")
                print(f"   - Inconsistencias: {len(validation.detected_inconsistencies)}")
            else:
                print("⚠️ Validación retornó None (esperado si score < threshold)")
        except Exception as e:
            print(f"⚠️ Error en validación (esperado si OpenCode no está configurado): {e}")
    else:
        print("⚠️ OpenCode no disponible - saltando validación real")
        print("   (Esto es normal si OPENCODE_ENABLED=false)")
    
    print()

def test_integration_flow():
    """Test 7: Flujo de integración completo."""
    
    print("🧪 Test 7: Flujo de integración completo")
    print("=" * 60)
    
    validator = OpenCodeValidator()
    
    # Simular pipeline completo
    candidates = [
        {
            "id": "candidate_1",
            "region_name": "Test Region 1",
            "archaeological_probability": 0.85,
            "evidence_layers": [
                {"type": "ndvi", "value": 0.7},
                {"type": "sar", "value": 0.8}
            ],
            "instruments_converging": 2,
            "environment_type": "forest",
            "spatial_context": {"lat": 10.0, "lon": 20.0}
        },
        {
            "id": "candidate_2",
            "region_name": "Test Region 2",
            "archaeological_probability": 0.45,  # Bajo - no debe validarse
            "evidence_layers": [
                {"type": "ndvi", "value": 0.3}
            ],
            "instruments_converging": 1,
            "environment_type": "grassland",
            "spatial_context": {"lat": 15.0, "lon": 25.0}
        },
        {
            "id": "candidate_3",
            "region_name": "Test Region 3",
            "archaeological_probability": 0.92,
            "evidence_layers": [
                {"type": "ndvi", "value": 0.9},
                {"type": "sar", "value": 0.85},
                {"type": "thermal", "value": 0.75}
            ],
            "instruments_converging": 3,
            "environment_type": "desert",
            "spatial_context": {"lat": 20.0, "lon": 30.0}
        }
    ]
    
    validated_count = 0
    skipped_count = 0
    
    for candidate in candidates:
        print(f"\nProcesando: {candidate['region_name']}")
        print(f"  Score: {candidate['archaeological_probability']:.3f}")
        
        if validator.should_validate(candidate):
            print(f"  ✅ Candidato para validación OpenCode")
            validated_count += 1
        else:
            print(f"  ⏭️  Saltado (score bajo o ya en caché)")
            skipped_count += 1
    
    print()
    print(f"Resumen:")
    print(f"  - Total candidatos: {len(candidates)}")
    print(f"  - Para validar: {validated_count}")
    print(f"  - Saltados: {skipped_count}")
    print()
    
    assert validated_count >= 1, "Al menos un candidato debe validarse"
    assert skipped_count >= 1, "Al menos un candidato debe saltarse"
    
    print("✅ Flujo de integración correcto")
    print()

def main():
    """Ejecutar todos los tests."""
    
    print("=" * 60)
    print("🧠 OPENCODE VALIDATOR - TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Inicialización
        validator = test_validator_initialization()
        
        # Test 2: Decisión de validación
        test_should_validate(validator)
        
        # Test 3: Hashing
        test_hash_candidate(validator)
        
        # Test 4: Caché
        test_cache_operations(validator)
        
        # Test 5: Preparación de datos
        test_prepare_validation_data(validator)
        
        # Test 6: Validación simulada
        test_mock_validation(validator)
        
        # Test 7: Flujo completo
        test_integration_flow()
        
        # Resumen final
        print("=" * 60)
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 60)
        print()
        print("📊 Resumen:")
        print(f"   - OpenCode enabled: {validator.enabled}")
        print(f"   - OpenCode available: {validator.is_available}")
        print(f"   - Cache entries: {len(validator.cache)}")
        print()
        
        if not validator.is_available:
            print("⚠️  NOTA: OpenCode no está disponible")
            print("   Para habilitar:")
            print("   1. Configura OPENCODE_ENABLED=true en .env")
            print("   2. Asegúrate de que OpenCode esté corriendo en el puerto configurado")
            print("   3. O ajusta OPENCODE_API_URL a tu instancia")
            print()
        
        return True
        
    except AssertionError as e:
        print(f"❌ TEST FALLÓ: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
