#!/usr/bin/env python3
"""
ArcheoScope Instrument Status System
====================================

Sistema de estados explícitos por instrumento para evitar abortar
el análisis completo cuando un instrumento falla.

Implementa el patrón recomendado:
- Estados explícitos por instrumento
- Nunca abortar por un instrumento
- Puntuar con lo que hay
- Mostrar "coverage score"
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class InstrumentStatus(Enum):
    """Estados posibles de un instrumento."""
    SUCCESS = "SUCCESS"           # Datos válidos obtenidos
    DEGRADED = "DEGRADED"        # Datos parciales o baja calidad
    FAILED = "FAILED"            # No se pudieron obtener datos
    UNAVAILABLE = "UNAVAILABLE"  # API/servicio no disponible
    INVALID = "INVALID"          # Datos inválidos (inf/nan)
    TIMEOUT = "TIMEOUT"          # Timeout en la consulta
    NO_DATA = "NO_DATA"          # Sin datos para la región/fecha

@dataclass
class InstrumentResult:
    """Resultado completo de un instrumento con estado explícito."""
    
    # Identificación
    instrument_name: str
    measurement_type: str
    
    # Estado y calidad
    status: InstrumentStatus
    confidence: float  # 0.0 - 1.0
    
    # Datos (pueden ser None si status != SUCCESS)
    value: Optional[float]
    unit: Optional[str]
    
    # Metadatos de calidad
    valid_pixels: Optional[int] = None
    total_pixels: Optional[int] = None
    quality_ratio: Optional[float] = None
    
    # Información de la fuente
    source: Optional[str] = None
    acquisition_date: Optional[str] = None
    
    # Diagnóstico
    reason: Optional[str] = None
    error_details: Optional[str] = None
    
    # Timing
    processing_time_s: Optional[float] = None
    
    @classmethod
    def create_success(cls, instrument_name: str, measurement_type: str,
                      value: float, unit: str, confidence: float = 1.0,
                      **kwargs) -> 'InstrumentResult':
        """Crear resultado exitoso."""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            status=InstrumentStatus.SUCCESS,
            confidence=confidence,
            value=value,
            unit=unit,
            **kwargs
        )
    
    @classmethod
    def create_degraded(cls, instrument_name: str, measurement_type: str,
                       value: Optional[float], unit: Optional[str],
                       confidence: float, reason: str, **kwargs) -> 'InstrumentResult':
        """Crear resultado degradado (datos parciales)."""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            status=InstrumentStatus.DEGRADED,
            confidence=confidence,
            value=value,
            unit=unit,
            reason=reason,
            **kwargs
        )
    
    @classmethod
    def create_failed(cls, instrument_name: str, measurement_type: str,
                     reason: str, error_details: Optional[str] = None,
                     **kwargs) -> 'InstrumentResult':
        """Crear resultado fallido."""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            status=InstrumentStatus.FAILED,
            confidence=0.0,
            value=None,
            unit=None,
            reason=reason,
            error_details=error_details,
            **kwargs
        )
    
    @classmethod
    def create_invalid(cls, instrument_name: str, measurement_type: str,
                      reason: str, **kwargs) -> 'InstrumentResult':
        """Crear resultado inválido (inf/nan)."""
        return cls(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            status=InstrumentStatus.INVALID,
            confidence=0.0,
            value=None,
            unit=None,
            reason=reason,
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para JSON."""
        return {
            "instrument": self.instrument_name,
            "measurement_type": self.measurement_type,
            "status": self.status.value,
            "confidence": self.confidence,
            "value": self.value,
            "unit": self.unit,
            "valid_pixels": self.valid_pixels,
            "total_pixels": self.total_pixels,
            "quality_ratio": self.quality_ratio,
            "source": self.source,
            "acquisition_date": self.acquisition_date,
            "reason": self.reason,
            "error_details": self.error_details,
            "processing_time_s": self.processing_time_s
        }

class InstrumentBatch:
    """Manejo de lote de instrumentos con estados explícitos."""
    
    def __init__(self):
        self.results: List[InstrumentResult] = []
        self.start_time = None
        self.end_time = None
    
    def add_result(self, result: InstrumentResult):
        """Agregar resultado de instrumento."""
        self.results.append(result)
        logger.info(f"Instrumento {result.instrument_name}: {result.status.value}")
    
    def get_coverage_score(self) -> float:
        """
        Calcular score de cobertura instrumental.
        
        Returns:
            Score 0.0-1.0 basado en instrumentos exitosos y degradados
        """
        if not self.results:
            return 0.0
        
        total_weight = 0.0
        achieved_weight = 0.0
        
        for result in self.results:
            # Peso base por instrumento
            weight = 1.0
            
            # Instrumentos críticos tienen más peso
            if result.instrument_name.lower() in ['sentinel-2', 'icesat-2', 'landsat']:
                weight = 1.5
            
            total_weight += weight
            
            # Contribución según estado
            if result.status == InstrumentStatus.SUCCESS:
                achieved_weight += weight * result.confidence
            elif result.status == InstrumentStatus.DEGRADED:
                achieved_weight += weight * result.confidence * 0.6  # Penalización por degradación
            # FAILED, INVALID, etc. contribuyen 0
        
        return achieved_weight / total_weight if total_weight > 0 else 0.0
    
    def get_status_summary(self) -> Dict[str, int]:
        """Obtener resumen de estados."""
        summary = {status.value: 0 for status in InstrumentStatus}
        
        for result in self.results:
            summary[result.status.value] += 1
        
        return summary
    
    def get_successful_instruments(self) -> List[InstrumentResult]:
        """Obtener solo instrumentos exitosos."""
        return [r for r in self.results if r.status == InstrumentStatus.SUCCESS]
    
    def get_usable_instruments(self) -> List[InstrumentResult]:
        """Obtener instrumentos exitosos + degradados con datos."""
        return [r for r in self.results 
                if r.status in [InstrumentStatus.SUCCESS, InstrumentStatus.DEGRADED] 
                and r.value is not None]
    
    def has_minimum_coverage(self, minimum_instruments: int = 2) -> bool:
        """Verificar si hay cobertura mínima."""
        usable = len(self.get_usable_instruments())
        return usable >= minimum_instruments
    
    def generate_report(self) -> Dict[str, Any]:
        """Generar reporte completo del lote."""
        status_summary = self.get_status_summary()
        coverage_score = self.get_coverage_score()
        usable_count = len(self.get_usable_instruments())
        
        return {
            "total_instruments": len(self.results),
            "status_summary": status_summary,
            "coverage_score": coverage_score,
            "usable_instruments": usable_count,
            "has_minimum_coverage": self.has_minimum_coverage(),
            "successful_rate": status_summary["SUCCESS"] / len(self.results) if self.results else 0.0,
            "degraded_rate": status_summary["DEGRADED"] / len(self.results) if self.results else 0.0,
            "failed_rate": (status_summary["FAILED"] + status_summary["INVALID"] + 
                           status_summary["UNAVAILABLE"] + status_summary["TIMEOUT"] + 
                           status_summary["NO_DATA"]) / len(self.results) if self.results else 0.0,
            "instruments": [result.to_dict() for result in self.results]
        }

def create_instrument_result_from_api_data(instrument_name: str, 
                                         measurement_type: str,
                                         api_data: Optional[Dict[str, Any]],
                                         processing_time: float = 0.0) -> InstrumentResult:
    """
    Crear InstrumentResult desde datos de API con manejo robusto de errores.
    
    Args:
        instrument_name: Nombre del instrumento
        measurement_type: Tipo de medición
        api_data: Datos de la API (puede ser None)
        processing_time: Tiempo de procesamiento
    
    Returns:
        InstrumentResult con estado apropiado
    """
    
    # Importar sanitizador
    from .data_sanitizer import safe_float, safe_int
    
    if api_data is None:
        return InstrumentResult.create_failed(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            reason="API_NO_DATA",
            processing_time_s=processing_time
        )
    
    # Extraer valor principal
    value = safe_float(api_data.get('value'))
    confidence = safe_float(api_data.get('confidence', 0.0))
    
    # Determinar estado basado en datos
    if value is None:
        # Verificar si hay razón específica
        reason = api_data.get('reason', 'NO_VALID_DATA')
        
        if 'timeout' in reason.lower():
            status = InstrumentStatus.TIMEOUT
        elif 'unavailable' in reason.lower() or 'service' in reason.lower():
            status = InstrumentStatus.UNAVAILABLE
        elif 'invalid' in reason.lower() or 'nan' in reason.lower() or 'inf' in reason.lower():
            status = InstrumentStatus.INVALID
        else:
            status = InstrumentStatus.NO_DATA
        
        return InstrumentResult(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            status=status,
            confidence=0.0,
            value=None,
            unit=None,
            reason=reason,
            source=api_data.get('source'),
            acquisition_date=api_data.get('acquisition_date'),
            processing_time_s=processing_time
        )
    
    # Hay valor válido - determinar si SUCCESS o DEGRADED
    quality_indicators = {
        'valid_pixels': safe_int(api_data.get('valid_pixels')),
        'total_pixels': safe_int(api_data.get('total_pixels')),
        'cloud_cover': safe_float(api_data.get('cloud_cover')),
        'quality_flag': safe_int(api_data.get('quality_flag'))
    }
    
    # Calcular ratio de calidad
    quality_ratio = None
    if quality_indicators['valid_pixels'] and quality_indicators['total_pixels']:
        quality_ratio = quality_indicators['valid_pixels'] / quality_indicators['total_pixels']
    
    # Determinar si es SUCCESS o DEGRADED
    is_degraded = False
    degraded_reasons = []
    
    if confidence and confidence < 0.7:
        is_degraded = True
        degraded_reasons.append(f"low_confidence_{confidence:.2f}")
    
    if quality_ratio and quality_ratio < 0.5:
        is_degraded = True
        degraded_reasons.append(f"low_quality_ratio_{quality_ratio:.2f}")
    
    if quality_indicators['cloud_cover'] and quality_indicators['cloud_cover'] > 0.3:
        is_degraded = True
        degraded_reasons.append(f"high_cloud_cover_{quality_indicators['cloud_cover']:.2f}")
    
    # Crear resultado
    if is_degraded:
        return InstrumentResult.create_degraded(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=value,
            unit=api_data.get('unit', 'units'),
            confidence=confidence or 0.5,
            reason=" | ".join(degraded_reasons),
            valid_pixels=quality_indicators['valid_pixels'],
            total_pixels=quality_indicators['total_pixels'],
            quality_ratio=quality_ratio,
            source=api_data.get('source'),
            acquisition_date=api_data.get('acquisition_date'),
            processing_time_s=processing_time
        )
    else:
        return InstrumentResult.create_success(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=value,
            unit=api_data.get('unit', 'units'),
            confidence=confidence or 0.8,
            valid_pixels=quality_indicators['valid_pixels'],
            total_pixels=quality_indicators['total_pixels'],
            quality_ratio=quality_ratio,
            source=api_data.get('source'),
            acquisition_date=api_data.get('acquisition_date'),
            processing_time_s=processing_time
        )

if __name__ == "__main__":
    # Test del sistema de estados
    batch = InstrumentBatch()
    
    # Simular resultados mixtos
    batch.add_result(InstrumentResult.create_success(
        "Sentinel-2", "NDVI", 0.75, "NDVI", 0.9
    ))
    
    batch.add_result(InstrumentResult.create_degraded(
        "ICESat-2", "elevation", 1234.5, "m", 0.6, "low_point_density"
    ))
    
    batch.add_result(InstrumentResult.create_failed(
        "Landsat", "thermal", "API_TIMEOUT"
    ))
    
    batch.add_result(InstrumentResult.create_invalid(
        "SAR", "backscatter", "all_values_nan"
    ))
    
    # Generar reporte
    report = batch.generate_report()
    print("Reporte del lote:")
    print(f"  Cobertura: {report['coverage_score']:.1%}")
    print(f"  Instrumentos usables: {report['usable_instruments']}/{report['total_instruments']}")
    print(f"  Estados: {report['status_summary']}")