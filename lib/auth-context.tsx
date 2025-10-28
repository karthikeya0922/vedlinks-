"use client"

import type React from "react"
import { createContext, useContext, useState, useCallback, useEffect } from "react"
import type { User, AuthContextType, UserRole } from "./types"
import { mockStudents, mockTeachers, mockParents, mockCredentials } from "./mock-data"

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Initialize from localStorage
  useEffect(() => {
    const storedUser = localStorage.getItem("lms-user")
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (error) {
        console.error("[v0] Failed to parse stored user:", error)
      }
    }
    setIsLoading(false)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true)
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500))

      // Check credentials
      const storedPassword = mockCredentials[email as keyof typeof mockCredentials]
      if (!storedPassword || storedPassword !== password) {
        throw new Error("Invalid email or password")
      }

      // Find user
      let foundUser: User | null = null

      const student = mockStudents.find((s) => s.email === email)
      if (student) foundUser = student

      const teacher = mockTeachers.find((t) => t.email === email)
      if (teacher) foundUser = teacher

      const parent = mockParents.find((p) => p.email === email)
      if (parent) foundUser = parent

      if (!foundUser) {
        throw new Error("User not found")
      }

      setUser(foundUser)
      localStorage.setItem("lms-user", JSON.stringify(foundUser))
    } catch (error) {
      console.error("[v0] Login error:", error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [])

  const signup = useCallback(async (email: string, password: string, name: string, role: UserRole) => {
    setIsLoading(true)
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500))

      // Check if user already exists
      const allUsers = [...mockStudents, ...mockTeachers, ...mockParents]
      if (allUsers.some((u) => u.email === email)) {
        throw new Error("Email already registered")
      }

      // Create new user based on role
      let newUser: User

      if (role === "student") {
        newUser = {
          id: `student-${Date.now()}`,
          email,
          name,
          role,
          gradeLevel: 9,
          parentIds: [],
          enrolledCourses: [],
          progress: {},
          createdAt: new Date(),
        } as any
        mockStudents.push(newUser as any)
      } else if (role === "teacher") {
        newUser = {
          id: `teacher-${Date.now()}`,
          email,
          name,
          role,
          subject: "General",
          courses: [],
          students: [],
          createdAt: new Date(),
        } as any
        mockTeachers.push(newUser as any)
      } else if (role === "parent") {
        newUser = {
          id: `parent-${Date.now()}`,
          email,
          name,
          role,
          childrenIds: [],
          createdAt: new Date(),
        } as any
        mockParents.push(newUser as any)
      } else {
        throw new Error("Invalid role")
      }

      // Store credentials
      mockCredentials[email as keyof typeof mockCredentials] = password

      setUser(newUser)
      localStorage.setItem("lms-user", JSON.stringify(newUser))
    } catch (error) {
      console.error("[v0] Signup error:", error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    localStorage.removeItem("lms-user")
  }, [])

  const value: AuthContextType = {
    user,
    isLoading,
    login,
    signup,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
