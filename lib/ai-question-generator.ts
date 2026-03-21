export interface GeneratedQuestion {
  id: string
  text: string
  type: "multiple-choice" | "short-answer" | "essay"
  options?: string[]
  correctAnswer?: string
  difficulty: "easy" | "medium" | "hard"
  explanation: string
  topic: string
}

export interface QuestionGenerationParams {
  lessonContent: string
  lessonTitle: string
  difficulty: "easy" | "medium" | "hard"
  questionType: "multiple-choice" | "short-answer" | "essay"
  count: number
  studentLevel?: number
}

// Mock AI question generation (simulates AI API calls)
// In production, this would call an actual AI API like OpenAI, Anthropic, etc.
export async function generateQuestionsFromContent(params: QuestionGenerationParams): Promise<GeneratedQuestion[]> {
  const { lessonContent, lessonTitle, difficulty, questionType, count, studentLevel = 9 } = params

  // Extract key concepts from lesson content
  const keyPhrases = extractKeyPhrases(lessonContent)

  // Generate questions based on extracted concepts
  const questions: GeneratedQuestion[] = []

  for (let i = 0; i < count; i++) {
    const concept = keyPhrases[i % keyPhrases.length]
    const question = generateSingleQuestion({
      concept,
      lessonTitle,
      difficulty,
      questionType,
      studentLevel,
      lessonContent,
    })
    questions.push(question)
  }

  return questions
}

interface SingleQuestionParams {
  concept: string
  lessonTitle: string
  difficulty: "easy" | "medium" | "hard"
  questionType: "multiple-choice" | "short-answer" | "essay"
  studentLevel: number
  lessonContent: string
}

function generateSingleQuestion(params: SingleQuestionParams): GeneratedQuestion {
  const { concept, lessonTitle, difficulty, questionType, studentLevel, lessonContent } = params

  const id = `q-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

  if (questionType === "multiple-choice") {
    return generateMultipleChoiceQuestion({
      id,
      concept,
      lessonTitle,
      difficulty,
      studentLevel,
      lessonContent,
    })
  } else if (questionType === "short-answer") {
    return generateShortAnswerQuestion({
      id,
      concept,
      lessonTitle,
      difficulty,
      studentLevel,
      lessonContent,
    })
  } else {
    return generateEssayQuestion({
      id,
      concept,
      lessonTitle,
      difficulty,
      studentLevel,
      lessonContent,
    })
  }
}

interface MCParams {
  id: string
  concept: string
  lessonTitle: string
  difficulty: "easy" | "medium" | "hard"
  studentLevel: number
  lessonContent: string
}

function generateMultipleChoiceQuestion(params: MCParams): GeneratedQuestion {
  const { id, concept, lessonTitle, difficulty, studentLevel, lessonContent } = params

  const questionTemplates = {
    easy: [
      `What is the definition of ${concept}?`,
      `Which of the following best describes ${concept}?`,
      `In the context of ${lessonTitle}, what does ${concept} mean?`,
    ],
    medium: [
      `How does ${concept} relate to the main concepts in ${lessonTitle}?`,
      `Which statement about ${concept} is most accurate?`,
      `What is an example of ${concept} in ${lessonTitle}?`,
    ],
    hard: [
      `Analyze how ${concept} applies to complex scenarios in ${lessonTitle}.`,
      `Compare and contrast ${concept} with related concepts.`,
      `What are the implications of ${concept} in advanced ${lessonTitle} applications?`,
    ],
  }

  const templates = questionTemplates[difficulty]
  const questionText = templates[Math.floor(Math.random() * templates.length)]

  const correctAnswers = {
    easy: [
      `${concept} is a fundamental concept in ${lessonTitle}`,
      `${concept} represents a key principle discussed in this lesson`,
      `${concept} is essential for understanding ${lessonTitle}`,
    ],
    medium: [
      `${concept} builds upon foundational concepts and enables deeper understanding`,
      `${concept} is interconnected with multiple concepts in ${lessonTitle}`,
      `${concept} demonstrates practical application of theoretical principles`,
    ],
    hard: [
      `${concept} integrates multiple theoretical frameworks and has broad implications`,
      `${concept} represents a synthesis of complex ideas with real-world applications`,
      `${concept} challenges conventional thinking and opens new perspectives`,
    ],
  }

  const correctAnswer = correctAnswers[difficulty][Math.floor(Math.random() * correctAnswers[difficulty].length)]

  // Generate plausible distractors
  const distractors = generateDistractors(concept, difficulty, 3)

  const options = [correctAnswer, ...distractors].sort(() => Math.random() - 0.5)

  const explanations = {
    easy: `${concept} is a key concept in ${lessonTitle}. The correct answer directly addresses the definition or basic understanding of this concept.`,
    medium: `${concept} plays an important role in ${lessonTitle}. Understanding how it relates to other concepts is crucial for mastery.`,
    hard: `${concept} represents a complex idea that requires synthesis of multiple concepts. The correct answer demonstrates deep understanding and critical thinking.`,
  }

  return {
    id,
    text: questionText,
    type: "multiple-choice",
    options,
    correctAnswer,
    difficulty,
    explanation: explanations[difficulty],
    topic: concept,
  }
}

function generateShortAnswerQuestion(params: MCParams): GeneratedQuestion {
  const { id, concept, lessonTitle, difficulty, studentLevel, lessonContent } = params

  const questionTemplates = {
    easy: [
      `Briefly explain what ${concept} means in the context of ${lessonTitle}.`,
      `Define ${concept} in your own words.`,
      `What is ${concept}?`,
    ],
    medium: [
      `Explain how ${concept} is used in ${lessonTitle} and provide an example.`,
      `Describe the relationship between ${concept} and other key concepts in this lesson.`,
      `How would you apply ${concept} to solve a problem in ${lessonTitle}?`,
    ],
    hard: [
      `Analyze the significance of ${concept} in ${lessonTitle} and discuss its broader implications.`,
      `Evaluate different perspectives on ${concept} and explain which is most valid.`,
      `How does ${concept} challenge or extend our understanding of ${lessonTitle}?`,
    ],
  }

  const templates = questionTemplates[difficulty]
  const questionText = templates[Math.floor(Math.random() * templates.length)]

  const correctAnswers = {
    easy: `${concept} is a fundamental concept in ${lessonTitle} that represents...`,
    medium: `${concept} is important in ${lessonTitle} because it helps us understand...`,
    hard: `${concept} represents a complex idea that integrates multiple perspectives and has significant implications for...`,
  }

  const explanations = {
    easy: `A good answer should clearly define ${concept} and relate it to ${lessonTitle}.`,
    medium: `A strong answer should explain ${concept}, provide examples, and show understanding of its role in ${lessonTitle}.`,
    hard: `An excellent answer should demonstrate critical thinking, analyze multiple perspectives, and show deep understanding of ${concept}'s significance.`,
  }

  return {
    id,
    text: questionText,
    type: "short-answer",
    correctAnswer: correctAnswers[difficulty],
    difficulty,
    explanation: explanations[difficulty],
    topic: concept,
  }
}

function generateEssayQuestion(params: MCParams): GeneratedQuestion {
  const { id, concept, lessonTitle, difficulty, studentLevel, lessonContent } = params

  const questionTemplates = {
    easy: [
      `Write a short essay explaining ${concept} and its importance in ${lessonTitle}.`,
      `Describe ${concept} and provide examples from the lesson.`,
    ],
    medium: [
      `Write an essay analyzing how ${concept} connects to other concepts in ${lessonTitle}.`,
      `Discuss the role of ${concept} in understanding ${lessonTitle} and provide supporting evidence.`,
    ],
    hard: [
      `Write a comprehensive essay evaluating ${concept} from multiple perspectives and discussing its implications for ${lessonTitle}.`,
      `Analyze how ${concept} challenges conventional thinking in ${lessonTitle} and propose new applications.`,
    ],
  }

  const templates = questionTemplates[difficulty]
  const questionText = templates[Math.floor(Math.random() * templates.length)]

  const rubrics = {
    easy: `Essay should clearly explain ${concept}, provide relevant examples, and demonstrate understanding of its role in ${lessonTitle}.`,
    medium: `Essay should analyze connections between ${concept} and other concepts, provide evidence, and show critical thinking.`,
    hard: `Essay should evaluate multiple perspectives, demonstrate synthesis of complex ideas, and propose innovative applications of ${concept}.`,
  }

  return {
    id,
    text: questionText,
    type: "essay",
    correctAnswer: rubrics[difficulty],
    difficulty,
    explanation: rubrics[difficulty],
    topic: concept,
  }
}

function generateDistractors(concept: string, difficulty: string, count: number): string[] {
  const distractorTemplates = {
    easy: [
      `${concept} is unrelated to the main topic`,
      `${concept} is a common misconception about this topic`,
      `${concept} is the opposite of what we learned`,
    ],
    medium: [
      `${concept} is partially correct but misses key nuances`,
      `${concept} applies to a different context`,
      `${concept} is a related but distinct concept`,
    ],
    hard: [
      `${concept} represents a valid alternative perspective`,
      `${concept} is correct in a limited context`,
      `${concept} requires additional conditions to be valid`,
    ],
  }

  const templates = distractorTemplates[difficulty] || distractorTemplates.easy
  const distractors: string[] = []

  for (let i = 0; i < count; i++) {
    distractors.push(templates[i % templates.length])
  }

  return distractors
}

function extractKeyPhrases(content: string): string[] {
  // Simple keyword extraction (in production, use NLP library)
  const words = content.toLowerCase().split(/\s+/)
  const stopWords = new Set([
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "is",
    "are",
    "was",
    "were",
  ])

  const keyPhrases = words
    .filter((word) => word.length > 4 && !stopWords.has(word))
    .slice(0, 10)
    .map((word) => word.replace(/[^a-z0-9]/g, ""))
    .filter((word) => word.length > 0)

  return keyPhrases.length > 0 ? keyPhrases : ["concept", "principle", "theory"]
}

// Adaptive difficulty adjustment based on student performance
export function adjustDifficultyLevel(
  currentDifficulty: "easy" | "medium" | "hard",
  studentPerformance: number, // 0-100 score
): "easy" | "medium" | "hard" {
  if (studentPerformance >= 85) {
    // Student is doing well, increase difficulty
    if (currentDifficulty === "easy") return "medium"
    if (currentDifficulty === "medium") return "hard"
    return "hard"
  } else if (studentPerformance < 60) {
    // Student is struggling, decrease difficulty
    if (currentDifficulty === "hard") return "medium"
    if (currentDifficulty === "medium") return "easy"
    return "easy"
  }
  // Keep current difficulty if performance is in the 60-85 range
  return currentDifficulty
}
