"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { mockParents, mockStudents } from "@/lib/mock-data"
import { BarChart3, TrendingUp, Users, Award } from "lucide-react"
import Link from "next/link"

export default function AnalyticsPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "parent") {
    redirect("/login")
  }

  const parent = mockParents.find((p) => p.id === user.id)
  if (!parent) redirect("/login")

  const children = mockStudents.filter((s) => parent.childrenIds.includes(s.id))

  const totalProgress =
    children.length > 0
      ? Math.round(
          children.reduce((sum, child) => {
            const childAvg =
              Object.values(child.progress).reduce((a, b) => a + b, 0) / Object.keys(child.progress).length
            return sum + childAvg
          }, 0) / children.length,
        )
      : 0

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-4xl font-bold mb-2">Family Analytics</h1>
          <p className="text-foreground/60">Comprehensive overview of your children's learning progress</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Children</p>
                <p className="text-3xl font-bold text-primary">{children.length}</p>
              </div>
              <Users size={32} className="text-primary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Family Progress</p>
                <p className="text-3xl font-bold text-accent">{totalProgress}%</p>
              </div>
              <TrendingUp size={32} className="text-accent/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Active Courses</p>
                <p className="text-3xl font-bold text-secondary">
                  {children.reduce((sum, child) => sum + child.enrolledCourses.length, 0)}
                </p>
              </div>
              <BarChart3 size={32} className="text-secondary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-950/30 dark:to-orange-950/30 border-yellow-200 dark:border-yellow-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Achievements</p>
                <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">12</p>
              </div>
              <Award size={32} className="text-yellow-500" />
            </div>
          </Card>
        </div>

        {/* Comparison Chart */}
        <Card className="p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">Children Comparison</h2>

          <div className="space-y-6">
            {children.map((child) => {
              const childAvg =
                Object.values(child.progress).reduce((a, b) => a + b, 0) / Object.keys(child.progress).length
              return (
                <div key={child.id}>
                  <div className="flex justify-between items-center mb-3">
                    <Link
                      href={`/parent/children/${child.id}`}
                      className="font-semibold hover:text-primary transition-smooth"
                    >
                      {child.name}
                    </Link>
                    <span className="text-sm font-bold text-primary">{Math.round(childAvg)}%</span>
                  </div>
                  <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                      style={{ width: `${childAvg}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </Card>

        {/* Learning Insights */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">Strengths</h2>

            <div className="space-y-4">
              {[
                { subject: "Mathematics", score: 85 },
                { subject: "Science", score: 82 },
                { subject: "Language Arts", score: 88 },
              ].map((item, index) => (
                <div
                  key={index}
                  className="p-4 bg-green-50 dark:bg-green-950/30 rounded-lg border border-green-200 dark:border-green-800"
                >
                  <div className="flex justify-between items-center mb-2">
                    <p className="font-medium">{item.subject}</p>
                    <span className="text-sm font-bold text-green-600 dark:text-green-400">{item.score}%</span>
                  </div>
                  <div className="w-full h-2 bg-green-200 dark:bg-green-800 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500" style={{ width: `${item.score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">Areas for Improvement</h2>

            <div className="space-y-4">
              {[
                { subject: "Advanced Algebra", score: 65 },
                { subject: "Chemistry", score: 58 },
                { subject: "Writing", score: 72 },
              ].map((item, index) => (
                <div
                  key={index}
                  className="p-4 bg-orange-50 dark:bg-orange-950/30 rounded-lg border border-orange-200 dark:border-orange-800"
                >
                  <div className="flex justify-between items-center mb-2">
                    <p className="font-medium">{item.subject}</p>
                    <span className="text-sm font-bold text-orange-600 dark:text-orange-400">{item.score}%</span>
                  </div>
                  <div className="w-full h-2 bg-orange-200 dark:bg-orange-800 rounded-full overflow-hidden">
                    <div className="h-full bg-orange-500" style={{ width: `${item.score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
