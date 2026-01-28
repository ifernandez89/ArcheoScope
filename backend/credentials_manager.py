#!/usr/bin/env python3
"""
Sistema de Gestión de Credenciales Encriptadas
Almacena credenciales de APIs en BD con encriptación AES-256
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from typing import Optional, Dict
from dotenv import load_dotenv
from .logger import info, error

load_dotenv()


class CredentialsManager:
    """
    Gestor de credenciales encriptadas en BD
    
    Usa AES-256 con clave derivada de PBKDF2
    """
    
    def __init__(self):
        """Inicializar gestor de credenciales"""
        self.db_url = os.getenv("DATABASE_URL")
        
        # Generar clave de encriptación desde variable de entorno
        master_password = os.getenv("CREDENTIALS_MASTER_KEY")
        env = os.getenv("ENV", "development")
        
        if not master_password:
            if env == "production":
                raise RuntimeError("CREDENTIALS_MASTER_KEY is required in production")
            else:
                info("⚠️  WARNING: Using default master key in development. Set CREDENTIALS_MASTER_KEY for production!")
                master_password = "archeoscope-default-key-dev-only"
        
        self.cipher = self._create_cipher(master_password)
        
        # Crear tabla si no existe
        self._create_table()
    
    def _create_cipher(self, password: str) -> Fernet:
        """Crear cipher Fernet desde password"""
        # Derivar clave de 32 bytes usando PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'archeoscope-salt-v1',  # Salt fijo (OK para este caso)
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def _create_table(self):
        """Crear tabla de credenciales si no existe"""
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS api_credentials (
                    id SERIAL PRIMARY KEY,
                    service_name VARCHAR(100) NOT NULL,
                    credential_key VARCHAR(100) NOT NULL,
                    credential_value_encrypted TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(service_name, credential_key)
                )
            """)
            
            # Índice para búsqueda rápida
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_service_key 
                ON api_credentials(service_name, credential_key)
            """)
            
            conn.commit()
            cur.close()
            conn.close()
            
            info("[OK] Tabla api_credentials lista")
            
        except Exception as e:
            error(f"[ERROR] Creando tabla de credenciales: {e}")
    
    def store_credential(self, service_name: str, credential_key: str, 
                        credential_value: str, description: str = "") -> bool:
        """
        Almacenar credencial encriptada en BD
        
        Args:
            service_name: Nombre del servicio (ej: 'earthdata', 'copernicus')
            credential_key: Clave de la credencial (ej: 'username', 'password', 'api_key')
            credential_value: Valor de la credencial (se encriptará)
            description: Descripción opcional
        
        Returns:
            True si se guardó correctamente
        """
        try:
            # Encriptar valor
            encrypted_value = self.cipher.encrypt(credential_value.encode()).decode()
            
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            
            # Upsert (insertar o actualizar)
            cur.execute("""
                INSERT INTO api_credentials (service_name, credential_key, credential_value_encrypted, description)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (service_name, credential_key) 
                DO UPDATE SET 
                    credential_value_encrypted = EXCLUDED.credential_value_encrypted,
                    description = EXCLUDED.description,
                    updated_at = CURRENT_TIMESTAMP
            """, (service_name, credential_key, encrypted_value, description))
            
            conn.commit()
            cur.close()
            conn.close()
            
            info(f"[OK] Credencial guardada: {service_name}.{credential_key}")
            return True
            
        except Exception as e:
            error(f"[ERROR] Guardando credencial {service_name}.{credential_key}: {e}")
            return False
    
    def get_credential(self, service_name: str, credential_key: str) -> Optional[str]:
        """
        Obtener credencial desencriptada desde BD
        
        Args:
            service_name: Nombre del servicio
            credential_key: Clave de la credencial
        
        Returns:
            Valor desencriptado o None si no existe
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT credential_value_encrypted 
                FROM api_credentials 
                WHERE service_name = %s AND credential_key = %s
            """, (service_name, credential_key))
            
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if not row:
                return None
            
            # Desencriptar valor
            encrypted_value = row['credential_value_encrypted']
            decrypted_value = self.cipher.decrypt(encrypted_value.encode()).decode()
            
            return decrypted_value
            
        except Exception as e:
            error(f"[ERROR] Obteniendo credencial {service_name}.{credential_key}: {e}")
            return None
    
    def get_all_credentials(self, service_name: str) -> Dict[str, str]:
        """
        Obtener todas las credenciales de un servicio
        
        Args:
            service_name: Nombre del servicio
        
        Returns:
            Dict con {credential_key: credential_value}
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT credential_key, credential_value_encrypted 
                FROM api_credentials 
                WHERE service_name = %s
            """, (service_name,))
            
            rows = cur.fetchall()
            cur.close()
            conn.close()
            
            credentials = {}
            for row in rows:
                key = row['credential_key']
                encrypted_value = row['credential_value_encrypted']
                decrypted_value = self.cipher.decrypt(encrypted_value.encode()).decode()
                credentials[key] = decrypted_value
            
            return credentials
            
        except Exception as e:
            error(f"[ERROR] Obteniendo credenciales de {service_name}: {e}")
            return {}
    
    def list_services(self) -> list:
        """Listar todos los servicios con credenciales"""
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("""
                SELECT DISTINCT service_name, description, updated_at
                FROM api_credentials
                ORDER BY service_name
            """)
            
            services = cur.fetchall()
            cur.close()
            conn.close()
            
            return [dict(s) for s in services]
            
        except Exception as e:
            error(f"[ERROR] Listando servicios: {e}")
            return []
    
    def delete_credential(self, service_name: str, credential_key: str = None) -> bool:
        """
        Eliminar credencial(es)
        
        Args:
            service_name: Nombre del servicio
            credential_key: Clave específica (opcional, si None elimina todo el servicio)
        
        Returns:
            True si se eliminó correctamente
        """
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            
            if credential_key:
                cur.execute("""
                    DELETE FROM api_credentials 
                    WHERE service_name = %s AND credential_key = %s
                """, (service_name, credential_key))
            else:
                cur.execute("""
                    DELETE FROM api_credentials 
                    WHERE service_name = %s
                """, (service_name,))
            
            conn.commit()
            cur.close()
            conn.close()
            
            info(f"[OK] Credencial eliminada: {service_name}" + (f".{credential_key}" if credential_key else ""))
            return True
            
        except Exception as e:
            error(f"[ERROR] Eliminando credencial: {e}")
            return False


# Función helper para migrar desde .env a BD
def migrate_credentials_from_env():
    """Migrar credenciales desde .env a BD"""
    load_dotenv()
    
    manager = CredentialsManager()
    
    info("\n" + "="*80)
    info("MIGRANDO CREDENCIALES DESDE .env A BD")
    info("="*80 + "\n")
    
    # NASA Earthdata
    earthdata_username = os.getenv("EARTHDATA_USERNAME")
    earthdata_password = os.getenv("EARTHDATA_PASSWORD")
    earthdata_token = os.getenv("EARTHDATA_TOKEN")
    
    if earthdata_username:
        manager.store_credential("earthdata", "username", earthdata_username, "NASA Earthdata username")
    if earthdata_password:
        manager.store_credential("earthdata", "password", earthdata_password, "NASA Earthdata password")
    if earthdata_token:
        manager.store_credential("earthdata", "token", earthdata_token, "NASA Earthdata token")
    
    # Copernicus Marine
    copernicus_username = os.getenv("COPERNICUS_MARINE_USERNAME")
    copernicus_password = os.getenv("COPERNICUS_MARINE_PASSWORD")
    
    if copernicus_username:
        manager.store_credential("copernicus_marine", "username", copernicus_username, "Copernicus Marine username")
    if copernicus_password:
        manager.store_credential("copernicus_marine", "password", copernicus_password, "Copernicus Marine password")
    
    # OpenTopography
    opentopo_key = os.getenv("OPENTOPOGRAPHY_API_KEY")
    
    if opentopo_key:
        manager.store_credential("opentopography", "api_key", opentopo_key, "OpenTopography API key")
    
    info("\n" + "="*80)
    info("MIGRACION COMPLETADA")
    info("="*80)
    
    # Listar servicios
    services = manager.list_services()
    info(f"\nServicios configurados: {len(services)}")
    for service in services:
        info(f"  - {service['service_name']}: {service['description']}")


if __name__ == "__main__":
    # Ejecutar migración
    migrate_credentials_from_env()
