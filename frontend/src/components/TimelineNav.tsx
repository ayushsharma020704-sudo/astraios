import { useState } from 'react'

const EPOCHS = [
  { id: 'big-bang', label: 'Big Bang' },
  { id: 'first-stars', label: 'First Stars' },
  { id: 'milky-way', label: 'Milky Way' },
  { id: 'solar-system', label: 'Solar System' },
  { id: 'now', label: 'Now' },
] as const

/**
 * Horizontal timeline navigation bar with 5 epoch labels.
 * Dark glassmorphism styling via the .glass utility class.
 */
export default function TimelineNav() {
  const [activeId, setActiveId] = useState<string>(EPOCHS[0].id)

  return (
    <nav
      id="timeline-nav"
      aria-label="Cosmic timeline"
      className="glass mx-auto mb-8 rounded-2xl max-w-fit"
    >
      <div className="timeline-nav">
        {EPOCHS.map((epoch, idx) => (
          <div key={epoch.id} className="flex items-center">
            <button
              id={`epoch-${epoch.id}`}
              className={`epoch-btn ${activeId === epoch.id ? 'active' : ''}`}
              onClick={() => setActiveId(epoch.id)}
              aria-current={activeId === epoch.id ? 'step' : undefined}
            >
              {epoch.label}
            </button>
            {idx < EPOCHS.length - 1 && <span className="epoch-connector" />}
          </div>
        ))}
      </div>
    </nav>
  )
}
