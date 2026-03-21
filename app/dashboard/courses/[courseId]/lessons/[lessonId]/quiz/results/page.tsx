"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect, useParams, useSearchParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle, XCircle, Download, Share2, TrendingUp } from "lucide-react"
import Link from "next/link"
import { generateFeedback } from "@/lib/grading-system"

export default function QuizResultsPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const searchParams = useSearchParams()
  const courseId = params.courseId as string
  const lessonId = params.lessonId as string

  const score = Number.parseInt(searchParams.get("score") || "0")
  const totalQuestions = Number.parseInt(searchParams.get("total") || "5")

  if (!isAuthenticated || user?.role !== "student") {
    redirect("/login")
  }

  const passed = score >= 70
  const mockCorrectAnswers: Record<string, string> = {
    "q-1": "A symbol representing an unknown value",
    "q-2": "7",
  }
  const mockStudentAnswers: Record<string, string> = {
    "q-1": "A symbol representing an unknown value",
    "q-2": "7",
  }
  const mockQuestionTexts: Record<string, string> = {
    "q-1": "Variables",
    "q-2": "Linear Equations",
  }

  const gradingResult = generateFeedback(score, mockStudentAnswers, mockCorrectAnswers, mockQuestionTexts)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-sm text-foreground/60">Quiz Results</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Score Card */}
        <Card className="p-12 text-center bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20 mb-8">
          <div className="mb-6">
            {passed ? (
              <CheckCircle size={80} className="mx-auto text-green-500 mb-4" />
            ) : (
              <XCircle size={80} className="mx-auto text-orange-500 mb-4" />
            )}
          </div>

          <h1 className="text-4xl font-bold mb-2">{passed ? "Great Job!" : "Keep Learning"}</h1>

          <div className="text-7xl font-bold text-primary mb-4">{score}%</div>

          <p className="text-xl text-foreground/60 mb-8">
            You answered {Math.round((score / 100) * totalQuestions)} out of {totalQuestions} questions correctly
          </p>

          <div className="inline-block px-6 py-3 bg-background rounded-lg border border-border mb-8">
            <p className="text-sm text-foreground/60 mb-1">Performance Level</p>
            <p className="text-lg font-bold">
              {score >= 90
                ? "Outstanding"
                : score >= 80
                  ? "Excellent"
                  : score >= 70
                    ? "Good"
                    : score >= 60
                      ? "Fair"
                      : "Needs Improvement"}
            </p>
          </div>
        </Card>

        {/* Feedback Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Main Feedback */}
          <div className="lg:col-span-2">
            <Card className="p-8 mb-8">
              <h2 className="text-2xl font-bold mb-4">Feedback</h2>
              <p className="text-foreground/80 leading-relaxed mb-6">{gradingResult.feedback}</p>

              {/* Strengths */}
              <div className="mb-6">
                <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
                  <CheckCircle size={20} className="text-green-500" />
                  Your Strengths
                </h3>
                <ul className="space-y-2">
                  {gradingResult.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-950/30 rounded-lg">
                      <span className="text-green-600 dark:text-green-400 font-bold mt-0.5">✓</span>
                      <span className="text-foreground/80">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Areas for Improvement */}
              <div>
                <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
                  <TrendingUp size={20} className="text-orange-500" />
                  Areas for Improvement
                </h3>
                <ul className="space-y-2">
                  {gradingResult.improvements.map((improvement, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-3 p-3 bg-orange-50 dark:bg-orange-950/30 rounded-lg"
                    >
                      <span className="text-orange-600 dark:text-orange-400 font-bold mt-0.5">→</span>
                      <span className="text-foreground/80">{improvement}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Card>

            {/* Next Steps */}
            <Card className="p-8 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
              <h2 className="text-2xl font-bold mb-4">Recommended Next Steps</h2>
              <ol className="space-y-3">
                {gradingResult.nextSteps.map((step, index) => (
                  <li key={index} className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <span className="text-foreground/80 pt-1">{step}</span>
                  </li>
                ))}
              </ol>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="p-6 sticky top-20">
              <h3 className="font-semibold text-lg mb-6">Actions</h3>

              <div className="space-y-3">
                <Button className="w-full bg-gradient-to-r from-primary to-secondary">
                  <Download size={16} className="mr-2" />
                  Download Report
                </Button>

                <Button variant="outline" className="w-full bg-transparent">
                  <Share2 size={16} className="mr-2" />
                  Share Results
                </Button>

                <Link href={`/dashboard/courses/${courseId}/lessons/${lessonId}`} className="block">
                  <Button variant="outline" className="w-full bg-transparent">
                    Back to Lesson
                  </Button>
                </Link>

                <Link href={`/dashboard/courses/${courseId}`} className="block">
                  <Button variant="outline" className="w-full bg-transparent">
                    Back to Course
                  </Button>
                </Link>
              </div>

              {/* Score Breakdown */}
              <div className="mt-8 pt-8 border-t border-border">
                <h4 className="font-semibold mb-4">Score Breakdown</h4>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground/60">Correct Answers</span>
                    <span className="font-bold text-green-600 dark:text-green-400">
                      {Math.round((score / 100) * totalQuestions)}/{totalQuestions}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground/60">Accuracy</span>
                    <span className="font-bold">{score}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground/60">Status</span>
                    <span
                      className={`font-bold ${passed ? "text-green-600 dark:text-green-400" : "text-orange-600 dark:text-orange-400"}`}
                    >
                      {passed ? "Passed" : "Needs Review"}
                    </span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Related Resources */}
        <Card className="p-8">
          <h2 className="text-2xl font-bold mb-6">Related Resources</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: "Review Lesson Content", icon: "📚" },
              { title: "Practice Problems", icon: "✏️" },
              { title: "Video Tutorial", icon: "🎥" },
            ].map((resource, index) => (
              <button
                key={index}
                className="p-4 border border-border rounded-lg hover:border-primary/50 transition-smooth text-left"
              >
                <p className="text-2xl mb-2">{resource.icon}</p>
                <p className="font-medium">{resource.title}</p>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
