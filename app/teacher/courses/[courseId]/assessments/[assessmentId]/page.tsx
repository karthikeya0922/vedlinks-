"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { mockCourses, mockTeachers, mockStudents } from "@/lib/mock-data"
import { ChevronRight, Download, Filter } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function AssessmentResultsPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const assessmentId = params.assessmentId as string

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId && c.teacherId === teacher.id)
  if (!course) redirect("/teacher/dashboard")

  const courseStudents = mockStudents.filter((s) => s.enrolledCourses.includes(courseId))

  const studentResults = courseStudents.map((student) => ({
    id: student.id,
    name: student.name,
    score: Math.round(Math.random() * 40 + 60),
    submittedAt: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000),
    status: Math.random() > 0.3 ? "graded" : "pending",
  }))

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
            <span className="text-foreground/60">Assessment Results</span>
          </div>

          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Variables Quiz - Results</h1>
              <p className="text-foreground/60">12 submissions • Average: 82%</p>
            </div>
            <Button variant="outline">
              <Download size={16} className="mr-2" />
              Export Results
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Filters */}
        <Card className="p-4 mb-8 flex items-center gap-4">
          <Filter size={20} className="text-foreground/60" />
          <input
            type="text"
            placeholder="Search student..."
            className="flex-grow px-3 py-2 bg-muted rounded-lg border border-border focus:border-primary outline-none"
          />
          <select className="px-3 py-2 bg-muted rounded-lg border border-border focus:border-primary outline-none">
            <option>All Status</option>
            <option>Graded</option>
            <option>Pending</option>
          </select>
        </Card>

        {/* Results Table */}
        <Card className="p-8">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-semibold">Student</th>
                  <th className="text-left py-3 px-4 font-semibold">Score</th>
                  <th className="text-left py-3 px-4 font-semibold">Status</th>
                  <th className="text-left py-3 px-4 font-semibold">Submitted</th>
                  <th className="text-left py-3 px-4 font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                {studentResults.map((result) => (
                  <tr key={result.id} className="border-b border-border hover:bg-muted/50 transition-smooth">
                    <td className="py-3 px-4">{result.name}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-primary to-secondary"
                            style={{ width: `${result.score}%` }}
                          />
                        </div>
                        <span className="font-bold text-primary">{result.score}%</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`text-xs font-medium px-2 py-1 rounded-full ${
                          result.status === "graded"
                            ? "bg-green-500/20 text-green-600 dark:text-green-400"
                            : "bg-yellow-500/20 text-yellow-600 dark:text-yellow-400"
                        }`}
                      >
                        {result.status === "graded" ? "Graded" : "Pending"}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm text-foreground/60">{result.submittedAt.toLocaleDateString()}</td>
                    <td className="py-3 px-4">
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
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
