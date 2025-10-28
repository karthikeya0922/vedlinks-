"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { CheckCircle2 } from "lucide-react"

const featureCategories = [
  {
    title: "For Students",
    features: [
      "AI-powered adaptive learning paths",
      "Dynamic question generation",
      "Real-time performance tracking",
      "Personalized study recommendations",
      "Interactive lessons and tutorials",
      "Progress visualization",
    ],
  },
  {
    title: "For Teachers",
    features: [
      "Lesson plan creation tools",
      "Attendance management",
      "Student performance analytics",
      "Custom assessment creation",
      "Class-wide insights and trends",
      "Automated grading system",
    ],
  },
  {
    title: "For Parents",
    features: [
      "Real-time progress monitoring",
      "Weekly performance reports",
      "Learning insights and analytics",
      "Improvement recommendations",
      "Communication with teachers",
      "Achievement milestones",
    ],
  },
  {
    title: "Platform Features",
    features: [
      "Enterprise-grade security",
      "FERPA & GDPR compliant",
      "Mobile-responsive design",
      "Real-time collaboration",
      "API integrations",
      "Advanced reporting",
    ],
  },
]

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 text-center">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Powerful Features
              </span>
            </h1>
            <p className="text-xl text-foreground/60 text-center max-w-2xl mx-auto">
              Everything you need for a complete learning management experience
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
              {featureCategories.map((category, index) => (
                <Card key={index} className="p-8 hover:shadow-lg transition-smooth">
                  <h2 className="text-2xl font-bold mb-6">{category.title}</h2>
                  <ul className="space-y-4">
                    {category.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3">
                        <CheckCircle2 size={20} className="text-primary mt-1 flex-shrink-0" />
                        <span className="text-foreground/80">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
