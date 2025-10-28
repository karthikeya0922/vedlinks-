"use client"

import type React from "react"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import Link from "next/link"

export default function SignupPage() {
  const [userType, setUserType] = useState<"student" | "teacher" | "parent">("student")
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Signup:", { userType, ...formData })
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20 pb-20">
        <div className="max-w-md mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="p-8">
            <h1 className="text-3xl font-bold mb-2 text-center">Create Account</h1>
            <p className="text-foreground/60 text-center mb-8">Join LearnAI and start learning today</p>

            <div className="grid grid-cols-3 gap-2 mb-8">
              {(["student", "teacher", "parent"] as const).map((type) => (
                <button
                  key={type}
                  onClick={() => setUserType(type)}
                  className={`py-2 px-3 rounded-lg text-sm font-medium transition-smooth capitalize ${
                    userType === type
                      ? "bg-gradient-to-r from-primary to-secondary text-white"
                      : "bg-muted text-foreground/70 hover:bg-muted/80"
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">Full Name</label>
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
                <label className="block text-sm font-medium mb-2">Password</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Confirm Password</label>
                <input
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary transition-smooth"
                  required
                />
              </div>

              <Button type="submit" className="w-full bg-gradient-to-r from-primary to-secondary">
                Create Account
              </Button>
            </form>

            <p className="text-center text-foreground/60 mt-6">
              Already have an account?{" "}
              <Link href="/login" className="text-primary font-semibold hover:underline">
                Sign in
              </Link>
            </p>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  )
}
