"use client"

import { useState } from "react"
import { Trophy, Star, Zap, Target } from "lucide-react"

interface AchievementBadgeProps {
  type: "gold" | "silver" | "bronze" | "lightning"
  title: string
  description: string
  delay?: number
}

export function AchievementBadge({ type, title, description, delay = 0 }: AchievementBadgeProps) {
  const [isHovered, setIsHovered] = useState(false)

  const badgeConfig = {
    gold: {
      icon: Trophy,
      color: "from-yellow-400 to-yellow-600",
      glow: "shadow-yellow-400/50",
      bg: "bg-yellow-50 dark:bg-yellow-950/30",
    },
    silver: {
      icon: Star,
      color: "from-gray-300 to-gray-500",
      glow: "shadow-gray-400/50",
      bg: "bg-gray-50 dark:bg-gray-950/30",
    },
    bronze: {
      icon: Target,
      color: "from-orange-400 to-orange-600",
      glow: "shadow-orange-400/50",
      bg: "bg-orange-50 dark:bg-orange-950/30",
    },
    lightning: {
      icon: Zap,
      color: "from-purple-400 to-pink-600",
      glow: "shadow-purple-400/50",
      bg: "bg-purple-50 dark:bg-purple-950/30",
    },
  }

  const config = badgeConfig[type]
  const Icon = config.icon

  return (
    <div
      className="animate-bounce-in"
      style={{ animationDelay: `${delay}ms` }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        className={`relative p-4 rounded-2xl ${config.bg} border border-primary/20 transition-smooth cursor-pointer ${
          isHovered ? `shadow-2xl ${config.glow}` : "shadow-lg"
        }`}
      >
        {/* Animated background glow */}
        {isHovered && (
          <div className={`absolute inset-0 bg-gradient-to-br ${config.color} rounded-2xl opacity-10 animate-pulse`} />
        )}

        <div className="relative flex flex-col items-center text-center">
          <div
            className={`w-16 h-16 bg-gradient-to-br ${config.color} rounded-full flex items-center justify-center mb-3 transition-smooth ${
              isHovered ? "scale-110 rotate-12" : ""
            }`}
          >
            <Icon size={32} className="text-white" />
          </div>
          <h3 className="font-bold text-sm">{title}</h3>
          <p className="text-xs text-foreground/60 mt-1">{description}</p>
        </div>
      </div>
    </div>
  )
}
