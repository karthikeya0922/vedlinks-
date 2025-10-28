export type UserRole = "student" | "teacher" | "parent" | "admin"

export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  avatar?: string
  createdAt: Date
}

export interface Student extends User {
  role: "student"
  gradeLevel: number
  parentIds: string[]
  enrolledCourses: string[]
  progress: Record<string, number> // courseId -> progress percentage
}

export interface Teacher extends User {
  role: "teacher"
  subject: string
  courses: string[]
  students: string[]
}

export interface Parent extends User {
  role: "parent"
  childrenIds: string[]
}

export interface Course {
  id: string
  title: string
  description: string
  subject: string
  gradeLevel: number
  teacherId: string
  lessons: string[]
  createdAt: Date
}

export interface Lesson {
  id: string
  courseId: string
  title: string
  description: string
  content: string
  order: number
  createdAt: Date
}

export interface Assessment {
  id: string
  lessonId: string
  title: string
  type: "quiz" | "assignment" | "test"
  questions: Question[]
  createdAt: Date
}

export interface Question {
  id: string
  text: string
  type: "multiple-choice" | "short-answer" | "essay"
  options?: string[]
  correctAnswer?: string
  difficulty: "easy" | "medium" | "hard"
}

export interface StudentProgress {
  id: string
  studentId: string
  courseId: string
  lessonsCompleted: string[]
  assessmentScores: Record<string, number>
  lastAccessed: Date
  overallProgress: number
}

export interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, name: string, role: UserRole) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}
