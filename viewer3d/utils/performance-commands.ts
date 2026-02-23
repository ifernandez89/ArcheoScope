/**
 * Performance Commands - Comandos de consola para debugging
 * Usar en DevTools Console
 */

import { performanceMonitor } from './performance-monitor'
import { fileLogger } from './file-logger'

// Exponer comandos globalmente
if (typeof window !== 'undefined') {
  const commands = {
    // Crear snapshot
    snapshot: (location: string = 'Unknown', weather: string = 'Clear', anomalies: number = 0) => {
      performanceMonitor.createSnapshot(location, weather, anomalies)
      console.log('✅ Snapshot created')
    },
    
    // Ver reporte
    report: () => {
      performanceMonitor.printReport()
    },
    
    // Limpiar snapshots
    clear: () => {
      performanceMonitor.clearSnapshots()
      console.log('✅ Snapshots cleared')
    },
    
    // NUEVO: Descargar logs
    download: () => {
      fileLogger.downloadLogs()
      console.log('✅ Logs downloaded')
    },
    
    // NUEVO: Ver logs
    logs: () => {
      console.log(fileLogger.getLogs())
    },
    
    // Ayuda
    help: () => {
      console.group('📊 PERFORMANCE COMMANDS')
      console.log('perf.snapshot(location, weather, anomalies) - Capturar snapshot')
      console.log('  Ejemplo: perf.snapshot("Machu Picchu", "Rain+Wind", 1)')
      console.log('')
      console.log('perf.report() - Ver reporte completo')
      console.log('perf.download() - Descargar logs como archivo TXT')
      console.log('perf.logs() - Ver todos los logs en consola')
      console.log('perf.clear() - Limpiar snapshots')
      console.log('perf.help() - Mostrar esta ayuda')
      console.groupEnd()
    }
  }
  
  ;(window as any).perf = commands
  
  console.log('💡 Performance commands loaded. Type "perf.help()" for usage')
  console.log('💡 Los logs se guardan automáticamente. Usa "perf.download()" para descargarlos')
}

export {}
