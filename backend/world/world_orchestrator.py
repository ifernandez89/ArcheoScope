"""
World Orchestrator - Orquestador del sistema de campos

Pipeline completo:
1. User selects coord
2. Compute Base Field (determinista)
3. Load Dynamic Field (json)
4. Combine
5. HRM (1-3 ciclos)
6. Update Dynamic Field
7. Save JSON
8. LLM narra si hace falta

HRM = física estructural
LLM = interfaz narrativa
Separados.

Author: Kiro AI Assistant
Date: 22 Feb 2026
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

from .field_system import (
    base_field_system,
    dynamic_field_system,
    field_combiner
)
from .hrm_analyzer import HRMWorldAnalyzer
from .narrative_generator import NarrativeGenerator

logger = logging.getLogger(__name__)


class WorldOrchestrator:
    """
    Orquestador principal del sistema de campos
    
    Coordina:
    - Campo Base (determinista)
    - Campo Dinámico (evolutivo)
    - HRM (física estructural)
    - LLM (narrativa)
    """
    
    def __init__(
        self,
        hrm_checkpoint_path: str,
        llm_model: str = "qwen2.5:3b",
        ollama_url: str = "http://localhost:11434"
    ):
        self.hrm_analyzer = HRMWorldAnalyzer(hrm_checkpoint_path)
        self.narrative_generator = NarrativeGenerator(
            model_name=llm_model,
            ollama_url=ollama_url
        )
    
    def process_location(
        self,
        lat: float,
        lon: float,
        radius_km: float = 10.0,
        dem_data: Optional[np.ndarray] = None,
        weather_active: Optional[str] = None,
        weather_intensity: float = 1.0,
        hrm_cycles: int = 1,
        generate_narrative: bool = True
    ) -> Dict:
        """
        Procesa una ubicación completa
        
        Pipeline:
        1. Compute Base Field
        2. Load Dynamic Field
        3. Evolve offline if needed
        4. Apply weather if active
        5. Combine fields
        6. Run HRM
        7. Update Dynamic Field
        8. Save
        9. Generate narrative
        
        Args:
            lat: Latitud
            lon: Longitud
            radius_km: Radio de análisis
            dem_data: Datos de elevación (opcional)
            weather_active: Tipo de clima activo (opcional)
            weather_intensity: Intensidad del clima (0-1)
            hrm_cycles: Número de ciclos HRM a ejecutar
            generate_narrative: Si generar narrativa con LLM
        
        Returns:
            Dict con resultados completos
        """
        timestamp = datetime.now()
        
        logger.info(f"🌍 Processing location: ({lat:.4f}, {lon:.4f})")
        
        # 1. Compute Base Field (determinista)
        logger.info("📐 Computing base field...")
        base_field = base_field_system.compute(
            lat=lat,
            lon=lon,
            radius_km=radius_km,
            dem_data=dem_data,
            timestamp=timestamp
        )
        
        # 2. Load Dynamic Field
        logger.info("📂 Loading dynamic field...")
        dynamic_field_data = dynamic_field_system.load(lat, lon)
        
        # 3. Evolve offline if needed
        dynamic_field_data = dynamic_field_system.evolve_offline(
            dynamic_field_data,
            timestamp
        )
        
        # 4. Apply weather perturbation if active
        if weather_active:
            logger.info(f"🌩️ Applying weather: {weather_active}")
            dynamic_field_data = dynamic_field_system.apply_weather_perturbation(
                dynamic_field_data,
                weather_type=weather_active,
                intensity=weather_intensity
            )
        
        # 5. Combine fields
        logger.info("🔗 Combining fields...")
        combined_field = field_combiner.combine(base_field, dynamic_field_data)
        
        # 6. Convert to sequence for HRM
        token_sequence = field_combiner.to_sequence(combined_field)
        
        # 7. Run HRM (física estructural)
        logger.info(f"🧠 Running HRM ({hrm_cycles} cycles)...")
        hrm_results = self.hrm_analyzer.analyze_sequence(
            token_sequence,
            num_cycles=hrm_cycles
        )
        
        # 8. Update Dynamic Field based on HRM output
        logger.info("🔄 Updating dynamic field...")
        dynamic_field_data = self._update_dynamic_from_hrm(
            dynamic_field_data,
            hrm_results
        )
        
        # 9. Save Dynamic Field
        dynamic_field_system.save(lat, lon, dynamic_field_data)
        
        # 10. Generate narrative if requested
        narrative = None
        if generate_narrative and hrm_results.get('events'):
            logger.info("📖 Generating narrative...")
            narrative = self.narrative_generator.generate_narrative(
                events=hrm_results['events'],
                location={'lat': lat, 'lon': lon},
                context={
                    'weather': weather_active,
                    'instability': dynamic_field_data['instability_score']
                }
            )
        
        # Resultado completo
        return {
            'location': {'lat': lat, 'lon': lon, 'radius_km': radius_km},
            'timestamp': timestamp.isoformat(),
            'base_field': base_field.tolist(),
            'dynamic_field': dynamic_field_data,
            'combined_field': combined_field.tolist(),
            'hrm_results': hrm_results,
            'narrative': narrative,
            'metadata': {
                'deterministic': True,
                'hrm_cycles': hrm_cycles,
                'weather_active': weather_active,
                'cache_size': len(list(dynamic_field_system.cache_dir.glob('*.json')))
            }
        }
    
    def _update_dynamic_from_hrm(
        self,
        dynamic_field_data: Dict,
        hrm_results: Dict
    ) -> Dict:
        """
        Actualiza campo dinámico basado en output del HRM
        
        El HRM detecta patrones y eventos, que modifican el campo dinámico
        """
        # Extraer métricas del HRM
        instability = hrm_results.get('instability_score', 0.0)
        pattern_strength = hrm_results.get('pattern_strength', 0.0)
        
        # Actualizar instability score
        dynamic_field_data['instability_score'] = (
            dynamic_field_data['instability_score'] * 0.7 +
            instability * 0.3
        )
        
        # Si hay eventos significativos, modificar energy_modifier
        events = hrm_results.get('events', [])
        if events:
            energy_modifier = np.array(dynamic_field_data['energy_modifier']).reshape(8, 8)
            
            for event in events:
                if event.get('severity', 0) > 0.5:
                    # Evento significativo: añadir energía en zona afectada
                    affected_cells = event.get('affected_cells', [])
                    for cell_idx in affected_cells:
                        i = cell_idx // 8
                        j = cell_idx % 8
                        energy_modifier[i, j] = min(energy_modifier[i, j] + 1, 5)
            
            dynamic_field_data['energy_modifier'] = energy_modifier.flatten().tolist()
        
        return dynamic_field_data
    
    def apply_user_action(
        self,
        lat: float,
        lon: float,
        action_type: str,
        cell_i: int,
        cell_j: int,
        intensity: int = 1
    ) -> Dict:
        """
        Aplica acción del usuario en una celda específica
        
        Args:
            lat, lon: Ubicación
            action_type: Tipo de acción ('add_energy', 'remove_energy', etc.)
            cell_i, cell_j: Coordenadas de celda (0-7)
            intensity: Intensidad de la acción
        
        Returns:
            Dict con campo dinámico actualizado
        """
        logger.info(f"👆 User action: {action_type} at cell ({cell_i},{cell_j})")
        
        # Cargar campo dinámico
        dynamic_field_data = dynamic_field_system.load(lat, lon)
        
        # Aplicar acción
        if action_type == 'add_energy':
            delta = intensity
        elif action_type == 'remove_energy':
            delta = -intensity
        else:
            delta = 0
        
        dynamic_field_data = dynamic_field_system.apply_user_interaction(
            dynamic_field_data,
            cell_i,
            cell_j,
            delta
        )
        
        # Guardar
        dynamic_field_system.save(lat, lon, dynamic_field_data)
        
        return dynamic_field_data
    
    def get_world_state(self, lat: float, lon: float) -> Dict:
        """
        Obtiene estado actual del mundo en una ubicación
        
        Sin ejecutar HRM, solo retorna campos actuales
        """
        # Base field
        base_field = base_field_system.compute(lat, lon, 10.0)
        
        # Dynamic field
        dynamic_field_data = dynamic_field_system.load(lat, lon)
        
        # Combined
        combined_field = field_combiner.combine(base_field, dynamic_field_data)
        
        return {
            'location': {'lat': lat, 'lon': lon},
            'base_field': base_field.tolist(),
            'dynamic_field': dynamic_field_data,
            'combined_field': combined_field.tolist(),
            'timestamp': datetime.now().isoformat()
        }
    
    def cleanup_cache(self, days: int = 30) -> int:
        """Limpia caché antiguo"""
        return dynamic_field_system.cleanup_old_tiles(days)
    
    def get_cache_stats(self) -> Dict:
        """Obtiene estadísticas del caché"""
        cache_files = list(dynamic_field_system.cache_dir.glob('*.json'))
        
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_tiles': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(dynamic_field_system.cache_dir)
        }


# Instancia global
world_orchestrator = None


def initialize_orchestrator(
    hrm_checkpoint_path: str,
    llm_model: str = "qwen2.5:3b",
    ollama_url: str = "http://localhost:11434"
) -> WorldOrchestrator:
    """Inicializa orquestador global"""
    global world_orchestrator
    
    world_orchestrator = WorldOrchestrator(
        hrm_checkpoint_path=hrm_checkpoint_path,
        llm_model=llm_model,
        ollama_url=ollama_url
    )
    
    logger.info("✅ World Orchestrator initialized")
    
    return world_orchestrator
