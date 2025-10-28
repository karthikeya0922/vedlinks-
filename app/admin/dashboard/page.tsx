"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockStudents, mockTeachers, mockCourses, mockParents } from "@/lib/mock-data"
import { Users, BookOpen, TrendingUp, BarChart3, Download } from "lucide-react"
import Link from "next/link"

export default function AdminDashboardPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "admin") {
    redirect("/login")
  }

  const totalStudents = mockStudents.length
  const totalTeachers = mockTeachers.length
  const totalCourses = mockCourses.length
  const totalParents = mockParents.length

  const avgStudentProgress =
    mockStudents.length > 0
      ? Math.round(
          mockStudents.reduce((sum, s) => {
            const avg = Object.values(s.progress).reduce((a, b) => a + b, 0) / Object.keys(s.progress).length
            return sum + avg
          }, 0) / mockStudents.length,
        )
      : 0

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
              <p className="text-foreground/60">Platform-wide analytics and management</p>
            </div>
            <Button className="bg-gradient-to-r from-primary to-secondary">
              <Download size={16} className="mr-2" />
              Export Data
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <Card className="p-6 bg-gradient-to-br from-primary/10 to-secondary/10 border-primary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Students</p>
                <p className="text-3xl font-bold text-primary">{totalStudents}</p>
              </div>
              <Users size={32} className="text-primary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-accent/10 to-primary/10 border-accent/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Teachers</p>
                <p className="text-3xl font-bold text-accent">{totalTeachers}</p>
              </div>
              <Users size={32} className="text-accent/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-secondary/10 to-accent/10 border-secondary/20">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Total Courses</p>
                <p className="text-3xl font-bold text-secondary">{totalCourses}</p>
              </div>
              <BookOpen size={32} className="text-secondary/50" />
            </div>
          </Card>

          <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-200 dark:border-green-800">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-foreground/60 mb-1">Avg Progress</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{avgStudentProgress}%</p>
              </div>
              <TrendingUp size={32} className="text-green-500" />
            </div>
          </Card>
        </div>

        {/* System Health */}
        <Card className="p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6">System Health</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-green-50 dark:bg-green-950/30 rounded-lg border border-green-200 dark:border-green-800">
              <p className="text-sm text-foreground/60 mb-2">Platform Status</p>
              <p className="text-lg font-bold text-green-600 dark:text-green-400">Operational</p>
              <p className="text-xs text-foreground/60 mt-2">All systems running normally</p>
            </div>

            <div className="p-4 bg-blue-50 dark:bg-blue-950/30 rounded-lg border border-blue-200 dark:border-blue-800">
              <p className="text-sm text-foreground/60 mb-2">Active Sessions</p>
              <p className="text-lg font-bold text-blue-600 dark:text-blue-400">24</p>
              <p className="text-xs text-foreground/60 mt-2">Users currently online</p>
            </div>

            <div className="p-4 bg-purple-50 dark:bg-purple-950/30 rounded-lg border border-purple-200 dark:border-purple-800">
              <p className="text-sm text-foreground/60 mb-2">Data Integrity</p>
              <p className="text-lg font-bold text-purple-600 dark:text-purple-400">100%</p>
              <p className="text-xs text-foreground/60 mt-2">All data verified</p>
            </div>
          </div>
        </Card>

        {/* Management Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">User Management</h2>

            <div className="space-y-3">
              <Link href="/admin/users/students" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <Users size={16} className="mr-2" />
                  Manage Students ({totalStudents})
                </Button>
              </Link>
              <Link href="/admin/users/teachers" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <Users size={16} className="mr-2" />
                  Manage Teachers ({totalTeachers})
                </Button>
              </Link>
              <Link href="/admin/users/parents" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <Users size={16} className="mr-2" />
                  Manage Parents ({totalParents})
                </Button>
              </Link>
            </div>
          </Card>

          <Card className="p-8">
            <h2 className="text-2xl font-bold mb-6">Content Management</h2>

            <div className="space-y-3">
              <Link href="/admin/courses" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <BookOpen size={16} className="mr-2" />
                  Manage Courses ({totalCourses})
                </Button>
              </Link>
              <Link href="/admin/reports" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <BarChart3 size={16} className="mr-2" />
                  View Reports
                </Button>
              </Link>
              <Link href="/admin/settings" className="block">
                <Button variant="outline" className="w-full bg-transparent justify-start">
                  <BarChart3 size={16} className="mr-2" />
                  System Settings
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
