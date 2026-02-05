
import os
import sys
import numpy as np
import json
import logging
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.abspath("c:/Python/ArcheoScope"))

from backend.volumetric.geometric_inference_engine import GeometricInferenceEngine, SpatialSignature, MorphologicalClass
from backend.volumetric.geometric_inference_engine import VolumetricField, GeometricModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def export_to_obj(model: GeometricModel, filename: str):
    """Export geometric model to OBJ format."""
    with open(filename, 'w') as f:
        f.write(f"# ArcheoScope Volumetric Reconstruction\n")
        f.write(f"# Volume: {model.estimated_volume_m3:.2f} m3\n")
        f.write(f"# Vertices: {len(model.vertices)}\n")
        f.write(f"# Faces: {len(model.faces)}\n")
        
        for v in model.vertices:
            # Scale for visualization if needed, but keeping meters is standard
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
        for face in model.faces:
            # OBJ indices are 1-based
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
            
    logger.info(f"💾 Model exported to {filename}")

def generate_visualization_html(model: GeometricModel, filename: str):
    """Generate a simple HTML 3D viewer using Plotly (if available) or basic geometric info."""
    try:
        import plotly.graph_objects as go
        
        # Extract vertices
        x, y, z = model.vertices[:, 0], model.vertices[:, 1], model.vertices[:, 2]
        
        # Extract faces for mesh3d
        i, j, k = model.faces[:, 0], model.faces[:, 1], model.faces[:, 2]
        
        fig = go.Figure(data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                i=i, j=j, k=k,
                colorscale='Viridis',
                intensity=z,
                opacity=0.8,
                name='Bermuda Node Internal Structure'
            )
        ])
        
        fig.update_layout(
            title='ArcheoScope Volumetric Reconstruction: Bermuda Node A',
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Depth (m)',
                aspectmode='data'
            )
        )
        
        fig.write_html(filename)
        logger.info(f"💾 Interactive visualization exported to {filename}")
        
    except ImportError:
        logger.warning("Plotly not installed. Skipping HTML generation.")

def main():
    print("🚀 INIT: Generating 3D Volumetric Field for Bermuda Node A...")
    
    # 1. Initialize Engine
    engine = GeometricInferenceEngine()
    
    # 2. Reconstruct Data Context (from Mission Logs)
    # Location: Bermuda Node A
    # Coordinates: [26.50, 26.65] x [-78.90, -78.75]
    bounds = (26.50, -78.90, 250.0) # approx origin
    
    anomaly_data = {
        "id": "BERMUDA_NODE_A_SYNC_CANDIDATE",
        "center_lat": 26.575,
        "center_lon": -78.825,
        "area_m2": 5000000, # Approx 5km2 footprint
        "signal_strength": 0.95
    }
    
    # Layer results from the recent scan (Step 360 logs)
    layer_results = {
        "sentinel_2_ndvi": {
            "value": -0.020, "confidence": 1.0, 
            "archaeological_probability": 0.1, "temporal_persistence": 0.9
        },
        "sentinel_1_sar": {
            "value": -15.565, "confidence": 0.8,
            "archaeological_probability": 0.85, "geometric_coherence": 0.995 # High coherence in logs
        },
        "thermal_inertia": {
            "value": 1.0, "confidence": 0.9,
            "archaeological_probability": 0.92 # "Thermal Anchor Zone"
        },
        "tas_score": {
            "value": 0.920, "confidence": 0.93
        },
        "gravimetry_inferred": {
            "density_anomaly": 0.125,
            "coherence_3d": 0.875
        }
    }
    
    # 3. Process Anomaly
    print("🧠 PROCESSING: Running Volumetric Inference...")
    result = engine.process_anomaly_complete(anomaly_data, layer_results, (0, 0, 1000, 1000)) # Local metric bounds
    
    if result["inference_successful"]:
        model = result["geometric_model"]
        field = result["volumetric_field"]
        
        print(f"✅ SUCCESS: Model Generated.")
        print(f"   Vertices: {len(model.vertices)}")
        print(f"   Volume: {model.estimated_volume_m3:.2f} m3")
        print(f"   Morphology: {result['morphological_class']}")
        print(f"   Confidence Core: {field.confidence_layers['core']:.2%}")
        
        # 4. Export
        obj_file = "bermuda_node_a_structure.obj"
        html_file = "bermuda_node_a_viz.html"
        
        export_to_obj(model, obj_file)
        generate_visualization_html(model, html_file)
        
        print("\n🎉 GENERATION COMPLETE")
        print(f"3D Model File: {os.path.abspath(obj_file)}")
        print(f"Visualization: {os.path.abspath(html_file)}")
        
    else:
        print(f"❌ FAILURE: {result.get('error')}")

if __name__ == "__main__":
    main()
