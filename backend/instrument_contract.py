#!/usr/bin/env python3
"""
Instrument Contract - Contrato estándar para TODOS los instrumentos
Garantiza respuestas robustas y científicamente defendibles
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, Dict
import json


class InstrumentStatus(Enum):
    """Estados posibles de una medición instrumental"""
    OK = "OK"                           # Medición exitosa con datos válidos
    NO_DATA = "NO_DATA"                 # No hay datos disponibles para la región/fecha
    INVALID = "INVALID"                 # Datos inválidos (inf, nan, out of bounds)
    LOW_QUALITY = "LOW_QUALITY"         # Datos de baja calidad (flags, nubes, etc)
    DERIVED = "DERIVED"                 # Datos derivados/estimados (no medición directa)
    TIMEOUT = "TIMEOUT"                 # Timeout en API
    ERROR = "ERROR"                     # Error técnico (red, parsing, etc)


@dataclass
class InstrumentMeasurement:
    """
    Contrato estándar de salida para TODOS los instrumentos
    
    REGLA DE ORO: NUNCA devolver float crudo - SIEMPRE usar este contrato
    """
    
    # Identificación
    instrument_name: str                # Nombre del instrumento (ej: "ICESat-2", "Sentinel-2")
    measurement_type: str               # Tipo de medición (ej: "elevation", "ndvi", "sar_backscatter")
    
    # Valor medido
    value: Optional[float]              # Valor numérico (None si no hay dato válido)
    unit: str                           # Unidad de medida (ej: "meters", "index", "dB")
    
    # Estado y calidad
    status: InstrumentStatus            # Estado de la medición
    confidence: float                   # Confianza en el dato (0.0 - 1.0)
    
    # Contexto científico
    reason: Optional[str]               # Razón del estado (ej: "all_values_nan", "cloud_cover_high")
    quality_flags: Dict[str, Any]       # Flags de calidad específicos del instrumento
    
    # Metadatos
    source: str                         # Fuente de datos (ej: "NASA Earthdata", "Planetary Computer")
    acquisition_date: Optional[str]     # Fecha de adquisición de datos
    processing_notes: Optional[str]     # Notas adicionales de procesamiento
    
    # Umbral arqueológico (si aplica)
    threshold: Optional[float] = None   # Umbral de anomalía arqueológica
    exceeds_threshold: bool = False     # Si excede el umbral
    
    def __post_init__(self):
        """Validación post-inicialización"""
        # Validar confidence
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence debe estar entre 0.0 y 1.0, recibido: {self.confidence}")
        
        # Validar consistencia value/status
        if self.status == InstrumentStatus.OK and self.value is None:
            raise ValueError("Status OK requiere value no-None")
        
        if self.status != InstrumentStatus.OK and self.value is not None:
            # Permitir DERIVED con value
            if self.status != InstrumentStatus.DERIVED:
                print(f"⚠️ Warning: Status {self.status} con value={self.value} (debería ser None)")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario JSON-serializable"""
        return {
            'instrument_name': self.instrument_name,
            'measurement_type': self.measurement_type,
            'value': self.value,
            'unit': self.unit,
            'status': self.status.value,
            'data_mode': self.status.value,  # AGREGADO: alias para compatibilidad
            'confidence': self.confidence,
            'reason': self.reason,
            'quality_flags': self.quality_flags,
            'source': self.source,
            'acquisition_date': self.acquisition_date,
            'processing_notes': self.processing_notes,
            'threshold': self.threshold,
            'exceeds_threshold': self.exceeds_threshold
        }
    
    def to_json(self) -> str:
        """Convertir a JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def is_usable(self) -> bool:
        """¿Es usable para análisis arqueológico?"""
        return self.status in [InstrumentStatus.OK, InstrumentStatus.DERIVED]
    
    def is_high_quality(self) -> bool:
        """¿Es de alta calidad?"""
        return self.status == InstrumentStatus.OK and self.confidence >= 0.7
    
    @classmethod
    def create_no_data(cls, instrument_name: str, measurement_type: str, 
                      reason: str, source: str) -> 'InstrumentMeasurement':
        """Factory: Crear medición sin datos"""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=None,
            unit="N/A",
            status=InstrumentStatus.NO_DATA,
            confidence=0.0,
            reason=reason,
            quality_flags={},
            source=source,
            acquisition_date=None,
            processing_notes=None
        )
    
    @classmethod
    def create_invalid(cls, instrument_name: str, measurement_type: str,
                      reason: str, source: str, unit: str = "N/A") -> 'InstrumentMeasurement':
        """Factory: Crear medición inválida"""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=None,
            unit=unit,
            status=InstrumentStatus.INVALID,
            confidence=0.0,
            reason=reason,
            quality_flags={},
            source=source,
            acquisition_date=None,
            processing_notes=None
        )
    
    @classmethod
    def create_error(cls, instrument_name: str, measurement_type: str,
                    error_msg: str, source: str) -> 'InstrumentMeasurement':
        """Factory: Crear medición con error"""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=None,
            unit="N/A",
            status=InstrumentStatus.ERROR,
            confidence=0.0,
            reason=f"Error: {error_msg}",
            quality_flags={},
            source=source,
            acquisition_date=None,
            processing_notes=None
        )
    
    @classmethod
    def create_derived(cls, instrument_name: str, measurement_type: str,
                      value: float, unit: str, confidence: float,
                      derivation_method: str, source: str) -> 'InstrumentMeasurement':
        """Factory: Crear medición derivada/estimada"""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=value,
            unit=unit,
            status=InstrumentStatus.DERIVED,
            confidence=confidence,
            reason=f"Derived using: {derivation_method}",
            quality_flags={'derivation_method': derivation_method},
            source=source,
            acquisition_date=None,
            processing_notes=f"NOT a direct measurement. Estimated using: {derivation_method}"
        )
    
    @classmethod
    def create_success(cls, instrument_name: str, measurement_type: str,
                      value: float, unit: str, confidence: float,
                      source: str, acquisition_date: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> 'InstrumentMeasurement':
        """Factory: Crear medición exitosa"""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=value,
            unit=unit,
            status=InstrumentStatus.OK,
            confidence=confidence,
            reason=None,
            quality_flags=metadata or {},
            source=source,
            acquisition_date=acquisition_date,
            processing_notes=None
        )


def validate_measurement(measurement: InstrumentMeasurement) -> bool:
    """
    Validar que una medición cumple el contrato
    
    Returns:
        True si es válida, False si no
    """
    try:
        # Validar tipos
        assert isinstance(measurement.instrument_name, str)
        assert isinstance(measurement.measurement_type, str)
        assert isinstance(measurement.status, InstrumentStatus)
        assert isinstance(measurement.confidence, (int, float))
        assert isinstance(measurement.source, str)
        
        # Validar rangos
        assert 0.0 <= measurement.confidence <= 1.0
        
        # Validar consistencia
        if measurement.status == InstrumentStatus.OK:
            assert measurement.value is not None
            assert isinstance(measurement.value, (int, float))
            assert not (measurement.value == float('inf') or measurement.value == float('-inf'))
            assert not (measurement.value != measurement.value)  # Check NaN
        
        return True
        
    except AssertionError as e:
        print(f"❌ Medición inválida: {e}")
        return False


# Ejemplos de uso
if __name__ == "__main__":
    print("="*80)
    print("EJEMPLOS DE USO - INSTRUMENT CONTRACT")
    print("="*80)
    
    # Ejemplo 1: Medición exitosa
    print("\n1. Medición exitosa (OK):")
    m1 = InstrumentMeasurement(
        instrument_name="ICESat-2",
        measurement_type="elevation",
        value=1234.56,
        unit="meters",
        status=InstrumentStatus.OK,
        confidence=0.95,
        reason=None,
        quality_flags={'signal_conf': 4, 'quality_flag': 0},
        source="NASA Earthdata",
        acquisition_date="2024-01-15",
        processing_notes="Filtered by quality flags",
        threshold=1200.0,
        exceeds_threshold=True
    )
    print(m1.to_json())
    print(f"Usable: {m1.is_usable()}, High Quality: {m1.is_high_quality()}")
    
    # Ejemplo 2: Sin datos
    print("\n2. Sin datos (NO_DATA):")
    m2 = InstrumentMeasurement.create_no_data(
        instrument_name="Sentinel-2",
        measurement_type="ndvi",
        reason="No scenes found for date range",
        source="Planetary Computer"
    )
    print(m2.to_json())
    print(f"Usable: {m2.is_usable()}")
    
    # Ejemplo 3: Datos inválidos
    print("\n3. Datos inválidos (INVALID):")
    m3 = InstrumentMeasurement.create_invalid(
        instrument_name="ICESat-2",
        measurement_type="elevation",
        reason="all_values_nan - insufficient valid points after quality filtering",
        source="NASA Earthdata",
        unit="meters"
    )
    print(m3.to_json())
    print(f"Usable: {m3.is_usable()}")
    
    # Ejemplo 4: Datos derivados
    print("\n4. Datos derivados (DERIVED):")
    m4 = InstrumentMeasurement.create_derived(
        instrument_name="NSIDC",
        measurement_type="sea_ice_concentration",
        value=0.4,
        unit="fraction",
        confidence=0.7,
        derivation_method="Location-based seasonal model (latitude + month)",
        source="NSIDC (estimated)"
    )
    print(m4.to_json())
    print(f"Usable: {m4.is_usable()}, High Quality: {m4.is_high_quality()}")
    
    # Ejemplo 5: Error
    print("\n5. Error técnico (ERROR):")
    m5 = InstrumentMeasurement.create_error(
        instrument_name="Sentinel-1",
        measurement_type="sar_backscatter",
        error_msg="TIFFReadEncodedTile() failed - corrupted COG tile",
        source="Planetary Computer"
    )
    print(m5.to_json())
    print(f"Usable: {m5.is_usable()}")
    
    print("\n" + "="*80)
    print("✅ Todos los ejemplos son JSON-serializables y científicamente defendibles")
    print("="*80)
