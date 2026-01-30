import logging
import sys
from pathlib import Path
import os
from unittest.mock import MagicMock

# Configurar logging para ver la salida
logging.basicConfig(level=logging.INFO)

backend_dir = Path("c:/Python/ArcheoScope/backend")
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

# Mock RealDataIntegratorV2 si es necesario
mock_integrator = MagicMock()

print("--- INICIANDO IMPORT DE TIMT ENGINE ---")
try:
    from territorial_inferential_tomography import TerritorialInferentialTomographyEngine
    print("✅ TerritorialInferentialTomographyEngine importado")
    
    # Intentar instanciarlo para ver si el __init__ falla
    engine = TerritorialInferentialTomographyEngine(mock_integrator)
    print("✅ TerritorialInferentialTomographyEngine instanciado")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
print("--- FIN ---")
