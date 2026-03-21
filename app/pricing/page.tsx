"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle2 } from "lucide-react"
import Link from "next/link"

const plans = [
  {
    name: "Student",
    price: "Free",
    description: "Perfect for individual learners",
    features: ["Unlimited lessons", "AI-powered questions", "Progress tracking", "Basic analytics", "Mobile access"],
    cta: "Get Started",
    highlighted: false,
  },
  {
    name: "Teacher",
    price: "$9.99",
    period: "/month",
    description: "For educators managing classes",
    features: [
      "Everything in Student",
      "Class management",
      "Attendance tracking",
      "Custom assessments",
      "Advanced analytics",
      "Student performance reports",
      "Priority support",
    ],
    cta: "Start Free Trial",
    highlighted: true,
  },
  {
    name: "School",
    price: "Custom",
    description: "For institutions",
    features: [
      "Everything in Teacher",
      "Unlimited classes",
      "Admin dashboard",
      "SSO integration",
      "API access",
      "Dedicated support",
      "Custom branding",
    ],
    cta: "Contact Sales",
    highlighted: false,
  },
]

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Simple, Transparent Pricing
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl mx-auto">
              Choose the plan that works best for you. All plans include a 30-day free trial.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {plans.map((plan, index) => (
                <Card
                  key={index}
                  className={`p-8 flex flex-col transition-smooth ${
                    plan.highlighted ? "border-primary/50 shadow-xl scale-105 md:scale-100" : "hover:shadow-lg"
                  }`}
                >
                  {plan.highlighted && (
                    <div className="mb-4 inline-block px-3 py-1 bg-primary/20 text-primary text-sm font-semibold rounded-full w-fit">
                      Most Popular
                    </div>
                  )}

                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <p className="text-foreground/60 mb-6">{plan.description}</p>

                  <div className="mb-6">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    {plan.period && <span className="text-foreground/60">{plan.period}</span>}
                  </div>

                  <Link href="/signup" className="mb-8">
                    <Button
                      className={`w-full ${plan.highlighted ? "bg-gradient-to-r from-primary to-secondary" : ""}`}
                      variant={plan.highlighted ? "default" : "outline"}
                    >
                      {plan.cta}
                    </Button>
                  </Link>

                  <ul className="space-y-3 flex-1">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <CheckCircle2 size={18} className="text-primary flex-shrink-0" />
                        <span className="text-sm text-foreground/80">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {[
                {
                  q: "Can I change plans anytime?",
                  a: "Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.",
                },
                {
                  q: "Is there a free trial?",
                  a: "Yes, all plans include a 30-day free trial. No credit card required to get started.",
                },
                {
                  q: "What payment methods do you accept?",
                  a: "We accept all major credit cards, PayPal, and bank transfers for enterprise plans.",
                },
                {
                  q: "Do you offer discounts for annual billing?",
                  a: "Yes, save 20% when you choose annual billing instead of monthly.",
                },
              ].map((faq, i) => (
                <Card key={i} className="p-6">
                  <h3 className="font-semibold mb-2">{faq.q}</h3>
                  <p className="text-foreground/70 text-sm">{faq.a}</p>
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
