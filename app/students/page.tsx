"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Brain, Zap, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function StudentsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Learn Smarter, Not Harder
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl">
              Personalized learning experiences powered by AI. Study at your own pace and achieve better results.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <div>
                <h2 className="text-3xl font-bold mb-6">Personalized Learning Paths</h2>
                <p className="text-foreground/70 mb-6">
                  Our AI adapts to your learning style and pace. Get customized lessons and practice questions that help
                  you master each topic.
                </p>
                <ul className="space-y-3">
                  {[
                    "Adaptive difficulty levels",
                    "Personalized recommendations",
                    "Learning style optimization",
                    "Progress tracking",
                  ].map((item, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 h-64 flex items-center justify-center">
                <Brain size={64} className="text-primary/50" />
              </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <Card className="p-8 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20 h-64 flex items-center justify-center order-2 md:order-1">
                <Zap size={64} className="text-secondary/50" />
              </Card>
              <div className="order-1 md:order-2">
                <h2 className="text-3xl font-bold mb-6">Instant Feedback</h2>
                <p className="text-foreground/70 mb-6">
                  Get immediate feedback on your answers with detailed explanations. Understand why you got something
                  wrong and learn from your mistakes.
                </p>
                <ul className="space-y-3">
                  {["Instant grading", "Detailed explanations", "Concept reinforcement", "Error analysis"].map(
                    (item, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-secondary rounded-full" />
                        {item}
                      </li>
                    ),
                  )}
                </ul>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl font-bold mb-6">Track Your Progress</h2>
                <p className="text-foreground/70 mb-6">
                  Visualize your learning journey with comprehensive progress reports. See which topics you've mastered
                  and where you need more practice.
                </p>
                <ul className="space-y-3">
                  {["Performance analytics", "Topic mastery tracking", "Achievement badges", "Goal setting"].map(
                    (item, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-accent rounded-full" />
                        {item}
                      </li>
                    ),
                  )}
                </ul>
              </div>
              <Card className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 h-64 flex items-center justify-center">
                <TrendingUp size={64} className="text-accent/50" />
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold mb-6">Start Your Learning Journey Today</h2>
            <p className="text-foreground/60 mb-8 max-w-2xl mx-auto">
              Join thousands of students achieving their learning goals with LearnAI.
            </p>
            <Link href="/signup">
              <Button size="lg" className="bg-gradient-to-r from-primary to-secondary">
                Sign Up Free
              </Button>
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
