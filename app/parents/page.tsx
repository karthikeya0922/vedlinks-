"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Eye, BarChart3, MessageSquare } from "lucide-react"
import Link from "next/link"

export default function ParentsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Stay Connected to Your Child's Learning
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl">
              Monitor progress, get insights, and support your child's educational journey with real-time information.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <div>
                <h2 className="text-3xl font-bold mb-6">Real-Time Progress Monitoring</h2>
                <p className="text-foreground/70 mb-6">
                  Access your child's learning dashboard anytime. See what they're learning, how they're performing, and
                  where they need support.
                </p>
                <ul className="space-y-3">
                  {["Live progress updates", "Performance metrics", "Learning timeline", "Achievement tracking"].map(
                    (item, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-primary rounded-full" />
                        {item}
                      </li>
                    ),
                  )}
                </ul>
              </div>
              <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 h-64 flex items-center justify-center">
                <Eye size={64} className="text-primary/50" />
              </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
              <Card className="p-8 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20 h-64 flex items-center justify-center order-2 md:order-1">
                <BarChart3 size={64} className="text-secondary/50" />
              </Card>
              <div className="order-1 md:order-2">
                <h2 className="text-3xl font-bold mb-6">Detailed Insights & Reports</h2>
                <p className="text-foreground/70 mb-6">
                  Receive comprehensive weekly reports with actionable insights. Understand your child's strengths and
                  areas for improvement.
                </p>
                <ul className="space-y-3">
                  {["Weekly reports", "Topic analysis", "Strength identification", "Improvement recommendations"].map(
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
                <h2 className="text-3xl font-bold mb-6">Communicate & Collaborate</h2>
                <p className="text-foreground/70 mb-6">
                  Connect directly with teachers to discuss your child's progress. Get personalized advice on how to
                  support their learning at home.
                </p>
                <ul className="space-y-3">
                  {["Teacher messaging", "Progress discussions", "Support strategies", "Learning tips"].map(
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
                <MessageSquare size={64} className="text-accent/50" />
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold mb-6">Support Your Child's Success</h2>
            <p className="text-foreground/60 mb-8 max-w-2xl mx-auto">
              Join thousands of parents using LearnAI to stay connected and support their children's education.
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
