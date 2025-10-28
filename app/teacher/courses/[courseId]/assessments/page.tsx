"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockCourses, mockTeachers, mockStudents } from "@/lib/mock-data"
import { ChevronRight, Plus, BarChart3, Users } from "lucide-react"
import Link from "next/link"
import { calculateClassStatistics } from "@/lib/grading-system"

export default function AssessmentsPage() {
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
  const mockScores = courseStudents.map((s) => s.progress[courseId] || 0)
  const classStats = calculateClassStatistics(mockScores)

  const assessments = [
    {
      id: "a-1",
      title: "Variables Quiz",
      type: "quiz",
      questions: 5,
      submissions: 12,
      averageScore: 82,
      dueDate: "2024-02-15",
    },
    {
      id: "a-2",
      title: "Linear Equations Test",
      type: "test",
      questions: 10,
      submissions: 10,
      averageScore: 75,
      dueDate: "2024-02-20",
    },
    {
      id: "a-3",
      title: "Problem Set 1",
      type: "assignment",
      questions: 8,
      submissions: 8,
      averageScore: 88,
      dueDate: "2024-02-25",
    },
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
            <span className="text-foreground/60">Assessments</span>
          </div>

          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Assessments</h1>
              <p className="text-foreground/60">Create and manage course assessments</p>
            </div>
            <Link href={`/teacher/courses/${courseId}/assessments/new`}>
              <Button className="bg-gradient-to-r from-primary to-secondary">
                <Plus size={16} className="mr-2" />
                Create Assessment
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Class Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Average Score</p>
                <p className="text-3xl font-bold text-primary">{classStats.averageScore}%</p>
              </div>
              <BarChart3 size={32} className="text-primary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Pass Rate</p>
                <p className="text-3xl font-bold text-accent">{classStats.passRate}%</p>
              </div>
              <Users size={32} className="text-accent/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-200 dark:border-green-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Highest Score</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{classStats.highestScore}%</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-950/30 dark:to-red-950/30 border-orange-200 dark:border-orange-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Lowest Score</p>
                <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">{classStats.lowestScore}%</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Score Distribution */}
        <Card className="p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">Score Distribution</h2>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {Object.entries(classStats.distribution).map(([range, count]) => (
              <div key={range} className="text-center p-4 bg-muted rounded-lg">
                <p className="text-sm text-foreground/60 mb-2">{range}</p>
                <p className="text-3xl font-bold text-primary">{count}</p>
                <p className="text-xs text-foreground/60 mt-2">
                  {courseStudents.length > 0 ? Math.round((count / courseStudents.length) * 100) : 0}%
                </p>
              </div>
            ))}
          </div>
        </Card>

        {/* Assessments List */}
        <div>
          <h2 className="text-2xl font-bold mb-6">All Assessments</h2>

          <div className="space-y-4">
            {assessments.map((assessment) => (
              <Link key={assessment.id} href={`/teacher/courses/${courseId}/assessments/${assessment.id}`}>
                <Card className="p-6 hover:shadow-lg transition-smooth group cursor-pointer">
                  <div className="flex items-start justify-between">
                    <div className="flex-grow">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-semibold text-lg group-hover:text-primary transition-smooth">
                          {assessment.title}
                        </h3>
                        <span className="text-xs font-medium px-2 py-1 bg-primary/20 rounded-full text-primary">
                          {assessment.type}
                        </span>
                      </div>

                      <div className="flex items-center gap-6 text-sm text-foreground/60">
                        <span>{assessment.questions} questions</span>
                        <span>{assessment.submissions} submissions</span>
                        <span>Avg: {assessment.averageScore}%</span>
                        <span>Due: {assessment.dueDate}</span>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        View Results
                      </Button>
                      <Button variant="outline" size="sm">
                        Edit
                      </Button>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
