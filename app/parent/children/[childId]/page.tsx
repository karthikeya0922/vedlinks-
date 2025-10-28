"use client"
import { redirect, useParams } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { mockParents, mockStudents, mockCourses } from "@/lib/mock-data"
import { ChevronRight, TrendingUp, BookOpen, Award, AlertCircle, Zap } from "lucide-react"
import Link from "next/link"

export default function ChildDetailPage() {
  const { user, isAuthenticated } = useParams()
  const params = useParams()
  const childId = params.childId as string

  if (!isAuthenticated || user?.role !== "parent") {
    redirect("/login")
  }

  const parent = mockParents.find((p) => p.id === user?.id)
  if (!parent || !parent.childrenIds.includes(childId)) {
    redirect("/parent/dashboard")
  }

  const child = mockStudents.find((s) => s.id === childId)
  if (!child) redirect("/parent/dashboard")

  const childCourses = mockCourses.filter((c) => child.enrolledCourses.includes(c.id))
  const avgProgress = Object.values(child.progress).reduce((a, b) => a + b, 0) / Object.keys(child.progress).length

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            href="/parent/dashboard"
            className="text-primary hover:text-secondary transition-smooth mb-4 inline-flex items-center"
          >
            <ChevronRight size={16} className="rotate-180 mr-1" />
            Back to Dashboard
          </Link>
          <h1 className="text-4xl font-bold mb-2">{child.name}'s Progress</h1>
          <p className="text-foreground/60">Grade {child.gradeLevel} • Detailed learning analytics</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Overall Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
              <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-sm text-foreground/60 mb-1">Overall Progress</p>
                    <p className="text-3xl font-bold text-primary">{Math.round(avgProgress)}%</p>
                  </div>
                  <TrendingUp size={32} className="text-primary/50" />
                </div>
                <Progress value={avgProgress} className="h-2" />
              </Card>

              <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-sm text-foreground/60 mb-1">Learning Streak</p>
                    <p className="text-3xl font-bold text-accent">7 Days</p>
                  </div>
                  <Zap size={32} className="text-accent/50" />
                </div>
                <p className="text-xs text-foreground/60">+50 XP per day</p>
              </Card>
            </div>

            {/* Courses */}
            <div className="mb-12">
              <h2 className="text-2xl font-bold mb-6">Enrolled Courses</h2>

              <div className="space-y-4">
                {childCourses.map((course) => {
                  const progress = child.progress[course.id] || 0
                  return (
                    <Card key={course.id} className="p-6 hover:shadow-lg transition-smooth">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-semibold text-lg mb-1">{course.title}</h3>
                          <p className="text-sm text-foreground/60">{course.subject}</p>
                        </div>
                        <BookOpen size={24} className="text-primary/50" />
                      </div>

                      <div className="space-y-3">
                        <div>
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-xs font-medium">Progress</span>
                            <span className="text-xs font-bold text-primary">{progress}%</span>
                          </div>
                          <Progress value={progress} className="h-2" />
                        </div>

                        {progress < 70 && (
                          <div className="flex items-start gap-2 p-3 bg-orange-50 dark:bg-orange-950/30 rounded-lg border border-orange-200 dark:border-orange-800">
                            <AlertCircle
                              size={16}
                              className="text-orange-600 dark:text-orange-400 flex-shrink-0 mt-0.5"
                            />
                            <p className="text-xs text-orange-700 dark:text-orange-300">
                              Your child is making progress but may benefit from additional support in this course.
                            </p>
                          </div>
                        )}
                      </div>
                    </Card>
                  )
                })}
              </div>
            </div>

            {/* Performance by Topic */}
            <Card className="p-8">
              <h2 className="text-2xl font-bold mb-6">Performance by Topic</h2>

              <div className="space-y-4">
                {[
                  { topic: "Variables", score: 85, status: "Strong" },
                  { topic: "Linear Equations", score: 78, status: "Good" },
                  { topic: "Systems of Equations", score: 65, status: "Needs Help" },
                ].map((item, index) => (
                  <div key={index} className="p-4 border border-border rounded-lg">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="font-semibold">{item.topic}</h3>
                      <span
                        className={`text-xs font-medium px-2 py-1 rounded-full ${
                          item.score >= 80
                            ? "bg-green-500/20 text-green-600 dark:text-green-400"
                            : item.score >= 70
                              ? "bg-blue-500/20 text-blue-600 dark:text-blue-400"
                              : "bg-orange-500/20 text-orange-600 dark:text-orange-400"
                        }`}
                      >
                        {item.status}
                      </span>
                    </div>
                    <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                        style={{ width: `${item.score}%` }}
                      />
                    </div>
                    <p className="text-xs text-foreground/60 mt-2">{item.score}% mastery</p>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Achievements */}
            <Card className="p-6 sticky top-20 mb-6">
              <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                <Award size={20} className="text-accent" />
                Achievements
              </h3>

              <div className="space-y-3">
                {[
                  { name: "Quick Learner", icon: "⚡" },
                  { name: "Consistent", icon: "🔥" },
                  { name: "Problem Solver", icon: "🧠" },
                ].map((achievement, index) => (
                  <div
                    key={index}
                    className="p-3 bg-gradient-to-br from-accent/10 to-primary/10 rounded-lg border border-accent/20"
                  >
                    <p className="text-sm font-medium">
                      {achievement.icon} {achievement.name}
                    </p>
                  </div>
                ))}
              </div>
            </Card>

            {/* Recommendations */}
            <Card className="p-6">
              <h3 className="font-semibold text-lg mb-4">How to Help</h3>

              <div className="space-y-4 text-sm">
                <div>
                  <p className="font-medium mb-1">Focus Areas</p>
                  <p className="text-foreground/60">
                    Your child needs extra support with Systems of Equations. Consider scheduling 15-20 minutes of
                    practice daily.
                  </p>
                </div>

                <div>
                  <p className="font-medium mb-1">Strengths</p>
                  <p className="text-foreground/60">
                    Excellent performance in Variables! Encourage your child to help peers with this topic.
                  </p>
                </div>

                <div>
                  <p className="font-medium mb-1">Next Steps</p>
                  <p className="text-foreground/60">
                    Complete the current course to unlock advanced topics and new challenges.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
