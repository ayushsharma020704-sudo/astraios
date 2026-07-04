import { useEffect, useRef } from 'react'

/**
 * Full-screen background video layer.
 * Pauses playback when the tab is hidden (Page Visibility API)
 * to save GPU/CPU resources.
 *
 * Swap the placeholder video by replacing /public/videos/nebula-loop.mp4
 * with your own file (see README for details).
 */
export default function VideoBackground() {
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const handleVisibilityChange = () => {
      if (document.hidden) {
        video.pause()
      } else {
        video.play().catch(() => {
          // Autoplay may be blocked; silently handle
        })
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [])

  return (
    <div className="layer-video">
      <video
        ref={videoRef}
        src="/videos/nebula-loop.mp4"
        muted
        loop
        autoPlay
        playsInline
        aria-hidden="true"
        style={{
          /* Fallback dark gradient when no video file is present */
          background: 'linear-gradient(180deg, #03050a 0%, #0d1526 40%, #1c0a30 70%, #03050a 100%)',
        }}
      />
    </div>
  )
}
