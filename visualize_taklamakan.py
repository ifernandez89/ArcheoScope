#!/usr/bin/env python3
"""
🛰️ ARCHEOSCOPE - TAKLAMAKAN SILK ROAD VIZ
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('dark_background')

def generate_silk_road_map():
    print("🎨 Generando mapa técnico de TAKLAMAKAN...")
    
    size = 100
    # Simulación de Dunas Barchan (arena móvil)
    # Patrón de ondas de arena
    sand_waves = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            sand_waves[i,j] = np.sin(i/5) * np.cos(j/10) * 0.2
            
    # La "Ciudad Fantasma" enterrada (Señal radar débil pero clara)
    ghost_city = np.zeros((size, size))
    # Patrón de red urbana (Silk Road style)
    for i in range(30, 70, 5):
        ghost_city[i-1:i+1, 30:70] = 0.6
        ghost_city[30:70, i-1:i+1] = 0.6
        
    fig, ax = plt.subplots(figsize=(10, 10))
    # Capa de arena (Dunas)
    ax.imshow(sand_waves, cmap='YlOrBr', alpha=0.4)
    # Capa de radar (Subsurface structures)
    ax.imshow(ghost_city, cmap='cool', alpha=0.7)
    
    ax.set_title("TAKLAMAKAN: SITE TAK-001\nSAR Subsurface Scan: Mud-Brick Grid", fontsize=15, color='#00eaff')
    ax.axis('off')
    
    plt.savefig("taklamakan_viz_ghost_city.png", dpi=150, facecolor='black')
    print("✅ Guardado: taklamakan_viz_ghost_city.png")

if __name__ == "__main__":
    generate_silk_road_map()
