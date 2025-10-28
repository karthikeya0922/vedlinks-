"use client"

import { useEffect, useState } from "react"

interface ProgressRingProps {
  percentage: number
  label: string
  color?: string
  size?: number
}

export function ProgressRing({
  percentage,
  label,
  color = "from-primary to-secondary",
  size = 120,
}: ProgressRingProps) {
  const [displayPercentage, setDisplayPercentage] = useState(0)

  useEffect(() => {
    const timer = setTimeout(() => setDisplayPercentage(percentage), 100)
    return () => clearTimeout(timer)
  }, [percentage])

  const circumference = 2 * Math.PI * 45
  const offset = circumference - (displayPercentage / 100) * circumference

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-muted"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r="45"
            fill="none"
            stroke="url(#gradient)"
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="var(--color-primary)" />
              <stop offset="100%" stopColor="var(--color-secondary)" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl font-bold">{displayPercentage}%</div>
            <div className="text-xs text-foreground/60">{label}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
