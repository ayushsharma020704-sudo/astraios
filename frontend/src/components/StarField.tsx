import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

const STAR_COUNT = 1500
const SPREAD = 50

/* ─── Vertex shader ─── */
const vertexShader = /* glsl */ `
  attribute float aPhase;
  varying float vPhase;

  void main() {
    vPhase = aPhase;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = (2.5 / -mvPosition.z) * 100.0;
    gl_PointSize = clamp(gl_PointSize, 1.0, 6.0);
    gl_Position = projectionMatrix * mvPosition;
  }
`

/* ─── Fragment shader ─── */
const fragmentShader = /* glsl */ `
  uniform float uTime;
  varying float vPhase;

  void main() {
    // Circular point shape
    vec2 center = gl_PointCoord - 0.5;
    float dist = length(center);
    if (dist > 0.5) discard;

    // Soft edge
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);

    // Sine-based twinkle — each star has its own phase offset
    float twinkle = 0.5 + 0.5 * sin(uTime * 1.8 + vPhase * 6.2831853);
    alpha *= mix(0.35, 1.0, twinkle);

    // Warm white with slight temperature variation per star
    vec3 warmWhite = vec3(0.95, 0.92, 0.85);
    vec3 coolBlue  = vec3(0.75, 0.85, 1.0);
    vec3 color = mix(warmWhite, coolBlue, vPhase);

    gl_FragColor = vec4(color, alpha);
  }
`

/**
 * Procedural star field rendered as a Points geometry
 * with a custom shader for per-point twinkle animation.
 */
export default function StarField() {
  const pointsRef = useRef<THREE.Points>(null!)
  const uniformsRef = useRef({ uTime: { value: 0 } })

  const { positions, phases } = useMemo(() => {
    const pos = new Float32Array(STAR_COUNT * 3)
    const pha = new Float32Array(STAR_COUNT)

    for (let i = 0; i < STAR_COUNT; i++) {
      // Distribute stars in a sphere
      const r = SPREAD * Math.cbrt(Math.random()) // cube root for uniform volume
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)

      pos[i * 3]     = r * Math.sin(phi) * Math.cos(theta)
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      pos[i * 3 + 2] = r * Math.cos(phi)

      pha[i] = Math.random() // random phase offset [0, 1]
    }

    return { positions: pos, phases: pha }
  }, [])

  useFrame((_state, delta) => {
    uniformsRef.current.uTime.value += delta

    // Very slow rotation for subtle motion
    if (pointsRef.current) {
      pointsRef.current.rotation.y += delta * 0.015
      pointsRef.current.rotation.x += delta * 0.005
    }
  })

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={STAR_COUNT}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-aPhase"
          array={phases}
          count={STAR_COUNT}
          itemSize={1}
        />
      </bufferGeometry>
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniformsRef.current}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}
