# ASTRAIOS — Interactive Cosmic Timeline

A space-themed interactive timeline app exploring the history of the universe, from the Big Bang to the present day.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Build | Vite + React 18 + TypeScript |
| 3D | three.js + @react-three/fiber + @react-three/drei |
| Animation | GSAP + ScrollTrigger (not yet wired) |
| Styling | TailwindCSS v4 |

## Getting Started

```bash
npm install
npm run dev
```

## Visual Architecture

The app renders three stacked full-screen layers:

1. **Video Background** (`z-index: 0`) — A full-screen looping `<video>` element with a dark gradient fallback.
2. **3D Canvas** (`z-index: 1`) — A transparent `@react-three/fiber` Canvas hosting the procedural star field.
3. **UI Overlay** (`z-index: 2`) — Header + timeline navigation with dark glassmorphism styling.

## Swapping the Placeholder Video

The app expects a background video at:

```
public/videos/nebula-loop.mp4
```

To use your own video:

1. **Choose a video** — Ideal specs: 1920×1080 or higher, 15–30 fps, H.264/MP4, ≤ 15 MB for fast loading. Space nebula, galaxy timelapse, or particle simulations work great. Good free sources:
   - [Pexels](https://www.pexels.com/search/videos/space/)
   - [Pixabay](https://pixabay.com/videos/search/nebula/)
   - [NASA Scientific Visualization Studio](https://svs.gsfc.nasa.gov/)

2. **Replace the file** — Drop your video into `public/videos/` as `nebula-loop.mp4`, or update the `src` attribute in `src/components/VideoBackground.tsx`:
   ```tsx
   <video src="/videos/your-video-name.mp4" ... />
   ```

3. **Optimize** — For web, compress with FFmpeg:
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -an -movflags +faststart public/videos/nebula-loop.mp4
   ```
   The `-an` flag strips audio (not needed since the video is muted).

4. **Fallback** — When no video file is present, a dark purple-black CSS gradient is shown automatically.

## Project Structure

```
src/
├── main.tsx                    # React 18 entry point
├── App.tsx                     # Root layout — composes all three layers
├── index.css                   # Global styles + Tailwind theme
└── components/
    ├── VideoBackground.tsx     # Layer 1 — Background video
    ├── StarField.tsx           # Layer 2 — Procedural 3D star field
    └── TimelineNav.tsx         # Layer 3 — Epoch navigation bar
```
