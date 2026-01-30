import sys
from pathlib import Path
import os

backend_dir = Path("c:/Python/ArcheoScope/backend")
os.chdir(backend_dir)
sys.path.append(str(backend_dir))

print(f"CWD: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import hrm.hrm_runner
    print("✅ hrm.hrm_runner imported successfully")
except ImportError as e:
    print(f"❌ hrm.hrm_runner import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from hrm.hrm_runner import load_models
    print("✅ load_models imported successfully")
except ImportError as e:
    print(f"❌ load_models import failed: {e}")
