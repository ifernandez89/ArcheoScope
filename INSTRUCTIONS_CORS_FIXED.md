# 🚀 ArcheoScope - Instrucciones de Uso Corregido

## ✅ **PROBLEMAS CONEXIÓN FRONTAL-BACKEND RESUELTOS**

### **🔧 Solución a Errores CORS:**
El problema era que el frontend se abría con `file://` protocolo, que bloquea las peticiones a `http://localhost:8002` por seguridad del navegador.

## **📋 Instrucciones para Iniciar Sistema:**

### **Paso 1: Iniciar Backend**
```bash
python run_archeoscope.py
```
- Backend corre en: `http://localhost:8002`
- Espera mensaje: "ArcheoScope listo"

### **Paso 2: Iniciar Frontend** (NUEVO)
```bash
python start_frontend.py
```
- Frontend corre en: `http://localhost:8080` (o puerto disponible)
- Abre automáticamente en navegador
- Resuelve problemas CORS sirviendo desde localhost

### **Paso 3: Usar Sistema**
1. Frontend: `http://localhost:8080/index.html`
2. Backend API: `http://localhost:8002/docs`
3. Estado sistema: `http://localhost:8002/status`

## **🎯 Verificación Rápida:**
```bash
python quick_test.py
```
Debe mostrar: "Backend funcionando correctamente"

## **🔍 Nueva Funcionalidad Implementada:**

### **Validación Real de Datos:**
- ✅ **10 sitios UNESCO** con URLs públicas verificables
- ✅ **2 sitios control** (moderno + natural)  
- ✅ **5 APIs públicas** documentadas (Sentinel-2, Landsat, MODIS, SRTM)
- ✅ **Transparencia completa** en cada análisis
- ✅ **Validación terreno obligatoria** en resultados

### **Endpoints Nuevos:**
- `GET /known-sites` - Sitios arqueológicos reales
- `GET /data-sources` - Fuentes de datos públicas
- `GET /validate-region` - Validación por coordenadas
- `POST /falsification-protocol` - Control de calidad

## **🎉 Sistema 100% Funcional y Científico:**
- **Regla Crítica NRO 1**: Completamente implementada
- **Contraste con datos reales**: Automático en cada análisis
- **APIs públicas**: Siempre documentadas y verificables
- **Validación terreno**: Requisito explícito e imprescindible

**ArcheoScope está listo para investigación arqueológica científica rigurosa.**