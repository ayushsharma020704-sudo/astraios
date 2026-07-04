import { Canvas } from '@react-three/fiber'
import VideoBackground from './components/VideoBackground'
import StarField from './components/StarField'
import TimelineNav from './components/TimelineNav'

/**
 * Root layout — composes the three visual layers:
 *   1. Video background  (z-index 0)
 *   2. 3D canvas         (z-index 1)
 *   3. UI overlay         (z-index 2)
 */
export default function App() {
  return (
    <div className="layer-stack">
      {/* ── Layer 1: Background Video ── */}
      <VideoBackground />

      {/* ── Layer 2: Interactive 3D (transparent background) ── */}
      <div className="layer-canvas">
        <Canvas
          gl={{ alpha: true, antialias: true }}
          camera={{ position: [0, 0, 25], fov: 60 }}
          style={{ background: 'transparent' }}
        >
          <StarField />
        </Canvas>
      </div>

      {/* ── Layer 3: UI Overlay ── */}
      <div className="layer-ui">
        {/* Header */}
        <header className="flex items-center justify-center pt-10">
          <h1 className="header-title text-3xl md:text-4xl tracking-widest">
            ASTRAIOS
          </h1>
        </header>

        {/* Timeline at bottom */}
        <TimelineNav />
      </div>
    </div>
  )
}
