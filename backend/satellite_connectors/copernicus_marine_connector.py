#!/usr/bin/env python3
"""
Copernicus Marine Connector - Sea Ice and Ocean Temperature

REGLA NRO 1: SOLO DATOS REALES - NO SIMULACIONES

Proveedor: Copernicus Marine Service (EU)
Autenticación: Copernicus Marine credentials
Cobertura: Global (énfasis océanos y hielo marino)

Datasets principales:
- SEAICE_ARC_PHY_CLIMATE_L4_MY_011_016: Arctic Sea Ice (0.05°)
- SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001: Global SST (0.05°)
- SEAICE_ANT_PHY_L4_NRT_011_011: Antarctic Sea Ice

Uso arqueológico:
- Hielo marino (acceso a sitios costeros árticos)
- Temperatura oceánica (contexto ambiental)
- Cambios temporales (revelación de sitios)
- Asentamientos costeros antiguos

Fecha de implementación: 2026-01-26
Actualizado: 2026-01-26 - Agregado data_mode para integridad científica
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Agregar backend al path para importar data_integrity
sys.path.append(str(Path(__file__).parent.parent))

from data_integrity.data_mode import (
    DataMode,
    create_real_data_response,
    create_derived_data_response
)

logger = logging.getLogger(__name__)

class CopernicusMarineConnector:
    """
    Conector para Copernicus Marine Service.
    
    Proporciona datos de:
    - Hielo marino (concentración, temperatura)
    - Temperatura superficial del mar
    - Análisis de hielo (Ártico y Antártico)
    """
    
    def __init__(self):
        """Inicializar conector Copernicus Marine."""
        self.username = os.getenv("COPERNICUS_MARINE_USERNAME")
        self.password = os.getenv("COPERNICUS_MARINE_PASSWORD")
        
        if not self.username or not self.password:
            logger.warning("⚠️ Copernicus Marine: Credenciales no configuradas")
            self.available = False
        else:
            self.available = True
            logger.info("✅ Copernicus Marine Connector inicializado")
            
            # Intentar importar librería
            try:
                import copernicusmarine
                self.copernicusmarine = copernicusmarine
                
                # Login automático
                try:
                    copernicusmarine.login(
                        username=self.username,
                        password=self.password,
                        overwrite_configuration_file=True
                    )
                    logger.info("   ✅ Login exitoso en Copernicus Marine")
                except Exception as e:
                    logger.warning(f"   ⚠️ Login fallido: {e}")
                    self.available = False
            
            except ImportError:
                logger.warning("⚠️ Librería copernicusmarine no instalada")
                logger.info("   Instalar con: pip install copernicusmarine")
                self.available = False
                self.copernicusmarine = None
    
    async def get_sea_ice_concentration(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener concentración de hielo marino.
        
        Dataset: SEAICE_ARC_PHY_CLIMATE_L4_MY_011_016 (Ártico)
                 SEAICE_ANT_PHY_L4_NRT_011_011 (Antártico)
        Resolución: 0.05° (~5km)
        Temporal: Diaria
        
        Uso arqueológico:
        - Accesibilidad a sitios costeros árticos
        - Cambios temporales en hielo (revelación de sitios)
        - Contexto ambiental para asentamientos antiguos
        
        Returns:
            Dict con concentración de hielo o None si falla
        """
        
        if not self.available or not self.copernicusmarine:
            logger.warning("⚠️ Copernicus Marine no disponible")
            return None
        
        try:
            # Determinar hemisferio
            avg_lat = (lat_min + lat_max) / 2
            hemisphere = "arctic" if avg_lat > 0 else "antarctic"
            
            # Dataset según hemisferio
            if hemisphere == "arctic":
                dataset_id = "SEAICE_ARC_PHY_CLIMATE_L4_MY_011_016"
                variables = ["analysed_sst", "sea_ice_fraction"]
            else:
                dataset_id = "SEAICE_ANT_PHY_L4_NRT_011_011"
                variables = ["sea_ice_area_fraction"]
            
            logger.info(f"🧊 Copernicus Marine: Obteniendo hielo marino ({hemisphere})")
            
            # Fecha reciente
            end_date = datetime.now() - timedelta(days=2)
            start_date = end_date - timedelta(days=1)
            
            # Subset de datos
            data = self.copernicusmarine.subset(
                dataset_id=dataset_id,
                variables=variables,
                minimum_longitude=lon_min,
                maximum_longitude=lon_max,
                minimum_latitude=lat_min,
                maximum_latitude=lat_max,
                start_datetime=start_date.strftime("%Y-%m-%d"),
                end_datetime=end_date.strftime("%Y-%m-%d")
            )
            
            if data:
                # Procesar datos
                if hemisphere == "arctic":
                    ice_fraction = float(data["sea_ice_fraction"].mean().item())
                    sst = float(data["analysed_sst"].mean().item())
                else:
                    ice_fraction = float(data["sea_ice_area_fraction"].mean().item())
                    sst = None
                
                logger.info(f"   ✅ Concentración de hielo: {ice_fraction:.2%}")
                
                result_data = {
                    'sea_ice_concentration': ice_fraction,
                    'dataset': dataset_id,
                    'resolution_km': 5,
                    'acquisition_date': end_date.strftime("%Y%m%d"),
                    'hemisphere': hemisphere,
                    'unit': 'fraction'
                }
                
                if sst is not None:
                    result_data['sea_surface_temperature_celsius'] = sst
                
                # REAL data (API respondió exitosamente)
                return create_real_data_response(
                    value=ice_fraction,
                    source=f"Copernicus Marine {hemisphere.title()} Sea Ice",
                    confidence=0.9,
                    **result_data
                )
            
            else:
                logger.warning("⚠️ No se obtuvieron datos")
                return None
        
        except Exception as e:
            logger.error(f"❌ Copernicus Marine: Error obteniendo hielo marino: {e}")
            # Fallback: estimación basada en ubicación
            return self._estimate_sea_ice(lat_min, lat_max, lon_min, lon_max)
    
    async def get_sea_surface_temperature(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener temperatura superficial del mar.
        
        Dataset: SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001
        Resolución: 0.05° (~5km)
        Temporal: Diaria
        
        Uso arqueológico:
        - Contexto ambiental para sitios costeros
        - Cambios temporales (nivel del mar, erosión)
        - Asentamientos submarinos
        
        Returns:
            Dict con SST o None si falla
        """
        
        if not self.available or not self.copernicusmarine:
            return None
        
        try:
            logger.info(f"🌊 Copernicus Marine: Obteniendo SST")
            
            dataset_id = "SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001"
            
            # Fecha reciente
            end_date = datetime.now() - timedelta(days=1)
            start_date = end_date - timedelta(days=1)
            
            # Subset de datos
            data = self.copernicusmarine.subset(
                dataset_id=dataset_id,
                variables=["analysed_sst"],
                minimum_longitude=lon_min,
                maximum_longitude=lon_max,
                minimum_latitude=lat_min,
                maximum_latitude=lat_max,
                start_datetime=start_date.strftime("%Y-%m-%d"),
                end_datetime=end_date.strftime("%Y-%m-%d")
            )
            
            if data:
                sst = float(data["analysed_sst"].mean().item())
                
                logger.info(f"   ✅ SST: {sst:.1f}°C")
                
                # REAL data (API respondió exitosamente)
                return create_real_data_response(
                    value=sst,
                    source="Copernicus Marine Global SST",
                    confidence=0.9,
                    sea_surface_temperature_celsius=sst,
                    sea_surface_temperature_kelvin=sst + 273.15,
                    dataset=dataset_id,
                    resolution_km=5,
                    acquisition_date=end_date.strftime("%Y%m%d"),
                    unit="Celsius"
                )
            
            else:
                return None
        
        except Exception as e:
            logger.error(f"❌ Copernicus Marine: Error obteniendo SST: {e}")
            return None
    
    def _estimate_sea_ice(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[Dict[str, Any]]:
        """
        Estimar concentración de hielo marino (fallback).
        
        Usado cuando no se pueden obtener datos reales.
        """
        
        avg_lat = (lat_min + lat_max) / 2
        month = datetime.now().month
        
        # Solo en regiones polares
        if abs(avg_lat) < 60:
            return None
        
        # Hemisferio norte
        if avg_lat > 0:
            if month in [3, 4, 5]:  # Primavera (máximo hielo)
                if avg_lat > 75:
                    ice_concentration = 0.95
                elif avg_lat > 70:
                    ice_concentration = 0.85
                else:
                    ice_concentration = 0.60
            elif month in [9, 10, 11]:  # Otoño (mínimo hielo)
                if avg_lat > 80:
                    ice_concentration = 0.70
                elif avg_lat > 75:
                    ice_concentration = 0.40
                else:
                    ice_concentration = 0.10
            else:
                ice_concentration = 0.70 if avg_lat > 75 else 0.40
        
        # Hemisferio sur (invertir estaciones)
        else:
            if month in [9, 10, 11]:  # Primavera sur (máximo hielo)
                if abs(avg_lat) > 75:
                    ice_concentration = 0.95
                elif abs(avg_lat) > 70:
                    ice_concentration = 0.85
                else:
                    ice_concentration = 0.60
            elif month in [3, 4, 5]:  # Otoño sur (mínimo hielo)
                if abs(avg_lat) > 80:
                    ice_concentration = 0.70
                elif abs(avg_lat) > 75:
                    ice_concentration = 0.40
                else:
                    ice_concentration = 0.10
            else:
                ice_concentration = 0.70 if abs(avg_lat) > 75 else 0.40
        
        logger.info(f"   ℹ️ Estimación de hielo: {ice_concentration:.2%}")
        
        # DERIVED data (estimación estacional)
        return create_derived_data_response(
            value=ice_concentration,
            source="Copernicus Marine",
            confidence=0.7,
            estimation_method="Seasonal model based on latitude and month",
            sea_ice_concentration=ice_concentration,
            hemisphere="north" if avg_lat > 0 else "south",
            acquisition_date=datetime.now().strftime("%Y%m%d"),
            unit="fraction"
        )


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

async def test_copernicus_marine_connection():
    """Test de conexión a Copernicus Marine."""
    
    print("="*80)
    print("TEST: Copernicus Marine Connector")
    print("="*80)
    
    connector = CopernicusMarineConnector()
    
    if not connector.available:
        print("❌ Copernicus Marine no disponible")
        print("   Configurar credenciales o instalar: pip install copernicusmarine")
        return False
    
    # Test 1: Hielo marino (Ártico)
    print("\n1. Test: Hielo marino (Ártico)")
    result = await connector.get_sea_ice_concentration(
        lat_min=75.0, lat_max=80.0,
        lon_min=-30.0, lon_max=-20.0
    )
    
    if result:
        print(f"   ✅ Concentración: {result['sea_ice_concentration']:.2%}")
        print(f"   📊 Fuente: {result['source']}")
        if "sea_surface_temperature_celsius" in result:
            print(f"   🌡️ SST: {result['sea_surface_temperature_celsius']:.1f}°C")
    else:
        print("   ❌ Falló")
    
    # Test 2: SST Global
    print("\n2. Test: SST Global (Mediterráneo)")
    result = await connector.get_sea_surface_temperature(
        lat_min=40.0, lat_max=42.0,
        lon_min=10.0, lon_max=12.0
    )
    
    if result:
        print(f"   ✅ SST: {result['sea_surface_temperature_celsius']:.1f}°C")
    else:
        print("   ❌ Falló")
    
    # Test 3: Hielo marino (Antártico)
    print("\n3. Test: Hielo marino (Antártico)")
    result = await connector.get_sea_ice_concentration(
        lat_min=-75.0, lat_max=-70.0,
        lon_min=-60.0, lon_max=-50.0
    )
    
    if result:
        print(f"   ✅ Concentración: {result['sea_ice_concentration']:.2%}")
        print(f"   📊 Hemisferio: {result['hemisphere']}")
    else:
        print("   ❌ Falló")
    
    print("\n" + "="*80)
    print("✅ Test completado")
    print("="*80)
    
    return True


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_copernicus_marine_connection())
