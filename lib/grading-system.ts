export interface AssessmentSubmission {
  id: string
  studentId: string
  assessmentId: string
  answers: Record<string, string>
  submittedAt: Date
  score?: number
  feedback?: string
  status: "submitted" | "graded" | "reviewed"
}

export interface GradingResult {
  score: number
  percentage: number
  feedback: string
  strengths: string[]
  improvements: string[]
  nextSteps: string[]
}

// Calculate score for multiple choice questions
export function calculateMultipleChoiceScore(
  answers: Record<string, string>,
  correctAnswers: Record<string, string>,
): number {
  let correct = 0
  let total = 0

  for (const [questionId, answer] of Object.entries(answers)) {
    total++
    if (answer === correctAnswers[questionId]) {
      correct++
    }
  }

  return total > 0 ? Math.round((correct / total) * 100) : 0
}

// Generate AI-powered feedback based on performance
export function generateFeedback(
  score: number,
  studentAnswers: Record<string, string>,
  correctAnswers: Record<string, string>,
  questionTexts: Record<string, string>,
): GradingResult {
  const percentage = score
  const missedQuestions = Object.entries(studentAnswers).filter(([qId, answer]) => answer !== correctAnswers[qId])

  const strengths: string[] = []
  const improvements: string[] = []

  if (percentage >= 90) {
    strengths.push("Excellent understanding of the material")
    strengths.push("Consistent accuracy across all topics")
  } else if (percentage >= 80) {
    strengths.push("Strong grasp of core concepts")
    strengths.push("Good problem-solving skills")
  } else if (percentage >= 70) {
    strengths.push("Solid foundational knowledge")
    strengths.push("Making good progress")
  }

  if (percentage < 70) {
    improvements.push("Review the fundamental concepts")
    improvements.push("Practice similar problems regularly")
  } else if (percentage < 85) {
    improvements.push("Focus on edge cases and complex scenarios")
    improvements.push("Deepen understanding of advanced topics")
  }

  if (missedQuestions.length > 0) {
    const missedTopics = missedQuestions.slice(0, 2).map(([qId]) => questionTexts[qId] || "this topic")
    improvements.push(`Pay special attention to: ${missedTopics.join(", ")}`)
  }

  const nextSteps: string[] = []
  if (percentage >= 85) {
    nextSteps.push("Ready for advanced topics")
    nextSteps.push("Consider helping peers with this material")
  } else if (percentage >= 70) {
    nextSteps.push("Complete additional practice problems")
    nextSteps.push("Review lesson materials before next assessment")
  } else {
    nextSteps.push("Schedule a tutoring session")
    nextSteps.push("Work through practice problems with guidance")
  }

  const feedbackText = generateFeedbackText(percentage, strengths, improvements)

  return {
    score: Math.round((percentage / 100) * 100),
    percentage,
    feedback: feedbackText,
    strengths,
    improvements,
    nextSteps,
  }
}

function generateFeedbackText(percentage: number, strengths: string[], improvements: string[]): string {
  let text = ""

  if (percentage >= 90) {
    text = "Outstanding performance! You've demonstrated excellent mastery of this material. "
  } else if (percentage >= 80) {
    text = "Great job! You've shown strong understanding of the concepts. "
  } else if (percentage >= 70) {
    text = "Good effort! You're making solid progress. "
  } else if (percentage >= 60) {
    text = "You're on the right track, but there's room for improvement. "
  } else {
    text = "This material needs more review and practice. "
  }

  text += `Your score of ${percentage}% shows that ${strengths[0]?.toLowerCase() || "you're learning"}. `
  text += `To improve, ${improvements[0]?.toLowerCase() || "keep practicing"}. `

  return text
}

// Grade essay/short answer questions (mock AI grading)
export function gradeEssayQuestion(
  studentAnswer: string,
  rubric: string,
  maxScore = 100,
): { score: number; feedback: string } {
  // Mock essay grading logic
  const wordCount = studentAnswer.split(/\s+/).length
  const hasKeywords = rubric.split(",").some((keyword) => studentAnswer.toLowerCase().includes(keyword.toLowerCase()))

  let score = 0

  if (wordCount < 20) {
    score = Math.max(0, maxScore * 0.3)
  } else if (wordCount < 50) {
    score = maxScore * 0.6
  } else {
    score = maxScore * 0.85
  }

  if (hasKeywords) {
    score = Math.min(maxScore, score + maxScore * 0.15)
  }

  const feedback =
    score >= 80
      ? "Excellent response with clear understanding and good detail."
      : score >= 60
        ? "Good response, but could include more specific examples or details."
        : "Response needs more development and specific examples to support your points."

  return { score: Math.round(score), feedback }
}

// Calculate class statistics
export interface ClassStatistics {
  averageScore: number
  highestScore: number
  lowestScore: number
  passRate: number
  distribution: Record<string, number>
}

export function calculateClassStatistics(scores: number[]): ClassStatistics {
  if (scores.length === 0) {
    return {
      averageScore: 0,
      highestScore: 0,
      lowestScore: 0,
      passRate: 0,
      distribution: {},
    }
  }

  const sorted = [...scores].sort((a, b) => a - b)
  const average = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
  const passCount = scores.filter((s) => s >= 70).length
  const passRate = Math.round((passCount / scores.length) * 100)

  const distribution: Record<string, number> = {
    "90-100": scores.filter((s) => s >= 90).length,
    "80-89": scores.filter((s) => s >= 80 && s < 90).length,
    "70-79": scores.filter((s) => s >= 70 && s < 80).length,
    "60-69": scores.filter((s) => s >= 60 && s < 70).length,
    "0-59": scores.filter((s) => s < 60).length,
  }

  return {
    averageScore: average,
    highestScore: sorted[sorted.length - 1],
    lowestScore: sorted[0],
    passRate,
    distribution,
  }
}
