import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

def generate_visoko_3d_conceptual():
    # 1. Load data
    try:
        with open("visoko_scan_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Data not found. Using defaults.")
        data = {'analysis_id': 'TIMT_VISOKO_MOCK', 'territorial_coherence_score': 0.45}

    coherence = data.get('territorial_coherence_score', 0.45)

    # 2. Create Grid (Visoko Valley)
    x = np.linspace(-150, 150, 80)
    y = np.linspace(-150, 150, 80)
    X, Y = np.meshgrid(x, y)
    
    # 3. Model Terrain (Visočica Hill - "Pyramid of the Sun")
    # Natural hill with a pyramidal shape (approx 220m height from valley)
    def visocica_shape(x_val, y_val):
        # A mix of natural slope and "pyramidal" facets
        base = 10 * np.sin(x_val/40) * np.cos(y_val/40) # Natural ripples
        # Sharp triangular facets model
        peak = 220 - 1.5 * (np.maximum(np.abs(x_val + 0.5*y_val), np.abs(y_val)))
        return np.maximum(base, peak)

    Z_hill = visocica_shape(X, Y)
    
    # 4. Create Plot
    fig = plt.figure(figsize=(14, 10), facecolor='#0b0d17')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0d17')
    
    # Plot Hill Surface (Vegetated / Sediment)
    hill_cmap = LinearSegmentedColormap.from_list("visoko", ["#1b4332", "#40916c", "#74c69d"])
    ax.plot_surface(X, Y, Z_hill, cmap=hill_cmap, alpha=0.5, antialiased=True, label='Visočica Surface')
    
    # 5. Represent Subsurface "Concrete" Slabs or Blocks (Inferred)
    # Highlight specific facets where HRM/SAR show stronger structural coherence
    facet_mask = (X > 20) & (X < 100) & (Y > -50) & (Y < 50)
    Z_slabs = np.copy(Z_hill)
    Z_slabs[~facet_mask] = np.nan
    ax.plot_surface(X, Y, Z_slabs + 1, color='#ced4da', alpha=0.4, edgecolor='#6c757d', lw=0.5, label='Inferred Block Structure')
    
    # 6. Ravne Tunnels (Subterranean Void Network)
    # Complex network below the valley/base
    theta = np.linspace(0, 2*np.pi, 100)
    tx = 80 + 20 * np.cos(theta)
    ty = 40 + 30 * np.sin(2*theta)
    tz = np.full_like(theta, -20) # 20m below base level
    ax.plot(tx, ty, tz, color='#00f5d4', lw=4, alpha=0.7, label='Ravne Tunnel Network (Inferred)')
    
    # 7. HRM Peak Activation Overlay
    # Peak activation on the corners/edges of the pyramidal hill
    hrm_mask = (np.abs(np.abs(X) - np.abs(Y)) < 15) & (Z_hill > 100)
    Z_hrm = np.copy(Z_hill)
    Z_hrm[~hrm_mask] = np.nan
    ax.plot_surface(X, Y, Z_hrm + 2, color='#e63946', alpha=0.3, label='HRM Geometric Peak')
    
    # 8. SAR Scanning Mesh
    scan_x = np.linspace(-120, 120, 15)
    scan_y = np.linspace(-120, 120, 15)
    SX, SY = np.meshgrid(scan_x, scan_y)
    SZ = 250 + 0*SX
    ax.plot_wireframe(SX, SY, SZ, color='cyan', alpha=0.2, label='SAR Atmospheric Baseline')
    
    # 9. Styling
    ax.view_init(elev=25, azim=210)
    ax.set_axis_off()
    
    # Titles
    plt.title(f"ARCHEOSCOPE TIMT v2.1: VISOKO PYRAMID 3D CONCEPTUAL MAP\nID: {data['analysis_id']}", 
              color='white', fontsize=16, pad=-20, weight='bold')
    
    # Legend
    proxy_hill = plt.Rectangle((0, 0), 1, 1, fc="#40916c", alpha=0.5)
    proxy_slabs = plt.Rectangle((0, 0), 1, 1, fc="#ced4da", alpha=0.4)
    proxy_tunnels = plt.Line2D([0], [0], color='#00f5d4', lw=3)
    proxy_hrm = plt.Rectangle((0, 0), 1, 1, fc="#e63946", alpha=0.3)
    
    ax.legend([proxy_hill, proxy_slabs, proxy_tunnels, proxy_hrm], 
              ['Visočica Hill Surface', 'Inferred Lithic Blocks', 'Subterranean Tunnels (DIL)', 'HRM Geometric Signal'],
              loc='lower right', facecolor='#1a1c2c', labelcolor='white', edgecolor='none')
    
    # Stats Banner
    metric_text = (f"TIMT COHERENCE: {coherence:.3f}\n"
                   f"GEOMETRY: PYRAMIDAL HILL\n"
                   f"MODEL: GEO-ANTHROPIC HYBRID\n"
                   f"STATUS: EVALUATING ANOMALIES")
    plt.figtext(0.15, 0.75, metric_text, color='cyan', weight='bold', 
                bbox=dict(facecolor='#1a1c2c', alpha=0.8, edgecolor='cyan'))

    plt.savefig("assets/visoko_3d_conceptual.png", dpi=200, transparent=False)
    print("✅ 3D Conceptual Map generated: assets/visoko_3d_conceptual.png")

if __name__ == "__main__":
    generate_visoko_3d_conceptual()
