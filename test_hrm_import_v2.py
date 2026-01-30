import logging
import sys
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")

backend_dir = Path("c:/Python/ArcheoScope/backend")
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

print(f"CWD: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    from hrm.hrm_runner import load_models as load_hrm_model, generate_response as generate_hrm_response
    print("✅ HRM imported successfully")
except ImportError as e:
    print(f"❌ ImportError: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
