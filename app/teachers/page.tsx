"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BookOpen, BarChart3, Users } from "lucide-react"
import Link from "next/link"

export default function TeachersPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Empower Your Teaching
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl">
              Create engaging lessons, track student progress, and make data-driven decisions to improve learning
              outcomes.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <div>
                <h2 className="text-3xl font-bold mb-6">Lesson Planning Made Easy</h2>
                <p className="text-foreground/70 mb-6">
                  Create comprehensive lesson plans with our intuitive tools. Add multimedia content, set learning
                  objectives, and organize your curriculum efficiently.
                </p>
                <ul className="space-y-3">
                  {[
                    "Drag-and-drop lesson builder",
                    "Content library integration",
                    "Learning objective tracking",
                    "Resource management",
                  ].map((item, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-primary rounded-full" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 h-64 flex items-center justify-center">
                <BookOpen size={64} className="text-primary/50" />
              </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <Card className="p-8 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20 h-64 flex items-center justify-center order-2 md:order-1">
                <BarChart3 size={64} className="text-secondary/50" />
              </Card>
              <div className="order-1 md:order-2">
                <h2 className="text-3xl font-bold mb-6">Advanced Analytics</h2>
                <p className="text-foreground/70 mb-6">
                  Get detailed insights into student performance. Identify struggling students, track progress by topic,
                  and make informed decisions about your teaching.
                </p>
                <ul className="space-y-3">
                  {[
                    "Real-time performance tracking",
                    "Topic-wise analysis",
                    "Student comparison reports",
                    "Trend identification",
                  ].map((item, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-secondary rounded-full" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl font-bold mb-6">Attendance & Assessment</h2>
                <p className="text-foreground/70 mb-6">
                  Manage attendance effortlessly and create custom assessments. Our AI-powered grading system saves you
                  time while providing detailed feedback to students.
                </p>
                <ul className="space-y-3">
                  {[
                    "Quick attendance marking",
                    "Custom question creation",
                    "AI-powered grading",
                    "Automated feedback generation",
                  ].map((item, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-accent rounded-full" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <Card className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 h-64 flex items-center justify-center">
                <Users size={64} className="text-accent/50" />
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Transform Your Classroom?</h2>
            <p className="text-foreground/60 mb-8 max-w-2xl mx-auto">
              Join thousands of teachers using LearnAI to create better learning experiences.
            </p>
            <Link href="/signup">
              <Button size="lg" className="bg-gradient-to-r from-primary to-secondary">
                Get Started Free
              </Button>
            </Link>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
