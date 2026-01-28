#!/usr/bin/env python3
"""
ArcheoScope - Test Completo Patagonia
Candidato #001: Región Proglaciar Patagónica

Coordenadas: -50.4760°S, -73.0450°W
Área: ~35 × 20 km
Región: Patagonia, Chile/Argentina

Instrumentos esperados:
- Sentinel-1 SAR (penetración hielo)
- MODIS LST (inercia térmica)
- NSIDC (hielo estacional/proglaciar)
- OpenTopography (DEM/topografía)

Fecha: 2026-01-26
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

async def test_patagonia_completo():
    """Test completo del sistema ArcheoScope en Patagonia"""
    
    print("="*80)
    print("ARCHEOSCOPE - TEST COMPLETO PATAGONIA")
    print("Candidato #001: Region Proglaciar Patagonica")
    print("="*80)
    print()
    print("Coordenadas Centro: -50.4760 S, -73.0450 W")
    print("Bounding Box:")
    print("  lat_min: -50.55")
    print("  lat_max: -50.40")
    print("  lon_min: -73.15")
    print("  lon_max: -72.90")
    print("Area: ~35 x 20 km")
    print("="*80)
    print()
    
    # Coordenadas
    lat = -50.4760
    lon = -73.0450
    lat_min = -50.55
    lat_max = -50.40
    lon_min = -73.15
    lon_max = -72.90
    region_name = "Patagonia Proglaciar - Candidato #001"
    
    # Limpiar log anterior
    try:
        with open('instrument_diagnostics.log', 'w', encoding='utf-8') as f:
            f.write(f"=== ARCHEOSCOPE TEST PATAGONIA 2026-01-26 ===\n")
            f.write(f"Candidato #001: {region_name}\n")
            f.write(f"Coordenadas: {lat}, {lon}\n")
            f.write(f"Bbox: [{lat_min}, {lat_max}] x [{lon_min}, {lon_max}]\n\n")
    except:
        pass
    
    # Importar sistema
    try:
        from core_anomaly_detector import CoreAnomalyDetector
        from environment_classifier import EnvironmentClassifier
        from validation.real_archaeological_validator import RealArchaeologicalValidator
        
        print("[INIT] Inicializando sistema ArcheoScope...")
        
        # Inicializar componentes
        env_classifier = EnvironmentClassifier()
        real_validator = RealArchaeologicalValidator()
        
        # ArchaeologicalDataLoader deshabilitado (usa np.random)
        # Pasar None - el sistema funciona sin él
        detector = CoreAnomalyDetector(
            environment_classifier=env_classifier,
            real_validator=real_validator,
            data_loader=None  # Deshabilitado - REGLA NRO 1
        )
        
        print("[OK] Sistema inicializado correctamente")
        print()
        
    except Exception as e:
        print(f"[FAIL] Error inicializando sistema: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Ejecutar análisis
    print("="*80)
    print("INICIANDO ANALISIS ARQUEOLOGICO")
    print("="*80)
    print()
    
    start_time = datetime.now()
    
    try:
        result = await detector.detect_anomaly(
            lat=lat,
            lon=lon,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            region_name=region_name
        )
        
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        
        print()
        print("="*80)
        print("RESULTADO DEL ANALISIS")
        print("="*80)
        print()
        
        # Resultado principal
        print(f"[RESULTADO] Anomalia detectada: {'SI' if result.anomaly_detected else 'NO'}")
        print(f"[CONFIANZA] Nivel: {result.confidence_level}")
        print(f"[PROBABILIDAD] Arqueologica: {result.archaeological_probability:.1%}")
        print()
        
        # Ambiente
        print(f"[AMBIENTE] Tipo: {result.environment_type}")
        print(f"[AMBIENTE] Confianza: {result.environment_confidence:.1%}")
        print()
        
        # Instrumentos
        print(f"[INSTRUMENTOS] Midiendo: {len(result.measurements)}")
        print(f"[CONVERGENCIA] Excediendo umbral: {result.instruments_converging}/{result.minimum_required}")
        print(f"[CONVERGENCIA] Alcanzada: {'SI' if result.instruments_converging >= result.minimum_required else 'NO'}")
        print()
        
        # Detalle de mediciones
        if result.measurements:
            print("="*80)
            print("DETALLE DE MEDICIONES")
            print("="*80)
            print()
            
            for i, m in enumerate(result.measurements, 1):
                print(f"[{i}] {m.instrument_name}")
                print(f"    Valor: {m.value:.3f} {m.unit}")
                print(f"    Umbral: {m.threshold:.3f} {m.unit}")
                print(f"    Excede: {'SI' if m.exceeds_threshold else 'NO'}")
                print(f"    Confianza: {m.confidence}")
                print(f"    Notas: {m.notes[:100]}...")
                print()
        
        # Sitios conocidos
        if result.known_site_nearby:
            print("="*80)
            print("SITIOS ARQUEOLOGICOS CONOCIDOS")
            print("="*80)
            print()
            print(f"[SITIO] Nombre: {result.known_site_name}")
            print(f"[SITIO] Distancia: {result.known_site_distance_km:.2f} km")
            print()
        
        # Explicación
        print("="*80)
        print("EXPLICACION CIENTIFICA")
        print("="*80)
        print()
        print(result.explanation)
        print()
        
        # Razonamiento
        if result.detection_reasoning:
            print("="*80)
            print("RAZONAMIENTO DE DETECCION")
            print("="*80)
            print()
            for reason in result.detection_reasoning:
                print(f"  - {reason}")
            print()
        
        # Riesgos de falsos positivos
        if result.false_positive_risks:
            print("="*80)
            print("RIESGOS DE FALSOS POSITIVOS")
            print("="*80)
            print()
            for risk in result.false_positive_risks:
                print(f"  - {risk}")
            print()
        
        # Recomendaciones
        if result.recommended_validation:
            print("="*80)
            print("RECOMENDACIONES DE VALIDACION")
            print("="*80)
            print()
            for rec in result.recommended_validation:
                print(f"  - {rec}")
            print()
        
        # Métricas finales
        print("="*80)
        print("METRICAS FINALES")
        print("="*80)
        print()
        print(f"Tiempo total: {elapsed:.2f} segundos")
        print(f"Instrumentos midiendo: {len(result.measurements)}")
        print(f"Convergencia: {result.instruments_converging}/{result.minimum_required}")
        print(f"Probabilidad arqueologica: {result.archaeological_probability:.1%}")
        print(f"Confianza: {result.confidence_level}")
        print()
        
        # Guardar resultado a JSON
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'region_name': region_name,
            'coordinates': {
                'center': {'lat': lat, 'lon': lon},
                'bbox': {
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'lon_min': lon_min,
                    'lon_max': lon_max
                }
            },
            'result': {
                'anomaly_detected': result.anomaly_detected,
                'confidence_level': result.confidence_level,
                'archaeological_probability': result.archaeological_probability,
                'environment_type': result.environment_type,
                'environment_confidence': result.environment_confidence,
                'instruments_converging': result.instruments_converging,
                'minimum_required': result.minimum_required,
                'convergence_met': result.instruments_converging >= result.minimum_required
            },
            'measurements': [
                {
                    'instrument': m.instrument_name,
                    'value': m.value,
                    'unit': m.unit,
                    'threshold': m.threshold,
                    'exceeds': m.exceeds_threshold,
                    'confidence': m.confidence
                }
                for m in result.measurements
            ],
            'known_site': {
                'nearby': result.known_site_nearby,
                'name': result.known_site_name,
                'distance_km': result.known_site_distance_km
            },
            'explanation': result.explanation,
            'elapsed_seconds': elapsed
        }
        
        filename = f"patagonia_candidato_001_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"[GUARDADO] Resultado guardado en: {filename}")
        print(f"[LOGS] Ver detalles en: instrument_diagnostics.log")
        print()
        
        print("="*80)
        print("TEST COMPLETADO EXITOSAMENTE")
        print("="*80)
        
        return True
        
    except Exception as e:
        print()
        print("="*80)
        print("ERROR EN ANALISIS")
        print("="*80)
        print()
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_patagonia_completo())
    sys.exit(0 if success else 1)
