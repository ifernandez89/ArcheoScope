"""
Sistema de Caché para Datos Satelitales
Optimiza velocidad evitando descargas repetidas
"""

import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pickle

logger = logging.getLogger(__name__)


class SatelliteCache:
    """
    Caché inteligente para datos satelitales
    
    Estrategia:
    - Caché en disco (JSON + pickle para arrays)
    - TTL: 7 días (datos satelitales no cambian rápido)
    - Key: hash de (bbox, fecha, tipo_dato)
    """
    
    def __init__(self, cache_dir: str = "cache/satellite"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.cache_dir / "metadata.json"
        self.ttl_days = 7
        
        # Cargar metadata
        self.metadata = self._load_metadata()
        
        logger.info(f"✅ Satellite cache initialized at {self.cache_dir}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Cargar metadata de caché"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache metadata: {e}")
                return {}
        return {}
    
    def _save_metadata(self):
        """Guardar metadata de caché"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata: {e}")
    
    def _generate_key(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        data_type: str,
        date: Optional[datetime] = None
    ) -> str:
        """
        Generar key única para caché
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Bounding box
            data_type: 'multispectral', 'sar', 'thermal'
            date: Fecha de adquisición (opcional)
        
        Returns:
            Hash MD5 como key
        """
        # Redondear coordenadas a 4 decimales (~11m precisión)
        bbox_str = f"{lat_min:.4f}_{lat_max:.4f}_{lon_min:.4f}_{lon_max:.4f}"
        
        # Fecha a nivel de día
        date_str = date.strftime("%Y%m%d") if date else "latest"
        
        # Combinar
        key_str = f"{bbox_str}_{data_type}_{date_str}"
        
        # Hash MD5
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        data_type: str,
        date: Optional[datetime] = None
    ) -> Optional[Any]:
        """
        Obtener datos de caché
        
        Returns:
            SatelliteData si existe y no expiró, None si no
        """
        key = self._generate_key(lat_min, lat_max, lon_min, lon_max, data_type, date)
        
        # Verificar si existe en metadata
        if key not in self.metadata:
            logger.debug(f"Cache MISS: {key}")
            return None
        
        entry = self.metadata[key]
        
        # Verificar TTL
        cached_date = datetime.fromisoformat(entry['cached_at'])
        age_days = (datetime.now() - cached_date).days
        
        if age_days > self.ttl_days:
            logger.info(f"Cache EXPIRED: {key} (age: {age_days} days)")
            self.delete(key)
            return None
        
        # Cargar datos
        cache_file = self.cache_dir / f"{key}.pkl"
        
        if not cache_file.exists():
            logger.warning(f"Cache file missing: {cache_file}")
            self.delete(key)
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
            
            # Marcar como cached
            data.cached = True
            
            logger.info(f"✅ Cache HIT: {key} (age: {age_days} days)")
            return data
            
        except Exception as e:
            logger.error(f"Error loading cache file {cache_file}: {e}")
            self.delete(key)
            return None
    
    def set(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        data_type: str,
        data: Any,
        date: Optional[datetime] = None
    ):
        """
        Guardar datos en caché
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Bounding box
            data_type: Tipo de dato
            data: SatelliteData a cachear
            date: Fecha de adquisición
        """
        key = self._generate_key(lat_min, lat_max, lon_min, lon_max, data_type, date)
        
        cache_file = self.cache_dir / f"{key}.pkl"
        
        try:
            # Guardar datos
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            
            # Actualizar metadata
            self.metadata[key] = {
                'bbox': [lat_min, lat_max, lon_min, lon_max],
                'data_type': data_type,
                'cached_at': datetime.now().isoformat(),
                'acquisition_date': data.acquisition_date.isoformat() if hasattr(data, 'acquisition_date') else None,
                'source': data.source if hasattr(data, 'source') else 'unknown',
                'file': str(cache_file)
            }
            
            self._save_metadata()
            
            logger.info(f"✅ Cached: {key} ({data_type})")
            
        except Exception as e:
            logger.error(f"Error caching data: {e}")
    
    def delete(self, key: str):
        """Eliminar entrada de caché"""
        if key in self.metadata:
            # Eliminar archivo
            cache_file = self.cache_dir / f"{key}.pkl"
            if cache_file.exists():
                cache_file.unlink()
            
            # Eliminar de metadata
            del self.metadata[key]
            self._save_metadata()
            
            logger.info(f"🗑️ Deleted cache: {key}")
    
    def clear_expired(self):
        """Limpiar entradas expiradas"""
        now = datetime.now()
        expired_keys = []
        
        for key, entry in self.metadata.items():
            cached_date = datetime.fromisoformat(entry['cached_at'])
            age_days = (now - cached_date).days
            
            if age_days > self.ttl_days:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)
        
        logger.info(f"🗑️ Cleared {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de caché"""
        total_entries = len(self.metadata)
        
        # Calcular tamaño total
        total_size_mb = 0
        for key in self.metadata:
            cache_file = self.cache_dir / f"{key}.pkl"
            if cache_file.exists():
                total_size_mb += cache_file.stat().st_size / (1024 * 1024)
        
        # Contar por tipo
        by_type = {}
        for entry in self.metadata.values():
            data_type = entry['data_type']
            by_type[data_type] = by_type.get(data_type, 0) + 1
        
        return {
            'total_entries': total_entries,
            'total_size_mb': round(total_size_mb, 2),
            'by_type': by_type,
            'cache_dir': str(self.cache_dir)
        }


# Instancia global
satellite_cache = SatelliteCache()
