# 🎯 QUICK START - Sistema Completo

## ✅ Lo que se implementó

1. **GPR Integration** - Validador secundario (13% peso)
2. **Void Detection** - Detector científico de cavidades
3. **Contextual Validation** 🆕 - Sitios conocidos como anclas (SIN mediciones)

## 🚀 Setup Rápido (En Casa)

```bash
# 1. Migración de BD
python apply_void_detection_migration.py

# 2. Crear tabla de sitios conocidos
psql -d archeoscope -f create_known_sites_table.sql

# 3. Test
python test_void_detection_with_db.py --lat 30.0 --lon 31.0
```

## 📊 Output Esperado

```
PASO 1: Clasificación de Ambiente
  ✅ desert (95% confianza)

PASO 2: Datos Satelitales
  ✅ Encontrados en BD

PASO 3: Detección de Vacío
  ✅ Tierra estable
  Score: 0.685 (PROBABLE_CAVITY)

PASO 3.5: Validación Contextual 🆕
  ✅ 25 sitios conocidos cargados
  Ambiente visto: ✓
  Penalización: -10%
  Score ajustado: 0.617

PASO 4: Guardado en BD
  ✅ ID: 123
```

## 🎯 Filosofía Clave

### Validación Contextual (NUEVO)

**Sitios conocidos = Anclas epistemológicas, NO sensores**

✅ Solo metadata (nombre, tipo, ambiente, coords)  
✅ NO requiere mediciones satelitales  
✅ Filtra plausibilidad ambiental  
✅ Detecta falsos positivos  
✅ Mantiene al sistema honesto  

### Ejemplo:

```
Candidata cerca de Petra:
- Void Score: 0.82 (STRONG_VOID)
- Sitios cercanos sin cavidades: 3
- Riesgo de FP: 60%
- Penalización: -30%
- Score ajustado: 0.52 (AMBIGUOUS)
```

## 📚 Documentación

- `README_SISTEMA_COMPLETO.md` - Setup completo
- `CONTEXTUAL_VALIDATION_GUIDE.md` - Validación contextual
- `SUBSURFACE_VOID_DETECTION.md` - Detección de vacíos
- `GPR_INTEGRATION_GUIDE.md` - Integración GPR

## ✅ Checklist

- [x] Código implementado
- [x] Migración de BD preparada
- [x] Tests preparados
- [x] Documentación completa
- [ ] **Ejecutar en casa con BD real** ← SIGUIENTE PASO

---

**Listo para testing. NO rompe nada existente.**
