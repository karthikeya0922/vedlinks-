"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                About LearnAI
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl">
              Transforming education through artificial intelligence and personalized learning experiences.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="prose prose-lg max-w-none">
              <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
              <p className="text-foreground/70 mb-8 leading-relaxed">
                At LearnAI, we believe that every student deserves a personalized learning experience. Our mission is to
                democratize quality education by leveraging artificial intelligence to create adaptive, engaging, and
                effective learning environments for students, teachers, and parents worldwide.
              </p>

              <h2 className="text-3xl font-bold mb-6 mt-12">Our Story</h2>
              <p className="text-foreground/70 mb-8 leading-relaxed">
                Founded in 2024, LearnAI was born from a simple observation: traditional education systems treat all
                students the same, despite their unique learning styles and paces. We recognized that AI could
                revolutionize this by creating truly personalized learning experiences.
              </p>

              <h2 className="text-3xl font-bold mb-6 mt-12">Our Values</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-8">
                {[
                  {
                    title: "Personalization",
                    description: "Every student learns differently. We adapt to individual needs.",
                  },
                  {
                    title: "Innovation",
                    description: "We continuously push the boundaries of what's possible in education.",
                  },
                  {
                    title: "Accessibility",
                    description: "Quality education should be available to everyone, everywhere.",
                  },
                ].map((value, i) => (
                  <Card key={i} className="p-6">
                    <h3 className="font-bold mb-2">{value.title}</h3>
                    <p className="text-foreground/70 text-sm">{value.description}</p>
                  </Card>
                ))}
              </div>

              <h2 className="text-3xl font-bold mb-6 mt-12">Our Team</h2>
              <p className="text-foreground/70 mb-8 leading-relaxed">
                Our team consists of educators, engineers, and AI researchers passionate about transforming education.
                We bring together decades of experience in education technology, machine learning, and pedagogy.
              </p>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
