#!/usr/bin/env python3
"""
Test Completo de APIs Reales - ArcheoScope
Prueba accesibilidad, tiempo de respuesta y funcionalidad de cada API
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from satellite_connectors.planetary_computer import PlanetaryComputerConnector
from satellite_connectors.icesat2_connector import ICESat2Connector
from satellite_connectors.opentopography_connector import OpenTopographyConnector
from satellite_connectors.copernicus_marine_connector import CopernicusMarineConnector
from satellite_connectors.modis_connector import MODISConnector
from satellite_connectors.palsar_connector import PALSARConnector
from satellite_connectors.smos_connector import SMOSConnector
from satellite_connectors.smap_connector import SMAPConnector
from satellite_connectors.nsidc_connector import NSIDCConnector


class APITester:
    """Tester completo de APIs reales"""
    
    def __init__(self):
        self.results = []
        self.test_coords = {
            'name': 'Giza Pyramids (Test)',
            'lat_min': 29.97,
            'lat_max': 29.98,
            'lon_min': 31.13,
            'lon_max': 31.14
        }
    
    async def test_api(
        self,
        name: str,
        connector,
        method_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Probar una API específica"""
        
        print(f"\n{'='*60}")
        print(f"🧪 Testing: {name}")
        print(f"{'='*60}")
        
        result = {
            'api_name': name,
            'available': connector.available,
            'tested_at': datetime.now().isoformat(),
            'success': False,
            'response_time_s': None,
            'error': None,
            'data_received': False,
            'data_quality': None
        }
        
        if not connector.available:
            print(f"⚠️  {name} no disponible (falta configuración)")
            result['error'] = 'Not configured'
            return result
        
        try:
            print(f"📡 Conectando a {name}...")
            start_time = time.time()
            
            # Llamar al método
            method = getattr(connector, method_name)
            data = await method(**kwargs)
            
            response_time = time.time() - start_time
            result['response_time_s'] = round(response_time, 2)
            
            if data:
                result['success'] = True
                result['data_received'] = True
                
                # Evaluar calidad de datos
                if hasattr(data, 'indices'):
                    result['data_quality'] = 'good'
                    result['indices'] = data.indices
                elif isinstance(data, dict):
                    result['data_quality'] = 'good'
                    result['data_sample'] = {k: v for k, v in list(data.items())[:5]}
                
                print(f"✅ {name} - OK")
                print(f"   Tiempo de respuesta: {response_time:.2f}s")
                print(f"   Datos recibidos: ✅")
                
            else:
                result['success'] = False
                result['error'] = 'No data returned'
                print(f"⚠️  {name} - Sin datos")
        
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {name} - Error: {e}")
        
        return result
    
    async def test_all_apis(self):
        """Probar todas las APIs"""
        
        print("\n" + "="*60)
        print("🚀 INICIANDO TESTS DE APIS REALES")
        print("="*60)
        print(f"Coordenadas de prueba: {self.test_coords['name']}")
        print(f"Lat: {self.test_coords['lat_min']}-{self.test_coords['lat_max']}")
        print(f"Lon: {self.test_coords['lon_min']}-{self.test_coords['lon_max']}")
        
        # 1. Planetary Computer - Sentinel-2
        pc = PlanetaryComputerConnector()
        result = await self.test_api(
            "Planetary Computer - Sentinel-2",
            pc,
            "get_multispectral_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 2. Planetary Computer - Sentinel-1
        result = await self.test_api(
            "Planetary Computer - Sentinel-1 SAR",
            pc,
            "get_sar_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 3. Planetary Computer - Landsat
        result = await self.test_api(
            "Planetary Computer - Landsat Thermal",
            pc,
            "get_thermal_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 4. ICESat-2
        icesat2 = ICESat2Connector()
        result = await self.test_api(
            "NASA ICESat-2",
            icesat2,
            "get_elevation_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 5. OpenTopography
        opentopo = OpenTopographyConnector()
        result = await self.test_api(
            "OpenTopography DEM",
            opentopo,
            "get_dem_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 6. Copernicus Marine (solo en zonas polares)
        copernicus = CopernicusMarineConnector()
        result = await self.test_api(
            "Copernicus Marine - Sea Ice",
            copernicus,
            "get_sea_ice_data",
            lat_min=70.0,  # Ártico
            lat_max=71.0,
            lon_min=-180.0,
            lon_max=-179.0
        )
        self.results.append(result)
        
        # 7. NSIDC (no requiere coordenadas específicas)
        nsidc = NSIDCConnector()
        result = await self.test_api(
            "NSIDC Ice Extent",
            nsidc,
            "get_ice_extent_timeseries",
            hemisphere="north",
            start_year=2020,
            end_year=2023
        )
        self.results.append(result)
        
        # 8. MODIS
        modis = MODISConnector()
        result = await self.test_api(
            "MODIS Thermal",
            modis,
            "get_lst_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 9. PALSAR
        palsar = PALSARConnector()
        result = await self.test_api(
            "PALSAR L-band",
            palsar,
            "get_lband_data",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 10. SMOS
        smos = SMOSConnector()
        result = await self.test_api(
            "SMOS Soil Moisture",
            smos,
            "get_soil_moisture",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
        
        # 11. SMAP
        smap = SMAPConnector()
        result = await self.test_api(
            "SMAP Soil Moisture",
            smap,
            "get_soil_moisture",
            lat_min=self.test_coords['lat_min'],
            lat_max=self.test_coords['lat_max'],
            lon_min=self.test_coords['lon_min'],
            lon_max=self.test_coords['lon_max']
        )
        self.results.append(result)
    
    def generate_report(self) -> Dict[str, Any]:
        """Generar reporte completo"""
        
        total_apis = len(self.results)
        available_apis = sum(1 for r in self.results if r['available'])
        successful_apis = sum(1 for r in self.results if r['success'])
        
        avg_response_time = None
        if successful_apis > 0:
            response_times = [r['response_time_s'] for r in self.results if r['response_time_s']]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
        
        report = {
            'test_date': datetime.now().isoformat(),
            'test_location': self.test_coords,
            'summary': {
                'total_apis': total_apis,
                'available_apis': available_apis,
                'successful_apis': successful_apis,
                'failed_apis': available_apis - successful_apis,
                'not_configured': total_apis - available_apis,
                'success_rate': (successful_apis / available_apis * 100) if available_apis > 0 else 0,
                'avg_response_time_s': round(avg_response_time, 2) if avg_response_time else None
            },
            'apis': self.results
        }
        
        return report
    
    def print_summary(self, report: Dict[str, Any]):
        """Imprimir resumen"""
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE TESTS")
        print("="*60)
        
        summary = report['summary']
        
        print(f"\nAPIs Totales: {summary['total_apis']}")
        print(f"APIs Disponibles: {summary['available_apis']}")
        print(f"APIs Exitosas: {summary['successful_apis']} ✅")
        print(f"APIs Fallidas: {summary['failed_apis']} ❌")
        print(f"APIs No Configuradas: {summary['not_configured']} ⚠️")
        print(f"Tasa de Éxito: {summary['success_rate']:.1f}%")
        
        if summary['avg_response_time_s']:
            print(f"Tiempo Promedio: {summary['avg_response_time_s']:.2f}s")
        
        print("\n" + "-"*60)
        print("DETALLE POR API")
        print("-"*60)
        
        for result in self.results:
            status = "✅" if result['success'] else ("⚠️" if not result['available'] else "❌")
            time_str = f"{result['response_time_s']:.2f}s" if result['response_time_s'] else "N/A"
            
            print(f"{status} {result['api_name']:<40} {time_str:>8}")
            
            if result['error'] and result['available']:
                print(f"   Error: {result['error']}")
        
        print("\n" + "="*60)
        
        if summary['success_rate'] >= 50:
            print("✅ Sistema listo para usar datos reales")
        elif summary['success_rate'] > 0:
            print("⚠️  Sistema parcialmente funcional - configura más APIs")
        else:
            print("❌ Sistema no funcional - configura API keys")
        
        print("="*60)
    
    def save_report(self, report: Dict[str, Any]):
        """Guardar reporte en JSON"""
        
        filename = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Reporte guardado: {filename}")


async def main():
    """Ejecutar tests"""
    
    tester = APITester()
    
    try:
        await tester.test_all_apis()
        report = tester.generate_report()
        tester.print_summary(report)
        tester.save_report(report)
        
        # Retornar código de salida basado en éxito
        success_rate = report['summary']['success_rate']
        return 0 if success_rate >= 50 else 1
    
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
