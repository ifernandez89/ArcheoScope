/**
 * FileLogger - Sistema de logging que guarda en archivos
 * Los logs se guardan automáticamente y pueden ser leídos después
 */

export class FileLogger {
  private logs: string[] = []
  private sessionId: string
  private startTime: number
  
  constructor() {
    this.sessionId = new Date().toISOString().replace(/[:.]/g, '-')
    this.startTime = Date.now()
    this.log('SESSION_START', `Session ID: ${this.sessionId}`)
  }
  
  /**
   * Agregar log
   */
  log(category: string, message: string, data?: any): void {
    const timestamp = Date.now() - this.startTime
    const logEntry = {
      timestamp,
      time: new Date().toISOString(),
      category,
      message,
      data
    }
    
    const logLine = `[${timestamp}ms] [${category}] ${message}${data ? ' | ' + JSON.stringify(data) : ''}`
    this.logs.push(logLine)
    
    // También log en consola
    console.log(`📝 ${logLine}`)
  }
  
  /**
   * Obtener todos los logs
   */
  getLogs(): string {
    return this.logs.join('\n')
  }
  
  /**
   * Descargar logs como archivo
   */
  downloadLogs(): void {
    const content = this.getLogs()
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `archeoscope-logs-${this.sessionId}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    console.log('📥 Logs descargados:', a.download)
  }
  
  /**
   * Guardar en localStorage
   */
  saveToStorage(): void {
    try {
      localStorage.setItem(`archeoscope-logs-${this.sessionId}`, this.getLogs())
      console.log('💾 Logs guardados en localStorage')
    } catch (e) {
      console.error('❌ Error guardando logs:', e)
    }
  }
  
  /**
   * Limpiar logs
   */
  clear(): void {
    this.logs = []
    console.log('🧹 Logs limpiados')
  }
}

// Singleton global
export const fileLogger = new FileLogger()

// Exponer globalmente
if (typeof window !== 'undefined') {
  (window as any).fileLogger = fileLogger
  
  // Auto-guardar cada 10 segundos
  setInterval(() => {
    fileLogger.saveToStorage()
  }, 10000)
  
  // Guardar al cerrar
  window.addEventListener('beforeunload', () => {
    fileLogger.saveToStorage()
  })
}
