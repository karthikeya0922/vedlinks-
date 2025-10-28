"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { mockCourses, mockTeachers, mockStudents } from "@/lib/mock-data"
import { ChevronRight, Save, Calendar } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function AttendancePage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const [attendance, setAttendance] = useState<Record<string, boolean>>({})

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId && c.teacherId === teacher.id)
  if (!course) redirect("/teacher/dashboard")

  const courseStudents = mockStudents.filter((s) => s.enrolledCourses.includes(courseId))

  const toggleAttendance = (studentId: string) => {
    setAttendance({
      ...attendance,
      [studentId]: !attendance[studentId],
    })
  }

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
            <span className="text-foreground/60">Attendance</span>
          </div>

          <h1 className="text-4xl font-bold mb-2">Mark Attendance</h1>
          <p className="text-foreground/60">Record attendance for today's class</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Card className="p-8">
          <div className="flex items-center gap-2 mb-6">
            <Calendar size={20} className="text-primary" />
            <p className="text-lg font-semibold">{new Date().toLocaleDateString()}</p>
          </div>

          <div className="space-y-3 mb-8">
            {courseStudents.map((student) => (
              <div
                key={student.id}
                className="flex items-center justify-between p-4 border border-border rounded-lg hover:border-primary/50 transition-smooth"
              >
                <div className="flex items-center gap-4 flex-grow">
                  <Checkbox
                    checked={attendance[student.id] || false}
                    onCheckedChange={() => toggleAttendance(student.id)}
                  />
                  <div>
                    <p className="font-medium">{student.name}</p>
                    <p className="text-sm text-foreground/60">Grade {student.gradeLevel}</p>
                  </div>
                </div>
                <span
                  className={`text-sm font-medium ${attendance[student.id] ? "text-green-500" : "text-foreground/40"}`}
                >
                  {attendance[student.id] ? "Present" : "Absent"}
                </span>
              </div>
            ))}
          </div>

          <div className="flex gap-4">
            <Button className="flex-1 bg-gradient-to-r from-primary to-secondary">
              <Save size={16} className="mr-2" />
              Save Attendance
            </Button>
            <Link href={`/teacher/courses/${courseId}`} className="flex-1">
              <Button variant="outline" className="w-full bg-transparent">
                Cancel
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    </div>
  )
}
