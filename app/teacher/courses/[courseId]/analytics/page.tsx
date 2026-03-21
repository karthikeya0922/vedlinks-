"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { mockCourses, mockTeachers, mockStudents } from "@/lib/mock-data"
import { ChevronRight, BarChart3, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function AnalyticsPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId && c.teacherId === teacher.id)
  if (!course) redirect("/teacher/dashboard")

  const courseStudents = mockStudents.filter((s) => s.enrolledCourses.includes(courseId))

  const topicPerformance = [
    { topic: "Variables", avgScore: 85, students: 12 },
    { topic: "Linear Equations", avgScore: 78, students: 12 },
    { topic: "Systems of Equations", avgScore: 72, students: 10 },
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center gap-2 mb-4">
            <Link href={`/teacher/courses/${courseId}`} className="text-primary hover:text-secondary transition-smooth">
              {course.title}
            </Link>
            <ChevronRight size={16} className="text-foreground/40" />
            <span className="text-foreground/60">Analytics</span>
          </div>

          <h1 className="text-4xl font-bold mb-2">Course Analytics</h1>
          <p className="text-foreground/60">Track student performance and identify improvement areas</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Students</p>
                <p className="text-3xl font-bold text-primary">{courseStudents.length}</p>
              </div>
              <BarChart3 size={32} className="text-primary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Avg Class Progress</p>
                <p className="text-3xl font-bold text-accent">
                  {courseStudents.length > 0
                    ? Math.round(
                        courseStudents.reduce((sum, s) => sum + (s.progress[courseId] || 0), 0) / courseStudents.length,
                      )
                    : 0}
                  %
                </p>
              </div>
              <TrendingUp size={32} className="text-accent/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Completion Rate</p>
                <p className="text-3xl font-bold text-secondary">87%</p>
              </div>
              <BarChart3 size={32} className="text-secondary/50" />
            </div>
          </Card>
        </div>

        {/* Topic Performance */}
        <Card className="p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">Performance by Topic</h2>
          <div className="space-y-4">
            {topicPerformance.map((topic, index) => (
              <div key={index} className="p-4 border border-border rounded-lg">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-semibold">{topic.topic}</h3>
                  <span className="text-sm font-bold text-primary">{topic.avgScore}%</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                    style={{ width: `${topic.avgScore}%` }}
                  />
                </div>
                <p className="text-xs text-foreground/60 mt-2">{topic.students} students assessed</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Student Performance Table */}
        <Card className="p-8">
          <h2 className="text-2xl font-bold mb-6">Student Performance</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-semibold">Student</th>
                  <th className="text-left py-3 px-4 font-semibold">Progress</th>
                  <th className="text-left py-3 px-4 font-semibold">Avg Score</th>
                  <th className="text-left py-3 px-4 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                {courseStudents.map((student) => (
                  <tr key={student.id} className="border-b border-border hover:bg-muted/50 transition-smooth">
                    <td className="py-3 px-4">{student.name}</td>
                    <td className="py-3 px-4">
                      <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-primary to-secondary"
                          style={{ width: `${student.progress[courseId] || 0}%` }}
                        />
                      </div>
                    </td>
                    <td className="py-3 px-4 font-medium">{student.progress[courseId] || 0}%</td>
                    <td className="py-3 px-4">
                      <span
                        className={`text-xs font-medium px-2 py-1 rounded-full ${
                          (student.progress[courseId] || 0) >= 70
                            ? "bg-green-500/20 text-green-600 dark:text-green-400"
                            : "bg-yellow-500/20 text-yellow-600 dark:text-yellow-400"
                        }`}
                      >
                        {(student.progress[courseId] || 0) >= 70 ? "On Track" : "Needs Help"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}
