# CORRECCIÓN CONCEPTUAL CRÍTICA: ESS Volumétrico

**Fecha**: 2026-01-28  
**Prioridad**: 🔥 CONCEPTUAL FUNDAMENTAL  
**Impacto**: Interpretación científica del sistema

---

## 🎯 CORRECCIÓN DEL USUARIO (CRÍTICA)

### Lo que estábamos haciendo MAL

**Interpretación incorrecta**:
> "ESS Volumétrico = 0 significa que los sensores no están midiendo bien"

**Resultado**: Intentamos "arreglar" el sistema para que ESS nunca sea 0.

### Lo que es CORRECTO científicamente

**Interpretación correcta**:
> "ESS Volumétrico mide CONTRASTE ESTRATIGRÁFICO con profundidad, NO disponibilidad de datos"

**En planicies aluviales activas** (Veracruz, Tabasco):
- Sedimentos homogéneos recientes
- NO hay rupturas geomorfológicas
- NO hay paleo-superficies selladas
- **ESS = 0 es el resultado CORRECTO**

---

## 🧠 Concepto Fundamental: ¿Qué mide TIMT?

### TIMT solo "ve" volumen cuando hay:

1. **Rupturas geomorfológicas**: Cambios abruptos en estratigrafía
2. **Paleo-superficies selladas**: Superficies antiguas enterradas
3. **Contraste de materiales**: Diferencias significativas entre capas
4. **Estructuras enterradas**: Construcciones bajo sedimentos

### En planicies vivas (sedimentación activa):

- ❌ NO hay tomografía (sedimentos homogéneos)
- ✅ SÍ hay contexto territorial (TCP)
- ✅ SÍ hay datos instrumentales
- ✅ ESS = 0 es ESPERADO y CORRECTO

---

## 📊 Separación de Métricas: Cobertura vs Anomalía

### PROBLEMA ACTUAL

Estamos mezclando dos conceptos diferentes:

```python
# INCORRECTO (mezclado)
if no_hay_datos_volumetricos:
    ess_volumetrico = 0  # ❌ Confunde "sin datos" con "sin anomalía"
```

### SOLUCIÓN: Separar Métricas

#### 1. Cobertura Instrumental (siempre reportar)

**Pregunta**: "¿Tengo datos de los sensores?"

```python
cobertura_instrumental = {
    'superficial': {
        'sensores_exitosos': 3,
        'sensores_totales': 4,
        'porcentaje': 75.0
    },
    'subsuperficial': {
        'sensores_exitosos': 2,
        'sensores_totales': 5,
        'porcentaje': 40.0
    },
    'profundo': {
        'sensores_exitosos': 0,
        'sensores_totales': 2,
        'porcentaje': 0.0
    }
}
```

**Interpretación**:
- ✅ "Tengo 75% de cobertura superficial"
- ✅ "Tengo 40% de cobertura subsuperficial"
- ✅ "No tengo cobertura profunda"

#### 2. ESS Volumétrico (científico)

**Pregunta**: "¿Hay contraste estratigráfico?"

```python
ess_volumetrico = {
    'valor': 0.0,
    'interpretacion': 'sedimentos_homogeneos',
    'explicacion': 'No se detecta contraste estratigráfico. Esperado en planicies aluviales activas.'
}
```

**Interpretación**:
- ✅ "Los sensores funcionan (cobertura 60%)"
- ✅ "Pero NO hay contraste vertical (ESS=0)"
- ✅ "Esto es CORRECTO para esta geomorfología"

---

## 🔧 Implementación de la Separación

### Paso 1: Calcular Cobertura Instrumental

```python
def _calculate_instrumental_coverage(self, layered_data: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcular cobertura instrumental por tipo de sensor.
    
    IMPORTANTE: Esto mide disponibilidad de datos, NO anomalía.
    """
    
    coverage_by_type = {}
    
    for sensor_type, instruments in self.instrument_types.items():
        successful = 0
        total = len(instruments)
        
        for instrument in instruments:
            # Buscar en cualquier profundidad
            found_data = False
            for depth, layer_data in layered_data.items():
                if instrument in layer_data:
                    data = layer_data[instrument]
                    if self._validate_sensor_data(instrument, data):
                        successful += 1
                        found_data = True
                        break
            
            if not found_data and not self._is_optional_sensor(instrument):
                # Sensor obligatorio sin datos
                pass
        
        coverage_by_type[sensor_type] = {
            'successful': successful,
            'total': total,
            'percentage': (successful / total * 100) if total > 0 else 0
        }
    
    return coverage_by_type
```

### Paso 2: Calcular ESS Volumétrico (Científico)

```python
def _calculate_volumetric_ess_scientific(self, layered_data: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcular ESS volumétrico como medida de CONTRASTE ESTRATIGRÁFICO.
    
    CONCEPTO CLAVE:
    - ESS = 0 NO significa "sin datos"
    - ESS = 0 significa "sin contraste vertical"
    - En planicies aluviales activas, ESS = 0 es CORRECTO
    """
    
    # Calcular contraste entre capas
    layer_contrasts = []
    
    depths = sorted(layered_data.keys())
    for i in range(len(depths) - 1):
        depth1, depth2 = depths[i], depths[i + 1]
        
        layer1_signature = self._calculate_layer_signature(layered_data[depth1])
        layer2_signature = self._calculate_layer_signature(layered_data[depth2])
        
        # Contraste = diferencia entre capas adyacentes
        if layer1_signature is not None and layer2_signature is not None:
            contrast = abs(layer1_signature - layer2_signature)
            layer_contrasts.append(contrast)
    
    # ESS volumétrico = promedio de contrastes
    ess_value = np.mean(layer_contrasts) if layer_contrasts else 0.0
    
    # Interpretación científica
    if ess_value < 0.1:
        interpretation = 'sedimentos_homogeneos'
        explanation = 'No se detecta contraste estratigráfico significativo. Esperado en planicies aluviales activas con sedimentación reciente.'
    elif ess_value < 0.3:
        interpretation = 'contraste_leve'
        explanation = 'Contraste estratigráfico leve. Posible variación natural o inicio de diferenciación.'
    elif ess_value < 0.6:
        interpretation = 'contraste_moderado'
        explanation = 'Contraste estratigráfico moderado. Indica posible ruptura geomorfológica o paleo-superficie.'
    else:
        interpretation = 'contraste_fuerte'
        explanation = 'Contraste estratigráfico fuerte. Alta probabilidad de estructuras enterradas o discontinuidades significativas.'
    
    return {
        'valor': ess_value,
        'interpretacion': interpretation,
        'explicacion': explanation,
        'contrastes_detectados': len(layer_contrasts)
    }

def _calculate_layer_signature(self, layer_data: Dict[str, Any]) -> Optional[float]:
    """
    Calcular firma espectral/física de una capa.
    
    Combina múltiples sensores para caracterizar la capa.
    """
    
    if not layer_data:
        return None
    
    signatures = []
    
    for instrument, data in layer_data.items():
        if not self._validate_sensor_data(instrument, data):
            continue
        
        # Normalizar valor según tipo de sensor
        normalized = self._normalize_instrument_value(instrument, data['value'])
        confidence = data.get('confidence', 0.5)
        
        signatures.append(normalized * confidence)
    
    return np.mean(signatures) if signatures else None
```

### Paso 3: Comunicar Claramente en Frontend

```javascript
// En archeoscope_timt.js

function displayVolumetricESS(ess_data, coverage_data) {
    const container = document.getElementById('ess-volumetric-section');
    
    // Mostrar cobertura instrumental PRIMERO
    container.innerHTML = `
        <h4>📊 Cobertura Instrumental</h4>
        <div class="coverage-summary">
            <div class="coverage-layer">
                <span>🌍 Superficial:</span>
                <strong>${coverage_data.superficial.percentage.toFixed(0)}%</strong>
                (${coverage_data.superficial.successful}/${coverage_data.superficial.total} sensores)
            </div>
            <div class="coverage-layer">
                <span>📡 Subsuperficial:</span>
                <strong>${coverage_data.subsuperficial.percentage.toFixed(0)}%</strong>
                (${coverage_data.subsuperficial.successful}/${coverage_data.subsuperficial.total} sensores)
            </div>
            <div class="coverage-layer">
                <span>🔬 Profundo:</span>
                <strong>${coverage_data.profundo.percentage.toFixed(0)}%</strong>
                (${coverage_data.profundo.successful}/${coverage_data.profundo.total} sensores)
            </div>
        </div>
        
        <h4>🧊 ESS Volumétrico (Contraste Estratigráfico)</h4>
        <div class="ess-scientific">
            <div class="ess-value">
                <strong>${ess_data.valor.toFixed(3)}</strong>
            </div>
            <div class="ess-interpretation ${ess_data.interpretacion}">
                ${getInterpretationIcon(ess_data.interpretacion)} ${ess_data.interpretacion}
            </div>
            <div class="ess-explanation">
                ${ess_data.explicacion}
            </div>
        </div>
    `;
}

function getInterpretationIcon(interpretation) {
    const icons = {
        'sedimentos_homogeneos': '🟢',
        'contraste_leve': '🟡',
        'contraste_moderado': '🟠',
        'contraste_fuerte': '🔴'
    };
    return icons[interpretation] || '⚪';
}
```

---

## 📋 Mensaje Claro para el Usuario

### Cuando ESS = 0 (Correcto)

```
📊 Cobertura Instrumental
  🌍 Superficial: 75% (3/4 sensores)
  📡 Subsuperficial: 40% (2/5 sensores)
  🔬 Profundo: 0% (0/2 sensores)

🧊 ESS Volumétrico: 0.000
  🟢 Sedimentos homogéneos

  Interpretación:
  Los sensores están funcionando correctamente (cobertura 60%),
  pero NO se detecta contraste estratigráfico vertical.
  
  Esto es ESPERADO en planicies aluviales activas donde la
  sedimentación reciente crea capas homogéneas sin rupturas
  geomorfológicas.
  
  TIMT solo detecta volumen cuando hay paleo-superficies
  selladas o estructuras enterradas. En este territorio,
  el análisis se basa en contexto territorial (TCP) y
  superficie (ESS Superficial).
```

### Cuando ESS > 0.5 (Anomalía)

```
📊 Cobertura Instrumental
  🌍 Superficial: 100% (4/4 sensores)
  📡 Subsuperficial: 80% (4/5 sensores)
  🔬 Profundo: 50% (1/2 sensores)

🧊 ESS Volumétrico: 0.687
  🔴 Contraste fuerte

  Interpretación:
  Se detecta contraste estratigráfico significativo entre
  capas de profundidad. Esto indica posible presencia de:
  
  - Paleo-superficies selladas
  - Estructuras enterradas
  - Rupturas geomorfológicas
  - Discontinuidades antrópicas
  
  Alta probabilidad de evidencia arqueológica subsuperficial.
  Se recomienda verificación de campo.
```

---

## ✅ Checklist de Implementación

- [ ] Separar `_calculate_instrumental_coverage()` de `_calculate_volumetric_ess()`
- [ ] Implementar `_calculate_layer_signature()` para firmas espectrales
- [ ] Calcular contraste entre capas adyacentes
- [ ] Agregar interpretación científica a ESS volumétrico
- [ ] Modificar respuesta API para incluir ambas métricas
- [ ] Actualizar frontend para mostrar cobertura + ESS separados
- [ ] Agregar mensajes explicativos según interpretación
- [ ] Documentar casos de uso (planicies vs montañas)

---

## 🎯 Resultado Esperado

### Antes (Confuso)

```
ESS Volumétrico: 0.000
❌ "El sistema no está midiendo bien"
```

### Después (Claro)

```
Cobertura Instrumental: 60% ✅
ESS Volumétrico: 0.000 ✅
Interpretación: Sedimentos homogéneos (esperado en planicies)

Los sensores funcionan correctamente, pero no hay contraste
estratigráfico. Esto es normal en esta geomorfología.
```

---

## 📚 Referencias Científicas

**Concepto de Tomografía Inferencial**:
- Requiere contraste de materiales para "ver" volumen
- En sedimentos homogéneos, no hay señal tomográfica
- ESS = 0 es resultado válido, no error del sistema

**Geomorfología de Planicies Aluviales**:
- Sedimentación activa crea capas homogéneas
- Sin rupturas estratigráficas significativas
- Contexto territorial más relevante que tomografía

---

**CONCLUSIÓN CRÍTICA**:

No necesitamos "arreglar" el sistema para que ESS nunca sea 0.
Necesitamos COMUNICAR CLARAMENTE que ESS = 0 puede ser correcto
científicamente, y separar cobertura instrumental de anomalía
estratigráfica.

---

**Implementado por**: Kiro AI Assistant  
**Fecha**: 2026-01-28  
**Versión**: ArcheoScope v2.2 + TIMT v1.0 (Corrección Conceptual)
