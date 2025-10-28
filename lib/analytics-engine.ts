export interface AnalyticsMetrics {
  totalStudents: number
  activeStudents: number
  averageProgress: number
  completionRate: number
  engagementScore: number
  averageScores: Record<string, number>
}

export interface StudentActivity {
  studentId: string
  studentName: string
  action: string
  timestamp: Date
  duration: number
  score?: number
}

export interface PerformanceTrend {
  date: string
  averageScore: number
  completionRate: number
  engagementLevel: number
}

export interface ReportData {
  title: string
  generatedAt: Date
  period: string
  metrics: AnalyticsMetrics
  trends: PerformanceTrend[]
  topPerformers: Array<{ name: string; score: number }>
  needsSupport: Array<{ name: string; score: number; reason: string }>
  recommendations: string[]
}

// Calculate real-time analytics metrics
export function calculateAnalyticsMetrics(
  students: Array<{ id: string; progress: Record<string, number> }>,
  activeStudentIds: string[],
): AnalyticsMetrics {
  const totalStudents = students.length
  const activeStudents = activeStudentIds.length

  const allScores = students.flatMap((s) => Object.values(s.progress))
  const averageProgress = allScores.length > 0 ? Math.round(allScores.reduce((a, b) => a + b, 0) / allScores.length) : 0

  const completedCount = allScores.filter((s) => s >= 100).length
  const completionRate = allScores.length > 0 ? Math.round((completedCount / allScores.length) * 100) : 0

  const engagementScore = Math.round((activeStudents / totalStudents) * 100)

  const averageScores: Record<string, number> = {}
  students.forEach((student) => {
    Object.entries(student.progress).forEach(([courseId, score]) => {
      if (!averageScores[courseId]) {
        averageScores[courseId] = 0
      }
      averageScores[courseId] += score
    })
  })

  Object.keys(averageScores).forEach((courseId) => {
    averageScores[courseId] = Math.round(averageScores[courseId] / students.length)
  })

  return {
    totalStudents,
    activeStudents,
    averageProgress,
    completionRate,
    engagementScore,
    averageScores,
  }
}

// Generate performance trends
export function generatePerformanceTrends(days = 30): PerformanceTrend[] {
  const trends: PerformanceTrend[] = []
  const today = new Date()

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)

    trends.push({
      date: date.toISOString().split("T")[0],
      averageScore: Math.round(Math.random() * 30 + 65),
      completionRate: Math.round(Math.random() * 20 + 70),
      engagementLevel: Math.round(Math.random() * 25 + 60),
    })
  }

  return trends
}

// Identify top performers
export function identifyTopPerformers(
  students: Array<{ id: string; name: string; progress: Record<string, number> }>,
  limit = 5,
): Array<{ name: string; score: number }> {
  return students
    .map((student) => ({
      name: student.name,
      score: Math.round(
        Object.values(student.progress).reduce((a, b) => a + b, 0) / Object.keys(student.progress).length,
      ),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
}

// Identify students needing support
export function identifyStudentsNeedingSupport(
  students: Array<{ id: string; name: string; progress: Record<string, number> }>,
  threshold = 60,
  limit = 5,
): Array<{ name: string; score: number; reason: string }> {
  return students
    .map((student) => {
      const avgScore = Math.round(
        Object.values(student.progress).reduce((a, b) => a + b, 0) / Object.keys(student.progress).length,
      )
      let reason = ""

      if (avgScore < 40) {
        reason = "Significantly below target - urgent intervention needed"
      } else if (avgScore < 60) {
        reason = "Below target - additional support recommended"
      } else {
        reason = "Approaching target - monitor progress"
      }

      return { name: student.name, score: avgScore, reason }
    })
    .filter((s) => s.score < threshold)
    .sort((a, b) => a.score - b.score)
    .slice(0, limit)
}

// Generate recommendations
export function generateRecommendations(metrics: AnalyticsMetrics): string[] {
  const recommendations: string[] = []

  if (metrics.engagementScore < 60) {
    recommendations.push("Engagement is low. Consider sending reminder notifications to inactive students.")
  }

  if (metrics.averageProgress < 50) {
    recommendations.push("Class average is below 50%. Review lesson difficulty and provide additional support.")
  }

  if (metrics.completionRate < 70) {
    recommendations.push("Completion rate is below target. Encourage students to finish their courses.")
  }

  if (metrics.activeStudents === metrics.totalStudents) {
    recommendations.push("Excellent engagement! All students are actively learning.")
  }

  if (metrics.averageProgress >= 80) {
    recommendations.push("Strong performance across the board. Consider introducing advanced topics.")
  }

  return recommendations.length > 0
    ? recommendations
    : ["Continue monitoring student progress and provide support as needed."]
}

// Generate comprehensive report
export function generateReport(
  students: Array<{ id: string; name: string; progress: Record<string, number> }>,
  activeStudentIds: string[],
  period = "Last 30 Days",
): ReportData {
  const metrics = calculateAnalyticsMetrics(students, activeStudentIds)
  const trends = generatePerformanceTrends(30)
  const topPerformers = identifyTopPerformers(students)
  const needsSupport = identifyStudentsNeedingSupport(students)
  const recommendations = generateRecommendations(metrics)

  return {
    title: "Learning Analytics Report",
    generatedAt: new Date(),
    period,
    metrics,
    trends,
    topPerformers,
    needsSupport,
    recommendations,
  }
}

// Format report for export
export function formatReportAsText(report: ReportData): string {
  let text = `${report.title}\n`
  text += `Generated: ${report.generatedAt.toLocaleDateString()}\n`
  text += `Period: ${report.period}\n\n`

  text += `=== METRICS ===\n`
  text += `Total Students: ${report.metrics.totalStudents}\n`
  text += `Active Students: ${report.metrics.activeStudents}\n`
  text += `Average Progress: ${report.metrics.averageProgress}%\n`
  text += `Completion Rate: ${report.metrics.completionRate}%\n`
  text += `Engagement Score: ${report.metrics.engagementScore}%\n\n`

  text += `=== TOP PERFORMERS ===\n`
  report.topPerformers.forEach((performer, index) => {
    text += `${index + 1}. ${performer.name} - ${performer.score}%\n`
  })
  text += `\n`

  text += `=== STUDENTS NEEDING SUPPORT ===\n`
  report.needsSupport.forEach((student) => {
    text += `${student.name} - ${student.score}% (${student.reason})\n`
  })
  text += `\n`

  text += `=== RECOMMENDATIONS ===\n`
  report.recommendations.forEach((rec) => {
    text += `• ${rec}\n`
  })

  return text
}
