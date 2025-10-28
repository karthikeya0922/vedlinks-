import { mockStudents, mockTeachers, mockCourses, mockLessons, mockAssessments } from "./mock-data"
import type { Student, Teacher, Course, Lesson, Assessment } from "./types"

export const db = {
  // Student queries
  getStudent: (id: string): Student | undefined => {
    return mockStudents.find((s) => s.id === id)
  },

  getStudentsByIds: (ids: string[]): Student[] => {
    return mockStudents.filter((s) => ids.includes(s.id))
  },

  getStudentCourses: (studentId: string): Course[] => {
    const student = mockStudents.find((s) => s.id === studentId)
    if (!student) return []
    return mockCourses.filter((c) => student.enrolledCourses.includes(c.id))
  },

  // Teacher queries
  getTeacher: (id: string): Teacher | undefined => {
    return mockTeachers.find((t) => t.id === id)
  },

  getTeacherCourses: (teacherId: string): Course[] => {
    return mockCourses.filter((c) => c.teacherId === teacherId)
  },

  getTeacherStudents: (teacherId: string): Student[] => {
    const teacher = mockTeachers.find((t) => t.id === teacherId)
    if (!teacher) return []
    return mockStudents.filter((s) => teacher.students.includes(s.id))
  },

  // Course queries
  getCourse: (id: string): Course | undefined => {
    return mockCourses.find((c) => c.id === id)
  },

  getAllCourses: (): Course[] => {
    return mockCourses
  },

  getCoursesByGradeLevel: (gradeLevel: number): Course[] => {
    return mockCourses.filter((c) => c.gradeLevel === gradeLevel)
  },

  // Lesson queries
  getLesson: (id: string): Lesson | undefined => {
    return mockLessons.find((l) => l.id === id)
  },

  getCourseLessons: (courseId: string): Lesson[] => {
    return mockLessons.filter((l) => l.courseId === courseId).sort((a, b) => a.order - b.order)
  },

  // Assessment queries
  getAssessment: (id: string): Assessment | undefined => {
    return mockAssessments.find((a) => a.id === id)
  },

  getLessonAssessments: (lessonId: string): Assessment[] => {
    return mockAssessments.filter((a) => a.lessonId === lessonId)
  },
}
