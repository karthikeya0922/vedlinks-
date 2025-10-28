"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockTeachers, mockCourses, mockStudents } from "@/lib/mock-data"
import { BookOpen, Users, BarChart3, Plus, ArrowRight, TrendingUp } from "lucide-react"
import Link from "next/link"

export default function TeacherDashboardPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const teacherCourses = mockCourses.filter((c) => c.teacherId === teacher.id)
  const teacherStudents = mockStudents.filter((s) => teacher.students.includes(s.id))

  const totalStudents = teacherStudents.length
  const totalCourses = teacherCourses.length
  const averageProgress =
    teacherStudents.length > 0
      ? Math.round(
          teacherStudents.reduce((sum, s) => {
            const courseProgress = Object.values(s.progress).reduce((a, b) => a + b, 0) / Object.keys(s.progress).length
            return sum + courseProgress
          }, 0) / teacherStudents.length,
        )
      : 0

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Welcome, {teacher.name}!</h1>
              <p className="text-foreground/60">Manage your courses and track student progress</p>
            </div>
            <Link href="/teacher/profile">
              <Button variant="outline">View Profile</Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 hover:border-primary/50 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Courses</p>
                <p className="text-3xl font-bold text-primary">{totalCourses}</p>
              </div>
              <BookOpen size={32} className="text-primary/50 group-hover:text-primary transition-smooth" />
            </div>
            <p className="text-xs text-foreground/60">Active courses</p>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 hover:border-accent/50 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Students</p>
                <p className="text-3xl font-bold text-accent">{totalStudents}</p>
              </div>
              <Users size={32} className="text-accent/50 group-hover:text-accent transition-smooth" />
            </div>
            <p className="text-xs text-foreground/60">Enrolled students</p>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-950/30 dark:to-orange-950/30 border-yellow-200 dark:border-yellow-800 hover:border-yellow-400 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Avg Progress</p>
                <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{averageProgress}%</p>
              </div>
              <TrendingUp size={32} className="text-yellow-500 group-hover:scale-110 transition-smooth" />
            </div>
            <Progress value={averageProgress} className="h-2" />
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 border-purple-200 dark:border-purple-800 hover:border-purple-400 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Completion Rate</p>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">87%</p>
              </div>
              <BarChart3 size={32} className="text-purple-500 group-hover:scale-110 transition-smooth" />
            </div>
            <p className="text-xs text-foreground/60">Lessons completed</p>
          </Card>
        </div>

        {/* Courses Section */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">My Courses</h2>
            <Link href="/teacher/courses/new">
              <Button className="bg-gradient-to-r from-primary to-secondary">
                <Plus size={16} className="mr-2" />
                Create Course
              </Button>
            </Link>
          </div>

          {teacherCourses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {teacherCourses.map((course) => {
                const courseStudents = teacherStudents.filter((s) => s.enrolledCourses.includes(course.id))
                const avgProgress =
                  courseStudents.length > 0
                    ? Math.round(
                        courseStudents.reduce((sum, s) => sum + (s.progress[course.id] || 0), 0) /
                          courseStudents.length,
                      )
                    : 0

                return (
                  <Link key={course.id} href={`/teacher/courses/${course.id}`}>
                    <Card className="p-6 hover:shadow-lg transition-smooth group cursor-pointer h-full flex flex-col">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                            {course.title}
                          </h3>
                          <p className="text-sm text-foreground/60">{course.subject}</p>
                        </div>
                        <BookOpen size={24} className="text-primary/50 group-hover:text-primary transition-smooth" />
                      </div>

                      <p className="text-sm text-foreground/60 mb-4 flex-grow">{course.description}</p>

                      <div className="space-y-3">
                        <div>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-xs font-medium">Class Progress</span>
                            <span className="text-xs font-bold text-primary">{avgProgress}%</span>
                          </div>
                          <Progress value={avgProgress} className="h-2" />
                        </div>
                        <div className="text-xs text-foreground/60">
                          {courseStudents.length} students • {course.lessons.length} lessons
                        </div>
                        <Button size="sm" className="w-full bg-gradient-to-r from-primary to-secondary">
                          Manage
                          <ArrowRight size={16} className="ml-2" />
                        </Button>
                      </div>
                    </Card>
                  </Link>
                )
              })}
            </div>
          ) : (
            <Card className="p-12 text-center">
              <BookOpen size={48} className="mx-auto mb-4 text-foreground/40" />
              <h3 className="text-xl font-semibold mb-2">No courses yet</h3>
              <p className="text-foreground/60 mb-6">Create your first course to get started</p>
              <Link href="/teacher/courses/new">
                <Button className="bg-gradient-to-r from-primary to-secondary">Create Course</Button>
              </Link>
            </Card>
          )}
        </div>

        {/* Recent Activity */}
        <div>
          <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>
          <Card className="p-6">
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between pb-4 border-b border-border last:border-0">
                  <div>
                    <p className="font-medium">Student {i} completed a quiz</p>
                    <p className="text-sm text-foreground/60">2 hours ago</p>
                  </div>
                  <span className="text-sm font-bold text-primary">85%</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
