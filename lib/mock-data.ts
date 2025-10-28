import type { Student, Teacher, Parent, Course, Lesson, Assessment } from "./types"

// Mock Users
export const mockStudents: Student[] = [
  {
    id: "student-1",
    email: "john@example.com",
    name: "John Doe",
    role: "student",
    gradeLevel: 10,
    parentIds: ["parent-1"],
    enrolledCourses: ["course-1", "course-2"],
    progress: { "course-1": 65, "course-2": 45 },
    createdAt: new Date("2024-01-15"),
  },
  {
    id: "student-2",
    email: "jane@example.com",
    name: "Jane Smith",
    role: "student",
    gradeLevel: 9,
    parentIds: ["parent-1"],
    enrolledCourses: ["course-1"],
    progress: { "course-1": 85 },
    createdAt: new Date("2024-02-20"),
  },
]

export const mockTeachers: Teacher[] = [
  {
    id: "teacher-1",
    email: "mr.wilson@example.com",
    name: "Mr. Wilson",
    role: "teacher",
    subject: "Mathematics",
    courses: ["course-1"],
    students: ["student-1", "student-2"],
    createdAt: new Date("2023-08-01"),
  },
  {
    id: "teacher-2",
    email: "ms.johnson@example.com",
    name: "Ms. Johnson",
    role: "teacher",
    subject: "Science",
    courses: ["course-2"],
    students: ["student-1"],
    createdAt: new Date("2023-09-01"),
  },
]

export const mockParents: Parent[] = [
  {
    id: "parent-1",
    email: "parent@example.com",
    name: "Sarah Doe",
    role: "parent",
    childrenIds: ["student-1", "student-2"],
    createdAt: new Date("2024-01-10"),
  },
]

// Mock Courses
export const mockCourses: Course[] = [
  {
    id: "course-1",
    title: "Algebra Fundamentals",
    description: "Master the basics of algebra with AI-powered personalized learning",
    subject: "Mathematics",
    gradeLevel: 9,
    teacherId: "teacher-1",
    lessons: ["lesson-1", "lesson-2", "lesson-3"],
    createdAt: new Date("2024-01-01"),
  },
  {
    id: "course-2",
    title: "Biology Essentials",
    description: "Explore the fundamentals of biology with interactive lessons",
    subject: "Science",
    gradeLevel: 10,
    teacherId: "teacher-2",
    lessons: ["lesson-4", "lesson-5"],
    createdAt: new Date("2024-01-05"),
  },
]

// Mock Lessons
export const mockLessons: Lesson[] = [
  {
    id: "lesson-1",
    courseId: "course-1",
    title: "Introduction to Variables",
    description: "Learn what variables are and how to use them",
    content: "Variables are symbols that represent unknown values...",
    order: 1,
    createdAt: new Date("2024-01-01"),
  },
  {
    id: "lesson-2",
    courseId: "course-1",
    title: "Solving Linear Equations",
    description: "Master the techniques to solve linear equations",
    content: "A linear equation is an equation of the first degree...",
    order: 2,
    createdAt: new Date("2024-01-05"),
  },
  {
    id: "lesson-3",
    courseId: "course-1",
    title: "Systems of Equations",
    description: "Learn to solve systems with multiple equations",
    content: "A system of equations is a set of two or more equations...",
    order: 3,
    createdAt: new Date("2024-01-10"),
  },
  {
    id: "lesson-4",
    courseId: "course-2",
    title: "Cell Structure",
    description: "Understand the basic structure of cells",
    content: "Cells are the basic unit of life...",
    order: 1,
    createdAt: new Date("2024-01-02"),
  },
  {
    id: "lesson-5",
    courseId: "course-2",
    title: "Photosynthesis",
    description: "Learn how plants convert light into energy",
    content: "Photosynthesis is the process by which plants...",
    order: 2,
    createdAt: new Date("2024-01-08"),
  },
]

// Mock Assessments
export const mockAssessments: Assessment[] = [
  {
    id: "assessment-1",
    lessonId: "lesson-1",
    title: "Variables Quiz",
    type: "quiz",
    questions: [
      {
        id: "q-1",
        text: "What is a variable?",
        type: "multiple-choice",
        options: [
          "A symbol representing an unknown value",
          "A fixed number",
          "A type of equation",
          "A mathematical operation",
        ],
        correctAnswer: "A symbol representing an unknown value",
        difficulty: "easy",
      },
      {
        id: "q-2",
        text: "If x + 5 = 12, what is x?",
        type: "multiple-choice",
        options: ["5", "7", "12", "17"],
        correctAnswer: "7",
        difficulty: "easy",
      },
    ],
    createdAt: new Date("2024-01-03"),
  },
]

// Mock credentials for testing
export const mockCredentials = {
  "john@example.com": "password123",
  "jane@example.com": "password123",
  "mr.wilson@example.com": "password123",
  "parent@example.com": "password123",
}
