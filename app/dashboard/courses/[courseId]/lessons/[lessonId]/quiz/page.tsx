"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockAssessments } from "@/lib/mock-data"
import { useState } from "react"
import { CheckCircle, XCircle, ArrowRight, RotateCcw } from "lucide-react"
import Link from "next/link"

export default function QuizPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const lessonId = params.lessonId as string

  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [showResults, setShowResults] = useState(false)

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const assessment = mockAssessments.find((a) => a.lessonId === lessonId)
  if (!assessment) redirect(`/dashboard/courses/${courseId}/lessons/${lessonId}`)

  const questions = assessment.questions
  const question = questions[currentQuestion]

  const handleAnswer = (answer: string) => {
    setAnswers({
      ...answers,
      [question.id]: answer,
    })
  }

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      setShowResults(true)
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const calculateScore = () => {
    let correct = 0
    questions.forEach((q) => {
      if (answers[q.id] === q.correctAnswer) {
        correct++
      }
    })
    return Math.round((correct / questions.length) * 100)
  }

  if (showResults) {
    const score = calculateScore()
    const passed = score >= 70

    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-2xl w-full p-12 text-center bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
          <div className="mb-6">
            {passed ? (
              <CheckCircle size={64} className="mx-auto text-green-500 mb-4" />
            ) : (
              <XCircle size={64} className="mx-auto text-red-500 mb-4" />
            )}
          </div>

          <h1 className="text-4xl font-bold mb-2">{passed ? "Great Job!" : "Keep Practicing"}</h1>

          <div className="text-6xl font-bold text-primary mb-2">{score}%</div>
          <p className="text-foreground/60 mb-8">
            You answered {Object.keys(answers).length} out of {questions.length} questions correctly
          </p>

          <div className="space-y-3">
            <Button
              onClick={() => {
                setCurrentQuestion(0)
                setAnswers({})
                setShowResults(false)
              }}
              className="w-full bg-gradient-to-r from-primary to-secondary"
            >
              <RotateCcw size={16} className="mr-2" />
              Retake Quiz
            </Button>

            <Link href={`/dashboard/courses/${courseId}`} className="block">
              <Button variant="outline" className="w-full bg-transparent">
                Back to Course
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-foreground/60 mb-1">
                Question {currentQuestion + 1} of {questions.length}
              </p>
              <div className="w-64 h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                  style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                />
              </div>
            </div>
            <Link href={`/dashboard/courses/${courseId}`}>
              <Button variant="outline" size="sm">
                Exit
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Card className="p-8 mb-8">
          <h2 className="text-2xl font-bold mb-8">{question.text}</h2>

          {question.type === "multiple-choice" && (
            <div className="space-y-3">
              {question.options?.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  className={`w-full p-4 text-left rounded-lg border-2 transition-smooth ${
                    answers[question.id] === option
                      ? "border-primary bg-primary/10"
                      : "border-border hover:border-primary/50"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        answers[question.id] === option ? "border-primary bg-primary" : "border-foreground/30"
                      }`}
                    >
                      {answers[question.id] === option && <div className="w-2 h-2 bg-white rounded-full" />}
                    </div>
                    <span>{option}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </Card>

        {/* Navigation */}
        <div className="flex gap-4">
          <Button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            variant="outline"
            className="flex-1 bg-transparent"
          >
            Previous
          </Button>

          <Button
            onClick={handleNext}
            disabled={!answers[question.id]}
            className="flex-1 bg-gradient-to-r from-primary to-secondary"
          >
            {currentQuestion === questions.length - 1 ? "Submit" : "Next"}
            <ArrowRight size={16} className="ml-2" />
          </Button>
        </div>
      </div>
    </div>
  )
}
