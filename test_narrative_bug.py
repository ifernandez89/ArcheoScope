#!/usr/bin/env python3
"""Test para reproducir el bug de NoneType / float en scientific_narrative"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from scientific_narrative import generate_archaeological_narrative

# Test con valores que podrían causar el error
try:
    narrative = generate_archaeological_narrative(
        thermal_stability=0.8,
        sar_structural_index=0.5,
        icesat2_rugosity=None,  # Puede ser None
        ndvi_persistence=0.3,
        tas_score=0.4,
        coverage_score=None,  # Puede ser None
        environment_type="temperate",
        flags=[],
        anomaly_score=0.75
    )
    
    print("✅ Narrativa generada sin errores")
    print(f"Clasificación: {narrative.classification.value}")
    print(f"Prioridad: {narrative.priority}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
