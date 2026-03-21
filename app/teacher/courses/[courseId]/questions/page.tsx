"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockCourses, mockTeachers } from "@/lib/mock-data"
import { ChevronRight, Plus } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function QuestionsPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const [questions, setQuestions] = useState([
    {
      id: "q-1",
      text: "What is a variable?",
      type: "multiple-choice",
      difficulty: "easy",
      topic: "Variables",
    },
    {
      id: "q-2",
      text: "Solve: 2x + 5 = 13",
      type: "multiple-choice",
      difficulty: "medium",
      topic: "Linear Equations",
    },
  ])

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const course = mockCourses.find((c) => c.id === courseId && c.teacherId === teacher.id)
  if (!course) redirect("/teacher/dashboard")

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
            <span className="text-foreground/60">Questions</span>
          </div>

          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Question Bank</h1>
              <p className="text-foreground/60">Create and manage custom questions for your course</p>
            </div>
            <Link href={`/teacher/courses/${courseId}/questions/new`}>
              <Button className="bg-gradient-to-r from-primary to-secondary">
                <Plus size={16} className="mr-2" />
                Create Question
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-4">
          {questions.map((question) => (
            <Card key={question.id} className="p-6 hover:shadow-lg transition-smooth group cursor-pointer">
              <div className="flex items-start justify-between">
                <div className="flex-grow">
                  <h3 className="font-semibold text-lg mb-2 group-hover:text-primary transition-smooth">
                    {question.text}
                  </h3>
                  <div className="flex items-center gap-4">
                    <span className="text-xs font-medium px-2 py-1 bg-primary/20 rounded-full text-primary">
                      {question.type}
                    </span>
                    <span className="text-xs font-medium px-2 py-1 bg-accent/20 rounded-full text-accent">
                      {question.difficulty}
                    </span>
                    <span className="text-xs text-foreground/60">{question.topic}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                  <Button variant="destructive" size="sm">
                    Delete
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
