"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockLessons } from "@/lib/mock-data"
import { useState, useEffect } from "react"
import { CheckCircle, XCircle, ArrowRight, RotateCcw, Zap, Brain } from "lucide-react"
import Link from "next/link"
import {
  generateQuestionsFromContent,
  adjustDifficultyLevel,
  type GeneratedQuestion,
} from "@/lib/ai-question-generator"

export default function AdaptiveQuizPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const courseId = params.courseId as string
  const lessonId = params.lessonId as string

  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [showResults, setShowResults] = useState(false)
  const [questions, setQuestions] = useState<GeneratedQuestion[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [difficulty, setDifficulty] = useState<"easy" | "medium" | "hard">("medium")
  const [scores, setScores] = useState<number[]>([])

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const lesson = mockLessons.find((l) => l.id === lessonId)
  if (!lesson) redirect(`/dashboard/courses/${courseId}`)

  // Generate questions on component mount
  useEffect(() => {
    const generateQuestions = async () => {
      setIsLoading(true)
      try {
        const generatedQuestions = await generateQuestionsFromContent({
          lessonContent: lesson.content,
          lessonTitle: lesson.title,
          difficulty,
          questionType: "multiple-choice",
          count: 5,
          studentLevel: 9,
        })
        setQuestions(generatedQuestions)
      } catch (error) {
        console.error("Error generating questions:", error)
      } finally {
        setIsLoading(false)
      }
    }

    generateQuestions()
  }, [lesson, difficulty])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="p-12 text-center">
          <Brain size={48} className="mx-auto mb-4 text-primary animate-spin-slow" />
          <h2 className="text-2xl font-bold mb-2">Generating AI Questions</h2>
          <p className="text-foreground/60">Creating personalized questions based on the lesson content...</p>
        </Card>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="p-12 text-center max-w-2xl">
          <Zap size={48} className="mx-auto mb-4 text-accent" />
          <h2 className="text-2xl font-bold mb-2">Unable to Generate Questions</h2>
          <p className="text-foreground/60 mb-6">Please try again or contact support</p>
          <Link href={`/dashboard/courses/${courseId}`}>
            <Button variant="outline">Back to Course</Button>
          </Link>
        </Card>
      </div>
    )
  }

  const question = questions[currentQuestion]

  const handleAnswer = (answer: string) => {
    setAnswers({
      ...answers,
      [question.id]: answer,
    })
  }

  const handleNext = () => {
    // Calculate score for current question
    const isCorrect = answers[question.id] === question.correctAnswer
    const questionScore = isCorrect ? 100 : 0
    setScores([...scores, questionScore])

    // Adjust difficulty based on performance
    if (scores.length > 0) {
      const averageScore = (scores.reduce((a, b) => a + b, 0) + questionScore) / (scores.length + 1)
      const newDifficulty = adjustDifficultyLevel(difficulty, averageScore)
      if (newDifficulty !== difficulty) {
        setDifficulty(newDifficulty)
      }
    }

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

          <h1 className="text-4xl font-bold mb-2">{passed ? "Excellent!" : "Keep Learning"}</h1>

          <div className="text-6xl font-bold text-primary mb-2">{score}%</div>
          <p className="text-foreground/60 mb-4">
            You answered {Object.keys(answers).length} out of {questions.length} questions correctly
          </p>

          <div className="bg-background rounded-lg p-4 mb-8 border border-border">
            <p className="text-sm text-foreground/60 mb-2">Difficulty Level: {difficulty.toUpperCase()}</p>
            <p className="text-xs text-foreground/50">
              {difficulty === "easy" && "Keep practicing to unlock harder questions"}
              {difficulty === "medium" && "You're doing great! Keep challenging yourself"}
              {difficulty === "hard" && "Outstanding performance! You're mastering this topic"}
            </p>
          </div>

          <div className="space-y-3">
            <Button
              onClick={() => {
                setCurrentQuestion(0)
                setAnswers({})
                setShowResults(false)
                setScores([])
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

  const isAnswered = !!answers[question.id]
  const isCorrect = answers[question.id] === question.correctAnswer

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
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
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium px-3 py-1 bg-primary/20 rounded-full text-primary">
                {question.difficulty.toUpperCase()}
              </span>
              <Link href={`/dashboard/courses/${courseId}`}>
                <Button variant="outline" size="sm">
                  Exit
                </Button>
              </Link>
            </div>
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
                  disabled={isAnswered}
                  className={`w-full p-4 text-left rounded-lg border-2 transition-smooth ${
                    answers[question.id] === option
                      ? isCorrect
                        ? "border-green-500 bg-green-500/10"
                        : "border-red-500 bg-red-500/10"
                      : "border-border hover:border-primary/50"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        answers[question.id] === option
                          ? isCorrect
                            ? "border-green-500 bg-green-500"
                            : "border-red-500 bg-red-500"
                          : "border-foreground/30"
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

          {isAnswered && (
            <Card className="mt-8 p-6 bg-muted/50 border-primary/20">
              <h3 className="font-semibold mb-2 flex items-center gap-2">
                {isCorrect ? (
                  <>
                    <CheckCircle size={20} className="text-green-500" />
                    Correct!
                  </>
                ) : (
                  <>
                    <XCircle size={20} className="text-red-500" />
                    Incorrect
                  </>
                )}
              </h3>
              <p className="text-sm text-foreground/70">{question.explanation}</p>
            </Card>
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
            disabled={!isAnswered}
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
