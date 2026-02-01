import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

def generate_giza_3d_conceptual():
    # 1. Load data
    try:
        with open("giza_scan_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Data not found. Using defaults.")
        data = {'analysis_id': 'TIMT_GIZA_MOCK', 'territorial_coherence_score': 0.72}

    coherence = data.get('territorial_coherence_score', 0.72)

    # 2. Create Grid
    x = np.linspace(-150, 150, 60)
    y = np.linspace(-150, 150, 60)
    X, Y = np.meshgrid(x, y)
    
    # 3. Model Terrain (Plateau)
    Z_plateau = 2 * np.sin(X/50) * np.cos(Y/50)
    
    # 4. Model Pyramid
    # Height 146m, Base 230m (half-base 115m)
    Z_pyramid = 146 - 1.27 * (np.maximum(np.abs(X), np.abs(Y)))
    Z_pyramid = np.maximum(Z_pyramid, Z_plateau)
    
    # 5. Create Plot
    fig = plt.figure(figsize=(14, 10), facecolor='#0b0d17')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0d17')
    
    # Plot Plateau Surface
    plateau_cmap = LinearSegmentedColormap.from_list("plateau", ["#1a1c2c", "#4a4e69"])
    ax.plot_surface(X, Y, Z_plateau, cmap=plateau_cmap, alpha=0.4, antialiased=True)
    
    # Plot Pyramid (Translucent stone)
    # Using a technical wireframe look + surface
    ax.plot_surface(X, Y, Z_pyramid, color='#f4d35e', alpha=0.3, edgecolor='#f4d35e', lw=0.5, antialiased=True)
    
    # 6. Internal Voids (DIL anomalies)
    # Queen's Chamber area
    ax.scatter([0], [0], [21], color='#00f5d4', s=200, alpha=0.8, label='Inferred Void (Queen\'s Level)')
    # King's Chamber area
    ax.scatter([0], [0], [43], color='#00f5d4', s=300, alpha=1.0, label='Inferred Void (King\'s Level)')
    # Grand Gallery (simplified as lines)
    ax.plot([0, 0], [0, 40], [21, 43], color='#00f5d4', lw=3, alpha=0.6)
    
    # 7. HRM Heatmap on Surface
    # Highlight the base where activity is higher
    mask = (np.abs(X) < 115) & (np.abs(Y) < 115)
    Z_hrm = np.copy(Z_pyramid)
    Z_hrm[~mask] = np.nan
    ax.plot_surface(X, Y, Z_hrm + 1, color='#e63946', alpha=0.2, label='HRM Activation Overlay')
    
    # 8. SAR Penetration Route
    # A dashed line crossing from side to base
    ax.plot([-140, 0], [-140, 0], [0, 90], '--', color='#fee440', lw=2, label='SAR Penetration Route')
    
    # 9. Styling
    ax.view_init(elev=25, azim=45)
    ax.set_axis_off()
    
    # Labels and Metadata
    plt.title(f"ARCHEOSCOPE TIMT v2.1: GIZA 3D CONCEPTUAL MAP\nID: {data['analysis_id']}", 
              color='white', fontsize=16, pad=-20, weight='bold')
    
    # Legend
    proxy_plateau = plt.Rectangle((0, 0), 1, 1, fc="#4a4e69", alpha=0.4)
    proxy_pyramid = plt.Rectangle((0, 0), 1, 1, fc="#f4d35e", alpha=0.3)
    proxy_void = plt.Line2D([0], [0], marker='o', color='none', markerfacecolor='#00f5d4', markersize=10)
    proxy_sar = plt.Line2D([0], [0], ls='--', color='#fee440', lw=2)
    
    ax.legend([proxy_plateau, proxy_pyramid, proxy_void, proxy_sar], 
              ['Limestone Plateau', 'Megalithic Geometry', 'Subsurface Voids (DIL)', 'SAR Radar Path'],
              loc='lower right', facecolor='#1a1c2c', labelcolor='white', edgecolor='none')
    
    # Metrics Banner
    metric_text = (f"TIMT COHERENCE: {coherence:.3f}\n"
                   f"MODEL: MEGALITHIC 3D\n"
                   f"STATUS: SCIENTIFIC RENDER")
    plt.figtext(0.15, 0.75, metric_text, color='#f4d35e', weight='bold', 
                bbox=dict(facecolor='#1a1c2c', alpha=0.8, edgecolor='#f4d35e'))

    plt.savefig("assets/giza_3d_conceptual.png", dpi=200, transparent=False)
    print("✅ 3D Conceptual Map generated: assets/giza_3d_conceptual.png")

if __name__ == "__main__":
    generate_giza_3d_conceptual()
