import Link from "next/link"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BookOpen, Users, Heart, ArrowRight } from "lucide-react"

const stakeholders = [
  {
    icon: BookOpen,
    title: "For Students",
    description:
      "Learn at your own pace with AI-powered personalized lessons and adaptive questions that help you think deeper.",
    features: ["Personalized learning paths", "AI tutoring support", "Progress tracking", "Instant feedback"],
    href: "/students",
    color: "from-primary to-secondary",
  },
  {
    icon: Users,
    title: "For Teachers",
    description:
      "Create engaging lessons, track student progress, and get AI-powered insights to improve teaching effectiveness.",
    features: ["Lesson planning tools", "Attendance tracking", "Performance analytics", "Custom assessments"],
    href: "/teachers",
    color: "from-secondary to-accent",
  },
  {
    icon: Heart,
    title: "For Parents",
    description:
      "Stay informed about your child's learning journey with detailed progress reports and actionable insights.",
    features: ["Progress monitoring", "Learning insights", "Weekly reports", "Improvement tips"],
    href: "/parents",
    color: "from-accent to-primary",
  },
]

export function StakeholdersSection() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-slide-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Built for Everyone</h2>
          <p className="text-xl text-foreground/60 max-w-2xl mx-auto">
            Tailored experiences for students, teachers, and parents
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {stakeholders.map((stakeholder, index) => {
            const Icon = stakeholder.icon
            return (
              <Link key={index} href={stakeholder.href}>
                <Card
                  className="p-8 h-full hover:shadow-xl transition-smooth hover:border-primary/50 group cursor-pointer animate-slide-up"
                  style={{ animationDelay: `${index * 150}ms` }}
                >
                  <div
                    className={`w-14 h-14 bg-gradient-to-br ${stakeholder.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-smooth`}
                  >
                    <Icon size={28} className="text-white" />
                  </div>

                  <h3 className="text-2xl font-bold mb-3">{stakeholder.title}</h3>
                  <p className="text-foreground/60 mb-6">{stakeholder.description}</p>

                  <ul className="space-y-2 mb-8">
                    {stakeholder.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2 text-sm text-foreground/70">
                        <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <Button
                    variant="outline"
                    className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-smooth bg-transparent"
                  >
                    Learn More
                    <ArrowRight size={16} className="ml-2" />
                  </Button>
                </Card>
              </Link>
            )
          })}
        </div>
      </div>
    </section>
  )
}
