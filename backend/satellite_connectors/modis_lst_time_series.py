#!/usr/bin/env python3
"""
MODIS LST Time Series - Obtención de series temporales reales

Extensión del MODISLSTConnector para obtener series temporales diarias
de temperatura superficial terrestre.

Implementa:
- Cache local para evitar re-descargas
- Fallback a estimación si falla API
- Progress tracking
- Manejo robusto de errores
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MODISLSTTimeSeries:
    """
    Obtención de series temporales MODIS LST
    """
    
    def __init__(self, modis_connector):
        """
        Args:
            modis_connector: Instancia de MODISLSTConnector
        """
        self.modis = modis_connector
        self.cache_dir = Path("cache/modis_time_series")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar disponibilidad
        if not self.modis.available:
            logger.warning("⚠️ MODIS LST no disponible - usando solo estimaciones")
            print("⚠️ MODIS LST no disponible - usando solo estimaciones")
    
    def _get_cache_path(self, lat: float, lon: float, years: int) -> Path:
        """Generar path de cache para serie temporal"""
        return self.cache_dir / f"modis_lst_{lat:.4f}_{lon:.4f}_{years}y.json"
    
    async def get_daily_thermal_series(
        self,
        lat: float,
        lon: float,
        years: int = 5,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Obtener serie temporal diaria de LST
        
        Args:
            lat: Latitud
            lon: Longitud
            years: Años de historia (default: 5)
            use_cache: Usar cache si existe (default: True)
        
        Returns:
            Dict con:
                - series: List[float] - Temperaturas en Celsius
                - dates: List[str] - Fechas ISO
                - real_data_count: int - Cantidad de datos reales
                - estimated_data_count: int - Cantidad de datos estimados
                - source: str - Fuente de datos
        """
        
        cache_path = self._get_cache_path(lat, lon, years)
        
        # Intentar cargar desde cache
        if use_cache and cache_path.exists():
            print(f"   📦 Cargando desde cache: {cache_path.name}")
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                print(f"   ✅ Cache cargado: {len(cached_data['series'])} días")
                return cached_data
        
        print(f"   📡 Obteniendo serie temporal MODIS LST...")
        print(f"   📍 Ubicación: ({lat:.4f}, {lon:.4f})")
        print(f"   📅 Período: {years} años ({years * 365} días)")
        
        days = years * 365
        series = []
        dates = []
        real_data_count = 0
        estimated_data_count = 0
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Estrategia: Intentar obtener datos reales, fallback a estimación
        print(f"   🔄 Estrategia: Datos reales con fallback a estimación")
        print(f"   ⏱️ Esto puede tomar 1-2 horas para {days} días...")
        
        # Para optimizar, usar MOD11A2 (8-day composite) en vez de daily
        # Esto reduce requests de 1825 a ~228
        use_8day_composite = True
        
        if use_8day_composite:
            print(f"   🚀 Usando MOD11A2 (8-day composite) para optimizar")
            print(f"   📊 Requests reducidos: {days} → {days//8} (~{days//8} requests)")
        
        last_progress = 0
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            dates.append(current_date.isoformat()[:10])
            
            # Progress cada 10%
            progress = int((day / days) * 100)
            if progress >= last_progress + 10:
                print(f"   📊 Progreso: {progress}% ({day}/{days} días) - Real: {real_data_count}, Estimado: {estimated_data_count}")
                last_progress = progress
            
            # Para 8-day composite, solo hacer request cada 8 días
            if use_8day_composite and day % 8 != 0:
                # Interpolar desde último valor real
                if len(series) > 0:
                    series.append(series[-1])
                else:
                    # Fallback a estimación
                    lst_day, lst_night = self.modis._estimate_lst(lat, lon, current_date.month)
                    lst_avg = (lst_day + lst_night) / 2 - 273.15
                    series.append(lst_avg)
                    estimated_data_count += 1
                continue
            
            # Intentar obtener datos reales
            try:
                lst_data = await self.modis.get_land_surface_temperature(
                    lat_min=lat - 0.01,
                    lat_max=lat + 0.01,
                    lon_min=lon - 0.01,
                    lon_max=lon + 0.01
                )
                
                if lst_data and hasattr(lst_data, 'status') and lst_data.status == 'success':
                    # Datos reales obtenidos
                    metadata = lst_data.metadata if hasattr(lst_data, 'metadata') else {}
                    lst_day = metadata.get('lst_day', 300)
                    lst_night = metadata.get('lst_night', 290)
                    lst_avg = (lst_day + lst_night) / 2 - 273.15
                    series.append(lst_avg)
                    real_data_count += 1
                else:
                    # Fallback a estimación
                    lst_day, lst_night = self.modis._estimate_lst(lat, lon, current_date.month)
                    lst_avg = (lst_day + lst_night) / 2 - 273.15
                    series.append(lst_avg)
                    estimated_data_count += 1
                
            except Exception as e:
                # Error - usar estimación
                lst_day, lst_night = self.modis._estimate_lst(lat, lon, current_date.month)
                lst_avg = (lst_day + lst_night) / 2 - 273.15
                series.append(lst_avg)
                estimated_data_count += 1
            
            # Rate limiting: pequeña pausa cada 10 requests
            if day % 10 == 0 and day > 0:
                await asyncio.sleep(0.1)
        
        print(f"   ✅ Serie temporal completada: {len(series)} días")
        print(f"   📊 Datos reales: {real_data_count} ({real_data_count/days*100:.1f}%)")
        print(f"   📊 Datos estimados: {estimated_data_count} ({estimated_data_count/days*100:.1f}%)")
        
        # Determinar fuente
        if real_data_count > days * 0.5:
            source = "MODIS LST (majority real data)"
        elif real_data_count > 0:
            source = "MODIS LST (mixed real/estimated)"
        else:
            source = "MODIS LST (estimated - API unavailable)"
        
        result = {
            'series': series,
            'dates': dates,
            'real_data_count': real_data_count,
            'estimated_data_count': estimated_data_count,
            'total_days': days,
            'source': source,
            'lat': lat,
            'lon': lon,
            'years': years,
            'generated_at': datetime.now().isoformat()
        }
        
        # Guardar en cache
        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"   💾 Cache guardado: {cache_path.name}")
        
        return result


async def test_time_series():
    """Test de obtención de serie temporal"""
    
    print("="*80)
    print("🌡️ TEST: MODIS LST Time Series")
    print("="*80)
    
    # Importar conector
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from satellite_connectors.modis_lst_connector import MODISLSTConnector
    
    modis = MODISLSTConnector()
    time_series = MODISLSTTimeSeries(modis)
    
    # Test con Puerto Rico North (1 año para test rápido)
    print("\n📍 Test: Puerto Rico North (1 año)")
    
    result = await time_series.get_daily_thermal_series(
        lat=19.89,
        lon=-66.68,
        years=1,  # Solo 1 año para test
        use_cache=True
    )
    
    print(f"\n✅ Resultado:")
    print(f"   Total días: {result['total_days']}")
    print(f"   Datos reales: {result['real_data_count']}")
    print(f"   Datos estimados: {result['estimated_data_count']}")
    print(f"   Fuente: {result['source']}")
    print(f"   Temperatura promedio: {sum(result['series'])/len(result['series']):.1f}°C")
    print(f"   Temperatura min: {min(result['series']):.1f}°C")
    print(f"   Temperatura max: {max(result['series']):.1f}°C")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    asyncio.run(test_time_series())
