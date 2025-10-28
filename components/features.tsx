import { Card } from "@/components/ui/card"
import { Brain, BarChart3, Users, Zap, Shield, Smartphone } from "lucide-react"
import { AchievementBadge } from "@/components/achievement-badge"

const features = [
  {
    icon: Brain,
    title: "AI-Powered Questions",
    description:
      "Dynamic, adaptive questions that help students think critically instead of memorizing static content.",
    color: "from-primary to-secondary",
  },
  {
    icon: BarChart3,
    title: "Advanced Analytics",
    description:
      "Real-time insights into student performance, topic mastery, and personalized improvement recommendations.",
    color: "from-secondary to-accent",
  },
  {
    icon: Users,
    title: "Multi-Stakeholder",
    description: "Seamless experience for students, teachers, and parents with role-specific dashboards and features.",
    color: "from-accent to-primary",
  },
  {
    icon: Zap,
    title: "Instant Feedback",
    description: "AI-powered grading and detailed explanations help students learn from mistakes immediately.",
    color: "from-primary to-accent",
  },
  {
    icon: Shield,
    title: "Secure & Compliant",
    description: "Enterprise-grade security with FERPA and GDPR compliance to protect student data.",
    color: "from-secondary to-primary",
  },
  {
    icon: Smartphone,
    title: "Mobile Ready",
    description: "Learn anywhere, anytime with our responsive design optimized for all devices.",
    color: "from-accent to-secondary",
  },
]

export function FeaturesSection() {
  return (
    <section className="py-20 bg-muted/30 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl -z-10" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-secondary/5 rounded-full blur-3xl -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-slide-up">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Powerful Features for
            <br />
            <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Modern Learning
            </span>
          </h2>
          <p className="text-xl text-foreground/60 max-w-2xl mx-auto">
            Everything you need to create an engaging, personalized learning experience
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Card
                key={index}
                className="p-6 hover:shadow-2xl transition-smooth hover:border-primary/50 group cursor-pointer animate-slide-up relative overflow-hidden"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-smooth" />

                <div className="relative z-10">
                  <div
                    className={`w-12 h-12 bg-gradient-to-br ${feature.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-125 transition-smooth shadow-lg`}
                  >
                    <Icon size={24} className="text-white" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2 group-hover:text-primary transition-smooth">
                    {feature.title}
                  </h3>
                  <p className="text-foreground/60 group-hover:text-foreground/80 transition-smooth">
                    {feature.description}
                  </p>
                </div>
              </Card>
            )
          })}
        </div>

        <div className="mt-20 pt-20 border-t border-border">
          <div className="text-center mb-12 animate-slide-up">
            <h3 className="text-3xl font-bold mb-2">Unlock Achievements</h3>
            <p className="text-foreground/60">Gamified learning keeps students motivated and engaged</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <AchievementBadge type="gold" title="Master" description="Complete 100 lessons" delay={0} />
            <AchievementBadge type="silver" title="Scholar" description="Score 95% or higher" delay={100} />
            <AchievementBadge type="bronze" title="Streak" description="7-day learning streak" delay={200} />
            <AchievementBadge type="lightning" title="Speed" description="Answer 10 questions in 5 mins" delay={300} />
          </div>
        </div>
      </div>
    </section>
  )
}
