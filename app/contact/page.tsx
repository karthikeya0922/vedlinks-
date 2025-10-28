"use client"

import type React from "react"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Mail, Phone, MapPin } from "lucide-react"
import { useState } from "react"

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Form submitted:", formData)
    setFormData({ name: "", email: "", subject: "", message: "" })
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20">
        <section className="py-20 bg-gradient-to-br from-primary/10 to-secondary/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Get in Touch
              </span>
            </h1>
            <p className="text-xl text-foreground/60 max-w-2xl mx-auto">
              Have questions? We'd love to hear from you. Send us a message and we'll respond as soon as possible.
            </p>
          </div>
        </section>

        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
              {[
                {
                  icon: Mail,
                  title: "Email",
                  value: "support@learnai.com",
                  color: "from-primary to-secondary",
                },
                {
                  icon: Phone,
                  title: "Phone",
                  value: "+1 (555) 123-4567",
                  color: "from-secondary to-accent",
                },
                {
                  icon: MapPin,
                  title: "Address",
                  value: "San Francisco, CA",
                  color: "from-accent to-primary",
                },
              ].map((contact, i) => {
                const Icon = contact.icon
                return (
                  <Card key={i} className="p-6 text-center hover:shadow-lg transition-smooth">
                    <div
                      className={`w-12 h-12 bg-gradient-to-br ${contact.color} rounded-lg flex items-center justify-center mx-auto mb-4`}
                    >
                      <Icon size={24} className="text-white" />
                    </div>
                    <h3 className="font-semibold mb-2">{contact.title}</h3>
                    <p className="text-foreground/70">{contact.value}</p>
                  </Card>
                )
              })}
            </div>

            <Card className="p-8 max-w-2xl mx-auto">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Subject</label>
                  <input
                    type="text"
                    value={formData.subject}
                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Message</label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    rows={5}
                    className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth resize-none"
                    required
                  />
                </div>

                <Button type="submit" className="w-full bg-gradient-to-r from-primary to-secondary">
                  Send Message
                </Button>
              </form>
            </Card>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
