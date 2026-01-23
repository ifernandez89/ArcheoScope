"""
ArcheoScope Water Module
Detección automática de agua y arqueología submarina
"""

from .water_detector import WaterDetector, WaterContext, WaterBodyType
from .submarine_archaeology import SubmarineArchaeologyEngine, WreckCandidate, SubmarineInstrument

__all__ = [
    'WaterDetector',
    'WaterContext', 
    'WaterBodyType',
    'SubmarineArchaeologyEngine',
    'WreckCandidate',
    'SubmarineInstrument'
]