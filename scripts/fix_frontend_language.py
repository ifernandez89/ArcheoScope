#!/usr/bin/env python3
"""
Fix Frontend Language - Scientific Integrity
=============================================

Corrige lenguaje científicamente irresponsable en el frontend.

Reemplaza palabras definitivas por lenguaje hipotético.

Fecha: 2026-01-26
"""

import re
from pathlib import Path
from typing import List, Tuple

# Mapeo de correcciones
CORRECTIONS = {
    # Spanish
    'hallazgo': 'hipótesis',
    'hallazgos': 'hipótesis',
    'estructura detectada': 'patrón instrumental anómalo',
    'estructuras detectadas': 'patrones instrumentales anómalos',
    'sitio confirmado': 'candidato de alta prioridad',
    'sitios confirmados': 'candidatos de alta prioridad',
    'confirmado': 'compatible con',
    'confirmada': 'compatible con',
    'confirmados': 'compatibles con',
    'confirmadas': 'compatibles con',
    'detectado': 'observado',
    'detectada': 'observada',
    'detectados': 'observados',
    'detectadas': 'observadas',
    'evidencia arqueológica': 'indicador arqueológico',
    'evidencias arqueológicas': 'indicadores arqueológicos',
    
    # English
    'discovery': 'hypothesis',
    'discoveries': 'hypotheses',
    'structure detected': 'anomalous instrumental pattern',
    'structures detected': 'anomalous instrumental patterns',
    'site confirmed': 'high-priority candidate',
    'sites confirmed': 'high-priority candidates',
    'confirmed': 'compatible with',
    'detected': 'observed',
    'archaeological evidence': 'archaeological indicator',
    
    # Specific phrases
    'Documentar hallazgos': 'Documentar hipótesis',
    'validación temporal CONFIRMADA': 'persistencia temporal detectada',
    'Validación temporal CONFIRMADA': 'Persistencia temporal detectada',
    'CONFIRMADO': 'COMPATIBLE',
    'Confirmado temporalmente': 'Con persistencia temporal',
    'confirmado temporalmente': 'con persistencia temporal',
    'Sitio arqueológico confirmado': 'Candidato arqueológico de alta prioridad',
    'sitio arqueológico confirmado': 'candidato arqueológico de alta prioridad',
    'Sensor temporal CONFIRMA': 'Sensor temporal detecta persistencia en',
    'sensor temporal CONFIRMA': 'sensor temporal detecta persistencia en',
    'Estructura detectada con': 'Patrón instrumental anómalo con',
    'estructura detectada con': 'patrón instrumental anómalo con',
}

# Archivos a procesar
FRONTEND_FILES = [
    'frontend/index.html',
    'frontend/archaeological_app.js',
    'frontend/volumetric_lidar_app.js',
    'frontend/volumetric_lidar_viewer.html'
]


def fix_file(filepath: str) -> Tuple[int, List[str]]:
    """
    Corregir lenguaje en un archivo
    
    Returns:
        (num_corrections, list_of_changes)
    """
    
    path = Path(filepath)
    
    if not path.exists():
        print(f"⚠️  Archivo no encontrado: {filepath}")
        return 0, []
    
    # Leer contenido
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Aplicar correcciones
    for old, new in CORRECTIONS.items():
        if old in content:
            # Contar ocurrencias
            count = content.count(old)
            content = content.replace(old, new)
            changes.append(f"  - '{old}' → '{new}' ({count} veces)")
    
    # Si hubo cambios, guardar
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return len(changes), changes
    
    return 0, []


def add_disclaimer_to_html(filepath: str) -> bool:
    """
    Agregar disclaimer científico a archivo HTML
    
    Returns:
        True si se agregó disclaimer
    """
    
    path = Path(filepath)
    
    if not path.exists():
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya tiene disclaimer
    if 'DISCLAIMER CIENTÍFICO' in content or 'SCIENTIFIC DISCLAIMER' in content:
        return False
    
    # Disclaimer HTML
    disclaimer_html = '''
    <!-- DISCLAIMER CIENTÍFICO - Integridad Científica -->
    <div id="scientific-disclaimer" style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 15px 20px;
        font-size: 13px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        z-index: 10000;
        border-top: 3px solid #c92a2a;
    ">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between;">
            <div style="flex: 1;">
                <strong>⚠️ DISCLAIMER CIENTÍFICO:</strong>
                ArcheoScope es un motor de hipótesis geoespaciales. Los "candidatos" son HIPÓTESIS que requieren validación física por arqueólogos profesionales.
                <span style="opacity: 0.9; font-size: 11px; display: block; margin-top: 5px;">
                    Modo de datos: REAL (mediciones directas) | DERIVED (estimaciones) | INFERRED (inferencias geométricas)
                </span>
            </div>
            <button onclick="document.getElementById('scientific-disclaimer').style.display='none'" style="
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin-left: 20px;
            ">Entendido</button>
        </div>
    </div>
'''
    
    # Insertar antes de </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{disclaimer_html}\n</body>')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False


def main():
    """Ejecutar correcciones"""
    
    print("="*80)
    print("CORRECCIÓN DE LENGUAJE FRONTEND - Integridad Científica")
    print("="*80)
    print()
    
    total_corrections = 0
    total_files_modified = 0
    
    # Procesar cada archivo
    for filepath in FRONTEND_FILES:
        print(f"📄 Procesando: {filepath}")
        
        num_corrections, changes = fix_file(filepath)
        
        if num_corrections > 0:
            print(f"   ✅ {num_corrections} correcciones aplicadas:")
            for change in changes:
                print(change)
            total_corrections += num_corrections
            total_files_modified += 1
        else:
            print(f"   ℹ️  No se encontraron correcciones necesarias")
        
        # Agregar disclaimer si es HTML
        if filepath.endswith('.html'):
            if add_disclaimer_to_html(filepath):
                print(f"   ✅ Disclaimer científico agregado")
        
        print()
    
    print("="*80)
    print(f"✅ COMPLETADO")
    print(f"   Archivos modificados: {total_files_modified}/{len(FRONTEND_FILES)}")
    print(f"   Total de correcciones: {total_corrections}")
    print("="*80)
    print()
    print("PRÓXIMO PASO: Cambiar visualizaciones 3D a wireframes")
    print("   Ejecutar: python fix_3d_visualizations.py")


if __name__ == "__main__":
    main()
