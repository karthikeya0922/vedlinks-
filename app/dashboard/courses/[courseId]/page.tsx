"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockCourses, mockLessons, mockStudents } from "@/lib/mock-data"
import { CheckCircle, Clock, ArrowRight, ChevronRight } from "lucide-react"
import Link from "next/link"

export default function CourseDetailPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const student = mockStudents.find((s) => s.id === user.id)
  if (!student) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId)
  if (!course) redirect("/dashboard/courses")

  const courseLessons = mockLessons.filter((l) => l.courseId === courseId)
  const progress = student.progress[courseId] || 0

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            href="/dashboard/courses"
            className="text-primary hover:text-secondary transition-smooth mb-4 inline-flex items-center"
          >
            <ChevronRight size={16} className="rotate-180 mr-1" />
            Back to Courses
          </Link>
          <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
          <p className="text-foreground/60">{course.description}</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Progress Card */}
            <Card className="p-6 mb-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-semibold">Course Progress</h3>
                <span className="text-2xl font-bold text-primary">{progress}%</span>
              </div>
              <Progress value={progress} className="h-3" />
              <p className="text-sm text-foreground/60 mt-4">
                {courseLessons.length} lessons • {Math.round((progress / 100) * courseLessons.length)} completed
              </p>
            </Card>

            {/* Lessons List */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold mb-6">Lessons</h2>
              {courseLessons.map((lesson, index) => {
                const isCompleted = Math.random() > 0.5 // Mock completion status
                return (
                  <Link key={lesson.id} href={`/dashboard/courses/${courseId}/lessons/${lesson.id}`}>
                    <Card className="p-6 hover:shadow-lg transition-smooth group cursor-pointer">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-4 flex-grow">
                          <div className="flex-shrink-0 mt-1">
                            {isCompleted ? (
                              <CheckCircle size={24} className="text-green-500" />
                            ) : (
                              <div className="w-6 h-6 rounded-full border-2 border-primary flex items-center justify-center">
                                <span className="text-xs font-bold text-primary">{index + 1}</span>
                              </div>
                            )}
                          </div>
                          <div className="flex-grow">
                            <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                              {lesson.title}
                            </h3>
                            <p className="text-sm text-foreground/60">{lesson.description}</p>
                          </div>
                        </div>
                        <ArrowRight
                          size={20}
                          className="text-foreground/40 group-hover:text-primary transition-smooth flex-shrink-0"
                        />
                      </div>
                    </Card>
                  </Link>
                )
              })}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="p-6 sticky top-20 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
              <h3 className="font-semibold text-lg mb-4">Course Info</h3>

              <div className="space-y-4">
                <div>
                  <p className="text-sm text-foreground/60 mb-1">Subject</p>
                  <p className="font-medium">{course.subject}</p>
                </div>

                <div>
                  <p className="text-sm text-foreground/60 mb-1">Grade Level</p>
                  <p className="font-medium">Grade {course.gradeLevel}</p>
                </div>

                <div>
                  <p className="text-sm text-foreground/60 mb-1">Total Lessons</p>
                  <p className="font-medium">{courseLessons.length} lessons</p>
                </div>

                <div className="pt-4 border-t border-border">
                  <p className="text-sm text-foreground/60 mb-3">Estimated Time</p>
                  <div className="flex items-center gap-2 text-sm">
                    <Clock size={16} className="text-accent" />
                    <span>{courseLessons.length * 30} minutes</span>
                  </div>
                </div>

                <Button className="w-full bg-gradient-to-r from-primary to-secondary mt-6">Continue Learning</Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
