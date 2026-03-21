"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockTeachers, mockStudents } from "@/lib/mock-data"
import { BarChart3, TrendingUp, Users, Activity, Download, Calendar } from "lucide-react"
import {
  calculateAnalyticsMetrics,
  generatePerformanceTrends,
  identifyTopPerformers,
  identifyStudentsNeedingSupport,
  generateRecommendations,
} from "@/lib/analytics-engine"

export default function TeacherAnalyticsPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const teacherStudents = mockStudents.filter((s) => teacher.students.includes(s.id))
  const activeStudentIds = teacherStudents.slice(0, Math.ceil(teacherStudents.length * 0.8)).map((s) => s.id)

  const metrics = calculateAnalyticsMetrics(teacherStudents, activeStudentIds)
  const trends = generatePerformanceTrends(30)
  const topPerformers = identifyTopPerformers(teacherStudents)
  const needsSupport = identifyStudentsNeedingSupport(teacherStudents)
  const recommendations = generateRecommendations(metrics)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Analytics Dashboard</h1>
              <p className="text-foreground/60">Real-time insights into student learning and engagement</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline">
                <Calendar size={16} className="mr-2" />
                Last 30 Days
              </Button>
              <Button className="bg-gradient-to-r from-primary to-secondary">
                <Download size={16} className="mr-2" />
                Export Report
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Students</p>
                <p className="text-3xl font-bold text-primary">{metrics.totalStudents}</p>
              </div>
              <Users size={32} className="text-primary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Active Now</p>
                <p className="text-3xl font-bold text-accent">{metrics.activeStudents}</p>
              </div>
              <Activity size={32} className="text-accent/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-200 dark:border-green-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Avg Progress</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{metrics.averageProgress}%</p>
              </div>
              <TrendingUp size={32} className="text-green-500" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30 border-blue-200 dark:border-blue-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Completion</p>
                <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{metrics.completionRate}%</p>
              </div>
              <BarChart3 size={32} className="text-blue-500" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 border-purple-200 dark:border-purple-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Engagement</p>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">{metrics.engagementScore}%</p>
              </div>
              <Activity size={32} className="text-purple-500" />
            </div>
          </Card>
        </div>

        {/* Performance Trend Chart */}
        <Card className="p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">Performance Trend (Last 30 Days)</h2>

          <div className="space-y-6">
            {trends.slice(-7).map((trend, index) => (
              <div key={index}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">{trend.date}</span>
                  <span className="text-sm font-bold text-primary">{trend.averageScore}%</span>
                </div>
                <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                    style={{ width: `${trend.averageScore}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Top Performers */}
          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">Top Performers</h2>

            <div className="space-y-4">
              {topPerformers.map((performer, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-green-50 dark:bg-green-950/30 rounded-lg border border-green-200 dark:border-green-800"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold text-sm">
                      {index + 1}
                    </div>
                    <span className="font-medium">{performer.name}</span>
                  </div>
                  <span className="font-bold text-green-600 dark:text-green-400">{performer.score}%</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Students Needing Support */}
          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">Students Needing Support</h2>

            <div className="space-y-4">
              {needsSupport.map((student, index) => (
                <div
                  key={index}
                  className="p-4 bg-orange-50 dark:bg-orange-950/30 rounded-lg border border-orange-200 dark:border-orange-800"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-medium">{student.name}</span>
                    <span className="font-bold text-orange-600 dark:text-orange-400">{student.score}%</span>
                  </div>
                  <p className="text-xs text-foreground/60">{student.reason}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Recommendations */}
        <Card className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
          <h2 className="text-2xl font-bold mb-6">Recommendations</h2>

          <div className="space-y-3">
            {recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-background rounded-lg border border-border">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-accent flex items-center justify-center text-white text-sm font-bold">
                  {index + 1}
                </div>
                <p className="text-foreground/80 pt-0.5">{rec}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
