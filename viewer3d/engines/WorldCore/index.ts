/**
 * WorldCore - Núcleo del motor de mundo
 * Sistema modular para gestión de mundo 3D
 * 
 * Arquitectura:
 * ├── WorldState          - Estado global del mundo
 * ├── WorldTime           - Sistema temporal
 * ├── SpatialIndex        - Índice espacial O(1)
 * ├── EntitySystem        - Gestión de entidades (ECS ligero)
 * ├── ProceduralGenerator - Generación procedural
 * ├── LOD                 - Level of Detail
 * ├── Streaming           - Carga/descarga de chunks
 * └── Persistence         - Save/Load
 */

export { WorldState, type WorldConfig, type WorldMetrics } from './WorldState'
export { WorldTime, type TimeState } from './WorldTime'
export { WorldSpatialIndex, type SpatialObject, type QueryResult } from './WorldSpatialIndex'
export { EntitySystem, type Entity } from './EntitySystem'
export { ProceduralGenerator, type GeneratorConfig } from './ProceduralGenerator'
export { WorldLOD, type LODLevel, type LODObject } from './WorldLOD'
export { WorldStreaming, type Chunk, type StreamingStats } from './WorldStreaming'
export { WorldPersistence, type SaveData } from './WorldPersistence'

// Singletons por defecto
import WorldStateInstance from './WorldState'
import WorldTimeInstance from './WorldTime'
import WorldSpatialIndexInstance from './WorldSpatialIndex'
import { EntitySystem } from './EntitySystem'
import { ProceduralGenerator } from './ProceduralGenerator'
import WorldLODInstance from './WorldLOD'
import WorldStreamingInstance from './WorldStreaming'
import WorldPersistenceInstance from './WorldPersistence'

// Instancias singleton
const EntitySystemInstance = new EntitySystem()
const ProceduralGeneratorInstance = new ProceduralGenerator(42)

export const WorldCore = {
  State: WorldStateInstance,
  Time: WorldTimeInstance,
  SpatialIndex: WorldSpatialIndexInstance,
  Entities: EntitySystemInstance,
  Procedural: ProceduralGeneratorInstance,
  LOD: WorldLODInstance,
  Streaming: WorldStreamingInstance,
  Persistence: WorldPersistenceInstance
}

export default WorldCore
