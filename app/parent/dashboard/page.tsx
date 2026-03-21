"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockParents, mockStudents, mockCourses } from "@/lib/mock-data"
import { Users, TrendingUp, AlertCircle, Award, Zap } from "lucide-react"
import Link from "next/link"

export default function ParentDashboardPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "parent") {
    redirect("/login")
  }

  const parent = mockParents.find((p) => p.id === user.id)
  if (!parent) redirect("/login")

  const children = mockStudents.filter((s) => parent.childrenIds.includes(s.id))

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Welcome, {parent.name}!</h1>
              <p className="text-foreground/60">Monitor your children's learning progress and achievements</p>
            </div>
            <Link href="/parent/profile">
              <Button variant="outline">View Profile</Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Children Overview */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Your Children</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {children.map((child) => {
              const childCourses = mockCourses.filter((c) => child.enrolledCourses.includes(c.id))
              const avgProgress =
                Object.values(child.progress).reduce((a, b) => a + b, 0) / Object.keys(child.progress).length

              return (
                <Link key={child.id} href={`/parent/children/${child.id}`}>
                  <Card className="p-6 hover:shadow-lg transition-smooth group cursor-pointer h-full flex flex-col">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                          {child.name}
                        </h3>
                        <p className="text-sm text-foreground/60">Grade {child.gradeLevel}</p>
                      </div>
                      <Users size={24} className="text-primary/50 group-hover:text-primary transition-smooth" />
                    </div>

                    <div className="space-y-4 flex-grow">
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs font-medium">Overall Progress</span>
                          <span className="text-xs font-bold text-primary">{Math.round(avgProgress)}%</span>
                        </div>
                        <Progress value={avgProgress} className="h-2" />
                      </div>

                      <div className="text-sm text-foreground/60">
                        {childCourses.length} courses • {Object.keys(child.progress).length} active
                      </div>
                    </div>

                    <Button size="sm" className="w-full bg-gradient-to-r from-primary to-secondary mt-4">
                      View Details
                    </Button>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Quick Insights */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-200 dark:border-green-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Achievements Unlocked</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">12</p>
              </div>
              <Award size={32} className="text-green-500" />
            </div>
            <p className="text-xs text-foreground/60">Across all children</p>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30 border-blue-200 dark:border-blue-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Learning Streak</p>
                <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">7 Days</p>
              </div>
              <Zap size={32} className="text-blue-500" />
            </div>
            <p className="text-xs text-foreground/60">Keep it going!</p>
          </Card>
        </div>

        {/* Recommendations */}
        <div>
          <h2 className="text-2xl font-bold mb-6">Recommendations</h2>

          <div className="space-y-4">
            {[
              {
                title: "Focus on Algebra",
                description: "John is struggling with linear equations. Consider scheduling extra study time.",
                icon: AlertCircle,
                color: "from-orange-50 to-red-50 dark:from-orange-950/30 dark:to-red-950/30",
                borderColor: "border-orange-200 dark:border-orange-800",
              },
              {
                title: "Celebrate Progress",
                description: "Jane has completed 85% of her Biology course! Encourage her to finish strong.",
                icon: Award,
                color: "from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30",
                borderColor: "border-green-200 dark:border-green-800",
              },
              {
                title: "Consistent Learning",
                description:
                  "Both children are maintaining a 7-day learning streak. Great job supporting their education!",
                icon: TrendingUp,
                color: "from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30",
                borderColor: "border-blue-200 dark:border-blue-800",
              },
            ].map((rec, index) => {
              const Icon = rec.icon
              return (
                <Card key={index} className={`p-6 bg-gradient-to-br ${rec.color} ${rec.borderColor}`}>
                  <div className="flex items-start gap-4">
                    <Icon size={24} className="text-foreground/60 flex-shrink-0 mt-1" />
                    <div className="flex-grow">
                      <h3 className="font-semibold mb-1">{rec.title}</h3>
                      <p className="text-sm text-foreground/60">{rec.description}</p>
                    </div>
                  </div>
                </Card>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
