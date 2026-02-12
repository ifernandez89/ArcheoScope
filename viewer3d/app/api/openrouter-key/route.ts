import { NextResponse } from 'next/server'

export async function GET() {
  // Este endpoint simplemente redirige al backend
  // El frontend debe llamar directamente a http://127.0.0.1:8000/api/credentials/openrouter/api_key
  return NextResponse.json({ 
    error: 'Use direct backend call',
    backendUrl: 'http://127.0.0.1:8000/api/credentials/openrouter/api_key',
    success: false 
  }, { status: 501 })
}
