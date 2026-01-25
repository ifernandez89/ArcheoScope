#!/usr/bin/env python3
"""
ArcheoScope - Comprehensive Archaeological Sites Harvester
Recopila sitios de múltiples fuentes públicas globales

Fuentes:
- UNESCO World Heritage (~1,200 sitios de máxima calidad)
- Wikidata SPARQL (~10,000+ sitios estructurados)
- OpenStreetMap Overpass API (~100,000+ sitios crowdsourced)
- Pleiades Gazetteer (~35,000 sitios del mundo clásico)

Uso:
    python scripts/harvest_archaeological_sites.py
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
import math

# Importar funciones del harvester simple
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Reutilizar las funciones del archivo simple
exec(open(Path(__file__).parent / 'harvest_sites_simple.py').read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harvest archaeological sites from multiple sources')
    parser.add_argument('--output', default='harvested_archaeological_sites.json', help='Output JSON file')
    parser.add_argument('--skip-osm', action='store_true', help='Skip OpenStreetMap (slow)')
    parser.add_argument('--skip-pleiades', action='store_true', help='Skip Pleiades (large download)')
    parser.add_argument('--osm-regions', type=int, help='Limit OSM to N regions (for testing)')
    
    args = parser.parse_args()
    
    main()
