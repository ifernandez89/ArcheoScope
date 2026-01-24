# ArcheoScope - Agent Development Guidelines

## Project Overview

ArcheoScope is an archaeological remote sensing engine that detects spatial persistences not explainable by current natural processes. It's built with Python FastAPI backend and JavaScript frontend, integrating AI reasoning through Ollama/OpenRouter.

## Build & Development Commands

### Backend Development
```bash
# Start backend server (primary method)
python run_archeoscope.py

# Alternative backend startup
python start_backend.py
# Serves on: http://localhost:8003

# Install dependencies
pip install -r backend/requirements.txt

# Backend status check
python quick_test.py
```

### Frontend Development
```bash
# Start frontend server
python start_frontend.py
# Serves on: http://localhost:8080

# Direct file access (for development)
file:///path/to/frontend/index.html
```

### Testing Commands
```bash
# Run single test file
python test_simple_debug.py
python test_backend_direct.py
python test_configured_model.py

# Quick backend connectivity test
python quick_test.py

# Determinism verification
python test_backend_determinism.py

# Comprehensive integration tests
python test_complete_integration.py
```

### AI/LLM Testing
```bash
# Test OpenRouter API integration
python test_openrouter_api.py

# Test configured AI models
python test_configured_model.py

# Simple AI reasoning test
python simple_openrouter_test.py
```

## Code Style Guidelines

### Python Backend Style

#### Import Organization
```python
# Standard library imports first
import sys
import os
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Third-party imports
import numpy as np
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scipy import ndimage, stats

# Local imports (use relative imports when possible)
from backend.data.archaeological_loader import ArchaeologicalDataLoader
from backend.rules.archaeological_rules import ArchaeologicalRulesEngine
```

#### Type Hints & Data Structures
- Use `typing` module for all function signatures
- Prefer `dataclass` for complex data structures
- Use `Enum` for categorical values
- Always include return types

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

class ArchaeologicalResult(Enum):
    CONSISTENT = "consistent"
    ANOMALOUS = "anomalous"
    ARCHAEOLOGICAL = "archaeological"

@dataclass
class ArchaeologicalEvaluation:
    result: ArchaeologicalResult
    confidence: float
    archaeological_probability: float
    affected_pixels: int
    evidence_details: Dict[str, Any]
```

#### Error Handling
```python
# Use specific exception types
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise HTTPException(status_code=400, detail=f"Invalid data: {e}")
except requests.RequestException as e:
    logger.error(f"API request failed: {e}")
    return {"error": "External service unavailable"}
```

#### Logging Standards
```python
import logging
logger = logging.getLogger(__name__)

# Use structured logging with context
logger.info(f"Processing archaeological analysis for region: {region_name}")
logger.warning(f"Low confidence result: {confidence:.2f}")
logger.error(f"Analysis failed: {error_details}", exc_info=True)
```

#### NumPy/Scientific Computing
```python
# Convert numpy types for JSON serialization
def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

# Use explicit random seeds for reproducibility
np.random.seed(42)  # When needed for testing
```

### JavaScript Frontend Style

#### Module Organization
```javascript
// Use IIFE pattern for encapsulation
(function() {
    'use strict';
    
    // Global constants
    const API_BASE_URL = 'http://localhost:8003';
    const DEFAULT_ZOOM = 10;
    
    // Main application class
    class ArcheoScopeApp {
        constructor() {
            this.map = null;
            this.currentAnalysis = null;
        }
    }
})();
```

#### API Communication
```javascript
// Use async/await with proper error handling
async function analyzeRegion(bounds) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bounds)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Analysis failed:', error);
        showErrorMessage('Analysis failed. Please try again.');
        throw error;
    }
}
```

#### DOM Manipulation
```javascript
// Use event delegation and querySelector
function initializeUI() {
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('analyze-btn')) {
            handleAnalysisClick(event);
        }
    });
    
    const mapContainer = document.querySelector('#map-container');
    if (mapContainer) {
        initializeMap(mapContainer);
    }
}
```

## Testing Guidelines

### Test File Naming
- Use `test_` prefix for all test files
- Descriptive names: `test_backend_determinism.py`, `test_water_detection_simple.py`
- Integration tests: `test_complete_integration.py`
- Debug tests: `test_simple_debug.py`

### Test Structure
```python
#!/usr/bin/env python3
"""
Brief description of test purpose.
"""

import requests
import json
from typing import Dict, Any

def test_specific_functionality():
    """Test specific functionality with clear description."""
    
    print("🔍 Testing: [specific feature]")
    
    test_data = {
        "lat_min": -16.55,
        "lat_max": -16.54,
        "lon_min": -68.67,
        "lon_max": -68.66,
        "region_name": "Test Region"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test passed")
            return True
        else:
            print(f"❌ Test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_specific_functionality()
    print(f"Result: {'✅ OK' if success else '❌ ERROR'}")
```

### Determinism Testing
- Always test same coordinates multiple times
- Verify consistent results across runs
- Use `test_backend_determinism.py` as template

## API Design Patterns

### FastAPI Endpoint Structure
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    region_name: str
    resolution_m: Optional[int] = 1000

@app.post("/analyze")
async def analyze_region(request: AnalysisRequest):
    """Analyze archaeological region for spatial persistences."""
    
    try:
        # Validate input
        if request.lat_min >= request.lat_max:
            raise HTTPException(status_code=400, detail="Invalid latitude range")
        
        # Process analysis
        result = await archaeological_analysis(request)
        
        # Convert numpy types
        return convert_numpy_types(result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis failed")
```

### Response Format
```python
# Standard response structure
{
    "analysis_id": "uuid",
    "region_name": "string",
    "spatial_context": {
        "area_km2": float,
        "analysis_mode": "fine|medium|coarse",
        "resolution_m": int
    },
    "archaeological_results": {
        "result_type": "consistent|anomalous|archaeological",
        "confidence": float,
        "archaeological_probability": float,
        "affected_pixels": int
    },
    "ai_explanations": {
        "ai_available": bool,
        "explanation": "string",
        "confidence": float
    },
    "evidence_layers": [...],
    "validation_metrics": {...}
}
```

## Configuration Management

### Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("ARCHEOSCOPE_API_URL", "http://localhost:8003")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model Configuration
DEFAULT_AI_MODEL = os.getenv("DEFAULT_AI_MODEL", "phi4-mini-reasoning")
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "60"))
```

### Spatial Thresholds
```python
# Archaeological analysis thresholds (in km²)
SPATIAL_THRESHOLDS = {
    "fine": 10,        # High-resolution archaeological analysis
    "medium": 100,     # Medium-resolution analysis
    "coarse": 1000,    # Large-scale analysis (limited validity)
    "maximum": 5000    # Absolute maximum for rejection
}
```

## Performance Guidelines

### Backend Optimization
- Use numpy arrays for spatial data processing
- Implement caching for repeated analyses
- Use async/await for I/O operations
- Limit analysis area based on spatial thresholds

### Frontend Optimization
- Implement lazy loading for map tiles
- Use debouncing for map interaction events
- Cache API responses in browser storage
- Optimize image loading for archaeological layers

## Security Considerations

### API Security
- Validate all input parameters
- Sanitize file uploads and user data
- Implement rate limiting for expensive operations
- Use environment variables for sensitive data

### Data Protection
- Never log API keys or sensitive coordinates
- Implement proper error messages without exposing internals
- Use HTTPS for production deployments
- Validate all geographic bounds

## Development Workflow

### Before Making Changes
1. Run existing tests: `python quick_test.py`
2. Check backend status: `python test_simple_debug.py`
3. Verify AI integration if needed: `python test_configured_model.py`

### After Making Changes
1. Run relevant test files
2. Test backend determinism: `python test_backend_determinism.py`
3. Verify frontend integration
4. Update documentation if needed

### Git Commit Guidelines
- Use conventional commit format: `feat:`, `fix:`, `docs:`, `test:`
- Include test file names in commit messages when relevant
- Reference issue numbers if available

## Debugging Common Issues

### Backend Connection Issues
```bash
# Check if backend is running
python quick_test.py

# Test specific endpoint
curl http://localhost:8003/status

# Check logs for errors
# Backend runs with detailed logging enabled
```

### AI Integration Issues
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test OpenRouter API
python test_configured_model.py

# Check model availability
python test_openrouter_api.py
```

### Frontend Issues
- Check browser console for JavaScript errors
- Verify CORS configuration in backend
- Test API endpoints directly before frontend integration
- Use browser network tab to inspect API calls

## Scientific Validation

### Archaeological Integrity
- All results must include confidence scores
- Use control sites for validation
- Implement falsification frameworks
- Maintain scientific rigor in interpretations

### Spatial Analysis Standards
- Validate coordinate systems and projections
- Use appropriate resolution for archaeological features
- Implement proper statistical significance testing
- Document all assumptions and limitations

This file serves as the comprehensive guide for AI agents working on the ArcheoScope codebase. Follow these guidelines to maintain code quality, scientific integrity, and system reliability.