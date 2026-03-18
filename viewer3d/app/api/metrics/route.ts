/**
 * API endpoint para recibir métricas de performance
 * POST /api/metrics
 */

import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const metric = await request.json()
    
    // Validar métrica
    if (!metric.name || typeof metric.value !== 'number') {
      return NextResponse.json(
        { error: 'Invalid metric data' },
        { status: 400 }
      )
    }
    
    // Log en servidor (desarrollo)
    if (process.env.NODE_ENV === 'development') {
      console.log('[Metric Received]', {
        name: metric.name,
        value: `${metric.value}ms`,
        rating: metric.rating,
        route: metric.route,
        device: metric.device
      })
    }
    
    // Aquí se puede:
    // 1. Guardar en base de datos
    // 2. Enviar a servicio de analytics
    // 3. Agregar a cola de procesamiento
    // 4. etc.
    
    // Por ahora, solo guardamos en archivo (desarrollo)
    if (process.env.NODE_ENV === 'development') {
      const fs = await import('fs/promises')
      const path = await import('path')
      
      const metricsFile = path.join(process.cwd(), 'metrics.jsonl')
      const line = JSON.stringify(metric) + '\n'
      
      try {
        await fs.appendFile(metricsFile, line)
      } catch (error) {
        console.error('Error writing metrics file:', error)
      }
    }
    
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error processing metric:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// GET para obtener métricas (desarrollo)
export async function GET() {
  if (process.env.NODE_ENV !== 'development') {
    return NextResponse.json(
      { error: 'Not available in production' },
      { status: 403 }
    )
  }
  
  try {
    const fs = await import('fs/promises')
    const path = await import('path')
    
    const metricsFile = path.join(process.cwd(), 'metrics.jsonl')
    
    try {
      const content = await fs.readFile(metricsFile, 'utf-8')
      const lines = content.trim().split('\n')
      const metrics = lines.map(line => JSON.parse(line))
      
      return NextResponse.json({ metrics })
    } catch (error) {
      // Archivo no existe o está vacío
      return NextResponse.json({ metrics: [] })
    }
  } catch (error) {
    console.error('Error reading metrics:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
