# 🚨 FIXES CRÍTICOS PENDIENTES

**Fecha**: 2026-01-23
**Reportado por**: Usuario
**Prioridad**: 🔴 CRÍTICA

---

## 🐛 PROBLEMAS REPORTADOS

### 1. **Lupa muestra números aleatorios de candidatos**
- **Síntoma**: "11 candidatos" cambia a "5 candidatos", "9 candidatos", etc.
- **Ubicación**: Popup en el mapa después del análisis
- **Estado**: 🔍 INVESTIGANDO
- **Nota**: Backend es 100% determinístico, problema está en frontend

### 2. **Los 4 inputs están pre-rellenados**
- **Síntoma**: Inputs latMin, latMax, lonMin, lonMax tienen valores por defecto
- **Problema**: Pueden interferir con el análisis
- **Solución**: Limpiarlos al inicio de cada análisis
- **Estado**: ⏳ PENDIENTE

### 3. **Panel de resultados muestra campos vacíos**
- **Síntoma**: Secciones como "Método Recomendado", "Sistema de Inferencia Volumétrica" muestran "--" o "Esperando análisis..."
- **Problema**: Ruido visual sin información útil
- **Solución**: Ocultar secciones que no tienen datos
- **Estado**: ⏳ PENDIENTE

### 4. **Calibración aparece fuera del cuadro**
- **Síntoma**: El rectángulo de calibración no coincide con las coordenadas ingresadas
- **Problema**: Puede estar usando los 4 inputs pre-rellenados en lugar del input único
- **Solución**: Asegurar que use las coordenadas correctas
- **Estado**: ⏳ PENDIENTE

---

## 🔍 INVESTIGACIÓN

### Backend - ✅ DETERMINÍSTICO
```
Jamaica (18.5, -77.5):
   Run 1: 1 candidato
   Run 2: 1 candidato
   Run 3: 1 candidato
   Run 4: 1 candidato
   Run 5: 1 candidato
   ✅ SIEMPRE 1 candidato con dimensiones idénticas
```

### Frontend - ❌ PROBLEMA ENCONTRADO
- El código en `index.html` línea 2805 usa `wreckCandidates` del backend correctamente
- El popup que muestra números aleatorios NO está en el código que estoy viendo
- **Posibilidad 1**: Usuario está usando un archivo HTML diferente
- **Posibilidad 2**: Hay código JavaScript inline que no estoy viendo
- **Posibilidad 3**: Hay caché del navegador (aunque usuario usa Ctrl+F5)

---

## 📋 ACCIONES REQUERIDAS

### 1. Identificar archivo HTML correcto
- Usuario reporta usar puerto 8080
- Necesito confirmar qué archivo HTML está sirviendo ese puerto

### 2. Limpiar inputs al inicio
```javascript
// Al inicio de investigateRegion()
document.getElementById('latMin').value = '';
document.getElementById('latMax').value = '';
document.getElementById('lonMin').value = '';
document.getElementById('lonMax').value = '';
```

### 3. Ocultar secciones vacías
```javascript
// Después de displayResults()
hideEmptySections();

function hideEmptySections() {
    const sections = [
        'volumetricInferenceSection',
        'volumetricModelSection',
        'syntheticInterpretationSection'
    ];
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const hasData = checkIfSectionHasData(section);
            section.style.display = hasData ? 'block' : 'none';
        }
    });
}
```

### 4. Fix calibración
```javascript
// En executeCalibrationProtocol()
// Asegurar que use selectedCoordinates o el input único
const coords = parseCoordinatesFromInput(); // Parsear "25.511, -70.361"
```

---

## 🎯 PRÓXIMOS PASOS

1. **URGENTE**: Usuario debe confirmar qué archivo HTML está usando
2. **URGENTE**: Usuario debe copiar logs de consola del navegador (F12)
3. Implementar limpieza de inputs
4. Implementar ocultación de secciones vacías
5. Fix calibración para usar coordenadas correctas

---

## 📝 NOTAS

- Backend es 100% determinístico - verificado con tests
- Problema está definitivamente en el frontend
- Necesito más información del usuario para localizar el código exacto que genera los números aleatorios

---

**ESTADO**: 🔴 BLOQUEADO - Esperando información del usuario
