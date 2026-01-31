#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - IRAN QANAT VIZ
"""
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')

def generate_qanat_map():
    print("🎨 Generando mapa técnico de IRÁN...")
    
    size = 100
    # Terreno: Desierto de Lut (Kaluts / Yardangs)
    lut_terrain = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            lut_terrain[i,j] = np.sin(i/15) * 0.1 # Yardangs paralelos
            
    # Firma de QANAT: Líneas de puntos circulares (pozos)
    qanat_line = np.zeros((size, size))
    # Una línea diagonal de pozos de ventilación
    for k in range(20, 80, 5):
        # Cada pozo es un pequeño círculo de alta reflectividad
        for i in range(-1, 2):
            for j in range(-1, 2):
                if k+i < size and k+10+j < size:
                    qanat_line[k+i, k+10+j] = 0.8
                    
    # Asentamiento Shahdad (Ruido complejo en el terminal)
    shahdad = np.zeros((size, size))
    shahdad[70:85, 75:90] = 0.6
    
    fig, ax = plt.subplots(figsize=(10, 10))
    # Capa de terreno
    ax.imshow(lut_terrain, cmap='copper', alpha=0.3)
    # Capa de Qanats (Radar)
    ax.imshow(qanat_line, cmap='winter', alpha=0.8)
    # Capa de Asentamiento
    ax.imshow(shahdad, cmap='magma', alpha=0.6)
    
    ax.set_title("IRAN CENTRAL: SHAHDAD & QANAT SYSTEM\nSignature: Subsurface Water Network", fontsize=15, color='#00ffcc')
    ax.axis('off')
    
    plt.savefig("iran_viz_qanat.png", dpi=150, facecolor='black')
    print("✅ Guardado: iran_viz_qanat.png")

if __name__ == "__main__":
    generate_qanat_map()
