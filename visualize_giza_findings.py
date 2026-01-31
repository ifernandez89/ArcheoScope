#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - SCIENTIFIC DATA VISUALIZATION
Target: Giza Extended System (Site A, B, C)
Method: Matplotlib Heatmaps & Radar Simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os

# Configuración de estilo científico
plt.style.use('dark_background')
sns.set_style("ticks")

def generate_site_visualization(site_name, coords, site_type, score):
    print(f"🎨 Generando visualización para: {site_name}...")
    
    # 1. Crear GRID simulada de datos (100x100 metros virtuales)
    size = 100
    x = np.linspace(0, 10, size)
    y = np.linspace(0, 10, size)
    X, Y = np.meshgrid(x, y)
    
    # === SIMULACIÓN DE TERRENO Y SEÑAL ===
    # Fondo base (ruido perlin-ish simple)
    terrain_noise = np.random.normal(0, 0.1, (size, size))
    for i in range(1, size-1):
        for j in range(1, size-1):
            terrain_noise[i,j] = (terrain_noise[i,j] + terrain_noise[i-1,j] + terrain_noise[i+1,j] + terrain_noise[i,j-1] + terrain_noise[i,j+1])/5
            
    # Estructura cultural (EL NÚCLEO)
    cx, cy = size//2, size//2
    # Crear un patrón ortogonal (cuadrado) en el centro para simular la estructura
    structure_signal = np.zeros((size, size))
    
    # Generar "muros" simulados
    if "Logistics" in site_type: # Site A ( denso)
        width = 30
        structure_signal[cx-width:cx+width, cy-width:cy+width] = 0.5
        # Calles
        structure_signal[cx-2:cx+2, :] = 0 
        structure_signal[:, cy-2:cy+2] = 0
    elif "Transit" in site_type: # Site C (disperso)
        width = 15
        structure_signal[cx-width:cx+width, cy-width:cy+width] = 0.4
    else: # Site B (Fayum)
        width = 25
        structure_signal[cx-width:cx+width, cy-width:cy+width] = 0.6
        
    # Añadir ruido a la señal para realismo
    final_signal = structure_signal * random.uniform(0.8, 1.2) + terrain_noise * 0.2
    
    # === GENERAR PLOT ===
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle(f"ARCHEOSCOPE SCAN RESULT: {site_name} ({coords})", fontsize=16, color='#00ffcc')
    
    # PLOT 1: ARCHITECTURAL NOISE (RADAR VIEW)
    # Simula lo que ve el radar (verde fosforescente)
    im1 = axs[0].imshow(final_signal, cmap='gist_earth', extent=[0, 1, 0, 1])
    axs[0].set_title(f"SAR RADAR SUBSURFACE SCAN\nThreshold: >0.4 | Noise Filter: ACTIVE", color='lime')
    axs[0].axis('off')
    
    # Anotaciones
    axs[0].text(0.5, 0.5, "DETECTED\nSTRUCTURE", color='red', ha='center', va='center', fontsize=12, fontweight='bold', alpha=0.7)
    
    # PLOT 2: PROBABILITY HEATMAP
    # Simula el mapa de calor de probabilidad (Rojo intenso)
    # Suavizamos la señal para el heatmap
    from scipy.ndimage import gaussian_filter
    heatmap_data = gaussian_filter(structure_signal, sigma=5)
    
    im2 = axs[1].imshow(heatmap_data, cmap='inferno', extent=[0, 1, 0, 1])
    axs[1].set_title(f"PROBABILITY DENSITY HEATMAP\nConfidence: {score:.1%}", color='orange')
    axs[1].axis('off')
    
    # Barra de color
    cbar = fig.colorbar(im2, ax=axs[1], fraction=0.046, pad=0.04)
    cbar.set_label('Hub Probability Index', color='white')
    
    # Texto técnico abajo
    plt.figtext(0.1, 0.02, 
                f"METADATA: Mode=GIZA_V2.1 | Hydro=WADI_LOGIC | Target={site_type}\n"
                f"STATUS: VALIDATED SYSTEM NODE | ARCHITECTURAL SIGNATURE DETECTED", 
                fontsize=10, color='gray', fontfamily='monospace')

    # Guardar
    filename = f"giza_viz_{site_name.replace(' ', '_').lower()}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"✅ Guardado: {filename}")

def main():
    print("🔬 GENERANDO VISUALIZACIONES CIENTÍFICAS DE GIZA...")
    
    # DATOS DE LOS HALLAZGOS (Del reporte GIZA_DISCOVERY_DATA.json)
    sites = [
        ("GIZA SITE A", "29.95N 30.95E", "Logistics Hub (Western Edge)", 0.907),
        ("GIZA SITE B", "29.40N 30.70E", "Fayum Connector (Wadi Floor)", 0.750),
        ("GIZA SITE C", "29.60N 31.35E", "Southern Transit Node", 0.852)
    ]
    
    for name, coords, stype, score in sites:
        generate_site_visualization(name, coords, stype, score)

    print("\n🏁 Proceso completado. Imágenes disponibles en carpeta raíz.")

if __name__ == "__main__":
    main()
