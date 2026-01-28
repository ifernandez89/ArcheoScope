#!/usr/bin/env python3
"""
FIX RÁPIDO Y DIRECTO - Sin unicode
"""

def fix_core_file():
    file_path = r"C:\Python\ArcheoScope\backend\core_anomaly_detector.py"
    
    print("FIX RAPIDO - CoreAnomalyDetector")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix 1: Linea 247 - return measurements
    if len(lines) > 247:
        lines[247] = '        return measurements\n'
        print("Linea 248 arreglada")
    
    # Fix 2: Linea 249 - definicion de metodo con indentacion correcta
    if len(lines) > 248:
        lines[248] = '    def _simulate_instrument_measurement(self, indicator_name: str, \n'
        print("Linea 249 arreglada")
    
    # Fix 3: Linea 250-253 - parametros con indentacion correcta
    if len(lines) > 249:
        lines[249] = '                                            indicator_config: Dict[str, Any],\n'
    if len(lines) > 250:
        lines[250] = '                                            env_context,\n'
    if len(lines) > 251:
        lines[251] = '                                            lat_min: float, lat_max: float,\n'
    if len(lines) > 252:
        lines[252] = '                                            lon_min: float, lon_max: float) -> Optional[InstrumentMeasurement]:\n'
    
    # Fix 4: Linea 439 - _get_site_type method
    if len(lines) > 438:
        lines[438] = '    def _get_site_type(self, site_info) -> str:\n'
        print("Linea 439 arreglada")
    
    # Guardar archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Archivo guardado - verificando compilacion...")
    
    # Verificar compilacion
    import py_compile
    try:
        py_compile.compile(file_path, doraise=True)
        print("COMPILACION EXITOSA!")
        return True
    except Exception as e:
        print(f"Error compilacion: {e}")
        return False

if __name__ == "__main__":
    if fix_core_file():
        print("EXITO - Backend arreglado")
    else:
        print("FALLO - Requiere revision manual")