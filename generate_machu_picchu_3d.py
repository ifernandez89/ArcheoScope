import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

def generate_mp_3d_conceptual():
    # 1. Load data
    try:
        with open("machu_picchu_benchmark_results.json", "r", encoding="utf-8") as f:
            full_data = json.load(f)
        data = full_data['mp_north_slope']
    except:
        print("Data not found. Using defaults.")
        data = {'analysis_id': 'TIMT_MP_MOCK', 'territorial_coherence_score': 0.68}

    coherence = data.get('territorial_coherence_score', 0.68)

    # 2. Create Grid (Andean Ridge)
    x = np.linspace(-100, 100, 60)
    y = np.linspace(-100, 100, 60)
    X, Y = np.meshgrid(x, y)
    
    # 3. Model Terrain (Macchu Picchu ridge between two peaks)
    # Steep slopes on the sides
    Z_plateau = 2400 - 0.5 * X - 0.05 * Y**2
    
    # 4. Model Terraces (Andenes)
    def andenes_filter(x_val, z_val):
        # Create steps every 15m
        step = 5 * np.floor(x_val / 15)
        return z_val + step

    Z_surface = np.copy(Z_plateau)
    # Apply terraces to a specific sector
    terrace_mask = (X < 50) & (X > -80)
    Z_surface[terrace_mask] = andenes_filter(X[terrace_mask], Z_plateau[terrace_mask])
    
    # 5. Model Buildings (Urban sector)
    urban_mask = (X > 50) & (abs(Y) < 40)
    Z_surface[urban_mask] += 8 # Building height
    
    # 6. Create Plot
    fig = plt.figure(figsize=(14, 10), facecolor='#0b0d17')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0d17')
    
    # Plot Mountain Base
    mountain_cmap = LinearSegmentedColormap.from_list("mountain", ["#1a1c2c", "#1e212d", "#4a4e69"])
    ax.plot_surface(X, Y, Z_plateau - 20, cmap=mountain_cmap, alpha=0.5, antialiased=True)
    
    # Plot Surface with Terraces and Buildings
    ax.plot_surface(X, Y, Z_surface, color='#52b788', alpha=0.4, edgecolor='#2d6a4f', lw=0.3, antialiased=True)
    
    # 7. Subsurface Engineering (Drainage layers)
    # Represented as a semitransparent layer below the terraces
    Z_eng = np.copy(Z_surface) - 5
    Z_eng[~terrace_mask] = np.nan
    ax.plot_surface(X, Y, Z_eng, color='#ffd60a', alpha=0.15, label='Subsurface Drainage Layer')
    
    # 8. HRM Activation Overlay
    # High coherence in the urban and main terrace areas
    hrm_mask = (X > -20) & (X < 80) & (abs(Y) < 50)
    Z_hrm = np.copy(Z_surface)
    Z_hrm[~hrm_mask] = np.nan
    ax.plot_surface(X, Y, Z_hrm + 1.5, color='#e63946', alpha=0.25, label='HRM Engineering Signal')
    
    # 9. SAR/LiDAR Scanning path
    # Scanning from the slope
    path_x = np.linspace(-120, 80, 20)
    path_y = np.linspace(-100, 20, 20)
    path_z = 2500 + 0 * path_x
    ax.plot(path_x, path_y, path_z, '--', color='cyan', lw=2, alpha=0.6, label='Orbital Scan Mesh')
    
    # 10. Styling
    ax.view_init(elev=30, azim=230)
    ax.set_axis_off()
    
    # Titles
    plt.title(f"ARCHEOSCOPE TIMT v2.1: MACHU PICCHU 3D MAP\nID: {data['analysis_id']}", 
              color='white', fontsize=16, pad=-20, weight='bold')
    
    # Legend
    proxy_mountain = plt.Rectangle((0, 0), 1, 1, fc="#4a4e69", alpha=0.5)
    proxy_surface = plt.Rectangle((0, 0), 1, 1, fc="#52b788", alpha=0.4)
    proxy_eng = plt.Rectangle((0, 0), 1, 1, fc="#ffd60a", alpha=0.15)
    proxy_hrm = plt.Rectangle((0, 0), 1, 1, fc="#e63946", alpha=0.25)
    
    ax.legend([proxy_mountain, proxy_surface, proxy_eng, proxy_hrm], 
              ['Granite Host Mountain', 'Andenes & Urban Surface', 'Incan Subsurface Engineering', 'HRM Signal Activation'],
              loc='lower right', facecolor='#1a1c2c', labelcolor='white', edgecolor='none')
    
    # Stats Banner
    metric_text = (f"TIMT COHERENCE: {coherence:.3f}\n"
                   f"GEOMETRY: LINEAR/MODULAR\n"
                   f"MODEL: ANDEAN-SYSTEMIC\n"
                   f"STATUS: BENCHMARKED")
    plt.figtext(0.15, 0.75, metric_text, color='cyan', weight='bold', 
                bbox=dict(facecolor='#1a1c2c', alpha=0.8, edgecolor='cyan'))

    plt.savefig("assets/machu_picchu_3d_conceptual.png", dpi=200, transparent=False)
    print("✅ 3D Conceptual Map generated: assets/machu_picchu_3d_conceptual.png")

if __name__ == "__main__":
    generate_mp_3d_conceptual()
