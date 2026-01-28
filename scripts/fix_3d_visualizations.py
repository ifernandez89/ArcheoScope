#!/usr/bin/env python3
"""
Fix 3D Visualizations - Scientific Integrity
=============================================

Cambia visualizaciones 3D sólidas a wireframes con disclaimers.

REGLA: Datos INFERRED deben mostrarse como wireframes transparentes,
NO como modelos sólidos que sugieren evidencia física.

Fecha: 2026-01-26
"""

import re
from pathlib import Path
from typing import List, Tuple

# Archivos a procesar
FRONTEND_FILES = [
    'frontend/index.html',
    'frontend/archaeological_app.js',
    'frontend/volumetric_lidar_app.js'
]


def fix_threejs_materials(content: str) -> Tuple[str, List[str]]:
    """
    Corregir materiales Three.js para usar wireframes
    
    Returns:
        (modified_content, list_of_changes)
    """
    
    changes = []
    
    # Patrón 1: MeshPhongMaterial con opacity alta
    pattern1 = r'new THREE\.MeshPhongMaterial\s*\(\s*\{([^}]+)\}\s*\)'
    
    def replace_phong(match):
        props = match.group(1)
        
        # Si no tiene wireframe o está en false
        if 'wireframe' not in props or 'wireframe: false' in props or 'wireframe:false' in props:
            changes.append("  - MeshPhongMaterial → MeshBasicMaterial con wireframe")
            
            # Extraer color si existe
            color_match = re.search(r'color:\s*(0x[0-9A-Fa-f]+|["\']#[0-9A-Fa-f]+["\'])', props)
            color = color_match.group(1) if color_match else '0x00FF00'
            
            return f'''new THREE.MeshBasicMaterial({{
                color: {color},
                wireframe: true,
                opacity: 0.3,
                transparent: true
            }})'''
        
        return match.group(0)
    
    content = re.sub(pattern1, replace_phong, content)
    
    # Patrón 2: MeshBasicMaterial sin wireframe
    pattern2 = r'new THREE\.MeshBasicMaterial\s*\(\s*\{([^}]+)\}\s*\)'
    
    def replace_basic(match):
        props = match.group(1)
        
        # Si no tiene wireframe o está en false
        if 'wireframe' not in props or 'wireframe: false' in props or 'wireframe:false' in props:
            # Si tiene opacity > 0.5, corregir
            if 'opacity' in props:
                opacity_match = re.search(r'opacity:\s*([0-9.]+)', props)
                if opacity_match:
                    opacity = float(opacity_match.group(1))
                    if opacity > 0.5:
                        changes.append(f"  - Opacity reducida: {opacity} → 0.3")
                        props = re.sub(r'opacity:\s*[0-9.]+', 'opacity: 0.3', props)
            
            # Agregar wireframe si no existe
            if 'wireframe' not in props:
                changes.append("  - Agregado wireframe: true")
                props += ',\n                wireframe: true'
            
            # Asegurar transparent: true
            if 'transparent' not in props:
                props += ',\n                transparent: true'
            
            return f'new THREE.MeshBasicMaterial({{{props}}})'
        
        return match.group(0)
    
    content = re.sub(pattern2, replace_basic, content)
    
    # Patrón 3: Opacity > 0.5 en cualquier material
    pattern3 = r'opacity:\s*([0-9.]+)'
    
    def replace_opacity(match):
        opacity = float(match.group(1))
        if opacity > 0.5:
            changes.append(f"  - Opacity corregida: {opacity} → 0.3")
            return 'opacity: 0.3'
        return match.group(0)
    
    content = re.sub(pattern3, replace_opacity, content)
    
    return content, changes


def add_3d_disclaimer_text(content: str) -> Tuple[str, bool]:
    """
    Agregar texto de disclaimer a visualizaciones 3D
    
    Returns:
        (modified_content, was_added)
    """
    
    # Buscar funciones que crean geometría 3D
    patterns = [
        r'(function\s+create3DVisualization\s*\([^)]*\)\s*\{)',
        r'(function\s+generateRealisticDimensions\s*\([^)]*\)\s*\{)',
        r'(function\s+create.*Geometry\s*\([^)]*\)\s*\{)',
    ]
    
    disclaimer_code = '''
    
    // DISCLAIMER: Geometría inferida - NO es evidencia física
    const disclaimerDiv = document.createElement('div');
    disclaimerDiv.style.cssText = `
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(255, 107, 107, 0.95);
        color: white;
        padding: 10px 15px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        z-index: 1000;
        border: 2px solid #c92a2a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    `;
    disclaimerDiv.innerHTML = '⚠️ GEOMETRÍA INFERIDA<br><span style="font-weight:normal;font-size:10px;">NO ES EVIDENCIA FÍSICA</span>';
    
    // Agregar al contenedor si existe
    if (typeof container !== 'undefined' && container) {
        container.appendChild(disclaimerDiv);
    }
'''
    
    added = False
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1' + disclaimer_code, content, count=1)
            added = True
            break
    
    return content, added


def fix_file(filepath: str) -> Tuple[int, List[str]]:
    """
    Corregir visualizaciones 3D en un archivo
    
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
    all_changes = []
    
    # Corregir materiales Three.js
    content, material_changes = fix_threejs_materials(content)
    all_changes.extend(material_changes)
    
    # Agregar disclaimer a visualizaciones 3D
    content, disclaimer_added = add_3d_disclaimer_text(content)
    if disclaimer_added:
        all_changes.append("  - Agregado disclaimer '⚠️ GEOMETRÍA INFERIDA' a visualización 3D")
    
    # Si hubo cambios, guardar
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return len(all_changes), all_changes
    
    return 0, []


def create_wireframe_example():
    """Crear archivo de ejemplo de visualización correcta"""
    
    example_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ejemplo: Visualización Científicamente Responsable</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; font-family: Arial, sans-serif; }
        #container { width: 100%; height: 100vh; position: relative; }
        .disclaimer {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 107, 107, 0.95);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            z-index: 1000;
            border: 3px solid #c92a2a;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            max-width: 300px;
        }
        .disclaimer-subtitle {
            font-weight: normal;
            font-size: 11px;
            margin-top: 5px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div id="container">
        <div class="disclaimer">
            ⚠️ GEOMETRÍA INFERIDA
            <div class="disclaimer-subtitle">
                Esta visualización representa una HIPÓTESIS basada en 
                patrones instrumentales. NO es evidencia física ni 
                confirmación arqueológica.
            </div>
        </div>
    </div>
    
    <script>
        // Configuración de escena
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('container').appendChild(renderer.domElement);
        
        // ✅ CORRECTO: Geometría como WIREFRAME transparente
        const geometry = new THREE.BoxGeometry(2, 2, 2);
        
        // Material científicamente responsable
        const material = new THREE.MeshBasicMaterial({
            color: 0x00FF00,        // Verde para hipótesis
            wireframe: true,        // ← CRÍTICO: wireframe, NO sólido
            opacity: 0.3,           // ← CRÍTICO: baja opacidad
            transparent: true
        });
        
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        
        // Agregar ejes de referencia
        const axesHelper = new THREE.AxesHelper(3);
        scene.add(axesHelper);
        
        // Animación
        function animate() {
            requestAnimationFrame(animate);
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Responsive
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
'''
    
    with open('frontend/wireframe_example.html', 'w', encoding='utf-8') as f:
        f.write(example_html)
    
    print("   ✅ Creado: frontend/wireframe_example.html (ejemplo de visualización correcta)")


def main():
    """Ejecutar correcciones"""
    
    print("="*80)
    print("CORRECCIÓN DE VISUALIZACIONES 3D - Integridad Científica")
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
        
        print()
    
    # Crear ejemplo
    print("📝 Creando ejemplo de visualización correcta...")
    create_wireframe_example()
    print()
    
    print("="*80)
    print(f"✅ COMPLETADO")
    print(f"   Archivos modificados: {total_files_modified}/{len(FRONTEND_FILES)}")
    print(f"   Total de correcciones: {total_corrections}")
    print("="*80)
    print()
    print("REGLAS APLICADAS:")
    print("  1. Materiales sólidos → Wireframes transparentes")
    print("  2. Opacity > 0.5 → Opacity = 0.3")
    print("  3. Agregados disclaimers '⚠️ GEOMETRÍA INFERIDA'")
    print()
    print("PRÓXIMO PASO: Rotar credenciales comprometidas")
    print("  1. Ir a https://urs.earthdata.nasa.gov/")
    print("  2. Cambiar password de Earthdata")
    print("  3. Ir a https://data.marine.copernicus.eu/")
    print("  4. Cambiar password de Copernicus Marine")


if __name__ == "__main__":
    main()
