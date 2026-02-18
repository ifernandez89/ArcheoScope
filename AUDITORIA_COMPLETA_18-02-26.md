📋 AUDITORÍA DEL SISTEMA ARCHEOSCOPE
1. ARQUITECTURA GENERAL
El proyecto ArcheoScope es un ecosistema polimicroservicio con 3 componentes principales:
┌─────────────────────────────────────────────────────────────────┐
│                     ARCHEOSCOPE ECOSYSTEM                       │
├─────────────────┬─────────────────────┬─────────────────────────┤
│  viewer3d       │  backend (API)      │  creador3d (API)        │
│  Puerto: 3000   │  Puerto: 8003       │  Puerto: 8004           │
│  Frontend       │  Backend CIENTÍFICO │  API Experimental 3D   │
└─────────────────┴─────────────────────┴─────────────────────────┘
---
2. STACKS TECNOLÓGICOS
📦 FRONTEND (viewer3d)
| Componente | Tecnología |
|------------|------------|
| Framework | Next.js 14 (App Router) |
| UI Library | React |
| 3D Engine | React Three Fiber + Three.js |
| State Management | Zustand |
| Language | TypeScript |
| Build Output | Static Export (SSG) |
| Deployment | GitHub Pages (/ArcheoScope basePath) |
🐍 BACKEND (Main API - Puerto 8003)
| Componente | Tecnología |
|------------|------------|
| Framework | FastAPI (Python) |
| ORM | Prisma |
| Database | PostgreSQL |
| IA/ML | OpenRouter (LLM), Ollama (local) |
| Satélite | Múltiples conectores (MODIS, SRTM, Copernicus, etc.) |
| Validación | Custom archaeological rules engine |
🐍 CREADOR3D API (Puerto 8004)
| Componente | Tecnología |
|------------|------------|
| Framework | FastAPI (Python) |
| 3D Generation | Trimesh + Matplotlib |
| ML | CulturallyConstrainedMIG (custom) |
| Output | PNG, OBJ |
---
3. ENDPOINTS
🔵 BACKEND PRINCIPAL (Puerto 8003) - backend/api/main.py
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | / | Información del sistema |
| GET | /status | Estado operacional básico |
| GET | /status/detailed | Estado detallado con instrumentos |
| GET | /anomaly-map/{filename} | Mapas de anomalías |
| GET | /data-sources | Fuentes de datos |
| GET | /lidar-benchmark | Datos LIDAR de referencia |
| GET | /instruments/archaeological-value | Matriz de valor arqueológico |
| GET | /archaeological-sites/candidates | Candidatos detectados |
| GET | /volumetric/sites/catalog | Catálogo volumétrico |
| POST | /test-analyze | Prueba de análisis |
| POST | /scientific/analyze | Análisis científico completo (7 fases) |
🟢 CREADOR3D API (Puerto 8004)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | / | Información API |
| GET | /status | Estado operacional |
| GET | /morphologies | Listar clases morfológicas |
| POST | /generate/description | Gen. desde texto (NO IMPLEMENTADO) |
| POST | /generate/parameters | Gen. desde parámetros geométricos |
| POST | /generate/morphology | Gen. desde clase morfológica |
| POST | /generate/custom | Gen. desde geometría custom |
| GET | /model/{filename} | Descargar modelo |
🟣 VIEWER3D (Puerto 3000)
| Ruta | Descripción |
|------|-------------|
| / | Homepage con visualizador 3D |
| /realistic-solar | Sistema solar realista |
---
4. ARQUITECTURA DETALLADA
📁 Estructura de Proyectos
ArcheoScope/
├── viewer3d/                    # Frontend Next.js
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx            # Homepage 3D
│   │   ├── layout.tsx          # Layout root
│   │   └── realistic-solar/    # Página sistema solar
│   ├── components/             # ~60+ componentes React
│   │   ├── Scene3D.tsx        # Escena principal
│   │   ├── ModelViewer.tsx     # Visor de modelos
│   │   ├── SolarSystem*.tsx    # Sistema solar
│   │   ├── TerrainSystem.tsx  # Terreno procedural
│   │   └── ...más
│   ├── engines/                # Motores especializados
│   │   ├── WorldEngine.ts      # Motor de mundo
│   │   ├── SolarEngine.ts      # Motor solar
│   │   ├── GeoEngine.ts        # Motor geoespacial
│   │   └── ...más
│   ├── ai/                     # Integraciones IA
│   │   ├── llm-integration.ts
│   │   ├── openrouter-integration.ts
│   │   ├── ollama-integration.ts
│   │   ├── voice-system.ts
│   │   └── avatar-*.ts
│   ├── store/                  # Zustand stores
│   │   └── scene-store.ts
│   ├── shaders/                # GLSL shaders
│   ├── astro/                  # Cálculos astronómicos
│   └── public/                 # Modelos .glb estáticos
│
├── backend/                    # Backend científico
│   ├── api/
│   │   ├── main.py             # API principal
│   │   ├── routers/            # Routers modulares
│   │   │   ├── analysis.py
│   │   │   ├── catalog.py
│   │   │   └── status.py
│   │   └── models.py           # Modelos Pydantic
│   ├── satellite_connectors/  # ~20+ conectores satelitales
│   │   ├── modis_connector.py
│   │   ├── copernicus_*.py
│   │   └── ...más
│   ├── rules/
│   │   ├── archaeological_rules.py
│   │   └── advanced_archaeological_rules.py
│   ├── validation/
│   │   ├── known_sites_validator.py
│   │   ├── real_archaeological_validator.py
│   │   └── data_source_transparency.py
│   ├── volumetric/
│   │   ├── geometric_inference_engine.py
│   │   └── lidar_fusion_engine.py
│   └── [otros módulos]
│
├── creador3d/                  # API generación 3D
│   ├── api_creador3d.py        # FastAPI
│   └── models/                 # Modelos generados
│
├── prisma/                     # Schema de base de datos
│   └── schema.prisma
│
└── scripts/
    └── migrate_json_to_postgres.py
---
5. DISEÑO Y UX
✅ FORTALEZAS EN DISEÑO
1. Visualizador 3D Avanzado
   - Iluminación dinámica (ambient, directional, point, spot)
   - Sombras de contacto y reflejos HDR
   - Post-processing (Bloom, SSAO)
   - Controles orbitales y cinematográficos
2. Sistema Solar Realista
   - Simulación astronómica con shader procedural del sol
   - Órbitas planetarias realísticas
   - Biome detector y terreno procedimental
   - Sistema de narrativa zoom
3. UI/UX
   - Interfaz responsiva
   - Loading states con spinners
   - Paneles de ayuda y controles
   - Temas claros/oscuros
⚠️ ÁREAS DE MEJORA
1. Documentación de API - Swagger/OpenAPI no configurado explícitamente
2. Testing - No se encontró suite de tests
3. TypeScript - Algunas áreas mezclan JS/TS
4. Componentes Duplicados - Múltiples implementaciones similares (Scene3D, ImmersiveScene, AstronomicalWorld)
---
6. SEGURIDAD Y CONFIGURACIÓN
| Aspecto | Estado |
|---------|--------|
| Variables de entorno | ✅ .env.local configurado |
| CORS | ⚠️ allow_origins=["*"] (permisivo) |
| Rate limiting | ❌ No implementado |
| Autenticación | ❌ No implementado |
| Validación input | ✅ Pydantic models |
| Serialización numpy | ✅ convert_numpy_types() |
---
7. PROBLEMAS Y DEBT TÉCNICO
1. Archivos deshabilitados: systems.disabled/, experience.disabled/, *.disabled - código no activo
2. Backups múltiples: main_backup_*.py, main_refactored.py, main_clean.py
3. Módulos sin usar: Possible código huérfano en backend/
4. Inconsistencia: API principal tiene 2 archivos (main.py, main_clean.py)
5. Falta CI/CD: No se encontró pipeline de deployment
6. Monitoreo: No hay logging estructurado ni métricas
---
8. RESUMEN EJECUTIVO
| Métrica | Valor |
|---------|-------|
| Componentes | 3 microservicios |
| Endpoints API | ~25+ |
| Componentes React | 60+ |
| Conectores satelitales | 20+ |
| Clases morfológicas | 7 |
| Lenguajes | TypeScript, Python |
Stack moderno y funcional con arquitectura limpia. El sistema de detección arqueológica es sofisticado, pero carece de tests, autenticación y documentación de API formal.