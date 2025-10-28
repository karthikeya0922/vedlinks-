"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { mockCourses, mockStudents } from "@/lib/mock-data"
import { BookOpen, ArrowRight, Search } from "lucide-react"
import Link from "next/link"
import { useState } from "react"
import { Input } from "@/components/ui/input"

export default function CoursesPage() {
  const { user, isAuthenticated } = useAuth()
  const [searchTerm, setSearchTerm] = useState("")

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const student = mockStudents.find((s) => s.id === user.id)
  if (!student) redirect("/login")

  const filteredCourses = mockCourses.filter(
    (course) =>
      course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.subject.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const enrolledCourses = filteredCourses.filter((c) => student.enrolledCourses.includes(c.id))
  const availableCourses = filteredCourses.filter((c) => !student.enrolledCourses.includes(c.id))

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-4xl font-bold mb-4">Courses</h1>
          <p className="text-foreground/60 mb-6">Browse and enroll in courses to expand your knowledge</p>

          <div className="relative">
            <Search className="absolute left-3 top-3 text-foreground/40" size={20} />
            <Input
              placeholder="Search courses..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Enrolled Courses */}
        {enrolledCourses.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6">My Courses</h2>
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
                          Continue
                          <ArrowRight size={16} className="ml-2" />
                        </Button>
                      </div>
                    </Card>
                  </Link>
                )
              })}
            </div>
          </div>
        )}

        {/* Available Courses */}
        {availableCourses.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Available Courses</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {availableCourses.map((course) => (
                <Card
                  key={course.id}
                  className="p-6 hover:shadow-lg transition-smooth group cursor-pointer h-full flex flex-col"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                        {course.title}
                      </h3>
                      <p className="text-sm text-foreground/60">{course.subject}</p>
                    </div>
                    <BookOpen size={24} className="text-secondary/50 group-hover:text-secondary transition-smooth" />
                  </div>

                  <p className="text-sm text-foreground/60 mb-4 flex-grow">{course.description}</p>

                  <div className="space-y-3">
                    <p className="text-xs text-foreground/60">Grade Level: {course.gradeLevel}</p>
                    <Button size="sm" className="w-full bg-gradient-to-r from-secondary to-accent">
                      Enroll Now
                      <ArrowRight size={16} className="ml-2" />
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {filteredCourses.length === 0 && (
          <Card className="p-12 text-center">
            <BookOpen size={48} className="mx-auto mb-4 text-foreground/40" />
            <h3 className="text-xl font-semibold mb-2">No courses found</h3>
            <p className="text-foreground/60">Try adjusting your search terms</p>
          </Card>
        )}
      </div>
    </div>
  )
}
