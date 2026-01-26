#!/usr/bin/env python3
"""
Data Mode and Integrity Validation
===================================

CRITICAL FOR SCIENTIFIC INTEGRITY

This module enforces data mode labeling and prevents scientifically
irresponsible language in outputs.

Data Modes:
- REAL: Direct measurements from satellite APIs
- DERIVED: Estimates based on location/models
- SIMULATED: Simulations (PROHIBITED in production)
- INFERRED: Geometric/statistical inferences

Created: 2026-01-26
Reason: Scientific integrity audit - prevent fraud risk
"""

from enum import Enum
from typing import Dict, Any, List
import re


class DataMode(Enum):
    """
    Data mode classification - CRITICAL for scientific integrity
    
    Every output MUST be labeled with its data mode to prevent
    misinterpretation of results.
    """
    REAL = "REAL"           # Direct satellite API measurement
    DERIVED = "DERIVED"     # Estimation based on location/season
    SIMULATED = "SIMULATED" # Simulation (PROHIBITED in production)
    INFERRED = "INFERRED"   # Geometric/statistical inference


class DataIntegrityValidator:
    """
    Validator for data integrity and scientific language
    
    Prevents:
    - Definitive language in non-REAL data
    - Missing disclaimers in DERIVED/INFERRED data
    - SIMULATED data in production
    - Misleading terminology
    """
    
    # Forbidden words for non-REAL data (definitive language)
    FORBIDDEN_WORDS_DEFINITIVE = [
        # Spanish
        'confirmado', 'detectado', 'hallazgo', 'descubrimiento',
        'estructura', 'sitio arqueológico', 'evidencia',
        # English
        'confirmed', 'detected', 'discovery', 'found',
        'structure', 'archaeological site', 'evidence'
    ]
    
    # Required words for non-REAL data (hypothetical language)
    REQUIRED_HYPOTHETICAL = [
        # Spanish
        'hipótesis', 'candidato', 'posible', 'compatible con',
        'patrón', 'anomalía', 'plausible',
        # English
        'hypothesis', 'candidate', 'possible', 'compatible with',
        'pattern', 'anomaly', 'plausible'
    ]
    
    @staticmethod
    def validate_output(data: Dict[str, Any], mode: DataMode) -> bool:
        """
        Validate that output is appropriate for data mode
        
        Args:
            data: Output data dictionary
            mode: Data mode (REAL, DERIVED, INFERRED, SIMULATED)
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If validation fails
        """
        
        # RULE 1: SIMULATED data is PROHIBITED in production
        if mode == DataMode.SIMULATED:
            raise ValueError(
                "SIMULATED data is PROHIBITED in production. "
                "ArcheoScope Rule #1: NEVER fake data."
            )
        
        # RULE 2: DERIVED/INFERRED data MUST include disclaimer
        if mode in [DataMode.DERIVED, DataMode.INFERRED]:
            if 'disclaimer' not in data:
                raise ValueError(
                    f"{mode.value} data MUST include 'disclaimer' field. "
                    f"Scientific integrity requires transparency about data limitations."
                )
        
        # RULE 3: Non-REAL data CANNOT use definitive language
        if mode != DataMode.REAL:
            text = str(data).lower()
            
            for word in DataIntegrityValidator.FORBIDDEN_WORDS_DEFINITIVE:
                if word.lower() in text:
                    raise ValueError(
                        f"Forbidden word '{word}' found in {mode.value} data. "
                        f"Use hypothetical language instead. "
                        f"Example: 'pattern compatible with' instead of 'structure detected'."
                    )
        
        # RULE 4: data_mode field MUST be present
        if 'data_mode' not in data:
            raise ValueError(
                "Missing 'data_mode' field. "
                "All outputs MUST be labeled with data mode for scientific integrity."
            )
        
        # RULE 5: Validate data_mode value
        if data['data_mode'] != mode.value:
            raise ValueError(
                f"data_mode mismatch: expected '{mode.value}', got '{data['data_mode']}'"
            )
        
        return True
    
    @staticmethod
    def create_disclaimer(mode: DataMode, context: str = "") -> str:
        """
        Generate appropriate disclaimer for data mode
        
        Args:
            mode: Data mode
            context: Additional context (optional)
        
        Returns:
            Disclaimer text
        """
        
        disclaimers = {
            DataMode.REAL: (
                "Direct measurement from satellite API. "
                "Subject to sensor limitations and atmospheric conditions."
            ),
            DataMode.DERIVED: (
                "Estimation based on location, season, and statistical models. "
                "NOT a direct measurement. Requires validation with real data."
            ),
            DataMode.INFERRED: (
                "Geometric/statistical inference based on instrumental patterns. "
                "NOT physical proof. Represents plausibility, not confirmation. "
                "Requires field validation by professional archaeologists."
            ),
            DataMode.SIMULATED: (
                "SIMULATED DATA - PROHIBITED IN PRODUCTION. "
                "For testing purposes only."
            )
        }
        
        base_disclaimer = disclaimers.get(mode, "Unknown data mode")
        
        if context:
            return f"{base_disclaimer} {context}"
        
        return base_disclaimer
    
    @staticmethod
    def sanitize_language(text: str, mode: DataMode) -> str:
        """
        Sanitize language to be scientifically appropriate
        
        Args:
            text: Input text
            mode: Data mode
        
        Returns:
            Sanitized text with appropriate language
        """
        
        if mode == DataMode.REAL:
            # REAL data can use more definitive language (but still careful)
            replacements = {
                'confirmado': 'medido instrumentalmente',
                'confirmed': 'instrumentally measured',
                'detectado': 'observado',
                'detected': 'observed'
            }
        else:
            # Non-REAL data MUST use hypothetical language
            replacements = {
                'confirmado': 'compatible con',
                'confirmed': 'compatible with',
                'detectado': 'patrón consistente con',
                'detected': 'pattern consistent with',
                'hallazgo': 'hipótesis',
                'discovery': 'hypothesis',
                'estructura': 'patrón geométrico',
                'structure': 'geometric pattern',
                'sitio arqueológico': 'candidato arqueológico',
                'archaeological site': 'archaeological candidate',
                'evidencia': 'indicador',
                'evidence': 'indicator'
            }
        
        sanitized = text
        for old, new in replacements.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old), re.IGNORECASE)
            sanitized = pattern.sub(new, sanitized)
        
        return sanitized
    
    @staticmethod
    def validate_visualization_config(config: Dict[str, Any], mode: DataMode) -> bool:
        """
        Validate visualization configuration for data mode
        
        Args:
            config: Visualization configuration
            mode: Data mode
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If visualization is misleading
        """
        
        # RULE: Non-REAL data MUST use wireframe visualization
        if mode != DataMode.REAL:
            if config.get('wireframe') != True:
                raise ValueError(
                    f"{mode.value} data MUST use wireframe visualization. "
                    f"Solid rendering is misleading for non-observed data."
                )
            
            if config.get('opacity', 1.0) > 0.5:
                raise ValueError(
                    f"{mode.value} data MUST have opacity <= 0.5. "
                    f"High opacity suggests physical evidence."
                )
        
        # RULE: INFERRED data MUST have visible disclaimer
        if mode == DataMode.INFERRED:
            if 'disclaimer_text' not in config:
                raise ValueError(
                    "INFERRED data visualization MUST include visible disclaimer text. "
                    "Example: 'GEOMETRÍA INFERIDA - NO ES EVIDENCIA FÍSICA'"
                )
        
        return True


class ScientificLanguageGuard:
    """
    Guard against scientifically irresponsible language
    
    Provides suggestions for better terminology.
    """
    
    TERMINOLOGY_GUIDE = {
        # Definitive → Hypothetical
        "estructura detectada": "patrón instrumental anómalo",
        "structure detected": "anomalous instrumental pattern",
        
        "sitio confirmado": "candidato de alta prioridad",
        "site confirmed": "high-priority candidate",
        
        "pirámide de Xm": "anomalía compatible con estructura compacta",
        "pyramid of Xm": "anomaly compatible with compact structure",
        
        "hallazgo arqueológico": "hipótesis arqueológica",
        "archaeological discovery": "archaeological hypothesis",
        
        "validación confirmada": "persistencia temporal detectada",
        "validation confirmed": "temporal persistence detected",
        
        "evidencia arqueológica": "indicador arqueológico",
        "archaeological evidence": "archaeological indicator",
        
        # Visualization
        "modelo 3D": "inferencia geométrica 3D",
        "3D model": "3D geometric inference",
        
        "reconstrucción": "visualización hipotética",
        "reconstruction": "hypothetical visualization"
    }
    
    @staticmethod
    def suggest_better_term(problematic_term: str) -> str:
        """
        Suggest scientifically appropriate alternative
        
        Args:
            problematic_term: Problematic terminology
        
        Returns:
            Suggested alternative
        """
        
        term_lower = problematic_term.lower()
        
        for bad, good in ScientificLanguageGuard.TERMINOLOGY_GUIDE.items():
            if bad.lower() in term_lower:
                return good
        
        return f"[NEEDS REVIEW: '{problematic_term}' - use hypothetical language]"
    
    @staticmethod
    def check_text(text: str) -> List[Dict[str, str]]:
        """
        Check text for problematic terminology
        
        Args:
            text: Text to check
        
        Returns:
            List of issues found with suggestions
        """
        
        issues = []
        text_lower = text.lower()
        
        for bad, good in ScientificLanguageGuard.TERMINOLOGY_GUIDE.items():
            if bad.lower() in text_lower:
                issues.append({
                    'problematic': bad,
                    'suggestion': good,
                    'reason': 'Definitive language in hypothetical context'
                })
        
        return issues


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_real_data_response(value: Any, source: str, confidence: float, **kwargs) -> Dict[str, Any]:
    """
    Create properly labeled REAL data response
    
    Args:
        value: Measured value
        source: Data source (e.g., "Sentinel-2", "MODIS LST")
        confidence: Confidence level (0.0-1.0)
        **kwargs: Additional fields
    
    Returns:
        Properly labeled response
    """
    
    response = {
        'value': value,
        'data_mode': DataMode.REAL.value,
        'source': source,
        'confidence': confidence,
        'disclaimer': DataIntegrityValidator.create_disclaimer(DataMode.REAL),
        **kwargs
    }
    
    # Validate before returning
    DataIntegrityValidator.validate_output(response, DataMode.REAL)
    
    return response


def create_derived_data_response(value: Any, source: str, confidence: float, 
                                 estimation_method: str, **kwargs) -> Dict[str, Any]:
    """
    Create properly labeled DERIVED data response
    
    Args:
        value: Estimated value
        source: Data source
        confidence: Confidence level (should be < 0.8 for derived data)
        estimation_method: How the value was estimated
        **kwargs: Additional fields
    
    Returns:
        Properly labeled response
    """
    
    if confidence >= 0.8:
        raise ValueError(
            f"DERIVED data should have confidence < 0.8 (got {confidence}). "
            f"High confidence suggests real measurement."
        )
    
    response = {
        'value': value,
        'data_mode': DataMode.DERIVED.value,
        'source': f"{source} (estimated)",
        'confidence': confidence,
        'estimation_method': estimation_method,
        'disclaimer': DataIntegrityValidator.create_disclaimer(
            DataMode.DERIVED,
            f"Estimated using: {estimation_method}"
        ),
        **kwargs
    }
    
    # Validate before returning
    DataIntegrityValidator.validate_output(response, DataMode.DERIVED)
    
    return response


def create_inferred_data_response(value: Any, inference_method: str, 
                                  confidence: float, **kwargs) -> Dict[str, Any]:
    """
    Create properly labeled INFERRED data response
    
    Args:
        value: Inferred value
        inference_method: How the value was inferred
        confidence: Plausibility level (NOT confirmation)
        **kwargs: Additional fields
    
    Returns:
        Properly labeled response
    """
    
    response = {
        'value': value,
        'data_mode': DataMode.INFERRED.value,
        'inference_method': inference_method,
        'plausibility': confidence,  # Use 'plausibility' not 'confidence'
        'disclaimer': DataIntegrityValidator.create_disclaimer(
            DataMode.INFERRED,
            f"Inferred using: {inference_method}. NOT physical evidence."
        ),
        **kwargs
    }
    
    # Validate before returning
    DataIntegrityValidator.validate_output(response, DataMode.INFERRED)
    
    return response


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("DATA INTEGRITY VALIDATOR - TESTS")
    print("="*80)
    
    # Test 1: REAL data (should pass)
    print("\n1. Test REAL data (should pass):")
    try:
        real_data = create_real_data_response(
            value=0.85,
            source="Sentinel-2 NDVI",
            confidence=0.9,
            acquisition_date="2026-01-26"
        )
        print("   ✅ REAL data validated")
        print(f"   Disclaimer: {real_data['disclaimer'][:50]}...")
    except ValueError as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 2: DERIVED data (should pass)
    print("\n2. Test DERIVED data (should pass):")
    try:
        derived_data = create_derived_data_response(
            value=0.7,
            source="NSIDC",
            confidence=0.7,
            estimation_method="Location-based seasonal model"
        )
        print("   ✅ DERIVED data validated")
        print(f"   Disclaimer: {derived_data['disclaimer'][:50]}...")
    except ValueError as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 3: INFERRED data (should pass)
    print("\n3. Test INFERRED data (should pass):")
    try:
        inferred_data = {
            'data_mode': 'INFERRED',
            'value': {'length': 120, 'width': 120},
            'inference_method': 'Geometric plausibility from thermal anomaly',
            'plausibility': 0.75,
            'disclaimer': 'Geometric/statistical inference. NOT physical proof. Requires field validation.'
        }
        DataIntegrityValidator.validate_output(inferred_data, DataMode.INFERRED)
        print("   ✅ INFERRED data validated")
        print(f"   Disclaimer: {inferred_data['disclaimer'][:50]}...")
    except ValueError as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 4: Forbidden language (should fail)
    print("\n4. Test forbidden language (should fail):")
    try:
        bad_data = {
            'data_mode': 'DERIVED',
            'value': 0.8,
            'description': 'Estructura detectada con alta confianza',
            'disclaimer': 'Some disclaimer'
        }
        DataIntegrityValidator.validate_output(bad_data, DataMode.DERIVED)
        print("   ❌ Should have failed!")
    except ValueError as e:
        print(f"   ✅ Correctly rejected: {str(e)[:60]}...")
    
    # Test 5: Missing disclaimer (should fail)
    print("\n5. Test missing disclaimer (should fail):")
    try:
        bad_data = {
            'data_mode': 'DERIVED',
            'value': 0.8
        }
        DataIntegrityValidator.validate_output(bad_data, DataMode.DERIVED)
        print("   ❌ Should have failed!")
    except ValueError as e:
        print(f"   ✅ Correctly rejected: {str(e)[:60]}...")
    
    # Test 6: Language sanitization
    print("\n6. Test language sanitization:")
    bad_text = "Estructura detectada con 85% de confianza. Sitio confirmado."
    sanitized = DataIntegrityValidator.sanitize_language(bad_text, DataMode.INFERRED)
    print(f"   Original: {bad_text}")
    print(f"   Sanitized: {sanitized}")
    
    # Test 7: Terminology checker
    print("\n7. Test terminology checker:")
    problematic_text = "Hemos detectado una estructura piramidal confirmada"
    issues = ScientificLanguageGuard.check_text(problematic_text)
    if issues:
        print(f"   Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - '{issue['problematic']}' → '{issue['suggestion']}'")
    
    print("\n" + "="*80)
    print("✅ Data Integrity Validator ready for use")
    print("="*80)
