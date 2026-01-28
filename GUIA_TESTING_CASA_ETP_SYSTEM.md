# 🏠 GUÍA DE TESTING EN CASA - SISTEMA ETP COMPLETO
## Environmental Tomographic Profile System - Pruebas Integrales

**FECHA**: 28 de enero de 2026  
**OBJETIVO**: Testear el sistema ETP revolucionario con datos reales  
**DURACIÓN ESTIMADA**: 2-3 horas de testing completo  

---

## 🎯 PLAN DE TESTING INTEGRAL

### FASE 1: Preparación del Entorno (15 min)
### FASE 2: Testing con Candidato Existente (45 min)
### FASE 3: Testing de Nuevos Instrumentos (30 min)
### FASE 4: Testing de Contextos Adicionales (45 min)
### FASE 5: Testing de Frontend y Visualización (30 min)
### FASE 6: Validación Final del Sistema (15 min)

---

## 🚀 FASE 1: PREPARACIÓN DEL ENTORNO

### 1.1 Verificar Sistema ETP
```bash
# Verificar que todos los archivos están presentes
python test_etp_simple.py

# Debería mostrar:
# ✅ TODOS LOS ARCHIVOS PRESENTES
# ✅ Sistema ETP: COMPLETAMENTE IMPLEMENTADO
```

### 1.2 Verificar Base de Datos
```bash
# Conectar a la BD y verificar candidatos existentes
python check_db_sites.py

# Buscar un candidato específico para testing
python -c "
import sqlite3
conn = sqlite3.connect('archeoscope.db')
cursor = conn.cursor()
cursor.execute('SELECT id, lat_min, lat_max, lon_min, lon_max, region_name FROM archaeological_sites WHERE status = \"CANDIDATE\" LIMIT 5')
candidates = cursor.fetchall()
print('🎯 CANDIDATOS DISPONIBLES PARA TESTING:')
for i, (id, lat_min, lat_max, lon_min, lon_max, region) in enumerate(candidates, 1):
    print(f'   {i}. ID: {id} | {region} | [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]')
conn.close()
"
```

### 1.3 Preparar Logs de Testing
```bash
# Crear directorio para logs de testing
mkdir -p testing_logs_etp
cd testing_logs_etp

# Crear archivo de log principal
echo "🧪 TESTING ETP SYSTEM - $(date)" > etp_testing_log.txt
echo "=======================================" >> etp_testing_log.txt
```

---

## 🎯 FASE 2: TESTING CON CANDIDATO EXISTENTE

### 2.1 Seleccionar Candidato de Prueba
```bash
# CANDIDATO RECOMENDADO: Usar uno de los 5 candidatos estratégicos
# Ejemplo: Candidato en región mediterránea o andina

# Verificar datos existentes del candidato
python -c "
import sqlite3
candidate_id = 1  # CAMBIAR POR ID REAL
conn = sqlite3.connect('archeoscope.db')
cursor = conn.cursor()

# Obtener datos del candidato
cursor.execute('SELECT * FROM archaeological_sites WHERE id = ?', (candidate_id,))
site = cursor.fetchone()
print(f'📍 CANDIDATO SELECCIONADO: {site}')

# Verificar mediciones existentes
cursor.execute('SELECT COUNT(*) FROM measurements WHERE site_id = ?', (candidate_id,))
measurements_count = cursor.fetchone()[0]
print(f'📊 MEDICIONES EXISTENTES: {measurements_count}')

conn.close()
"
```

---

## 🚀 EJECUCIÓN RÁPIDA - TESTING COMPLETO

### Opción 1: Testing Automático Completo
```bash
# Ejecutar todos los tests automáticamente
python test_sistema_completo_casa.py

# Este script ejecuta:
# 1. Verificación del sistema ETP
# 2. Testing con candidato real de la BD
# 3. Testing de nuevos instrumentos
# 4. Generación de reporte final
```

### Opción 2: Testing Manual Paso a Paso
```bash
# 1. Verificar sistema
python test_etp_simple.py

# 2. Testear candidato real
python test_candidato_etp_casa.py

# 3. Testear nuevos instrumentos
python test_nuevos_instrumentos_casa.py
```

---

## 📊 RESULTADOS ESPERADOS

### ✅ ÉXITO COMPLETO:
- **Tasa de éxito**: >80%
- **Candidato ETP**: Análisis completo generado
- **Nuevos instrumentos**: 8/8 operativos
- **Contextos**: 4/4 sistemas funcionando
- **Visualización**: Datos preparados
- **Reporte**: Generado automáticamente

### 🎯 MÉTRICAS CLAVE A VERIFICAR:
- **ESS Evolucionado**: Superficial → Volumétrico → Temporal
- **GCS**: Geological Compatibility Score
- **Water Score**: Disponibilidad histórica de agua
- **ECS**: External Consistency Score
- **Use Profile**: Territorial Use Profile
- **Comprehensive Score**: Integración multi-dominio

---

## 🔍 TROUBLESHOOTING

### Problema: "ImportError" en módulos ETP
**Solución**:
```bash
# Verificar estructura de archivos
python test_etp_simple.py

# Si faltan archivos, verificar que el commit se aplicó correctamente
git status
git pull origin main
```

### Problema: "No candidates in database"
**Solución**:
```bash
# Verificar BD
python check_db_sites.py

# Si no hay sitios, usar coordenadas por defecto
# El script automáticamente usará coordenadas de prueba
```

### Problema: Instrumentos fallan
**Solución**:
- Los scripts usan simulación automática si las APIs reales fallan
- Esto es normal para testing en casa
- El sistema ETP funcionará con datos simulados

---

## 📁 ARCHIVOS GENERADOS

Después del testing encontrarás en `testing_logs_etp/`:

```
testing_logs_etp/
├── etp_testing_log.txt                    # Log principal
├── candidato_etp_results_YYYYMMDD_HHMMSS.txt  # Resultados candidato
├── nuevos_instrumentos_results_YYYYMMDD_HHMMSS.txt  # Resultados instrumentos
├── REPORTE_SISTEMA_COMPLETO_YYYYMMDD_HHMMSS.txt    # Reporte final
└── etp_visualization.html                 # Visualización (si se genera)
```

---

## 🎉 CRITERIOS DE ÉXITO

### 🟢 SISTEMA COMPLETAMENTE OPERATIVO:
- ✅ Todos los archivos ETP presentes
- ✅ Candidato analizado exitosamente
- ✅ Nuevos instrumentos respondiendo
- ✅ Métricas integradas calculadas
- ✅ Narrativa territorial generada
- ✅ Recomendación arqueológica emitida

### 🟡 SISTEMA FUNCIONAL:
- ✅ Archivos principales presentes
- ✅ Análisis básico funcionando
- ⚠️ Algunos instrumentos con problemas
- ✅ Métricas principales calculadas

### 🔴 SISTEMA NECESITA AJUSTES:
- ❌ Archivos faltantes
- ❌ Errores en análisis principal
- ❌ Múltiples instrumentos fallan

---

## 📋 CHECKLIST FINAL

### Antes de Testing:
- [ ] Repositorio actualizado (`git pull`)
- [ ] Base de datos accesible
- [ ] Python y dependencias instaladas

### Durante Testing:
- [ ] Ejecutar `test_sistema_completo_casa.py`
- [ ] Verificar logs en tiempo real
- [ ] Anotar cualquier error específico

### Después de Testing:
- [ ] Revisar reporte final generado
- [ ] Verificar métricas ETP calculadas
- [ ] Confirmar transformación DETECTOR → EXPLICADOR
- [ ] Documentar cualquier problema encontrado

---

## 🎯 MENSAJE FINAL

**¡SISTEMA ETP LISTO PARA TESTING EN CASA!**

Esta guía te llevará paso a paso a través de la validación completa del sistema ETP revolucionario. Al final tendrás:

- **Confirmación** de que ArcheoScope evolucionó exitosamente
- **Evidencia** de la transformación conceptual
- **Datos** de todos los componentes funcionando
- **Reporte** completo para documentación

**El sistema ETP representa una revolución en arqueología remota:**
- De detector binario a explicador territorial
- De análisis 2D a tomografía 4D
- De métricas aisladas a validación cruzada
- De respuestas simples a narrativas complejas

**¡Que tengas un excelente testing!** 🔬✨

---

*Guía de Testing ETP System*  
*Environmental Tomographic Profile*  
*ArcheoScope: Detector → Explicador Territorial*  
*Enero 28, 2026*

**INSTRUCCIONES DE EJECUCIÓN:**
1. `cd` al directorio del proyecto
2. Ejecutar: `python test_sistema_completo_casa.py`
3. Esperar resultados (2-5 minutos)
4. Revisar reporte en `testing_logs_etp/`
5. ¡Celebrar el sistema ETP revolucionario! 🎉