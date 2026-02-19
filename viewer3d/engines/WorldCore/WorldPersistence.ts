/**
 * WorldPersistence - Sistema de persistencia de estado
 * Responsable de: Save/Load, serialización, localStorage/IndexedDB
 */

export interface SaveData {
  version: string
  timestamp: number
  worldState: any
  playerState: any
  customData?: Record<string, any>
}

export class WorldPersistence {
  private static instance: WorldPersistence
  
  private storageKey: string = 'archeoscope_world_save'
  private version: string = '1.0.0'
  private autoSaveInterval: number = 60000 // 1 minuto
  private autoSaveTimer?: NodeJS.Timeout
  
  private constructor() {
    console.log('💾 WorldPersistence: Inicializado')
  }
  
  static getInstance(): WorldPersistence {
    if (!WorldPersistence.instance) {
      WorldPersistence.instance = new WorldPersistence()
    }
    return WorldPersistence.instance
  }
  
  /**
   * Guardar estado
   */
  async save(data: Partial<SaveData>): Promise<boolean> {
    try {
      const saveData: SaveData = {
        version: this.version,
        timestamp: Date.now(),
        worldState: data.worldState || {},
        playerState: data.playerState || {},
        customData: data.customData || {}
      }
      
      const serialized = JSON.stringify(saveData)
      
      // Guardar en localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem(this.storageKey, serialized)
        console.log('💾 WorldPersistence: Guardado exitoso')
        return true
      }
      
      return false
    } catch (error) {
      console.error('❌ WorldPersistence: Error al guardar', error)
      return false
    }
  }
  
  /**
   * Cargar estado
   */
  async load(): Promise<SaveData | null> {
    try {
      if (typeof window === 'undefined') {
        return null
      }
      
      const serialized = localStorage.getItem(this.storageKey)
      
      if (!serialized) {
        console.log('ℹ️ WorldPersistence: No hay datos guardados')
        return null
      }
      
      const data = JSON.parse(serialized) as SaveData
      
      // Verificar versión
      if (data.version !== this.version) {
        console.warn('⚠️ WorldPersistence: Versión incompatible', data.version)
        // Aquí podrías implementar migración de datos
      }
      
      console.log('📂 WorldPersistence: Cargado exitoso')
      return data
    } catch (error) {
      console.error('❌ WorldPersistence: Error al cargar', error)
      return null
    }
  }
  
  /**
   * Verificar si existe save
   */
  hasSave(): boolean {
    if (typeof window === 'undefined') return false
    return localStorage.getItem(this.storageKey) !== null
  }
  
  /**
   * Eliminar save
   */
  deleteSave(): boolean {
    try {
      if (typeof window === 'undefined') return false
      
      localStorage.removeItem(this.storageKey)
      console.log('🗑️ WorldPersistence: Save eliminado')
      return true
    } catch (error) {
      console.error('❌ WorldPersistence: Error al eliminar', error)
      return false
    }
  }
  
  /**
   * Habilitar auto-save
   */
  enableAutoSave(callback: () => Partial<SaveData>): void {
    this.disableAutoSave()
    
    this.autoSaveTimer = setInterval(() => {
      const data = callback()
      this.save(data)
      console.log('💾 WorldPersistence: Auto-save ejecutado')
    }, this.autoSaveInterval)
    
    console.log('⏰ WorldPersistence: Auto-save habilitado')
  }
  
  /**
   * Deshabilitar auto-save
   */
  disableAutoSave(): void {
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer)
      this.autoSaveTimer = undefined
      console.log('⏸️ WorldPersistence: Auto-save deshabilitado')
    }
  }
  
  /**
   * Configurar intervalo de auto-save
   */
  setAutoSaveInterval(milliseconds: number): void {
    this.autoSaveInterval = Math.max(10000, milliseconds) // Mínimo 10s
    console.log(`⏱️ WorldPersistence: Intervalo = ${this.autoSaveInterval}ms`)
  }
  
  /**
   * Exportar save como JSON
   */
  async exportSave(): Promise<string | null> {
    const data = await this.load()
    if (!data) return null
    
    return JSON.stringify(data, null, 2)
  }
  
  /**
   * Importar save desde JSON
   */
  async importSave(json: string): Promise<boolean> {
    try {
      const data = JSON.parse(json) as SaveData
      return await this.save(data)
    } catch (error) {
      console.error('❌ WorldPersistence: Error al importar', error)
      return false
    }
  }
  
  /**
   * Obtener info del save
   */
  async getSaveInfo(): Promise<{ exists: boolean; timestamp?: number; version?: string } | null> {
    const data = await this.load()
    
    if (!data) {
      return { exists: false }
    }
    
    return {
      exists: true,
      timestamp: data.timestamp,
      version: data.version
    }
  }
}

export default WorldPersistence.getInstance()
