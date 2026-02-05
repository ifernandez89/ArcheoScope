#!/usr/bin/env python3
"""
Misión: Reconstrucción del Mundo a través de Sensores Fósiles
============================================================

Usa los sitios medidos para inferir qué tipo de mundo obligó a su creación.
Aplica el Emulador de Modo Cognitivo (SAM).
"""

import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from cognitive_emulator import CognitiveModeEmulator

def run_world_reconstruction_mission():
    emulator = CognitiveModeEmulator()
    
    # Datos de sensores fósiles (inferidos de mediciones previas)
    fossil_sensors = [
        {
            "name": "Anatolia (Göbekli Tepe Cluster)",
            "data": {
                'alignment_priority': 0.85,  # Alineación estelar fuerte
                'stability_index': 1.0,     # Sellado intencional (estabilidad total)
                'temporal_scale_years': 2000 # Persistencia del sitio antes del fin
            }
        },
        {
            "name": "Altiplano (Tiwanaku/Puma Punku)",
            "data": {
                'alignment_priority': 0.95, 
                'stability_index': 0.98,
                'temporal_scale_years': 5000 # Escala de uso y diseño
            }
        },
        {
            "name": "Valle de Giza (Plataforma Primaria)",
            "data": {
                'alignment_priority': 0.99,
                'stability_index': 0.99,
                'temporal_scale_years': 26000 # Ciclo precesional completo codificado
            }
        }
    ]
    
    print("\n" + "="*90)
    print("🌍 ARCHEOSCOPE: MISIÓN DE RECONSTRUCCIÓN DE MUNDO (LÍNEA C)")
    print("="*90)
    print("Interrogando sitios como sensores fósiles para inferir presiones del entorno.\n")
    
    reconstructions = []
    for sensor in fossil_sensors:
        recon = emulator.run_reconstruction(sensor['name'], sensor['data'])
        reconstructions.append(recon)
        print(f"✅ Reconstrucción completada para: {sensor['name']}")
        
    master_file = "RECONSTRUCCION_MUNDO_FOSIL.md"
    with open(master_file, "w", encoding="utf-8") as f:
        f.write("# ARCHEOSCOPE: INFORME DE RECONSTRUCCIÓN DE MUNDO ANTIGUO\n\n")
        f.write("## 🧬 Premisa: El Diseño es el Mensaje del Entorno\n\n")
        f.write("Si el diseño prioriza la estabilidad sobre la eficiencia, el entorno es catastrófico. ")
        f.write("Si prioriza la alineación sobre la función, el entorno es referencialmente inestable.\n\n")
        
        for r in reconstructions:
            f.write(r + "\n\n")
            
        f.write("\n## 🎯 SÍNTESIS DE LA HIPÓTESIS PREPRECISA\n\n")
        f.write("### El Mundo de la Cognición SAM (Supra-generational Alignment Mode)\n\n")
        f.write("1. **Alta Entropía Local**: El sistema de referencia terrestre (clima, polos, costas) era volátil.\n")
        f.write("2. **Falla de Memoria Orgánica**: La transmisión de conocimiento vía lenguaje (oral/escrito) se identificó como un punto crítico de falla. El sistema cambió a **Transmisión Mineral de Geometría Dura**.\n")
        f.write("3. **Sincronización como Supervivencia**: La 'alineación' no era un ritual, era un **chequeo de saludPlanetaria**. Si el monumento se desvía del cosmos, el mundo está cambiando.\n")
        f.write("4. **Modo 'Deep Clock'**: Operaban en un tiempo profundo donde el 'ahora' es solo una fase de un ciclo precesional. La arquitectura es la aguja de un reloj que nunca debe dejar de marcar el norte estelar.\n")

    print(f"\n{'='*90}")
    print(f"📁 INFORME DE RECONSTRUCCIÓN GENERADO: {master_file}")
    print(f"{'='*90}\n")
    
    print("🧠 CONCLUSIÓN:");
    print("La Línea C no es sobre 'quiénes eran', sino sobre cómo el universo los obligó a pensar.")
    print("Estamos ante una **Ingeniería de la Persistencia** diseñada para tiempos de obscuridad total de datos.\n")

if __name__ == "__main__":
    run_world_reconstruction_mission()
