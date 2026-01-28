# 🔬 PIPELINE DE ANÁLISIS TOMOGRÁFICO MULTIMODAL
## ArcheoScope - Análisis Volumétrico 3D/4D

---

## 📋 RESUMEN EJECUTIVO

**Objetivo**: Crear un análisis tomográfico completo de sitios CANDIDATE combinando los 10 instrumentos operacionales para generar visualizaciones volumétricas 3D/4D y scores de interés revolucionarios.

**Concepto**: Como una tomografía computada (CT scan), pero para arqueología remota.

---

## 1️⃣ INSTRUMENTOS OPERACIONALES (10 TOTAL)

### Capa Superficial (2D)
1. **NDVI Vegetation** (Sentinel-2/Landsat) - Vegetación superficial
2. **Thermal LST** (MODIS/Landsat) - Temperatura superficial
3. **SAR C-band** (Sentinel-1) - Retrodispersión superficial
4. **Surface Roughness** (Scatterometer) - Rugosidad superficial
5. **Soil Salinity** (SMOS) - Salinidad superficial

### Capa Volumétrica (3D)
6. **Elevation DEM** (OpenTopography) - Micro-relieve
7. **SAR L-band** (ASF PALSAR) - Penetración bajo vegetación
8. **ICESat-2** - Perfiles láser verticales (precisión centimétrica)
9. **GEDI** - Estructura 3D de vegetación
10. **SMAP** - Humedad del suelo (penetración ~5cm)

---

## 2️⃣ PREPROCESAMIENTO

### 2.1 Reproyección y Alineación
```python
# backend/volumetric/tomographic_preprocessor.py

import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np

class TomographicPreprocessor:
    """Preprocesador para análisis tomográfico multimodal"""
    
    def __init__(self, target_crs='EPSG:4326', resolution=30):
        self.target_crs = target_crs
        self.resolution = resolution  # metros
    
    def align_datasets(self, datasets):
        """
        Alinear todos los datasets a la misma referencia espacial
        
        Args:
            datasets: Dict con {instrument_name: raster_data}
        
        Returns:
            aligned_stack: Array 3D [bands, height, width]
        """
        
        # 1. Determinar bbox común
        common_bounds = self._calculate_common_bounds(datasets)
        
        # 2. Reproyectar cada dataset
        aligned = {}
        for name, data in datasets.items():
            aligned[name] = self._reproject_to_common(
                data, 
                common_bounds,
                self.target_crs,
                self.resolution
            )
        
        # 3. Stack en array 3D
        stack = np.stack([aligned[k] for k in sorted(aligned.keys())])
        
        return stack, aligned
```

### 2.2 Generación de Raster Stack 2D
```python
def create_2d_stack(self, datasets):
    """
    Crear stack 2D de todas las bandas superficiales
    
    Capas:
    - NDVI (1 banda)
    - LST (1 banda)
    - SAR C-band VV (1 banda)
    - SAR C-band VH (1 banda)
    - Roughness (1 banda)
    - Salinity (1 banda)
    
    Total: 6 bandas 2D
    """
    
    stack_2d = np.stack([
        datasets['ndvi'],
        datasets['lst'],
        datasets['sar_c_vv'],
        datasets['sar_c_vh'],
        datasets['roughness'],
        datasets['salinity']
    ])
    
    return stack_2d  # Shape: [6, height, width]
```

### 2.3 Generación de Volumen 3D
```python
def create_3d_volume(self, datasets):
    """
    Crear volumen 3D combinando elevación + vegetación + penetración
    
    Estructura vertical (de arriba hacia abajo):
    - Capa 10: Tope de vegetación (GEDI canopy height)
    - Capa 9: Estructura alta vegetación (GEDI)
    - Capa 8: Estructura media vegetación (GEDI)
    - Capa 7: Estructura baja vegetación (GEDI)
    - Capa 6: Superficie terrestre (DEM + ICESat-2)
    - Capa 5: Sub-superficie 0-10cm (SAR L-band)
    - Capa 4: Sub-superficie 10-20cm (SAR L-band)
    - Capa 3: Sub-superficie 20-30cm (SAR L-band + SMAP)
    - Capa 2: Sub-superficie 30-40cm (SMAP)
    - Capa 1: Sub-superficie 40-50cm (SMAP)
    
    Total: 10 capas verticales
    """
    
    # Obtener altura de vegetación de GEDI
    canopy_height = datasets['gedi_canopy_height']
    
    # Obtener elevación de DEM + ICESat-2
    ground_elevation = self._merge_dem_icesat2(
        datasets['dem'],
        datasets['icesat2']
    )
    
    # Crear capas de vegetación (4 capas)
    veg_layers = self._create_vegetation_layers(
        datasets['gedi_structure'],
        canopy_height,
        n_layers=4
    )
    
    # Crear capas sub-superficie (5 capas)
    subsurface_layers = self._create_subsurface_layers(
        datasets['sar_l_band'],
        datasets['smap_moisture'],
        n_layers=5
    )
    
    # Stack vertical completo
    volume_3d = np.stack([
        veg_layers[3],      # Tope
        veg_layers[2],      # Alta
        veg_layers[1],      # Media
        veg_layers[0],      # Baja
        ground_elevation,   # Superficie
        subsurface_layers[0],  # 0-10cm
        subsurface_layers[1],  # 10-20cm
        subsurface_layers[2],  # 20-30cm
        subsurface_layers[3],  # 30-40cm
        subsurface_layers[4]   # 40-50cm
    ])
    
    return volume_3d  # Shape: [10, height, width]
```

### 2.4 Normalización para ML
```python
def normalize_for_ml(self, stack):
    """
    Normalizar todos los valores para ML multimodal
    
    Métodos:
    - Min-Max scaling [0, 1]
    - Z-score normalization
    - Robust scaling (percentiles)
    """
    
    normalized = np.zeros_like(stack, dtype=np.float32)
    
    for i in range(stack.shape[0]):
        band = stack[i]
        
        # Robust scaling (percentiles 2-98)
        p2, p98 = np.percentile(band[~np.isnan(band)], [2, 98])
        normalized[i] = np.clip((band - p2) / (p98 - p2), 0, 1)
    
    return normalized
```

---

## 3️⃣ ANÁLISIS ML MULTIMODAL

### 3.1 Vector Multidimensional por Sitio
```python
# backend/ai/tomographic_ml_analyzer.py

class TomographicMLAnalyzer:
    """Analizador ML para datos tomográficos"""
    
    def extract_site_features(self, volume_3d, stack_2d, temporal_data):
        """
        Extraer vector de features multidimensional por sitio
        
        Features (50 total):
        - Superficiales (6): NDVI, LST, SAR_C, Roughness, Salinity, SMAP
        - Volumétricas (10): Capas 3D del volumen
        - Temporales (15): Medias, tendencias, anomalías de NDVI, LST, SMAP
        - Geométricas (10): Gradientes, texturas, simetrías
        - Contextuales (9): ESS, anomaly_score, cobertura, etc.
        """
        
        features = {}
        
        # 1. Features superficiales (6)
        features['ndvi_mean'] = np.nanmean(stack_2d[0])
        features['ndvi_std'] = np.nanstd(stack_2d[0])
        features['lst_mean'] = np.nanmean(stack_2d[1])
        features['lst_std'] = np.nanstd(stack_2d[1])
        features['sar_c_mean'] = np.nanmean(stack_2d[2])
        features['roughness_mean'] = np.nanmean(stack_2d[4])
        
        # 2. Features volumétricas (10)
        for i in range(10):
            features[f'volume_layer_{i}_mean'] = np.nanmean(volume_3d[i])
            features[f'volume_layer_{i}_std'] = np.nanstd(volume_3d[i])
        
        # 3. Features temporales (15)
        temporal_features = self._extract_temporal_features(temporal_data)
        features.update(temporal_features)
        
        # 4. Features geométricas (10)
        geometric_features = self._extract_geometric_features(volume_3d)
        features.update(geometric_features)
        
        # 5. Features contextuales (9)
        features['ess_score'] = temporal_data.get('ess_score', 0)
        features['anomaly_score'] = temporal_data.get('anomaly_score', 0)
        features['coverage'] = temporal_data.get('coverage', 0)
        
        return features  # Dict con 50 features
```

### 3.2 Series Temporales
```python
def extract_temporal_features(self, temporal_data):
    """
    Extraer features de series temporales
    
    Variables temporales:
    - NDVI histórico (12 meses)
    - LST histórico (12 meses)
    - SMAP humedad (12 meses)
    
    Features extraídas:
    - Media anual
    - Desviación estándar
    - Tendencia (slope)
    - Estacionalidad (amplitud)
    - Anomalías (picos)
    """
    
    features = {}
    
    for var in ['ndvi', 'lst', 'smap']:
        series = temporal_data[f'{var}_timeseries']
        
        # Media y std
        features[f'{var}_mean_annual'] = np.mean(series)
        features[f'{var}_std_annual'] = np.std(series)
        
        # Tendencia (regresión lineal)
        x = np.arange(len(series))
        slope, _ = np.polyfit(x, series, 1)
        features[f'{var}_trend'] = slope
        
        # Estacionalidad (amplitud)
        features[f'{var}_seasonality'] = np.max(series) - np.min(series)
        
        # Anomalías (valores >2 std)
        anomalies = np.abs(series - np.mean(series)) > 2 * np.std(series)
        features[f'{var}_anomaly_count'] = np.sum(anomalies)
    
    return features
```

### 3.3 Modelo de Scoring
```python
def train_interest_scoring_model(self, training_data):
    """
    Entrenar modelo de scoring de interés
    
    Arquitectura:
    - Random Forest Regressor (baseline)
    - Gradient Boosting (mejor performance)
    - Neural Network (experimental)
    
    Target: Score de interés [0, 1]
    - 0.0-0.3: Bajo interés (natural)
    - 0.3-0.6: Interés moderado (investigar)
    - 0.6-0.8: Alto interés (prioridad)
    - 0.8-1.0: Interés excepcional (urgente)
    """
    
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import cross_val_score
    
    # Preparar datos
    X = np.array([site['features'] for site in training_data])
    y = np.array([site['interest_score'] for site in training_data])
    
    # Entrenar modelo
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    
    model.fit(X, y)
    
    # Validación cruzada
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"R² score: {scores.mean():.3f} ± {scores.std():.3f}")
    
    return model
```

---


## 4️⃣ VISUALIZACIÓN AVANZADA

### 4.1 Mapas 3D Interactivos
```python
# backend/volumetric/tomographic_visualizer.py

import plotly.graph_objects as go
import numpy as np

class TomographicVisualizer:
    """Visualizador 3D para análisis tomográfico"""
    
    def create_3d_volume_plot(self, volume_3d, metadata):
        """
        Crear visualización volumétrica 3D interactiva
        
        Vistas:
        - XY: Mapa normal con overlay de ESS y anomaly score
        - XZ: Corte vertical (Este-Oeste)
        - YZ: Corte vertical (Norte-Sur)
        - 3D: Volumen completo con transparencia
        """
        
        # Crear figura con subplots
        fig = go.Figure()
        
        # 1. Vista XY (mapa superior)
        surface_layer = volume_3d[4]  # Capa de superficie
        fig.add_trace(go.Surface(
            z=surface_layer,
            colorscale='Earth',
            name='Superficie',
            showscale=True
        ))
        
        # 2. Overlay de ESS
        ess_overlay = self._create_ess_overlay(metadata['ess_score'])
        fig.add_trace(go.Surface(
            z=surface_layer + 10,  # Elevado 10m
            surfacecolor=ess_overlay,
            colorscale='Hot',
            opacity=0.5,
            name='ESS Score'
        ))
        
        # 3. Cortes volumétricos
        # Corte XZ (vertical Este-Oeste)
        mid_y = volume_3d.shape[2] // 2
        xz_slice = volume_3d[:, :, mid_y]
        
        fig.add_trace(go.Heatmap(
            z=xz_slice,
            colorscale='Viridis',
            name='Corte XZ',
            visible=False
        ))
        
        # Corte YZ (vertical Norte-Sur)
        mid_x = volume_3d.shape[1] // 2
        yz_slice = volume_3d[:, mid_x, :]
        
        fig.add_trace(go.Heatmap(
            z=yz_slice,
            colorscale='Viridis',
            name='Corte YZ',
            visible=False
        ))
        
        # Layout con controles
        fig.update_layout(
            title='Análisis Tomográfico 3D',
            scene=dict(
                xaxis_title='Longitud',
                yaxis_title='Latitud',
                zaxis_title='Elevación (m)'
            ),
            updatemenus=[
                dict(
                    buttons=[
                        dict(label="Vista XY", method="update", args=[{"visible": [True, True, False, False]}]),
                        dict(label="Corte XZ", method="update", args=[{"visible": [False, False, True, False]}]),
                        dict(label="Corte YZ", method="update", args=[{"visible": [False, False, False, True]}]),
                        dict(label="3D Completo", method="update", args=[{"visible": [True, True, True, True]}])
                    ],
                    direction="down",
                    showactive=True,
                )
            ]
        )
        
        return fig
```

### 4.2 Heatmaps Dinámicos
```python
def create_dynamic_heatmaps(self, stack_2d, volume_3d):
    """
    Crear heatmaps dinámicos por variable
    
    Variables:
    - Humedad (SMAP)
    - Salinidad (SMOS)
    - Vegetación (NDVI)
    - Temperatura (LST)
    - Penetración SAR (L-band)
    """
    
    fig = go.Figure()
    
    # Agregar cada variable como trace
    variables = [
        ('NDVI', stack_2d[0], 'Greens'),
        ('LST', stack_2d[1], 'Hot'),
        ('Humedad', stack_2d[5], 'Blues'),
        ('Salinidad', stack_2d[4], 'YlOrRd'),
        ('SAR L-band', volume_3d[5], 'Greys')
    ]
    
    for i, (name, data, colorscale) in enumerate(variables):
        fig.add_trace(go.Heatmap(
            z=data,
            colorscale=colorscale,
            name=name,
            visible=(i == 0)  # Solo primera visible
        ))
    
    # Dropdown para seleccionar variable
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(label=name, method="update", 
                         args=[{"visible": [j == i for j in range(len(variables))]}])
                    for i, (name, _, _) in enumerate(variables)
                ],
                direction="down",
                showactive=True,
            )
        ],
        title='Heatmaps Dinámicos por Variable'
    )
    
    return fig
```

### 4.3 Filtros por Instrumento
```python
def create_instrument_filter_view(self, datasets):
    """
    Vista con filtros por instrumento
    
    Permite activar/desactivar cada instrumento para ver su contribución
    """
    
    fig = go.Figure()
    
    instruments = [
        'NDVI', 'LST', 'SAR C-band', 'SAR L-band',
        'Roughness', 'Salinity', 'DEM', 'ICESat-2',
        'GEDI', 'SMAP'
    ]
    
    for i, instrument in enumerate(instruments):
        data = datasets[instrument.lower().replace(' ', '_').replace('-', '_')]
        
        fig.add_trace(go.Heatmap(
            z=data,
            name=instrument,
            visible=True,
            opacity=0.7
        ))
    
    # Checkboxes para cada instrumento
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Todos",
                        method="update",
                        args=[{"visible": [True] * len(instruments)}]
                    ),
                    dict(
                        label="Ninguno",
                        method="update",
                        args=[{"visible": [False] * len(instruments)}]
                    )
                ] + [
                    dict(
                        label=inst,
                        method="update",
                        args=[{"visible": [j == i for j in range(len(instruments))]}]
                    )
                    for i, inst in enumerate(instruments)
                ]
            )
        ]
    )
    
    return fig
```

---

## 5️⃣ OUTPUTS FINALES

### 5.1 Score Global por Sitio
```python
class TomographicScorer:
    """Calculador de score global tomográfico"""
    
    def calculate_global_score(self, features, ml_model):
        """
        Calcular score global combinando múltiples factores
        
        Componentes:
        - ML Interest Score (40%): Predicción del modelo
        - Volumetric Anomaly Score (25%): Anomalías en volumen 3D
        - Temporal Anomaly Score (15%): Anomalías temporales
        - ESS Score (10%): Explanatory Strangeness
        - Geometric Score (10%): Geometría y simetría
        
        Output: Score [0, 1]
        """
        
        # 1. ML Interest Score
        ml_score = ml_model.predict([features])[0]
        
        # 2. Volumetric Anomaly Score
        volumetric_score = self._calculate_volumetric_anomaly(features)
        
        # 3. Temporal Anomaly Score
        temporal_score = self._calculate_temporal_anomaly(features)
        
        # 4. ESS Score
        ess_score = features.get('ess_score', 0)
        
        # 5. Geometric Score
        geometric_score = self._calculate_geometric_score(features)
        
        # Combinar con pesos
        global_score = (
            ml_score * 0.40 +
            volumetric_score * 0.25 +
            temporal_score * 0.15 +
            ess_score * 0.10 +
            geometric_score * 0.10
        )
        
        return {
            'global_score': global_score,
            'ml_score': ml_score,
            'volumetric_score': volumetric_score,
            'temporal_score': temporal_score,
            'ess_score': ess_score,
            'geometric_score': geometric_score,
            'classification': self._classify_score(global_score)
        }
    
    def _classify_score(self, score):
        """Clasificar score en categorías"""
        if score >= 0.8:
            return "EXCEPTIONAL_INTEREST"
        elif score >= 0.6:
            return "HIGH_INTEREST"
        elif score >= 0.3:
            return "MODERATE_INTEREST"
        else:
            return "LOW_INTEREST"
```

### 5.2 Visualización Volumétrica Exportable
```python
def export_3d_visualization(self, volume_3d, metadata, output_path):
    """
    Exportar visualización volumétrica en múltiples formatos
    
    Formatos:
    - HTML interactivo (Plotly)
    - PNG/JPG (imágenes estáticas)
    - GIF animado (rotación 360°)
    - MP4 video (fly-through)
    - OBJ/STL (modelo 3D para impresión)
    """
    
    # 1. HTML interactivo
    fig = self.create_3d_volume_plot(volume_3d, metadata)
    fig.write_html(f"{output_path}/tomographic_view.html")
    
    # 2. Imágenes estáticas (múltiples ángulos)
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for angle in angles:
        fig.update_layout(scene_camera=dict(eye=dict(x=np.cos(np.radians(angle)), 
                                                       y=np.sin(np.radians(angle)), 
                                                       z=1)))
        fig.write_image(f"{output_path}/view_{angle}.png")
    
    # 3. GIF animado
    self._create_animated_gif(volume_3d, f"{output_path}/rotation.gif")
    
    # 4. Datos procesados
    self._export_processed_data(volume_3d, metadata, output_path)
```

### 5.3 Export de Datos Procesados
```python
def export_processed_data(self, volume_3d, stack_2d, metadata, output_path):
    """
    Exportar datos procesados en formatos estándar
    
    Formatos:
    - GeoTIFF: Rasters georreferenciados
    - Shapefile: Vectores con scores
    - NetCDF: Volumen 3D completo
    - JSON: Metadata y scores
    """
    
    import rasterio
    from rasterio.transform import from_bounds
    
    # 1. GeoTIFF para cada capa
    bounds = metadata['bounds']
    transform = from_bounds(
        bounds['lon_min'], bounds['lat_min'],
        bounds['lon_max'], bounds['lat_max'],
        volume_3d.shape[2], volume_3d.shape[1]
    )
    
    for i in range(volume_3d.shape[0]):
        with rasterio.open(
            f"{output_path}/layer_{i}.tif",
            'w',
            driver='GTiff',
            height=volume_3d.shape[1],
            width=volume_3d.shape[2],
            count=1,
            dtype=volume_3d.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(volume_3d[i], 1)
    
    # 2. NetCDF para volumen completo
    import netCDF4 as nc
    
    dataset = nc.Dataset(f"{output_path}/volume_3d.nc", 'w')
    dataset.createDimension('z', volume_3d.shape[0])
    dataset.createDimension('y', volume_3d.shape[1])
    dataset.createDimension('x', volume_3d.shape[2])
    
    volume_var = dataset.createVariable('volume', 'f4', ('z', 'y', 'x'))
    volume_var[:] = volume_3d
    
    dataset.close()
    
    # 3. JSON con metadata y scores
    import json
    
    output_json = {
        'metadata': metadata,
        'scores': metadata.get('scores', {}),
        'instruments_used': metadata.get('instruments', []),
        'processing_date': metadata.get('timestamp', ''),
        'bounds': bounds
    }
    
    with open(f"{output_path}/metadata.json", 'w') as f:
        json.dump(output_json, f, indent=2)
```

### 5.4 Dashboard con Series Temporales
```python
def create_temporal_dashboard(self, temporal_data, scores):
    """
    Crear dashboard con series temporales y scores
    
    Componentes:
    - Gráficos de series temporales (NDVI, LST, SMAP)
    - Heatmap de correlaciones
    - Scores por componente
    - Recomendaciones
    """
    
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'NDVI Temporal', 'LST Temporal',
            'SMAP Humedad', 'Correlaciones',
            'Scores Componentes', 'Clasificación'
        )
    )
    
    # 1. NDVI temporal
    fig.add_trace(
        go.Scatter(x=temporal_data['dates'], y=temporal_data['ndvi'],
                   name='NDVI', line=dict(color='green')),
        row=1, col=1
    )
    
    # 2. LST temporal
    fig.add_trace(
        go.Scatter(x=temporal_data['dates'], y=temporal_data['lst'],
                   name='LST', line=dict(color='red')),
        row=1, col=2
    )
    
    # 3. SMAP humedad
    fig.add_trace(
        go.Scatter(x=temporal_data['dates'], y=temporal_data['smap'],
                   name='Humedad', line=dict(color='blue')),
        row=2, col=1
    )
    
    # 4. Heatmap de correlaciones
    corr_matrix = self._calculate_correlations(temporal_data)
    fig.add_trace(
        go.Heatmap(z=corr_matrix, colorscale='RdBu'),
        row=2, col=2
    )
    
    # 5. Scores por componente
    fig.add_trace(
        go.Bar(
            x=list(scores.keys()),
            y=list(scores.values()),
            marker=dict(color='lightblue')
        ),
        row=3, col=1
    )
    
    # 6. Clasificación final
    classification = scores.get('classification', 'UNKNOWN')
    color = self._get_classification_color(classification)
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=scores.get('global_score', 0) * 100,
            title={'text': classification},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': color}}
        ),
        row=3, col=2
    )
    
    fig.update_layout(height=1000, showlegend=False,
                      title_text="Dashboard Tomográfico Temporal")
    
    return fig
```

---

## 6️⃣ COMBINACIONES CRÍTICAS

### 6.1 Stack Reducido (Inicio Rápido)
```python
# Combinación mínima para análisis volumétrico informativo

CRITICAL_STACK = {
    'elevation': 'DEM',           # Micro-relieve
    'laser': 'ICESat-2',          # Precisión vertical
    'vegetation_3d': 'GEDI',      # Estructura vegetación
    'penetration': 'SAR L-band',  # Bajo vegetación
    'surface': 'NDVI'             # Estado superficial
}

# Esto da:
# - Cortes volumétricos XY, XZ, YZ
# - Penetración bajo vegetación
# - Micro-relieve preciso
# - Estructura 3D completa
```

### 6.2 Estado Ecosistémico
```python
# Combinación para análisis de "salud" del ecosistema

ECOSYSTEM_STACK = {
    'vegetation': 'NDVI',
    'temperature': 'LST',
    'moisture': 'SMAP',
    'salinity': 'SMOS'
}

# Permite:
# - Correlación humedad-vegetación
# - Anomalías térmicas
# - Estrés hídrico
# - Salinización
```

### 6.3 Penetración Completa
```python
# Combinación para máxima penetración

PENETRATION_STACK = {
    'surface': 'SAR C-band',      # Superficie
    'subsurface': 'SAR L-band',   # 0-30cm
    'deep': 'SMAP',               # 30-50cm
    'structure': 'GEDI'           # Vegetación
}

# Permite:
# - Ver bajo vegetación densa
# - Detectar estructuras enterradas
# - Mapear humedad profunda
```

### 6.4 Temporalidad Completa
```python
# Series temporales para análisis 4D

TEMPORAL_STACK = {
    'ndvi_12m': 'NDVI histórico (12 meses)',
    'lst_12m': 'LST histórico (12 meses)',
    'smap_12m': 'SMAP histórico (12 meses)'
}

# Permite:
# - Detectar estacionalidad
# - Identificar tendencias
# - Anomalías temporales
# - Cambios de uso de suelo
```

---


## 7️⃣ IMPLEMENTACIÓN PRÁCTICA

### 7.1 Estructura de Archivos
```
backend/
├── volumetric/
│   ├── tomographic_preprocessor.py      # Preprocesamiento
│   ├── tomographic_ml_analyzer.py       # Análisis ML
│   ├── tomographic_visualizer.py        # Visualización 3D
│   ├── tomographic_scorer.py            # Scoring global
│   └── tomographic_exporter.py          # Export de datos
├── ai/
│   └── multimodal_ml_model.py           # Modelo ML multimodal
└── api/
    └── tomographic_endpoint.py          # API endpoint

frontend/
├── modules/
│   ├── tomographic_viewer_module.js     # Visor 3D
│   └── temporal_dashboard_module.js     # Dashboard temporal
└── styles/
    └── tomographic_viewer.css           # Estilos
```

### 7.2 API Endpoint
```python
# backend/api/tomographic_endpoint.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/tomographic", tags=["tomographic"])

class TomographicAnalysisRequest(BaseModel):
    site_id: str
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    include_temporal: bool = True
    temporal_months: int = 12
    resolution_m: int = 30

@router.post("/analyze")
async def analyze_tomographic(request: TomographicAnalysisRequest):
    """
    Análisis tomográfico completo de un sitio
    
    Pasos:
    1. Obtener datos de 10 instrumentos
    2. Preprocesar y alinear
    3. Crear volumen 3D
    4. Extraer features
    5. Calcular scores ML
    6. Generar visualizaciones
    7. Exportar resultados
    """
    
    try:
        # 1. Obtener datos
        datasets = await fetch_all_instruments(
            request.lat_min, request.lat_max,
            request.lon_min, request.lon_max
        )
        
        # 2. Preprocesar
        preprocessor = TomographicPreprocessor()
        stack_2d = preprocessor.create_2d_stack(datasets)
        volume_3d = preprocessor.create_3d_volume(datasets)
        
        # 3. Análisis ML
        analyzer = TomographicMLAnalyzer()
        features = analyzer.extract_site_features(
            volume_3d, stack_2d, 
            temporal_data=datasets.get('temporal', {})
        )
        
        # 4. Scoring
        scorer = TomographicScorer()
        scores = scorer.calculate_global_score(features, ml_model)
        
        # 5. Visualización
        visualizer = TomographicVisualizer()
        viz_3d = visualizer.create_3d_volume_plot(volume_3d, {
            'ess_score': scores['ess_score'],
            'bounds': {
                'lat_min': request.lat_min,
                'lat_max': request.lat_max,
                'lon_min': request.lon_min,
                'lon_max': request.lon_max
            }
        })
        
        # 6. Export
        exporter = TomographicExporter()
        export_path = f"exports/{request.site_id}"
        exporter.export_all(volume_3d, stack_2d, scores, export_path)
        
        return {
            'site_id': request.site_id,
            'scores': scores,
            'features': features,
            'visualization_url': f"/exports/{request.site_id}/tomographic_view.html",
            'data_exports': {
                'geotiff': f"{export_path}/layers/",
                'netcdf': f"{export_path}/volume_3d.nc",
                'metadata': f"{export_path}/metadata.json"
            },
            'instruments_used': list(datasets.keys()),
            'coverage': len(datasets) / 10.0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tomographic analysis failed: {str(e)}")
```

### 7.3 Frontend Integration
```javascript
// frontend/modules/tomographic_viewer_module.js

class TomographicViewerModule {
    constructor() {
        this.currentSite = null;
        this.volume3D = null;
        this.viewer = null;
    }
    
    async analyzeSite(siteId, bounds) {
        console.log(`[Tomographic] Analyzing site ${siteId}...`);
        
        try {
            // 1. Llamar API
            const response = await fetch('/api/tomographic/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    site_id: siteId,
                    lat_min: bounds.lat_min,
                    lat_max: bounds.lat_max,
                    lon_min: bounds.lon_min,
                    lon_max: bounds.lon_max,
                    include_temporal: true,
                    temporal_months: 12,
                    resolution_m: 30
                })
            });
            
            const result = await response.json();
            
            // 2. Mostrar scores
            this.displayScores(result.scores);
            
            // 3. Cargar visualización 3D
            this.loadVisualization(result.visualization_url);
            
            // 4. Mostrar dashboard temporal
            this.loadTemporalDashboard(result.site_id);
            
            // 5. Notificar
            this.showNotification(
                `Análisis tomográfico completado. Score global: ${(result.scores.global_score * 100).toFixed(1)}%`,
                'success'
            );
            
            return result;
            
        } catch (error) {
            console.error('[Tomographic] Error:', error);
            this.showNotification('Error en análisis tomográfico', 'error');
            throw error;
        }
    }
    
    displayScores(scores) {
        const container = document.getElementById('tomographicScores');
        
        container.innerHTML = `
            <div class="tomographic-scores">
                <h3>📊 Scores Tomográficos</h3>
                
                <div class="score-card global">
                    <div class="score-label">Score Global</div>
                    <div class="score-value">${(scores.global_score * 100).toFixed(1)}%</div>
                    <div class="score-classification">${scores.classification}</div>
                </div>
                
                <div class="score-components">
                    <div class="score-item">
                        <span>ML Interest:</span>
                        <span>${(scores.ml_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="score-item">
                        <span>Volumétrico:</span>
                        <span>${(scores.volumetric_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="score-item">
                        <span>Temporal:</span>
                        <span>${(scores.temporal_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="score-item">
                        <span>ESS:</span>
                        <span>${(scores.ess_score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="score-item">
                        <span>Geométrico:</span>
                        <span>${(scores.geometric_score * 100).toFixed(1)}%</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    loadVisualization(url) {
        const iframe = document.getElementById('tomographicViewer');
        iframe.src = url;
    }
}

// Exportar
window.tomographicViewerModule = new TomographicViewerModule();
```

---

## 8️⃣ ROADMAP DE IMPLEMENTACIÓN

### Fase 1: Fundamentos (2 semanas)
```
✅ Semana 1:
- Implementar TomographicPreprocessor
- Crear stack 2D básico
- Alinear datasets
- Tests unitarios

✅ Semana 2:
- Implementar volumen 3D básico
- Integrar DEM + ICESat-2 + GEDI
- Visualización simple 3D
- Tests de integración
```

### Fase 2: ML y Scoring (2 semanas)
```
✅ Semana 3:
- Extraer features multidimensionales
- Implementar series temporales
- Crear dataset de entrenamiento
- Tests de features

✅ Semana 4:
- Entrenar modelo ML
- Implementar scoring global
- Validación cruzada
- Tests de modelo
```

### Fase 3: Visualización Avanzada (2 semanas)
```
✅ Semana 5:
- Visualizador 3D interactivo
- Cortes volumétricos
- Heatmaps dinámicos
- Tests de visualización

✅ Semana 6:
- Dashboard temporal
- Filtros por instrumento
- Export de visualizaciones
- Tests de UI
```

### Fase 4: Integración y Deploy (1 semana)
```
✅ Semana 7:
- API endpoint completo
- Frontend integration
- Export de datos
- Documentación
- Tests E2E
```

---

## 9️⃣ CASOS DE USO

### Caso 1: Sitio en Selva Amazónica
```
Instrumentos críticos:
- SAR L-band (penetración bajo vegetación densa)
- GEDI (estructura 3D de canopy)
- SMAP (humedad del suelo)
- NDVI (vegetación superficial)

Análisis:
- Detectar claros anómalos bajo canopy
- Identificar micro-relieve enterrado
- Mapear patrones de drenaje
- Correlacionar humedad con vegetación

Score esperado: 0.7-0.9 (alto interés)
```

### Caso 2: Sitio en Desierto
```
Instrumentos críticos:
- DEM (micro-relieve)
- SAR C-band (superficie)
- Salinity (salinización)
- LST (anomalías térmicas)

Análisis:
- Detectar estructuras enterradas
- Identificar patrones geométricos
- Mapear anomalías de salinidad
- Detectar variaciones térmicas

Score esperado: 0.6-0.8 (alto interés)
```

### Caso 3: Sitio en Glaciar
```
Instrumentos críticos:
- ICESat-2 (precisión centimétrica)
- SAR C-band (penetración hielo)
- LST (temperatura superficial)
- DEM (topografía)

Análisis:
- Detectar estructuras bajo hielo
- Mapear variaciones de espesor
- Identificar anomalías térmicas
- Correlacionar con topografía

Score esperado: 0.5-0.7 (interés moderado-alto)
```

---

## 🔟 MÉTRICAS DE ÉXITO

### Métricas Técnicas
```
✅ Cobertura instrumental: >80% de los 10 instrumentos
✅ Tiempo de procesamiento: <5 minutos por sitio
✅ Precisión del modelo ML: R² >0.75
✅ Resolución espacial: 30m o mejor
✅ Resolución vertical: 10 capas mínimo
```

### Métricas Científicas
```
✅ Reproducibilidad: 100% (determinístico)
✅ Validación con sitios conocidos: >90% accuracy
✅ Detección de falsos positivos: <10%
✅ Correlación con validación de campo: >0.80
```

### Métricas de Usuario
```
✅ Tiempo de carga visualización: <10 segundos
✅ Interactividad: 60 FPS en 3D
✅ Facilidad de uso: <5 clicks para análisis completo
✅ Exportabilidad: 5 formatos disponibles
```

---

## 📚 REFERENCIAS Y RECURSOS

### Papers Científicos
1. "Multi-sensor fusion for archaeological prospection" (2023)
2. "3D volumetric analysis using LiDAR and SAR" (2022)
3. "Machine learning for remote sensing archaeology" (2024)

### Datasets
1. Copernicus Open Access Hub (Sentinel-1, Sentinel-2)
2. NASA EarthData (MODIS, ICESat-2, GEDI, SMAP)
3. ASF DAAC (PALSAR)
4. OpenTopography (DEM)

### Herramientas
1. GDAL/Rasterio (procesamiento geoespacial)
2. Scikit-learn (ML)
3. Plotly (visualización 3D)
4. NetCDF4 (datos volumétricos)

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Preprocesamiento
- [ ] Reproyección de datasets
- [ ] Alineación espacial
- [ ] Stack 2D (6 bandas)
- [ ] Volumen 3D (10 capas)
- [ ] Normalización para ML

### Análisis ML
- [ ] Extracción de features (50 total)
- [ ] Series temporales (NDVI, LST, SMAP)
- [ ] Modelo de scoring
- [ ] Validación cruzada
- [ ] Interpretabilidad

### Visualización
- [ ] Visor 3D interactivo
- [ ] Cortes volumétricos (XY, XZ, YZ)
- [ ] Heatmaps dinámicos
- [ ] Dashboard temporal
- [ ] Filtros por instrumento

### Export
- [ ] GeoTIFF (capas individuales)
- [ ] NetCDF (volumen completo)
- [ ] Shapefile (vectores)
- [ ] JSON (metadata)
- [ ] HTML (visualización)

### Integración
- [ ] API endpoint
- [ ] Frontend module
- [ ] Tests E2E
- [ ] Documentación
- [ ] Deploy

---

## 🎯 CONCLUSIÓN

Este pipeline tomográfico multimodal representa un **salto cualitativo** en el análisis arqueológico remoto:

### Ventajas
✅ **Análisis volumétrico completo** (no solo superficial)
✅ **Integración de 10 instrumentos** (máxima información)
✅ **ML para scoring inteligente** (pero NO para decisiones)
✅ **Visualización tipo CT scan** (intuitivarevolucionaria)
✅ **Reproducible y científico** (determinístico + validable)

### Aplicaciones
🔬 Detección de estructuras enterradas
🌳 Análisis bajo vegetación densa
🏔️ Micro-relieve y topografía
💧 Patrones de humedad y drenaje
📊 Anomalías volumétricas
⏱️ Cambios temporales (4D)

### Próximos Pasos
1. Implementar Fase 1 (fundamentos)
2. Validar con sitios conocidos
3. Entrenar modelo ML
4. Integrar en ArcheoScope
5. Publicar resultados

---

**Fecha**: 27 de Enero de 2026  
**Sistema**: ArcheoScope v2.2  
**Módulo**: Tomographic Multimodal Pipeline  
**Estado**: Diseño completo ✅ | Implementación pendiente 🚧
