"""
Configuración para HRM-World Engine

Variables de entorno y configuración centralizada
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class WorldEngineConfig:
    """Configuración del World Engine"""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    CHECKPOINT_DIR = BASE_DIR / "hrm" / "checkpoints"
    MAZE_CHECKPOINT = CHECKPOINT_DIR / "maze-30x30-hard" / "checkpoint"
    SUDOKU_CHECKPOINT = CHECKPOINT_DIR / "sudoku-extreme" / "checkpoint"
    
    # HRM Configuration
    HRM_CHECKPOINT_PATH: str = os.getenv(
        "HRM_CHECKPOINT_PATH",
        str(MAZE_CHECKPOINT)
    )
    HRM_DEVICE: str = os.getenv("HRM_DEVICE", "cpu")
    HRM_CYCLES: int = int(os.getenv("HRM_CYCLES", "2"))
    
    # LLM Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen2.5:3b")
    LLM_SMALL_MODEL: str = os.getenv("LLM_SMALL_MODEL", "qwen2.5:0.5b")
    LLM_MEDIUM_MODEL: str = os.getenv("LLM_MEDIUM_MODEL", "qwen2.5:1.5b")
    LLM_LARGE_MODEL: str = os.getenv("LLM_LARGE_MODEL", "qwen2.5:3b")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    # World Configuration
    WORLD_ZONES: int = int(os.getenv("WORLD_ZONES", "64"))
    ENABLE_PROPAGATION: bool = os.getenv("ENABLE_PROPAGATION", "true").lower() == "true"
    PROPAGATION_STEPS: int = int(os.getenv("PROPAGATION_STEPS", "3"))
    ENABLE_CASCADE: bool = os.getenv("ENABLE_CASCADE", "true").lower() == "true"
    
    # Performance
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "100"))
    CACHE_SIZE: int = int(os.getenv("CACHE_SIZE", "1000"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8003"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "1"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)
    
    # Monitoring
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_INTERVAL: int = int(os.getenv("METRICS_INTERVAL", "60"))
    
    @classmethod
    def validate(cls) -> bool:
        """Valida configuración"""
        errors = []
        
        # Verificar checkpoint
        if not Path(cls.HRM_CHECKPOINT_PATH).exists():
            errors.append(f"Checkpoint no encontrado: {cls.HRM_CHECKPOINT_PATH}")
        
        # Verificar device
        if cls.HRM_DEVICE not in ["cpu", "cuda"]:
            errors.append(f"Device inválido: {cls.HRM_DEVICE}")
        
        # Verificar zonas
        if cls.WORLD_ZONES not in [32, 64, 128]:
            errors.append(f"Número de zonas inválido: {cls.WORLD_ZONES}")
        
        if errors:
            print("❌ Errores de configuración:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Imprime configuración actual"""
        print("\n" + "="*60)
        print("HRM-WORLD ENGINE - CONFIGURACIÓN")
        print("="*60)
        
        print("\n[HRM]")
        print(f"  Checkpoint: {cls.HRM_CHECKPOINT_PATH}")
        print(f"  Device: {cls.HRM_DEVICE}")
        print(f"  Cycles: {cls.HRM_CYCLES}")
        
        print("\n[LLM]")
        print(f"  Model: {cls.LLM_MODEL}")
        print(f"  Small: {cls.LLM_SMALL_MODEL}")
        print(f"  Medium: {cls.LLM_MEDIUM_MODEL}")
        print(f"  Large: {cls.LLM_LARGE_MODEL}")
        print(f"  Ollama URL: {cls.OLLAMA_URL}")
        
        print("\n[World]")
        print(f"  Zones: {cls.WORLD_ZONES}")
        print(f"  Propagation: {cls.ENABLE_PROPAGATION}")
        print(f"  Propagation Steps: {cls.PROPAGATION_STEPS}")
        print(f"  Cascade: {cls.ENABLE_CASCADE}")
        
        print("\n[Performance]")
        print(f"  Max History: {cls.MAX_HISTORY}")
        print(f"  Cache Size: {cls.CACHE_SIZE}")
        
        print("\n[API]")
        print(f"  Host: {cls.API_HOST}")
        print(f"  Port: {cls.API_PORT}")
        print(f"  Workers: {cls.API_WORKERS}")
        
        print("\n[Logging]")
        print(f"  Level: {cls.LOG_LEVEL}")
        print(f"  File: {cls.LOG_FILE or 'None'}")
        
        print("\n[Monitoring]")
        print(f"  Metrics: {cls.ENABLE_METRICS}")
        print(f"  Interval: {cls.METRICS_INTERVAL}s")
        
        print("\n" + "="*60 + "\n")


# Configuración por defecto
config = WorldEngineConfig()


if __name__ == "__main__":
    # Validar y mostrar configuración
    config.print_config()
    
    if config.validate():
        print("✅ Configuración válida")
    else:
        print("❌ Configuración inválida")
        exit(1)
