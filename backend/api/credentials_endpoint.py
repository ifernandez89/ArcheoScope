"""
Endpoint para obtener credenciales desencriptadas
SOLO para uso interno - NO exponer públicamente
"""

from fastapi import APIRouter, HTTPException
from credentials_manager import CredentialsManager

router = APIRouter(prefix="/api/credentials", tags=["credentials"])

@router.get("/{service_name}/{credential_key}")
async def get_credential(service_name: str, credential_key: str):
    """
    Obtener credencial desencriptada desde la BD
    
    Args:
        service_name: Nombre del servicio (ej: 'openrouter')
        credential_key: Clave de la credencial (ej: 'api_key')
    
    Returns:
        dict con la credencial desencriptada
    """
    try:
        manager = CredentialsManager()
        value = manager.get_credential(service_name, credential_key)
        
        if value is None:
            raise HTTPException(
                status_code=404,
                detail=f"Credential not found: {service_name}.{credential_key}"
            )
        
        return {
            "service": service_name,
            "key": credential_key,
            "value": value,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving credential: {str(e)}"
        )
