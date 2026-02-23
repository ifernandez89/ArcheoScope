import { NextRequest, NextResponse } from 'next/server'
import { writeFile, appendFile, readFile } from 'fs/promises'
import { existsSync } from 'fs'
import path from 'path'

const LOG_FILE = path.join(process.cwd(), 'PERFORMANCE_LOGS.txt')

export async function POST(request: NextRequest) {
  try {
    const { log } = await request.json()
    
    // Agregar al archivo
    await appendFile(LOG_FILE, log + '\n', 'utf-8')
    
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error writing log:', error)
    return NextResponse.json({ success: false }, { status: 500 })
  }
}

export async function GET() {
  try {
    if (!existsSync(LOG_FILE)) {
      return NextResponse.json({ logs: '' })
    }
    
    const logs = await readFile(LOG_FILE, 'utf-8')
    return NextResponse.json({ logs })
  } catch (error) {
    return NextResponse.json({ logs: '' })
  }
}
