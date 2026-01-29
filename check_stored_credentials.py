#!/usr/bin/env python3
"""
Check Stored Credentials - Ver qué credenciales están en BD
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.credentials_manager import CredentialsManager

def main():
    print("="*80)
    print("CREDENCIALES ALMACENADAS EN BD")
    print("="*80)
    print()
    
    cm = CredentialsManager()
    
    # Listar todos los servicios
    services = cm.list_services()
    
    if not services:
        print("❌ No hay credenciales almacenadas en BD")
        print()
        print("💡 Para agregar credenciales, ejecutar:")
        print("   python migrate_credentials_to_db.py")
        return
    
    print(f"Total servicios: {len(services)}")
    print()
    
    for service in services:
        service_name = service['service_name']
        description = service.get('description', 'N/A')
        updated_at = service.get('updated_at', 'N/A')
        
        print(f"📦 {service_name}")
        print(f"   Descripción: {description}")
        print(f"   Actualizado: {updated_at}")
        
        # Obtener todas las credenciales del servicio
        creds = cm.get_all_credentials(service_name)
        
        if creds:
            print(f"   Credenciales:")
            for key, value in creds.items():
                # Mostrar solo primeros caracteres por seguridad
                if len(value) > 20:
                    display_value = f"{value[:10]}...{value[-5:]}"
                else:
                    display_value = f"{value[:10]}..."
                print(f"      - {key}: {display_value}")
        else:
            print(f"   ⚠️ Sin credenciales")
        
        print()
    
    print("="*80)
    print()


if __name__ == "__main__":
    main()
