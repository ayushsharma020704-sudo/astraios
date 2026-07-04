import { useEffect, useState } from 'react'

type Status = 'checking' | 'connected' | 'offline'

/**
 * Tiny badge that pings the backend /health endpoint on mount
 * and shows connection status.
 */
export default function BackendStatus() {
  const [status, setStatus] = useState<Status>('checking')

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then((res) => res.json())
      .then((data) => {
        setStatus(data.status === 'ok' ? 'connected' : 'offline')
      })
      .catch(() => {
        setStatus('offline')
      })
  }, [])

  const color =
    status === 'connected'
      ? '#34d399'
      : status === 'offline'
        ? '#f87171'
        : '#94a3b8'

  const label =
    status === 'connected'
      ? 'Connected'
      : status === 'offline'
        ? 'Offline'
        : 'Checking…'

  return (
    <div
      id="backend-status"
      style={{
        position: 'fixed',
        bottom: 12,
        right: 16,
        zIndex: 50,
        display: 'flex',
        alignItems: 'center',
        gap: 6,
        padding: '4px 10px',
        borderRadius: 6,
        background: 'rgba(7,11,20,0.7)',
        backdropFilter: 'blur(8px)',
        fontSize: 11,
        fontFamily: 'monospace',
        color,
        border: `1px solid ${color}33`,
        pointerEvents: 'auto',
      }}
    >
      <span
        style={{
          width: 6,
          height: 6,
          borderRadius: '50%',
          background: color,
          boxShadow: status === 'connected' ? `0 0 6px ${color}` : 'none',
        }}
      />
      Backend: {label}
    </div>
  )
}
