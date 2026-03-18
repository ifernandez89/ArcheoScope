/**
 * Dashboard de Métricas de Performance
 * Solo disponible en desarrollo
 */

'use client'

import { useState, useEffect } from 'react'
import { getMetricsSummary, getLocalStorageMetrics, clearMetrics } from '@/lib/webVitals'
import { get3DSummary, performance3D, clear3DMetrics } from '@/lib/performance3D'

export default function MetricsPage() {
  const [webVitalsSummary, setWebVitalsSummary] = useState<any>(null)
  const [metrics3DSummary, setMetrics3DSummary] = useState<any>(null)
  const [rawMetrics, setRawMetrics] = useState<any[]>([])
  const [raw3DMetrics, setRaw3DMetrics] = useState<any[]>([])
  
  const loadMetrics = () => {
    setWebVitalsSummary(getMetricsSummary())
    setMetrics3DSummary(get3DSummary())
    setRawMetrics(getLocalStorageMetrics())
    setRaw3DMetrics(performance3D.getLocalStorageMetrics())
  }
  
  useEffect(() => {
    loadMetrics()
  }, [])
  
  const handleClearAll = () => {
    clearMetrics()
    clear3DMetrics()
    loadMetrics()
  }
  
  return (
    <div style={{
      padding: '40px',
      maxWidth: '1400px',
      margin: '0 auto',
      fontFamily: 'monospace',
      background: '#0a0a0a',
      minHeight: '100vh',
      color: '#fff'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '40px'
      }}>
        <h1 style={{ fontSize: '32px', margin: 0 }}>📊 Performance Metrics Dashboard</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={loadMetrics}
            style={{
              padding: '10px 20px',
              background: '#4299e1',
              border: 'none',
              borderRadius: '6px',
              color: 'white',
              cursor: 'pointer',
              fontFamily: 'monospace'
            }}
          >
            🔄 Refresh
          </button>
          <button
            onClick={handleClearAll}
            style={{
              padding: '10px 20px',
              background: '#e53e3e',
              border: 'none',
              borderRadius: '6px',
              color: 'white',
              cursor: 'pointer',
              fontFamily: 'monospace'
            }}
          >
            🗑️ Clear All
          </button>
        </div>
      </div>
      
      {/* Web Vitals Summary */}
      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '20px', color: '#4299e1' }}>
          🌐 Web Vitals (Real User Metrics)
        </h2>
        
        {webVitalsSummary && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '20px'
          }}>
            {Object.entries(webVitalsSummary).map(([key, data]: [string, any]) => (
              <div
                key={key}
                style={{
                  background: '#1a1a1a',
                  padding: '20px',
                  borderRadius: '8px',
                  border: '1px solid #333'
                }}
              >
                <div style={{ fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                  {key.toUpperCase()}
                </div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>
                  {data.avg}ms
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>
                  Min: {data.min}ms | Max: {data.max}ms
                </div>
                <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                  Samples: {data.values.length}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
      
      {/* 3D Metrics Summary */}
      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '20px', color: '#48bb78' }}>
          🎮 3D Performance Metrics
        </h2>
        
        {metrics3DSummary && Object.keys(metrics3DSummary).length > 0 ? (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '20px'
          }}>
            {Object.entries(metrics3DSummary).map(([key, data]: [string, any]) => (
              <div
                key={key}
                style={{
                  background: '#1a1a1a',
                  padding: '20px',
                  borderRadius: '8px',
                  border: '1px solid #333'
                }}
              >
                <div style={{ fontSize: '12px', color: '#888', marginBottom: '8px' }}>
                  {key}
                </div>
                <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>
                  {data.avg}ms
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>
                  Min: {data.min}ms | Max: {data.max}ms
                </div>
                <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                  Count: {data.count}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>
            No 3D metrics collected yet. Visit /game to generate metrics.
          </div>
        )}
      </section>
      
      {/* Raw Metrics Table */}
      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '20px', color: '#ed8936' }}>
          📋 Recent Web Vitals (Last 20)
        </h2>
        
        {rawMetrics.length > 0 ? (
          <div style={{
            background: '#1a1a1a',
            borderRadius: '8px',
            overflow: 'hidden',
            border: '1px solid #333'
          }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#2d2d2d' }}>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Metric</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Value</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Rating</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Route</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Device</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Time</th>
                </tr>
              </thead>
              <tbody>
                {rawMetrics.slice(-20).reverse().map((metric, i) => (
                  <tr key={i} style={{ borderTop: '1px solid #333' }}>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.name}</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.value}ms</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>
                      <span style={{
                        padding: '2px 8px',
                        borderRadius: '4px',
                        background: metric.rating === 'good' ? '#48bb78' : 
                                   metric.rating === 'needs-improvement' ? '#ed8936' : '#e53e3e',
                        fontSize: '10px'
                      }}>
                        {metric.rating}
                      </span>
                    </td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.route}</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.device}</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>
                      {new Date(metric.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>
            No metrics collected yet.
          </div>
        )}
      </section>
      
      {/* Raw 3D Metrics */}
      <section>
        <h2 style={{ fontSize: '24px', marginBottom: '20px', color: '#9f7aea' }}>
          🎯 Recent 3D Metrics (Last 20)
        </h2>
        
        {raw3DMetrics.length > 0 ? (
          <div style={{
            background: '#1a1a1a',
            borderRadius: '8px',
            overflow: 'hidden',
            border: '1px solid #333'
          }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#2d2d2d' }}>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Metric</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Value</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Metadata</th>
                  <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px' }}>Time</th>
                </tr>
              </thead>
              <tbody>
                {raw3DMetrics.slice(-20).reverse().map((metric, i) => (
                  <tr key={i} style={{ borderTop: '1px solid #333' }}>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.name}</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>{metric.value}ms</td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>
                      {metric.metadata ? JSON.stringify(metric.metadata) : '-'}
                    </td>
                    <td style={{ padding: '12px', fontSize: '12px' }}>
                      {new Date(metric.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>
            No 3D metrics collected yet.
          </div>
        )}
      </section>
    </div>
  )
}
