# Deep Analysis - Quick Start Guide

## 🚀 Inicio Rápido (3 pasos)

### 1. Test de Conexiones (5 min)
```bash
python test_deep_analysis_connections.py
```

### 2. Análisis Completo (40-60 min)
```bash
python run_deep_analysis_complete.py
```

### 3. Ver Resultados
```bash
# Archivo generado:
deep_analysis_complete_puerto_rico_north_YYYYMMDD_HHMMSS.json
```

---

## 📋 Comandos Rápidos

### Análisis Individual

```bash
# Phase A: Temporal (5-10 min)
python deep_temporal_analysis.py

# Phase B: SAR (10-15 min)
python deep_sar_analysis.py

# Phases C & D: Multi-Scale (25-35 min)
python deep_multiscale_analysis.py
```

---

## 🎯 Zonas Disponibles

1. **Puerto Rico North** (Prioridad 🥇)
   - TAS: 1.000 | SAR: 0.997 | Thermal: 0.955

2. **Bermuda Node A** (Prioridad 🥈)
   - TAS: 1.000 | 3D: 0.943

3. **Puerto Rico Trench** (Prioridad 🥉)
   - TAS: 1.000 | 29 escenas SAR

---

## 📊 Scores Clave

| Score | Rango Crítico | Significado |
|-------|---------------|-------------|
| Thermal Inertia | > 0.7 | Masa térmica |
| SAR Behavior | > 0.8 | Estructura rígida |
| Scale Invariance | > 0.7 | **ANÓMALO** |

---

## 🔑 Principio Fundamental

```
Natural → Pierde coherencia al bajar escala
Artificial → NO pierde coherencia
```

---

## ⏱️ Tiempos

- Phase A: 5-10 min
- Phase B: 10-15 min
- Phase C: 5 min
- Phase D: 20-30 min
- **Total: 40-60 min**

---

## 📄 Output

```json
{
  "zone": "Puerto Rico North",
  "duration_minutes": 45.4,
  "phases": {
    "phase_a_temporal": {
      "thermal_inertia_score": 0.85
    },
    "phase_b_sar": {
      "behavior_score": 0.92
    },
    "phase_c_icesat2": {
      "rigidity_score": 0.80
    },
    "phase_d_multiscale": {
      "invariance_score": 0.82
    }
  }
}
```

---

## 🚨 Interpretación Rápida

### Máxima Prioridad
```
Thermal > 0.7
+ SAR > 0.8
+ Scale Invariance > 0.7
= ESTRUCTURA INTEGRADA
```

### Alta Prioridad
```
SAR Rigidity > 0.9
+ Stratification > 2 layers
= ESTRUCTURA ESTRATIFICADA
```

---

## ⚠️ Notas Importantes

1. **ICESat-2**: Es normal no tener cobertura
2. **Phase D**: Toma 20-30 minutos (opcional)
3. **SAR**: Descarga puede ser lenta (2-5 min)

---

## 📚 Documentación Completa

- `DEEP_ANALYSIS_README.md` - Guía completa
- `DEEP_ANALYSIS_ARCHITECTURE.md` - Diagramas
- `RESUMEN_IMPLEMENTACION_DEEP_ANALYSIS.md` - Resumen técnico

---

## ✅ Checklist Pre-Ejecución

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r backend/requirements.txt`)
- [ ] Test de conexiones ejecutado
- [ ] Zona seleccionada
- [ ] Tiempo disponible (40-60 min)

---

**¿Listo?** → `python run_deep_analysis_complete.py`
