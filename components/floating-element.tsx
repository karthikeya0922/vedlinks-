"use client"

import type React from "react"

import { useEffect, useState } from "react"

interface FloatingElementProps {
  children: React.ReactNode
  delay?: number
  duration?: number
}

export function FloatingElement({ children, delay = 0, duration = 3 }: FloatingElementProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const randomX = Math.random() * 20 - 10
    const randomY = Math.random() * 20 - 10
    setPosition({ x: randomX, y: randomY })
  }, [])

  return (
    <div
      className="animate-float"
      style={{
        animationDelay: `${delay}ms`,
        animationDuration: `${duration}s`,
        transform: `translate(${position.x}px, ${position.y}px)`,
      }}
    >
      {children}
    </div>
  )
}
