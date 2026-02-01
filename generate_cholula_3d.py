import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import os

def generate_cholula_3d_conceptual():
    # 1. Load data
    try:
        with open("target_site_scan_results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Data not found. Using defaults.")
        data = {
            'analysis_id': 'TIMT_CHOLULA_MOCK', 
            'etp_summary': {'coherencia_3d': 0.9428, 'ess_superficial': 0.4875}
        }

    coherence = data.get('etp_summary', {}).get('coherencia_3d', 0.9428)
    ess = data.get('etp_summary', {}).get('ess_superficial', 0.4875)

    # 2. Create Grid (Cholula Site)
    x = np.linspace(-100, 100, 100)
    y = np.linspace(-100, 100, 100)
    X, Y = np.meshgrid(x, y)
    
    # 3. Model Great Pyramid of Cholula (Tlachihualtepetl)
    # The largest pyramid base in the world, with a church on top.
    def cholula_shape(x_val, y_val):
        # Base platform (approx 400x400m base)
        base = 15 - (np.maximum(np.abs(x_val), np.abs(y_val))) / 10
        base = np.maximum(0, base)
        
        # Pyramid structure (layered mound)
        pyr = 55 - 0.7 * (np.maximum(np.abs(x_val), np.abs(y_val)))
        pyr = np.maximum(base, pyr)
        
        # Iglesia de Nuestra Señora de los Remedios (on top)
        church_base = (np.abs(x_val) < 10) & (np.abs(y_val) < 15)
        church = np.where(church_base, pyr + 15, pyr)
        
        return church

    Z_pyr = cholula_shape(X, Y)
    
    # 4. Create Plot
    fig = plt.figure(figsize=(14, 10), facecolor='#0b0d17')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0b0d17')
    
    # Plot Pyramid Surface (Vegetated / Excavated)
    # Colormap: browns and greens
    site_cmap = LinearSegmentedColormap.from_list("cholula", ["#582f0e", "#7f4f24", "#936639", "#a68a64", "#b6ad90"])
    ax.plot_surface(X, Y, Z_pyr, cmap=site_cmap, alpha=0.7, antialiased=True, label='Mound Surface')
    
    # 5. Represent Subsurface Voids / Tunnels (DIL)
    # Cholula has 8km of tunnels
    t = np.linspace(0, 10, 100)
    tx_base = np.linspace(-60, 60, 100)
    ty_base = 40 * np.cos(tx_base/20)
    tz_base = np.full_like(tx_base, 10)
    ax.plot(tx_base, ty_base, tz_base, color='#00f5d4', lw=3, alpha=0.8, label='Inferred Tunnel Network')
    
    # 6. HRM Peak Activation Overlay
    # High coherence detected in the square base geometry
    hrm_mask = (np.abs(np.abs(X) - np.abs(Y)) < 5) & (Z_pyr > 10)
    Z_hrm = np.copy(Z_pyr)
    Z_hrm[~hrm_mask] = np.nan
    ax.plot_surface(X, Y, Z_hrm + 1, color='#e63946', alpha=0.4, label='HRM Structural Coherence')
    
    # 7. Church Geometry
    church_mask = (np.abs(X) < 8) & (np.abs(Y) < 12) & (Z_pyr > 55)
    Z_church = np.copy(Z_pyr)
    Z_church[~church_mask] = np.nan
    ax.plot_surface(X, Y, Z_church, color='#fb8500', alpha=0.9)
    
    # 8. Scanning Mesh (TIMT)
    scan_x = np.linspace(-110, 110, 20)
    scan_y = np.linspace(-110, 110, 20)
    SX, SY = np.meshgrid(scan_x, scan_y)
    SZ = 90 + 0*SX
    ax.plot_wireframe(SX, SY, SZ, color='cyan', alpha=0.1)
    
    # 9. Styling
    ax.view_init(elev=30, azim=225)
    ax.set_axis_off()
    
    # Titles
    plt.title(f"ARCHEOSCOPE TIMT v2.1: CHOLULA PYRAMID (TLACHIHUALTEPETL)\nID: {data['analysis_id']}", 
              color='white', fontsize=16, pad=-20, weight='bold')
    
    # Legend
    proxy_mound = plt.Rectangle((0, 0), 1, 1, fc="#7f4f24", alpha=0.7)
    proxy_church = plt.Rectangle((0, 0), 1, 1, fc="#fb8500", alpha=0.9)
    proxy_tunnels = plt.Line2D([0], [0], color='#00f5d4', lw=3)
    proxy_hrm = plt.Rectangle((0, 0), 1, 1, fc="#e63946", alpha=0.4)
    
    ax.legend([proxy_mound, proxy_church, proxy_tunnels, proxy_hrm], 
              ['Pyramid Mound Surface', 'Iglesia de los Remedios', 'Subsurface Tunnels (DIL)', 'Neural Peak Analysis'],
              loc='lower right', facecolor='#1a1c2c', labelcolor='white', edgecolor='none')
    
    # Stats Banner
    metric_text = (f"GEOMETRIC COHERENCE: {coherence:.4f}\n"
                   f"ANOMALY INTENSITY (ESS): {ess:.4f}\n"
                   f"REGIO: CHOLULA, MEXICO\n"
                   f"CLASSIFICATION: MONUMENTAL STRUCTURE")
    plt.figtext(0.15, 0.75, metric_text, color='cyan', weight='bold', 
                bbox=dict(facecolor='#1a1c2c', alpha=0.8, edgecolor='cyan'))

    # Ensure assets directory exists
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    plt.savefig("assets/cholula_3d_conceptual.png", dpi=200, transparent=False)
    print("✅ 3D Conceptual Map generated: assets/cholula_3d_conceptual.png")

if __name__ == "__main__":
    generate_cholula_3d_conceptual()
