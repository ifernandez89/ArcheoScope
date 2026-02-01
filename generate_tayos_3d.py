import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

def generate_tayos_3d_conceptual():
    # 1. Load data
    try:
        with open("cuevas_tayos_scan_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Data not found. Using defaults.")
        data = {'analysis_id': 'TIMT_TAYOS_MOCK', 'territorial_coherence_score': 0.757}

    coherence = data.get('territorial_coherence_score', 0.757)

    # 2. Create Grid (Amazonian Terrain)
    x = np.linspace(-100, 100, 60)
    y = np.linspace(-100, 100, 60)
    X, Y = np.meshgrid(x, y)
    
    # 3. Model Terrain (Jungle Mountain/Slope)
    # A bit more rugged for the Amazonian foothills
    Z_plateau = 500 + 15 * np.sin(X/40) + 10 * np.cos(Y/30)
    
    # 4. Create Plot
    fig = plt.figure(figsize=(14, 10), facecolor='#0b0d17')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0d17')
    
    # Plot Jungle Canopy Surface
    jungle_cmap = LinearSegmentedColormap.from_list("jungle", ["#081c15", "#1b4332", "#2d6a4f"])
    ax.plot_surface(X, Y, Z_plateau, cmap=jungle_cmap, alpha=0.6, antialiased=True, label='Jungle Canopy')
    
    # 5. The Chimney (Primary Entrance)
    # A vertical shaft through the surface
    shaft_x = np.linspace(-5, 5, 20)
    shaft_z = np.linspace(440, 510, 20)
    SX, SZ = np.meshgrid(shaft_x, shaft_z)
    SY = np.sqrt(25 - SX**2) # Cylinder side 1
    ax.plot_surface(SX, SY, SZ, color='#00f5d4', alpha=0.4)
    ax.plot_surface(SX, -SY, SZ, color='#00f5d4', alpha=0.4)
    
    # 6. Subterranean Galleries (Void Inferences)
    # Large horizontal voids at ~60m depth
    void_x = np.linspace(-40, 60, 30)
    void_y = np.linspace(-20, 20, 30)
    VX, VY = np.meshgrid(void_x, void_y)
    VZ = 440 + 5 * np.sin(VX/10) * np.cos(VY/10)
    ax.plot_surface(VX, VY, VZ, color='#00f5d4', alpha=0.3, label='Inferred Large Galleries (DIL)')
    ax.plot_surface(VX, VY, VZ-10, color='#00f5d4', alpha=0.2) # Floor of gallery
    
    # 7. HRM Activation Overlay on Surface
    # Highlight the area around the entrance
    mask = (X**2 + Y**2 < 400)
    Z_hrm = np.copy(Z_plateau)
    Z_hrm[~mask] = np.nan
    ax.plot_surface(X, Y, Z_hrm + 2, color='#e63946', alpha=0.4, label='HRM Peak Activation (Entrance)')
    
    # 8. LiDAR Penetration Path
    # Snaking through the shaft to the galleries
    path_x = [0, 0, 30, 50]
    path_y = [0, 0, 10, 0]
    path_z = [520, 440, 440, 440]
    ax.plot(path_x, path_y, path_z, '--', color='#fee440', lw=3, label='LiDAR Penetration Route')
    
    # 9. Styling
    ax.view_init(elev=20, azim=130)
    ax.set_axis_off()
    
    # Titles
    plt.title(f"ARCHEOSCOPE TIMT v2.1: CUEVA DE LOS TAYOS 3D MAP\nID: {data['analysis_id']}", 
              color='white', fontsize=16, pad=-20, weight='bold')
    
    # Legend
    proxy_jungle = plt.Rectangle((0, 0), 1, 1, fc="#2d6a4f", alpha=0.6)
    proxy_void = plt.Rectangle((0, 0), 1, 1, fc="#00f5d4", alpha=0.3)
    proxy_hrm = plt.Rectangle((0, 0), 1, 1, fc="#e63946", alpha=0.4)
    proxy_path = plt.Line2D([0], [0], ls='--', color='#fee440', lw=2)
    
    ax.legend([proxy_jungle, proxy_void, proxy_hrm, proxy_path], 
              ['Amazonian High Canopy', 'Subterranean Voids (DIL)', 'HRM Area of Interest', 'LiDAR Target Path'],
              loc='lower right', facecolor='#1a1c2c', labelcolor='white', edgecolor='none')
    
    # Stats Banner
    metric_text = (f"TIMT COHERENCE: {coherence:.3f}\n"
                   f"DEPTH: ~60-80m\n"
                   f"MODEL: KARSTIC-TECH\n"
                   f"STATUS: SUBTERRANEAN SCAN")
    plt.figtext(0.15, 0.75, metric_text, color='#00f5d4', weight='bold', 
                bbox=dict(facecolor='#1a1c2c', alpha=0.8, edgecolor='#00f5d4'))

    plt.savefig("assets/cuevas_tayos_3d_conceptual.png", dpi=200, transparent=False)
    print("✅ 3D Conceptual Map generated: assets/cuevas_tayos_3d_conceptual.png")

if __name__ == "__main__":
    generate_tayos_3d_conceptual()
