"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockCourses, mockStudents } from "@/lib/mock-data"
import { BookOpen, Flame, Trophy, Zap, ArrowRight } from "lucide-react"
import Link from "next/link"

export default function DashboardPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const student = mockStudents.find((s) => s.id === user.id)
  if (!student) redirect("/login")

  const enrolledCourses = mockCourses.filter((c) => student.enrolledCourses.includes(c.id))
  const totalProgress =
    Object.values(student.progress).reduce((a, b) => a + b, 0) / Object.keys(student.progress).length

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Welcome back, {student.name}!</h1>
              <p className="text-foreground/60">Keep learning and unlock new achievements</p>
            </div>
            <Link href="/dashboard/profile">
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
                <p className="text-sm text-foreground/60 mb-1">Overall Progress</p>
                <p className="text-3xl font-bold text-primary">{Math.round(totalProgress)}%</p>
              </div>
              <BookOpen size={32} className="text-primary/50 group-hover:text-primary transition-smooth" />
            </div>
            <Progress value={totalProgress} className="h-2" />
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20 hover:border-accent/50 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Current Streak</p>
                <p className="text-3xl font-bold text-accent">7 Days</p>
              </div>
              <Flame size={32} className="text-orange-500 group-hover:animate-pulse" />
            </div>
            <p className="text-xs text-foreground/60">+50 XP per day</p>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-950/30 dark:to-orange-950/30 border-yellow-200 dark:border-yellow-800 hover:border-yellow-400 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total XP</p>
                <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">2,450</p>
              </div>
              <Zap size={32} className="text-yellow-500 group-hover:animate-spin-slow" />
            </div>
            <p className="text-xs text-foreground/60">Level 12</p>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 border-purple-200 dark:border-purple-800 hover:border-purple-400 transition-smooth group cursor-pointer">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Achievements</p>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">12</p>
              </div>
              <Trophy size={32} className="text-purple-500 group-hover:scale-110 transition-smooth" />
            </div>
            <p className="text-xs text-foreground/60">Keep going!</p>
          </Card>
        </div>

        {/* Courses Section */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">My Courses</h2>
            <Link href="/dashboard/courses">
              <Button variant="outline" size="sm">
                View All
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {enrolledCourses.map((course) => {
              const progress = student.progress[course.id] || 0
              return (
                <Link key={course.id} href={`/dashboard/courses/${course.id}`}>
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
                          <span className="text-xs font-medium">Progress</span>
                          <span className="text-xs font-bold text-primary">{progress}%</span>
                        </div>
                        <Progress value={progress} className="h-2" />
                      </div>
                      <Button size="sm" className="w-full bg-gradient-to-r from-primary to-secondary">
                        Continue Learning
                        <ArrowRight size={16} className="ml-2" />
                      </Button>
                    </div>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Recommended Section */}
        <div>
          <h2 className="text-2xl font-bold mb-6">Recommended for You</h2>
          <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 text-center">
            <Trophy size={48} className="mx-auto mb-4 text-primary" />
            <h3 className="text-xl font-semibold mb-2">Ready for a new challenge?</h3>
            <p className="text-foreground/60 mb-6">Explore more courses to expand your knowledge</p>
            <Link href="/dashboard/courses">
              <Button className="bg-gradient-to-r from-primary to-secondary">Explore Courses</Button>
            </Link>
          </Card>
        </div>
      </div>
    </div>
  )
}
