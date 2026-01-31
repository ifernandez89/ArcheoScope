#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - ATACAMA DATA VIZ
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('dark_background')

def generate_atacama_map():
    print("🎨 Generando mapa técnico de ATACAMA...")
    
    size = 100
    # Simulación de un Bofedal (Oasis de altura)
    # Verde esmeralda sobre desierto ocre
    terrain = np.random.normal(0.2, 0.05, (size, size))
    
    # El Oasis (señal hídrica)
    for i in range(size):
        for j in range(size):
            dist = np.sqrt((i-50)**2 + (j-50)**2)
            if dist < 15: terrain[i,j] = 0.8 # Centro bofedal
            elif dist < 25: terrain[i,j] = 0.5 # Borde fértil
            
    # La Fortaleza (Pucara) - Ruido angular
    fortress = np.zeros((size, size))
    cx, cy = 40, 60 # Desplazada del agua por seguridad
    fortress[cx-5:cx+5, cy-5:cy+5] = 0.7
    fortress[cx-8:cx+8, cy-1:cy+1] = 0.7 # Muros exteriores
    fortress[cx-1:cx+1, cy-8:cy+8] = 0.7
    
    fig, ax = plt.subplots(figsize=(10, 10))
    # Capa de terreno (Oasis)
    ax.imshow(terrain, cmap='terrain', alpha=0.6)
    # Capa de radar (Pucara)
    ax.imshow(fortress, cmap='hot', alpha=0.5)
    
    ax.set_title("ATACAMA INTERIOR: SITE ATC-001\nRadar-Scan: Pucara de Altura", fontsize=15, color='#ff9900')
    ax.axis('off')
    
    plt.savefig("atacama_viz_pucara.png", dpi=150, facecolor='black')
    print("✅ Guardado: atacama_viz_pucara.png")

if __name__ == "__main__":
    generate_atacama_map()
