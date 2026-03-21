import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export function CTASection() {
  return (
    <section className="py-20 bg-gradient-to-r from-primary/10 via-secondary/10 to-accent/10 relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-10 right-10 w-40 h-40 bg-primary/20 rounded-full blur-3xl -z-10" />
      <div className="absolute bottom-10 left-10 w-40 h-40 bg-secondary/20 rounded-full blur-3xl -z-10" />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center animate-slide-up">
        <h2 className="text-4xl md:text-5xl font-bold mb-6">
          Ready to Transform
          <br />
          <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            Your Learning Experience?
          </span>
        </h2>

        <p className="text-xl text-foreground/60 mb-8 max-w-2xl mx-auto">
          Join thousands of students, teachers, and parents already using LearnAI to achieve better learning outcomes.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/signup">
            <Button
              size="lg"
              className="bg-gradient-to-r from-primary to-secondary hover:shadow-lg hover:shadow-primary/50 transition-smooth"
            >
              Start Free Trial
              <ArrowRight className="ml-2" size={20} />
            </Button>
          </Link>
          <Link href="/contact">
            <Button size="lg" variant="outline">
              Schedule Demo
            </Button>
          </Link>
        </div>

        <p className="text-sm text-foreground/50 mt-8">No credit card required. Free for 30 days.</p>
      </div>
    </section>
  )
}
