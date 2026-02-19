/**
 * Logger - Sistema de logging centralizado
 * Reemplaza console.log con niveles y control de producción
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
  NONE = 4
}

class Logger {
  private level: LogLevel
  private enabled: boolean
  private prefix: string
  
  constructor() {
    // En producción, solo errores
    this.level = process.env.NODE_ENV === 'production' ? LogLevel.ERROR : LogLevel.DEBUG
    this.enabled = true
    this.prefix = '🎮'
  }
  
  /**
   * Configurar nivel de logging
   */
  setLevel(level: LogLevel): void {
    this.level = level
  }
  
  /**
   * Habilitar/deshabilitar logging
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled
  }
  
  /**
   * Configurar prefijo
   */
  setPrefix(prefix: string): void {
    this.prefix = prefix
  }
  
  /**
   * Log de debug (solo desarrollo)
   */
  debug(...args: any[]): void {
    if (!this.enabled || this.level > LogLevel.DEBUG) return
    console.log(`${this.prefix} [DEBUG]`, ...args)
  }
  
  /**
   * Log de información
   */
  info(...args: any[]): void {
    if (!this.enabled || this.level > LogLevel.INFO) return
    console.log(`${this.prefix} [INFO]`, ...args)
  }
  
  /**
   * Log de advertencia
   */
  warn(...args: any[]): void {
    if (!this.enabled || this.level > LogLevel.WARN) return
    console.warn(`${this.prefix} [WARN]`, ...args)
  }
  
  /**
   * Log de error
   */
  error(...args: any[]): void {
    if (!this.enabled || this.level > LogLevel.ERROR) return
    console.error(`${this.prefix} [ERROR]`, ...args)
  }
  
  /**
   * Crear logger con categoría
   */
  category(name: string): CategoryLogger {
    return new CategoryLogger(name, this)
  }
}

/**
 * Logger con categoría (para sistemas específicos)
 */
class CategoryLogger {
  constructor(
    private name: string,
    private parent: Logger
  ) {}
  
  debug(...args: any[]): void {
    this.parent.debug(`[${this.name}]`, ...args)
  }
  
  info(...args: any[]): void {
    this.parent.info(`[${this.name}]`, ...args)
  }
  
  warn(...args: any[]): void {
    this.parent.warn(`[${this.name}]`, ...args)
  }
  
  error(...args: any[]): void {
    this.parent.error(`[${this.name}]`, ...args)
  }
}

// Instancia global
const logger = new Logger()

export default logger

/**
 * Loggers por categoría (pre-configurados)
 */
export const loggers = {
  engine: logger.category('Engine'),
  weather: logger.category('Weather'),
  world: logger.category('World'),
  avatar: logger.category('Avatar'),
  audio: logger.category('Audio'),
  performance: logger.category('Performance'),
  ui: logger.category('UI')
}

/**
 * Hook de React para usar logger
 */
export function useLogger(category?: string) {
  if (category) {
    return logger.category(category)
  }
  return logger
}
