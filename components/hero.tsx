import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, Sparkles, Zap, Target } from "lucide-react"
import { FloatingElement } from "@/components/floating-element"

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Enhanced gradient background with multiple layers */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-secondary/10 -z-10" />
      <div className="absolute top-20 right-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl -z-10 animate-pulse" />
      <div className="absolute bottom-20 left-10 w-72 h-72 bg-secondary/20 rounded-full blur-3xl -z-10 animate-pulse" />

      <div className="absolute top-40 right-20 -z-10">
        <FloatingElement delay={0} duration={4}>
          <div className="w-20 h-20 bg-gradient-to-br from-primary/30 to-secondary/30 rounded-full blur-2xl" />
        </FloatingElement>
      </div>
      <div className="absolute bottom-40 left-20 -z-10">
        <FloatingElement delay={500} duration={5}>
          <div className="w-24 h-24 bg-gradient-to-br from-accent/30 to-primary/30 rounded-full blur-2xl" />
        </FloatingElement>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="animate-slide-up">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-6 border border-primary/20 hover:border-primary/50 transition-smooth cursor-pointer group">
              <Sparkles size={16} className="text-primary group-hover:animate-spin-slow" />
              <span className="text-sm font-medium text-primary">AI-Powered Learning</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent animate-pulse">
                Transform Education
              </span>
              <br />
              <span className="text-foreground">with AI</span>
            </h1>

            <p className="text-xl text-foreground/70 mb-8 leading-relaxed max-w-lg">
              Personalized learning experiences powered by AI. Students learn better, teachers teach smarter, and
              parents stay informed. All in one platform.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-primary to-secondary hover:shadow-2xl hover:shadow-primary/50 transition-smooth w-full sm:w-auto group"
                >
                  Get Started Free
                  <ArrowRight className="ml-2 group-hover:translate-x-1 transition-smooth" size={20} />
                </Button>
              </Link>
              <Link href="/features">
                <Button
                  size="lg"
                  variant="outline"
                  className="w-full sm:w-auto bg-transparent hover:bg-primary/10 transition-smooth"
                >
                  Learn More
                </Button>
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-6 mt-12 pt-8 border-t border-border">
              <div className="group cursor-pointer">
                <div className="text-3xl font-bold text-primary group-hover:scale-110 transition-smooth">10K+</div>
                <p className="text-sm text-foreground/60">Active Students</p>
              </div>
              <div className="group cursor-pointer">
                <div className="text-3xl font-bold text-secondary group-hover:scale-110 transition-smooth">500+</div>
                <p className="text-sm text-foreground/60">Schools</p>
              </div>
              <div className="group cursor-pointer">
                <div className="text-3xl font-bold text-accent group-hover:scale-110 transition-smooth">95%</div>
                <p className="text-sm text-foreground/60">Satisfaction</p>
              </div>
            </div>
          </div>

          {/* Right Visual - Enhanced with gamification */}
          <div className="relative h-96 md:h-full min-h-96 animate-fade-in">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-2xl blur-xl" />
            <div className="relative h-full bg-gradient-to-br from-primary/10 to-secondary/10 rounded-2xl border border-primary/20 flex items-center justify-center overflow-hidden group hover:border-primary/50 transition-smooth">
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-smooth duration-500">
                <div className="absolute top-8 right-8">
                  <FloatingElement delay={0}>
                    <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center shadow-lg">
                      <Zap size={24} className="text-white" />
                    </div>
                  </FloatingElement>
                </div>
                <div className="absolute bottom-8 left-8">
                  <FloatingElement delay={200}>
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-600 rounded-full flex items-center justify-center shadow-lg">
                      <Target size={24} className="text-white" />
                    </div>
                  </FloatingElement>
                </div>
              </div>

              <div className="text-center z-10">
                <div className="w-24 h-24 bg-gradient-to-br from-primary to-secondary rounded-full mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-smooth shadow-lg">
                  <Sparkles size={48} className="text-white animate-spin-slow" />
                </div>
                <p className="text-foreground/60 font-medium">AI-Powered Learning Platform</p>
                <p className="text-sm text-foreground/40 mt-2">Hover to see gamification features</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
