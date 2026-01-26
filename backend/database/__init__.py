"""
Database module - Gestión de base de datos
"""

from .measurements_logger import MeasurementsLogger

# Para compatibilidad con imports existentes
db = None  # Se inicializa en main.py

__all__ = ['MeasurementsLogger', 'db']
