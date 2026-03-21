"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockCourses, mockLessons, mockTeachers, mockStudents } from "@/lib/mock-data"
import { ChevronRight, Plus, Users, BookOpen, BarChart3, Edit } from "lucide-react"
import Link from "next/link"

export default function CourseManagementPage() {
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

  const courseLessons = mockLessons.filter((l) => l.courseId === courseId)
  const courseStudents = mockStudents.filter((s) => s.enrolledCourses.includes(courseId))

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            href="/teacher/dashboard"
            className="text-primary hover:text-secondary transition-smooth mb-4 inline-flex items-center"
          >
            <ChevronRight size={16} className="rotate-180 mr-1" />
            Back to Dashboard
          </Link>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
              <p className="text-foreground/60">{course.description}</p>
            </div>
            <Link href={`/teacher/courses/${courseId}/edit`}>
              <Button variant="outline">
                <Edit size={16} className="mr-2" />
                Edit Course
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Lessons Section */}
            <div className="mb-12">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Lessons</h2>
                <Link href={`/teacher/courses/${courseId}/lessons/new`}>
                  <Button size="sm" className="bg-gradient-to-r from-primary to-secondary">
                    <Plus size={16} className="mr-2" />
                    Add Lesson
                  </Button>
                </Link>
              </div>

              <div className="space-y-4">
                {courseLessons.map((lesson, index) => (
                  <Link key={lesson.id} href={`/teacher/courses/${courseId}/lessons/${lesson.id}`}>
                    <Card className="p-6 hover:shadow-lg transition-smooth group cursor-pointer">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-4 flex-grow">
                          <div className="flex-shrink-0 mt-1">
                            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                              <span className="text-sm font-bold text-primary">{index + 1}</span>
                            </div>
                          </div>
                          <div className="flex-grow">
                            <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                              {lesson.title}
                            </h3>
                            <p className="text-sm text-foreground/60">{lesson.description}</p>
                          </div>
                        </div>
                        <ChevronRight
                          size={20}
                          className="text-foreground/40 group-hover:text-primary transition-smooth flex-shrink-0"
                        />
                      </div>
                    </Card>
                  </Link>
                ))}
              </div>
            </div>

            {/* Student Performance */}
            <div>
              <h2 className="text-2xl font-bold mb-6">Student Performance</h2>
              <Card className="p-6">
                <div className="space-y-4">
                  {courseStudents.slice(0, 5).map((student) => (
                    <div
                      key={student.id}
                      className="flex items-center justify-between pb-4 border-b border-border last:border-0"
                    >
                      <div className="flex-grow">
                        <p className="font-medium">{student.name}</p>
                        <p className="text-sm text-foreground/60">Grade {student.gradeLevel}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="w-32">
                          <Progress value={student.progress[courseId] || 0} className="h-2" />
                        </div>
                        <span className="text-sm font-bold text-primary min-w-12 text-right">
                          {student.progress[courseId] || 0}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Course Stats */}
            <Card className="p-6 sticky top-20 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 mb-6">
              <h3 className="font-semibold text-lg mb-6">Course Stats</h3>

              <div className="space-y-6">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <BookOpen size={16} className="text-primary" />
                    <p className="text-sm text-foreground/60">Total Lessons</p>
                  </div>
                  <p className="text-3xl font-bold text-primary">{courseLessons.length}</p>
                </div>

                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Users size={16} className="text-accent" />
                    <p className="text-sm text-foreground/60">Enrolled Students</p>
                  </div>
                  <p className="text-3xl font-bold text-accent">{courseStudents.length}</p>
                </div>

                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <BarChart3 size={16} className="text-secondary" />
                    <p className="text-sm text-foreground/60">Avg Progress</p>
                  </div>
                  <p className="text-3xl font-bold text-secondary">
                    {courseStudents.length > 0
                      ? Math.round(
                          courseStudents.reduce((sum, s) => sum + (s.progress[courseId] || 0), 0) /
                            courseStudents.length,
                        )
                      : 0}
                    %
                  </p>
                </div>
              </div>
            </Card>

            {/* Quick Actions */}
            <Card className="p-6">
              <h3 className="font-semibold text-lg mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Link href={`/teacher/courses/${courseId}/attendance`} className="block">
                  <Button variant="outline" className="w-full bg-transparent justify-start">
                    <Plus size={16} className="mr-2" />
                    Mark Attendance
                  </Button>
                </Link>
                <Link href={`/teacher/courses/${courseId}/analytics`} className="block">
                  <Button variant="outline" className="w-full bg-transparent justify-start">
                    <BarChart3 size={16} className="mr-2" />
                    View Analytics
                  </Button>
                </Link>
                <Link href={`/teacher/courses/${courseId}/questions`} className="block">
                  <Button variant="outline" className="w-full bg-transparent justify-start">
                    <Plus size={16} className="mr-2" />
                    Create Questions
                  </Button>
                </Link>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
