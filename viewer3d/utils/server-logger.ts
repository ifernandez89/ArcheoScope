/**
 * ServerLogger - Guarda logs en archivo del servidor
 */

export class ServerLogger {
  private logs: string[] = []
  private sessionId: string
  
  constructor() {
    this.sessionId = new Date().toISOString().replace(/[:.]/g, '-')
    this.log('SESSION_START', `Session: ${this.sessionId}`)
  }
  
  log(category: string, message: string, data?: any): void {
    const timestamp = Date.now()
    const logLine = `[${new Date().toISOString()}] [${category}] ${message}${data ? ' | ' + JSON.stringify(data) : ''}`
    this.logs.push(logLine)
    console.log(`📝 ${logLine}`)
    
    // Enviar al servidor
    this.sendToServer(logLine)
  }
  
  private async sendToServer(logLine: string): Promise<void> {
    try {
      await fetch('/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ log: logLine })
      })
    } catch (e) {
      // Silencioso si falla
    }
  }
  
  getLogs(): string {
    return this.logs.join('\n')
  }
}

export const serverLogger = new ServerLogger()
