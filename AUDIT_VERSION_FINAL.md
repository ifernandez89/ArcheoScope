# 🏛️ AUDITORÍA DE SISTEMA: ArcheoScope v2.0 (Versión Estándar de Oro)
## "De la Detección de Objetos a la Inferencia de Territorios"

---

## 1. ARQUITECTURA DEL SISTEMA (Applied Architecture)
ArcheoScope se basa en una arquitectura de **Microservicios Híbridos** diseñada para el procesamiento masivo de datos geoespaciales y el razonamiento jerárquico.

### **Componentes Core:**
*   **Backend:** FastAPI (Python 3.10+) con ejecución asíncrona para pipelines concurrentes.
*   **Frontend:** Interfaz de Alta Fidelidad (Glassmorphism) basada en Vanilla JS.
*   **Base de Datos:** PostgreSQL con pool de conexiones `asyncpg`.
*   **Motor de IA (HRM):** ACT-V1 (Hierarchical Reasoning Model).

---

## 2. SEGURIDAD Y GESTIÓN DE CREDENCIALES (CRÍTICO)
El sistema implementa un protocolo de seguridad militar para el acceso a APIs de terceros:
*   **Encriptación en Reposo:** Todas las credenciales de acceso (Planetary Computer, Earthdata, OpenTopography, etc.) están **encriptadas en la Base de Datos**.
*   **Capa de Desencriptación Transparente:** El `CredentialsManager` recupera y desencripta las llaves en tiempo de ejecución solo cuando el motor TIMT las requiere.
*   **Prevención de Fugas:** Ninguna credencial se expone en logs ni se guarda en texto plano en archivos de configuración.

---

## 3. METODOLOGÍA CIENTÍFICA (TIMT v3)
El sistema ha migrado del modelo de "detección simple" a la **Tomografía Territorial Inferencial Multi-dominio (TIMT)**:

| Capa | Nombre | Función |
| :--- | :--- | :--- |
| **Capa 0** | **TCP (Territorial Context)** | Análisis pre-medición: Geología, Hidrología y Trazas Humanas. |
| **Capa 1** | **Adquisición Dirigida** | Selección de instrumentos basada en el potencial de preservación. |
| **Capa 2** | **ETP (Tomographic Profile)** | Reconstrucción volumétrica (XZ/YZ) y ESS (Explanatory Strangeness Score). |
| **Capa 3** | **Honestidad Académica** | Reporte de transparencia y límites del sistema. |

---

## 4. MATRIZ DE INSTRUMENTOS (Los 15 Sensores)
ArcheoScope integra 15 flujos de datos distribuidos por capacidad de penetración:
*   **Superficie:** Sentinel-2, VIIRS NDVI/Thermal, SRTM, Landsat NDVI.
*   **Subsuperficie:** Sentinel-1 SAR, Landsat Thermal, MODIS LST, PALSAR Backscatter.
*   **Profundidad:** ICESat-2, PALSAR Penetration, Geometric Inference Engine.

---

## 5. INNOVACIONES TÉCNICAS RECIENTES
*   **Neural Activations (HRM):** Visualización del proceso de razonamiento IA mediante heatmaps de activación `z_H`.
*   **Resiliencia Dataclass:** Soporte nativo para iteración y subscriptibilidad en objetos `Carry` (ACT-V1).
*   **Robustez de Reportes:** Generación automática de métricas cuantitativas de transparencia (hipótesis validadas vs rechazadas).

### **VEREDICTO: VERSIÓN ESTABLE Y LISTA PARA DESPLIEGUE OPERACIONAL CON SEGURIDAD REFORZADA.**
