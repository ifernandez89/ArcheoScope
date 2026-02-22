"""
HRMWorldAnalyzer - Ejecuta HRM sobre secuencia simbólica del mundo

Usa el checkpoint Maze (27M params) para analizar patrones jerárquicos
y predecir eventos emergentes.
"""

from typing import Dict, List, Tuple, Optional
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path


class HRMWorldAnalyzer:
    """
    Ejecuta HRM (Hierarchical Recurrent Memory) sobre secuencia simbólica
    
    El HRM tiene:
    - H-level: Visión global del mundo
    - L-level: Interacciones locales
    - Ciclos de refinamiento jerárquico
    
    Perfecto para detectar:
    - Patrones de inestabilidad
    - Eventos emergentes
    - Propagación de efectos
    - Transiciones de estado
    """
    
    def __init__(self, checkpoint_path: str, device: str = 'cpu'):
        """
        Inicializa HRM con checkpoint pre-entrenado
        
        Args:
            checkpoint_path: Ruta al checkpoint (maze_hrm_27M.pt)
            device: 'cpu' o 'cuda'
        """
        self.device = torch.device(device)
        self.model = self._load_model(checkpoint_path)
        self.model.eval()
        
        # Configuración
        self.vocab_size = 6  # 0-5 tokens
        self.seq_len = 64    # 64 zonas
        
    def _load_model(self, checkpoint_path: str) -> nn.Module:
        """
        Carga modelo HRM desde checkpoint
        
        TODO: Adaptar según estructura real del checkpoint
        """
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        
        # Extraer modelo
        if 'model' in checkpoint:
            model = checkpoint['model']
        elif 'state_dict' in checkpoint:
            # Reconstruir modelo desde state_dict
            model = self._build_hrm_model()
            model.load_state_dict(checkpoint['state_dict'])
        else:
            raise ValueError("Checkpoint format not recognized")
        
        model.to(self.device)
        return model
    
    def _build_hrm_model(self) -> nn.Module:
        """
        Construye arquitectura HRM según checkpoint real
        
        Arquitectura del checkpoint maze-30x30-hard:
        - hidden_size: 512
        - H_layers: 4, H_cycles: 2
        - L_layers: 4, L_cycles: 2
        - num_heads: 8
        - expansion: 4
        - pos_encodings: rope
        """
        try:
            # Intentar importar arquitectura real si existe
            from backend.hrm.hrm_act_v1 import HierarchicalReasoningModel_ACTV1
            
            # Configuración del checkpoint
            config = {
                'hidden_size': 512,
                'H_layers': 4,
                'H_cycles': 2,
                'L_layers': 4,
                'L_cycles': 2,
                'num_heads': 8,
                'expansion': 4,
                'vocab_size': 6,  # Reinterpretado para mundo (0-5)
                'max_seq_len': 64,  # 64 zonas
                'pos_encodings': 'rope'
            }
            
            model = HierarchicalReasoningModel_ACTV1(config)
            return model
            
        except ImportError:
            # Fallback: arquitectura simplificada compatible
            class HRMWorldModel(nn.Module):
                def __init__(self, vocab_size=6, hidden_size=512, h_layers=4, l_layers=4):
                    super().__init__()
                    self.hidden_size = hidden_size
                    self.vocab_size = vocab_size
                    
                    # Embedding
                    self.embedding = nn.Embedding(vocab_size, hidden_size)
                    
                    # H-level (global reasoning)
                    self.h_transformer = nn.TransformerEncoder(
                        nn.TransformerEncoderLayer(
                            d_model=hidden_size,
                            nhead=8,
                            dim_feedforward=hidden_size * 4,
                            batch_first=True
                        ),
                        num_layers=h_layers
                    )
                    
                    # L-level (local reasoning)
                    self.l_transformer = nn.TransformerEncoder(
                        nn.TransformerEncoderLayer(
                            d_model=hidden_size,
                            nhead=8,
                            dim_feedforward=hidden_size * 4,
                            batch_first=True
                        ),
                        num_layers=l_layers
                    )
                    
                    # Output head
                    self.output_head = nn.Linear(hidden_size, vocab_size)
                    
                def forward(self, x, num_cycles=2):
                    # Embedding
                    x = self.embedding(x)  # [batch, seq_len, hidden_size]
                    
                    # Ciclos H-level / L-level
                    for cycle in range(num_cycles):
                        # H-level: visión global
                        h_out = self.h_transformer(x)
                        
                        # L-level: refinamiento local
                        l_out = self.l_transformer(h_out)
                        
                        # Residual connection
                        x = x + l_out
                    
                    # Output logits
                    logits = self.output_head(x)
                    return logits
            
            return HRMWorldModel()
    
    def analyze(
        self, 
        symbolic_sequence: List[int], 
        cycles: int = 2,
        temperature: float = 1.0
    ) -> Dict:
        """
        Analiza secuencia simbólica con HRM
        
        Args:
            symbolic_sequence: Lista de 64 tokens (0-5)
            cycles: Número de ciclos H-level / L-level
            temperature: Temperatura para sampling (1.0 = normal)
            
        Returns:
            Dict con análisis estructurado
        """
        # Validar input
        assert len(symbolic_sequence) == self.seq_len, f"Expected {self.seq_len} tokens, got {len(symbolic_sequence)}"
        assert all(0 <= t <= 5 for t in symbolic_sequence), "Tokens must be in range 0-5"
        
        # Convertir a tensor
        input_tensor = torch.tensor(symbolic_sequence, dtype=torch.long).unsqueeze(0).to(self.device)
        
        # Ejecutar HRM
        with torch.no_grad():
            output_logits = self.model(input_tensor, num_cycles=cycles)
        
        # Procesar output
        output_probs = torch.softmax(output_logits / temperature, dim=-1)
        output_tokens = torch.argmax(output_probs, dim=-1).squeeze(0).cpu().numpy()
        
        # Analizar cambios
        analysis = self._interpret_output(
            input_sequence=symbolic_sequence,
            output_sequence=output_tokens.tolist(),
            output_probs=output_probs.squeeze(0).cpu().numpy()
        )
        
        return analysis
    
    def _interpret_output(
        self,
        input_sequence: List[int],
        output_sequence: List[int],
        output_probs: np.ndarray
    ) -> Dict:
        """
        Interpreta output del HRM
        
        Detecta:
        - Cambios de estado (transiciones)
        - Patrones globales (clusters)
        - Zonas afectadas
        - Nivel de confianza
        - Tipo de evento emergente
        """
        # 1. Detectar cambios de estado
        state_changes = self._detect_state_changes(input_sequence, output_sequence)
        
        # 2. Detectar patrones globales
        global_patterns = self._detect_global_patterns(output_sequence)
        
        # 3. Calcular confianza
        confidence = self._calculate_confidence(output_probs)
        
        # 4. Calcular nivel de inestabilidad
        instability = self._calculate_instability(output_sequence)
        
        # 5. Identificar zonas afectadas
        affected_zones = self._get_affected_zones(state_changes)
        
        # 6. Calcular vector de propagación
        propagation = self._calculate_propagation(state_changes)
        
        # 7. Predecir evento emergente
        emergent_event = self._predict_event(global_patterns, instability)
        
        # 8. Clasificar cambio de estado del mundo
        world_shift = self._classify_world_shift(state_changes, instability)
        
        return {
            "world_state_shift": world_shift,
            "emergent_event": emergent_event,
            "confidence": float(confidence),
            "instability_level": float(instability),
            "affected_zones": affected_zones,
            "propagation_vector": propagation,
            "state_changes": state_changes,
            "global_patterns": global_patterns,
            "output_sequence": output_sequence
        }
    
    def _detect_state_changes(
        self, 
        input_seq: List[int], 
        output_seq: List[int]
    ) -> List[Dict]:
        """
        Detecta cambios de estado entre input y output
        """
        changes = []
        
        for zone_id, (input_state, output_state) in enumerate(zip(input_seq, output_seq)):
            if input_state != output_state:
                changes.append({
                    "zone_id": zone_id,
                    "from_state": input_state,
                    "to_state": output_state,
                    "delta": output_state - input_state,
                    "region": self._get_region_name(zone_id)
                })
        
        return changes
    
    def _detect_global_patterns(self, sequence: List[int]) -> Dict:
        """
        Detecta patrones globales en la secuencia
        
        - Clusters de estados similares
        - Distribución de estados
        - Tendencias
        """
        # Distribución de estados
        state_counts = {i: sequence.count(i) for i in range(6)}
        
        # Estado dominante
        dominant_state = max(state_counts, key=state_counts.get)
        
        # Entropía de distribución
        total = len(sequence)
        probs = [count / total for count in state_counts.values()]
        entropy = -sum(p * np.log2(p + 1e-10) for p in probs if p > 0)
        
        # Detectar clusters (zonas contiguas con mismo estado)
        clusters = self._find_clusters(sequence)
        
        return {
            "state_distribution": state_counts,
            "dominant_state": dominant_state,
            "entropy": float(entropy),
            "num_clusters": len(clusters),
            "largest_cluster_size": max(len(c) for c in clusters) if clusters else 0
        }
    
    def _find_clusters(self, sequence: List[int]) -> List[List[int]]:
        """
        Encuentra clusters de zonas contiguas con mismo estado
        """
        clusters = []
        current_cluster = [0]
        
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i-1]:
                current_cluster.append(i)
            else:
                if len(current_cluster) > 1:
                    clusters.append(current_cluster)
                current_cluster = [i]
        
        if len(current_cluster) > 1:
            clusters.append(current_cluster)
        
        return clusters
    
    def _calculate_confidence(self, probs: np.ndarray) -> float:
        """
        Calcula confianza del modelo (0-1)
        
        Basado en entropía de las probabilidades
        """
        # Entropía promedio de todas las predicciones
        entropies = []
        for prob_dist in probs:
            entropy = -np.sum(prob_dist * np.log2(prob_dist + 1e-10))
            entropies.append(entropy)
        
        avg_entropy = np.mean(entropies)
        max_entropy = np.log2(6)  # 6 estados posibles
        
        # Confianza = 1 - (entropía normalizada)
        confidence = 1.0 - (avg_entropy / max_entropy)
        
        return float(np.clip(confidence, 0.0, 1.0))
    
    def _calculate_instability(self, sequence: List[int]) -> float:
        """
        Calcula nivel de inestabilidad del mundo (0-1)
        
        Basado en:
        - Cantidad de estados altos (3, 4, 5)
        - Variabilidad de estados
        """
        # Contar estados inestables
        unstable_count = sum(1 for s in sequence if s >= 3)
        unstable_ratio = unstable_count / len(sequence)
        
        # Variabilidad (desviación estándar)
        variability = np.std(sequence) / 2.5  # Normalizar (max std ≈ 2.5)
        
        # Combinar
        instability = (unstable_ratio * 0.7 + variability * 0.3)
        
        return float(np.clip(instability, 0.0, 1.0))
    
    def _get_affected_zones(self, state_changes: List[Dict]) -> List[int]:
        """
        Obtiene lista de zonas afectadas por cambios
        """
        return [change["zone_id"] for change in state_changes]
    
    def _calculate_propagation(self, state_changes: List[Dict]) -> Dict:
        """
        Calcula vector de propagación de efectos
        
        Detecta dirección y velocidad de propagación
        """
        if not state_changes:
            return {"direction": "none", "speed": 0.0, "intensity": 0.0}
        
        # Calcular centro de masa de cambios
        zone_ids = [c["zone_id"] for c in state_changes]
        center = np.mean(zone_ids)
        
        # Calcular dispersión
        spread = np.std(zone_ids)
        
        # Detectar dirección (basado en regiones afectadas)
        regions = [c["region"] for c in state_changes]
        dominant_region = max(set(regions), key=regions.count)
        
        # Calcular intensidad (promedio de deltas)
        deltas = [abs(c["delta"]) for c in state_changes]
        intensity = np.mean(deltas) / 5.0  # Normalizar
        
        return {
            "direction": dominant_region,
            "speed": float(spread / 64.0),  # Normalizar
            "intensity": float(intensity),
            "center": float(center)
        }
    
    def _predict_event(self, patterns: Dict, instability: float) -> str:
        """
        Predice tipo de evento emergente
        
        Basado en patrones globales y nivel de inestabilidad
        """
        dominant_state = patterns["dominant_state"]
        entropy = patterns["entropy"]
        
        # Lógica de predicción
        if instability > 0.8 and dominant_state >= 4:
            return "electromagnetic_storm"
        elif instability > 0.7 and entropy > 2.0:
            return "reality_fracture"
        elif instability > 0.6 and dominant_state == 3:
            return "temporal_anomaly"
        elif instability > 0.5:
            return "energy_surge"
        elif entropy > 2.5:
            return "chaos_wave"
        elif dominant_state == 5:
            return "dimensional_shift"
        else:
            return "minor_disturbance"
    
    def _classify_world_shift(self, state_changes: List[Dict], instability: float) -> str:
        """
        Clasifica cambio de estado del mundo
        """
        num_changes = len(state_changes)
        
        if num_changes == 0:
            return "stable"
        elif num_changes < 5:
            return "minor_fluctuation"
        elif num_changes < 15:
            return "moderate_shift"
        elif num_changes < 30:
            return "instability_increase"
        else:
            return "critical_transition"
    
    def _get_region_name(self, zone_id: int) -> str:
        """
        Obtiene nombre de región de la zona
        """
        if 0 <= zone_id <= 7:
            return "norte"
        elif 8 <= zone_id <= 15:
            return "este"
        elif 16 <= zone_id <= 23:
            return "sur"
        elif 24 <= zone_id <= 31:
            return "oeste"
        elif 32 <= zone_id <= 39:
            return "central"
        elif 40 <= zone_id <= 47:
            return "subterranea"
        elif 48 <= zone_id <= 55:
            return "atmosferica"
        elif 56 <= zone_id <= 63:
            return "temporal"
        else:
            return "desconocida"
    
    def simulate_propagation(
        self, 
        initial_sequence: List[int], 
        steps: int = 5,
        cycles_per_step: int = 2
    ) -> List[Dict]:
        """
        Simula propagación multi-step
        
        Ejecuta HRM múltiples veces para simular evolución temporal
        
        Args:
            initial_sequence: Secuencia inicial
            steps: Número de pasos de simulación
            cycles_per_step: Ciclos H/L por paso
            
        Returns:
            Lista de análisis por cada paso
        """
        results = []
        current_sequence = initial_sequence
        
        for step in range(steps):
            # Analizar estado actual
            analysis = self.analyze(current_sequence, cycles=cycles_per_step)
            analysis["step"] = step
            results.append(analysis)
            
            # Usar output como input del siguiente paso
            current_sequence = analysis["output_sequence"]
        
        # Detectar emergencia
        emergence = self._detect_emergence(results)
        
        return {
            "steps": results,
            "emergence": emergence,
            "final_instability": results[-1]["instability_level"],
            "total_changes": sum(len(r["state_changes"]) for r in results)
        }
    
    def _detect_emergence(self, results: List[Dict]) -> Dict:
        """
        Detecta emergencia en simulación multi-step
        
        Busca:
        - Escalamiento de inestabilidad
        - Propagación acelerada
        - Puntos de inflexión
        """
        instabilities = [r["instability_level"] for r in results]
        
        # Detectar tendencia
        if len(instabilities) > 1:
            trend = np.polyfit(range(len(instabilities)), instabilities, 1)[0]
        else:
            trend = 0.0
        
        # Detectar aceleración
        if len(instabilities) > 2:
            acceleration = instabilities[-1] - 2*instabilities[-2] + instabilities[-3]
        else:
            acceleration = 0.0
        
        # Detectar punto de inflexión
        inflection_point = None
        for i in range(1, len(instabilities) - 1):
            if instabilities[i] > instabilities[i-1] and instabilities[i] > instabilities[i+1]:
                inflection_point = i
                break
        
        return {
            "trend": "increasing" if trend > 0.05 else "decreasing" if trend < -0.05 else "stable",
            "acceleration": float(acceleration),
            "inflection_point": inflection_point,
            "peak_instability": float(max(instabilities)),
            "emergent": trend > 0.1 or acceleration > 0.2
        }
    
    def inject_player_action(
        self,
        symbolic_sequence: List[int],
        player_zone: int,
        action_intensity: float
    ) -> List[int]:
        """
        Inyecta perturbación del jugador en la secuencia
        
        Modifica tokens según acción del jugador
        
        Args:
            symbolic_sequence: Secuencia actual
            player_zone: Zona donde está el jugador (0-63)
            action_intensity: Intensidad de la acción (0-1)
            
        Returns:
            Secuencia modificada
        """
        modified_sequence = symbolic_sequence.copy()
        
        # Aumentar inestabilidad en zona del jugador
        delta = int(action_intensity * 2)
        modified_sequence[player_zone] = min(5, modified_sequence[player_zone] + delta)
        
        # Propagar a zonas adyacentes
        adjacent_zones = self._get_adjacent_zones(player_zone)
        for zone in adjacent_zones:
            modified_sequence[zone] = min(5, modified_sequence[zone] + 1)
        
        return modified_sequence
    
    def _get_adjacent_zones(self, zone_id: int) -> List[int]:
        """
        Obtiene zonas adyacentes a una zona
        
        Considera zonas en la misma región y regiones vecinas
        """
        adjacent = []
        
        # Zonas en la misma región (±1)
        if zone_id % 8 > 0:
            adjacent.append(zone_id - 1)
        if zone_id % 8 < 7:
            adjacent.append(zone_id + 1)
        
        # Zonas en regiones vecinas
        if zone_id >= 8:
            adjacent.append(zone_id - 8)
        if zone_id < 56:
            adjacent.append(zone_id + 8)
        
        return adjacent
