#!/usr/bin/env python3
"""
Sistema de Logging Centralizado para ArcheoScope
===============================================

Configuración unificada de logging para reemplazar print() statements
sin alterar lógica de negocio.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = "archeoscope", level: str = None) -> logging.Logger:
    """
    Configurar logger centralizado.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configurado
    """
    
    # Determinar nivel desde env o parámetro
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Crear logger
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level, logging.INFO))
    
    # Formato de log
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (opcional)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        # Crear directorio si no existe
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger por defecto para el proyecto
logger = setup_logger()

# Funciones de conveniencia para reemplazar print()
def info(message: str):
    """Log info message (reemplazo directo de print)"""
    logger.info(message)

def debug(message: str):
    """Log debug message"""
    logger.debug(message)

def warning(message: str):
    """Log warning message"""
    logger.warning(message)

def error(message: str):
    """Log error message"""
    logger.error(message)

def critical(message: str):
    """Log critical message"""
    logger.critical(message)

# Alias para compatibilidad
log_info = info
log_debug = debug
log_warning = warning
log_error = error