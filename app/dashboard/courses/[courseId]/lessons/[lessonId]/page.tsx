"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockCourses, mockLessons, mockAssessments } from "@/lib/mock-data"
import { ChevronRight, CheckCircle, BookOpen, Zap, Brain } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function LessonPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const lessonId = params.lessonId as string
  const [isCompleted, setIsCompleted] = useState(false)

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const course = mockCourses.find((c) => c.id === courseId)
  const lesson = mockLessons.find((l) => l.id === lessonId)
  const assessment = mockAssessments.find((a) => a.lessonId === lessonId)

  if (!course || !lesson) redirect("/dashboard/courses")

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Link
                href={`/dashboard/courses/${courseId}`}
                className="text-primary hover:text-secondary transition-smooth"
              >
                {course.title}
              </Link>
              <ChevronRight size={16} className="text-foreground/40" />
              <span className="text-foreground/60">{lesson.title}</span>
            </div>
            <Link href={`/dashboard/courses/${courseId}`}>
              <Button variant="outline" size="sm">
                Back
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Lesson Content */}
        <Card className="p-8 mb-8 bg-gradient-to-br from-primary/5 to-secondary/5 border-primary/20">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold mb-2">{lesson.title}</h1>
              <p className="text-foreground/60">{lesson.description}</p>
            </div>
            <BookOpen size={40} className="text-primary/50" />
          </div>

          <div className="prose prose-invert max-w-none">
            <div className="bg-background rounded-lg p-6 border border-border">
              <p className="text-foreground/80 leading-relaxed">{lesson.content}</p>
            </div>
          </div>
        </Card>

        {/* Key Concepts */}
        <Card className="p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Key Concepts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="p-4 bg-muted rounded-lg border border-border hover:border-primary/50 transition-smooth"
              >
                <div className="flex items-start gap-3">
                  <Zap size={20} className="text-accent flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold mb-1">Concept {i}</h3>
                    <p className="text-sm text-foreground/60">Important concept description goes here</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Assessment Section - Updated with AI Quiz */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {assessment && (
            <Card className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold mb-2">{assessment.title}</h2>
                  <p className="text-foreground/60">{assessment.questions.length} questions</p>
                </div>
                <Zap size={40} className="text-accent/50" />
              </div>

              <p className="text-foreground/70 mb-6">Test your understanding with static questions from the lesson.</p>

              <Link href={`/dashboard/courses/${courseId}/lessons/${lessonId}/quiz`}>
                <Button className="bg-gradient-to-r from-accent to-primary w-full">
                  Start Quiz
                  <ChevronRight size={16} className="ml-2" />
                </Button>
              </Link>
            </Card>
          )}

          {/* AI-Powered Adaptive Quiz */}
          <Card className="p-8 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold mb-2">AI Adaptive Quiz</h2>
                <p className="text-foreground/60">Personalized questions</p>
              </div>
              <Brain size={40} className="text-primary/50" />
            </div>

            <p className="text-foreground/70 mb-6">
              Get AI-generated questions that adapt to your learning level and performance.
            </p>

            <Link href={`/dashboard/courses/${courseId}/lessons/${lessonId}/adaptive-quiz`}>
              <Button className="bg-gradient-to-r from-primary to-secondary w-full">
                Start AI Quiz
                <ChevronRight size={16} className="ml-2" />
              </Button>
            </Link>
          </Card>
        </div>

        {/* Completion Section */}
        <div className="flex gap-4">
          <Button
            onClick={() => setIsCompleted(true)}
            className="flex-1 bg-gradient-to-r from-primary to-secondary"
            disabled={isCompleted}
          >
            {isCompleted ? (
              <>
                <CheckCircle size={16} className="mr-2" />
                Lesson Completed
              </>
            ) : (
              "Mark as Complete"
            )}
          </Button>

          <Link href={`/dashboard/courses/${courseId}`} className="flex-1">
            <Button variant="outline" className="w-full bg-transparent">
              Back to Course
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
