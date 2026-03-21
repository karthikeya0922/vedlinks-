"use client"

import { ProgressRing } from "@/components/progress-ring"
import { Card } from "@/components/ui/card"
import { Flame, Zap } from "lucide-react"

export function GamificationShowcaseSection() {
  return (
    <section className="py-20 bg-gradient-to-b from-background to-muted/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-slide-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Gamified Learning Experience
            </span>
          </h2>
          <p className="text-xl text-foreground/60 max-w-2xl mx-auto">
            Keep students engaged with achievements, streaks, and real-time progress tracking
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {/* Progress Rings */}
          <Card className="p-8 flex flex-col items-center justify-center hover:shadow-lg transition-smooth animate-slide-up">
            <ProgressRing percentage={75} label="Mastery" />
          </Card>

          <Card
            className="p-8 flex flex-col items-center justify-center hover:shadow-lg transition-smooth animate-slide-up"
            style={{ animationDelay: "100ms" }}
          >
            <ProgressRing percentage={92} label="Accuracy" />
          </Card>

          <Card
            className="p-8 flex flex-col items-center justify-center hover:shadow-lg transition-smooth animate-slide-up"
            style={{ animationDelay: "200ms" }}
          >
            <ProgressRing percentage={60} label="Completion" />
          </Card>

          <Card
            className="p-8 flex flex-col items-center justify-center hover:shadow-lg transition-smooth animate-slide-up"
            style={{ animationDelay: "300ms" }}
          >
            <ProgressRing percentage={88} label="Engagement" />
          </Card>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 hover:border-primary/50 transition-smooth group cursor-pointer animate-slide-up">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold mb-2">Current Streak</h3>
                <p className="text-foreground/60">Keep the momentum going</p>
              </div>
              <Flame size={32} className="text-orange-500 group-hover:animate-pulse" />
            </div>
            <div className="text-4xl font-bold text-primary">7 Days</div>
            <p className="text-sm text-foreground/60 mt-2">+50 XP per day</p>
          </Card>

          <Card
            className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 hover:border-accent/50 transition-smooth group cursor-pointer animate-slide-up"
            style={{ animationDelay: "100ms" }}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold mb-2">Total XP</h3>
                <p className="text-foreground/60">Experience points earned</p>
              </div>
              <Zap size={32} className="text-yellow-500 group-hover:animate-spin-slow" />
            </div>
            <div className="text-4xl font-bold text-accent">2,450 XP</div>
            <p className="text-sm text-foreground/60 mt-2">Level 12 - Next level in 550 XP</p>
          </Card>
        </div>
      </div>
    </section>
  )
}
