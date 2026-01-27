#!/usr/bin/env python3
"""
ArcheoScope Scientific Dataset Analysis
======================================

Análisis offline de datos capturados para:
- Normalización por terreno
- Detección de outliers
- Correlaciones cruzadas
- Ranking arqueológico reproducible

FASE 2: Análisis científico sobre datos congelados
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False
    print("⚠️ Analysis libraries not available - install with: pip install pandas numpy scipy")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("⚠️ Plotting libraries not available - install with: pip install matplotlib seaborn")

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from dotenv import load_dotenv
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️ PostgreSQL not available - will analyze JSON files only")

class ScientificDatasetAnalyzer:
    """Analizador de dataset científico ArcheoScope."""
    
    def __init__(self):
        self.db_conn = None
        self.measurements_df = None
        self.candidates_df = None
        self.results_data = None
        
        # Intentar conectar a BD
        self._connect_database()
    
    def _connect_database(self):
        """Conectar a PostgreSQL si está disponible."""
        if not POSTGRES_AVAILABLE:
            return
        
        try:
            load_dotenv()
            db_url = os.getenv("DATABASE_URL")
            
            if db_url:
                self.db_conn = psycopg2.connect(db_url)
                logger.info("✅ Database connected")
            else:
                logger.info("⚠️ DATABASE_URL not configured")
                
        except Exception as e:
            logger.info(f"⚠️ Database connection failed: {e}")
    
    def load_data_from_database(self) -> bool:
        """Cargar datos desde PostgreSQL."""
        if not self.db_conn:
            return False
        
        try:
            # Cargar mediciones
            measurements_query = """
                SELECT 
                    candidate_id, candidate_name, terrain_type, country,
                    lat_min, lat_max, lon_min, lon_max,
                    instrument, measurement_type, value, unit, confidence, status,
                    source, measured_at, analysis_version, reason, processing_time_seconds
                FROM raw_measurements 
                WHERE status IN ('SUCCESS', 'DEGRADED')
                ORDER BY candidate_id, instrument;
            """
            
            self.measurements_df = pd.read_sql(measurements_query, self.db_conn)
            logger.info(f"✅ Loaded {len(self.measurements_df)} measurements from database")
            
            # Cargar candidatos
            candidates_query = """
                SELECT 
                    candidate_id, candidate_name, terrain_type, country,
                    lat_min, lat_max, lon_min, lon_max,
                    analysis_status, measurements_count, successful_measurements, coverage_score,
                    created_at, analyzed_at
                FROM analysis_candidates 
                WHERE analysis_status = 'COMPLETED'
                ORDER BY terrain_type, candidate_name;
            """
            
            self.candidates_df = pd.read_sql(candidates_query, self.db_conn)
            logger.info(f"✅ Loaded {len(self.candidates_df)} candidates from database")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load from database: {e}")
            return False
    
    def load_data_from_json(self) -> bool:
        """Cargar datos desde archivos JSON."""
        
        # Buscar el archivo de resultados más reciente
        json_files = list(Path('.').glob('scientific_dataset_results_*.json'))
        
        if not json_files:
            logger.error("❌ No scientific dataset JSON files found")
            return False
        
        # Usar el más reciente
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_file, 'r') as f:
                self.results_data = json.load(f)
            
            logger.info(f"✅ Loaded data from: {latest_file}")
            
            # Convertir a DataFrames
            self._convert_json_to_dataframes()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load JSON: {e}")
            return False
    
    def _convert_json_to_dataframes(self):
        """Convertir datos JSON a DataFrames de pandas."""
        
        if not self.results_data:
            return
        
        # Extraer mediciones de todos los candidatos
        measurements_data = []
        candidates_data = []
        
        for candidate in self.results_data.get('candidate_details', []):
            if not candidate.get('success', False):
                continue
            
            # Datos del candidato
            candidates_data.append({
                'candidate_id': candidate['candidate_id'],
                'candidate_name': candidate['candidate_name'],
                'terrain_type': candidate['terrain'],
                'country': candidate.get('country', 'Unknown'),
                'lat_min': candidate['coordinates']['lat_min'],
                'lat_max': candidate['coordinates']['lat_max'],
                'lon_min': candidate['coordinates']['lon_min'],
                'lon_max': candidate['coordinates']['lon_max'],
                'coverage_score': candidate['coverage_score'],
                'total_instruments': candidate['total_instruments'],
                'usable_instruments': candidate['usable_instruments']
            })
            
            # Mediciones del candidato
            for measurement in candidate.get('measurements', []):
                if measurement.get('status') in ['SUCCESS', 'DEGRADED'] and measurement.get('value') is not None:
                    measurements_data.append({
                        'candidate_id': candidate['candidate_id'],
                        'candidate_name': candidate['candidate_name'],
                        'terrain_type': candidate['terrain'],
                        'country': candidate.get('country', 'Unknown'),
                        'instrument': measurement['instrument'],
                        'measurement_type': measurement.get('measurement_type', 'unknown'),
                        'value': measurement['value'],
                        'unit': measurement.get('unit', 'units'),
                        'confidence': measurement.get('confidence', 0.5),
                        'status': measurement['status'],
                        'source': measurement.get('source', 'unknown'),
                        'reason': measurement.get('reason', ''),
                        'processing_time_seconds': measurement.get('processing_time_s', 0)
                    })
        
        self.measurements_df = pd.DataFrame(measurements_data)
        self.candidates_df = pd.DataFrame(candidates_data)
        
        logger.info(f"✅ Converted to DataFrames: {len(self.measurements_df)} measurements, {len(self.candidates_df)} candidates")
    
    def load_data(self) -> bool:
        """Cargar datos desde BD o JSON."""
        
        # Intentar BD primero
        if self.load_data_from_database():
            return True
        
        # Fallback a JSON
        return self.load_data_from_json()
    
    def normalize_by_terrain(self) -> pd.DataFrame:
        """Normalizar valores por terreno e instrumento."""
        
        if self.measurements_df is None or len(self.measurements_df) == 0:
            logger.error("❌ No measurements data available")
            return pd.DataFrame()
        
        logger.info("🔄 Normalizing measurements by terrain and instrument...")
        
        normalized_data = self.measurements_df.copy()
        normalized_data['normalized_value'] = np.nan
        
        for terrain in normalized_data['terrain_type'].unique():
            terrain_mask = normalized_data['terrain_type'] == terrain
            
            for instrument in normalized_data[terrain_mask]['instrument'].unique():
                instrument_mask = (normalized_data['terrain_type'] == terrain) & (normalized_data['instrument'] == instrument)
                values = normalized_data[instrument_mask]['value'].dropna()
                
                if len(values) > 1:
                    # Z-score normalization
                    mean_val = values.mean()
                    std_val = values.std()
                    
                    if std_val > 0:
                        normalized_values = (values - mean_val) / std_val
                        normalized_data.loc[instrument_mask, 'normalized_value'] = normalized_values
                    else:
                        # Si no hay variación, usar 0
                        normalized_data.loc[instrument_mask, 'normalized_value'] = 0.0
        
        logger.info(f"✅ Normalized {len(normalized_data)} measurements")
        return normalized_data
    
    def detect_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Detectar outliers por terreno e instrumento."""
        
        logger.info("🔍 Detecting outliers...")
        
        outliers = []
        
        for terrain in data['terrain_type'].unique():
            for instrument in data['instrument'].unique():
                subset = data[
                    (data['terrain_type'] == terrain) & 
                    (data['instrument'] == instrument)
                ]
                
                if len(subset) >= 3:
                    values = subset['value'].dropna()
                    
                    if len(values) >= 3:
                        z_scores = np.abs(stats.zscore(values))
                        outlier_mask = z_scores > 2.5
                        
                        if outlier_mask.any():
                            outlier_data = subset.iloc[outlier_mask.values].copy()
                            outlier_data['outlier_score'] = z_scores[outlier_mask]
                            outliers.append(outlier_data)
        
        outliers_df = pd.concat(outliers, ignore_index=True) if outliers else pd.DataFrame()
        
        logger.info(f"✅ Detected {len(outliers_df)} outliers")
        return outliers_df
    
    def calculate_correlations(self, data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Calcular correlaciones entre instrumentos por terreno."""
        
        logger.info("📊 Calculating instrument correlations...")
        
        correlations = {}
        
        for terrain in data['terrain_type'].unique():
            terrain_data = data[data['terrain_type'] == terrain]
            
            # Pivot para tener instrumentos como columnas
            pivot_data = terrain_data.pivot_table(
                index='candidate_id',
                columns='instrument',
                values='value',
                aggfunc='mean'
            )
            
            if len(pivot_data) > 2 and len(pivot_data.columns) > 1:
                corr_matrix = pivot_data.corr()
                correlations[terrain] = corr_matrix
                
                logger.info(f"   {terrain}: {len(pivot_data)} candidates, {len(pivot_data.columns)} instruments")
        
        logger.info(f"✅ Calculated correlations for {len(correlations)} terrains")
        return correlations
    
    def generate_archaeological_ranking(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generar ranking arqueológico basado en anomalías."""
        
        logger.info("🏆 Generating archaeological ranking...")
        
        candidate_scores = []
        
        for candidate_id in data['candidate_id'].unique():
            candidate_data = data[data['candidate_id'] == candidate_id]
            
            if len(candidate_data) == 0:
                continue
            
            # Información básica del candidato
            first_row = candidate_data.iloc[0]
            
            # Score basado en desviaciones normalizadas
            anomaly_score = 0.0
            weight_sum = 0.0
            instrument_count = 0
            
            for _, row in candidate_data.iterrows():
                if pd.notna(row.get('normalized_value')):
                    # Peso por confianza del instrumento
                    confidence = row.get('confidence', 0.5)
                    weight = max(confidence, 0.1)  # Mínimo 0.1
                    
                    # Contribución de anomalía (valores extremos = más arqueológico)
                    normalized_val = row['normalized_value']
                    anomaly_contribution = abs(normalized_val) * weight
                    
                    anomaly_score += anomaly_contribution
                    weight_sum += weight
                    instrument_count += 1
            
            # Normalizar score
            if weight_sum > 0:
                final_score = anomaly_score / weight_sum
            else:
                final_score = 0.0
            
            # Bonus por diversidad de instrumentos
            diversity_bonus = min(instrument_count / 4.0, 1.0)  # Máximo con 4+ instrumentos
            final_score *= (0.7 + 0.3 * diversity_bonus)
            
            # Obtener coverage score si está disponible
            coverage_score = 0.0
            if self.candidates_df is not None:
                candidate_info = self.candidates_df[
                    self.candidates_df['candidate_id'] == candidate_id
                ]
                if len(candidate_info) > 0:
                    coverage_score = candidate_info.iloc[0].get('coverage_score', 0.0)
            
            candidate_scores.append({
                'candidate_id': candidate_id,
                'candidate_name': first_row['candidate_name'],
                'terrain_type': first_row['terrain_type'],
                'country': first_row.get('country', 'Unknown'),
                'anomaly_score': final_score,
                'coverage_score': coverage_score,
                'instrument_count': instrument_count,
                'weighted_instruments': weight_sum
            })
        
        ranking_df = pd.DataFrame(candidate_scores)
        ranking_df = ranking_df.sort_values('anomaly_score', ascending=False)
        ranking_df['rank'] = range(1, len(ranking_df) + 1)
        
        logger.info(f"✅ Generated ranking for {len(ranking_df)} candidates")
        return ranking_df
    
    def generate_terrain_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generar resumen por terreno."""
        
        logger.info("🌍 Generating terrain summary...")
        
        terrain_stats = []
        
        for terrain in data['terrain_type'].unique():
            terrain_data = data[data['terrain_type'] == terrain]
            
            # Estadísticas básicas
            candidates = terrain_data['candidate_id'].nunique()
            measurements = len(terrain_data)
            instruments = terrain_data['instrument'].nunique()
            
            # Estadísticas de valores
            values = terrain_data['value'].dropna()
            
            stats_dict = {
                'terrain_type': terrain,
                'candidates': candidates,
                'measurements': measurements,
                'instruments': instruments,
                'avg_confidence': terrain_data['confidence'].mean(),
                'value_mean': values.mean() if len(values) > 0 else 0,
                'value_std': values.std() if len(values) > 0 else 0,
                'value_min': values.min() if len(values) > 0 else 0,
                'value_max': values.max() if len(values) > 0 else 0
            }
            
            # Coverage score promedio si está disponible
            if self.candidates_df is not None:
                terrain_candidates = self.candidates_df[
                    self.candidates_df['terrain_type'] == terrain
                ]
                if len(terrain_candidates) > 0:
                    stats_dict['avg_coverage_score'] = terrain_candidates['coverage_score'].mean()
            
            terrain_stats.append(stats_dict)
        
        terrain_df = pd.DataFrame(terrain_stats)
        terrain_df = terrain_df.sort_values('candidates', ascending=False)
        
        logger.info(f"✅ Generated summary for {len(terrain_df)} terrains")
        return terrain_df
    
    def save_analysis_results(self, normalized_data: pd.DataFrame, 
                            outliers: pd.DataFrame,
                            correlations: Dict[str, pd.DataFrame],
                            ranking: pd.DataFrame,
                            terrain_summary: pd.DataFrame):
        """Guardar resultados del análisis."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Crear directorio de resultados
        results_dir = Path(f'analysis_results_{timestamp}')
        results_dir.mkdir(exist_ok=True)
        
        try:
            # Guardar DataFrames
            normalized_data.to_csv(results_dir / 'normalized_measurements.csv', index=False)
            outliers.to_csv(results_dir / 'outliers.csv', index=False)
            ranking.to_csv(results_dir / 'archaeological_ranking.csv', index=False)
            terrain_summary.to_csv(results_dir / 'terrain_summary.csv', index=False)
            
            # Guardar correlaciones
            correlations_dir = results_dir / 'correlations'
            correlations_dir.mkdir(exist_ok=True)
            
            for terrain, corr_matrix in correlations.items():
                corr_matrix.to_csv(correlations_dir / f'{terrain}_correlations.csv')
            
            # Generar reporte JSON
            report = {
                'analysis_timestamp': datetime.now().isoformat(),
                'data_summary': {
                    'total_measurements': len(normalized_data),
                    'total_candidates': normalized_data['candidate_id'].nunique(),
                    'total_terrains': normalized_data['terrain_type'].nunique(),
                    'total_instruments': normalized_data['instrument'].nunique(),
                    'outliers_detected': len(outliers)
                },
                'top_candidates': ranking.head(10).to_dict('records'),
                'terrain_summary': terrain_summary.to_dict('records'),
                'files_generated': {
                    'normalized_measurements': 'normalized_measurements.csv',
                    'outliers': 'outliers.csv',
                    'ranking': 'archaeological_ranking.csv',
                    'terrain_summary': 'terrain_summary.csv',
                    'correlations': 'correlations/'
                }
            }
            
            with open(results_dir / 'analysis_report.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"✅ Analysis results saved to: {results_dir}")
            return results_dir
            
        except Exception as e:
            logger.error(f"❌ Failed to save results: {e}")
            return None
    
    def print_summary_report(self, ranking: pd.DataFrame, terrain_summary: pd.DataFrame, 
                           outliers: pd.DataFrame, correlations: Dict[str, pd.DataFrame]):
        """Imprimir reporte resumen."""
        
        print("\n" + "=" * 60)
        print("📊 ARCHEOSCOPE SCIENTIFIC DATASET ANALYSIS REPORT")
        print("=" * 60)
        
        # Estadísticas generales
        if self.measurements_df is not None:
            print(f"📈 DATASET STATISTICS:")
            print(f"   Total measurements: {len(self.measurements_df)}")
            print(f"   Total candidates: {self.measurements_df['candidate_id'].nunique()}")
            print(f"   Terrains analyzed: {self.measurements_df['terrain_type'].nunique()}")
            print(f"   Instruments used: {self.measurements_df['instrument'].nunique()}")
            print(f"   Outliers detected: {len(outliers)}")
        
        # Top candidatos arqueológicos
        print(f"\n🏆 TOP 10 ARCHAEOLOGICAL CANDIDATES:")
        print("-" * 50)
        for _, row in ranking.head(10).iterrows():
            print(f"{row['rank']:2d}. {row['candidate_name']:20} ({row['terrain_type']:8}) "
                  f"Score: {row['anomaly_score']:.3f} | Instruments: {row['instrument_count']}")
        
        # Resumen por terreno
        print(f"\n🌍 TERRAIN ANALYSIS:")
        print("-" * 50)
        for _, row in terrain_summary.iterrows():
            coverage_info = ""
            if 'avg_coverage_score' in row:
                coverage_info = f" | Coverage: {row['avg_coverage_score']:.1%}"
            
            print(f"{row['terrain_type']:8}: {row['candidates']} candidates, "
                  f"{row['measurements']} measurements, {row['instruments']} instruments{coverage_info}")
        
        # Correlaciones más fuertes
        print(f"\n📊 STRONGEST CORRELATIONS:")
        print("-" * 50)
        
        for terrain, corr_matrix in correlations.items():
            if len(corr_matrix) > 1:
                # Encontrar la correlación más fuerte (excluyendo diagonal)
                corr_values = corr_matrix.values
                np.fill_diagonal(corr_values, 0)  # Excluir diagonal
                
                max_corr_idx = np.unravel_index(np.argmax(np.abs(corr_values)), corr_values.shape)
                max_corr_value = corr_values[max_corr_idx]
                
                if abs(max_corr_value) > 0.1:  # Solo mostrar correlaciones significativas
                    inst1 = corr_matrix.index[max_corr_idx[0]]
                    inst2 = corr_matrix.columns[max_corr_idx[1]]
                    print(f"   {terrain:8}: {inst1} ↔ {inst2} (r={max_corr_value:.3f})")
        
        print("\n🔬 SCIENTIFIC INSIGHTS:")
        print("-" * 50)
        
        # Insights automáticos
        if len(ranking) > 0:
            top_terrain = ranking.iloc[0]['terrain_type']
            print(f"   • Top candidate is in {top_terrain} terrain")
            
            terrain_counts = ranking['terrain_type'].value_counts()
            if len(terrain_counts) > 1:
                dominant_terrain = terrain_counts.index[0]
                print(f"   • {dominant_terrain} terrain dominates top rankings ({terrain_counts.iloc[0]}/{len(ranking.head(10))} in top 10)")
        
        if len(outliers) > 0:
            outlier_terrains = outliers['terrain_type'].value_counts()
            print(f"   • Most outliers in {outlier_terrains.index[0]} terrain ({outlier_terrains.iloc[0]} outliers)")
        
        print(f"\n✅ ANALYSIS COMPLETE - ArcheoScope dataset scientifically analyzed!")
        print("=" * 60)
    
    def run_complete_analysis(self) -> bool:
        """Ejecutar análisis completo."""
        
        logger.info("🚀 Starting ArcheoScope Scientific Dataset Analysis")
        
        # Cargar datos
        if not self.load_data():
            logger.error("❌ Failed to load data")
            return False
        
        if self.measurements_df is None or len(self.measurements_df) == 0:
            logger.error("❌ No measurement data available")
            return False
        
        # Análisis paso a paso
        normalized_data = self.normalize_by_terrain()
        outliers = self.detect_outliers(normalized_data)
        correlations = self.calculate_correlations(normalized_data)
        ranking = self.generate_archaeological_ranking(normalized_data)
        terrain_summary = self.generate_terrain_summary(normalized_data)
        
        # Guardar resultados
        results_dir = self.save_analysis_results(
            normalized_data, outliers, correlations, ranking, terrain_summary
        )
        
        # Mostrar reporte
        self.print_summary_report(ranking, terrain_summary, outliers, correlations)
        
        if results_dir:
            print(f"\n📁 Detailed results saved to: {results_dir}")
            return True
        else:
            return False

def main():
    """Función principal."""
    
    if not ANALYSIS_AVAILABLE:
        print("❌ Analysis libraries not available")
        print("Install with: pip install pandas numpy scipy")
        return False
    
    try:
        analyzer = ScientificDatasetAnalyzer()
        success = analyzer.run_complete_analysis()
        
        if success:
            print("\n🎉 SCIENTIFIC ANALYSIS COMPLETED SUCCESSFULLY!")
            print("ArcheoScope dataset has been scientifically analyzed!")
            print("\nNext steps:")
            print("1. Review archaeological ranking")
            print("2. Investigate top candidates")
            print("3. Refine algorithms based on patterns")
            print("4. Prepare scientific publication")
        else:
            print("\n⚠️ Analysis completed with issues")
            print("Check logs for details")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)