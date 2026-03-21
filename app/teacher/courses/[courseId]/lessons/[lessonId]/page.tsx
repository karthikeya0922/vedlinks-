"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockLessons, mockCourses, mockTeachers } from "@/lib/mock-data"
import { ChevronRight, Edit, Trash2, Plus } from "lucide-react"
import Link from "next/link"

export default function LessonManagementPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const lessonId = params.lessonId as string

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId && c.teacherId === teacher.id)
  if (!course) redirect("/teacher/dashboard")

  const lesson = mockLessons.find((l) => l.id === lessonId && l.courseId === courseId)
  if (!lesson) redirect(`/teacher/courses/${courseId}`)

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
            <span className="text-foreground/60">{lesson.title}</span>
          </div>

          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">{lesson.title}</h1>
              <p className="text-foreground/60">{lesson.description}</p>
            </div>
            <div className="flex gap-2">
              <Link href={`/teacher/courses/${courseId}/lessons/${lessonId}/edit`}>
                <Button variant="outline">
                  <Edit size={16} className="mr-2" />
                  Edit
                </Button>
              </Link>
              <Button variant="destructive">
                <Trash2 size={16} className="mr-2" />
                Delete
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Lesson Content */}
            <Card className="p-8 mb-8 bg-gradient-to-br from-primary/5 to-secondary/5 border-primary/20">
              <h2 className="text-2xl font-bold mb-6">Lesson Content</h2>
              <div className="bg-background rounded-lg p-6 border border-border">
                <p className="text-foreground/80 leading-relaxed">{lesson.content}</p>
              </div>
            </Card>

            {/* Assessment Section */}
            <Card className="p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Assessments</h2>
                <Link href={`/teacher/courses/${courseId}/lessons/${lessonId}/assessments/new`}>
                  <Button size="sm" className="bg-gradient-to-r from-primary to-secondary">
                    <Plus size={16} className="mr-2" />
                    Add Assessment
                  </Button>
                </Link>
              </div>

              <div className="space-y-4">
                {[1, 2].map((i) => (
                  <div
                    key={i}
                    className="p-4 border border-border rounded-lg hover:border-primary/50 transition-smooth"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold">Quiz {i}</h3>
                        <p className="text-sm text-foreground/60">5 questions • Multiple choice</p>
                      </div>
                      <Button variant="outline" size="sm">
                        Edit
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="p-6 sticky top-20">
              <h3 className="font-semibold text-lg mb-6">Lesson Info</h3>

              <div className="space-y-6">
                <div>
                  <p className="text-sm text-foreground/60 mb-1">Order</p>
                  <p className="font-medium">Lesson {lesson.order}</p>
                </div>

                <div>
                  <p className="text-sm text-foreground/60 mb-1">Created</p>
                  <p className="font-medium">{lesson.createdAt.toLocaleDateString()}</p>
                </div>

                <div>
                  <p className="text-sm text-foreground/60 mb-1">Estimated Duration</p>
                  <p className="font-medium">30 minutes</p>
                </div>

                <div className="pt-4 border-t border-border">
                  <p className="text-sm text-foreground/60 mb-3">Student Engagement</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Completed</span>
                      <span className="font-bold">87%</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Avg Score</span>
                      <span className="font-bold">82%</span>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
