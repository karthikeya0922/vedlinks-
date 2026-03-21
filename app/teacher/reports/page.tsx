"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockTeachers, mockStudents } from "@/lib/mock-data"
import { FileText, Download, Eye, Trash2, Plus, Calendar } from "lucide-react"
import { generateReport, formatReportAsText } from "@/lib/analytics-engine"

export default function ReportsPage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "teacher") {
    redirect("/login")
  }

  const teacher = mockTeachers.find((t) => t.id === user.id)
  if (!teacher) redirect("/login")

  const teacherStudents = mockStudents.filter((s) => teacher.students.includes(s.id))
  const activeStudentIds = teacherStudents.slice(0, Math.ceil(teacherStudents.length * 0.8)).map((s) => s.id)

  const reports = [
    {
      id: "r-1",
      title: "Monthly Performance Report",
      period: "January 2024",
      generatedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
      type: "monthly",
    },
    {
      id: "r-2",
      title: "Weekly Summary",
      period: "Week of Jan 22-28",
      generatedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
      type: "weekly",
    },
    {
      id: "r-3",
      title: "Course Performance Analysis",
      period: "Algebra 101",
      generatedAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
      type: "course",
    },
  ]

  const handleGenerateReport = () => {
    const report = generateReport(teacherStudents, activeStudentIds, "Last 30 Days")
    const reportText = formatReportAsText(report)
    const element = document.createElement("a")
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(reportText))
    element.setAttribute("download", `report-${new Date().toISOString().split("T")[0]}.txt`)
    element.style.display = "none"
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Reports</h1>
              <p className="text-foreground/60">Generate and manage learning reports</p>
            </div>
            <Button onClick={handleGenerateReport} className="bg-gradient-to-r from-primary to-secondary">
              <Plus size={16} className="mr-2" />
              Generate Report
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Report Templates */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Quick Generate</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "Daily Report", icon: "📅", description: "Today's learning activity" },
              { title: "Weekly Report", icon: "📊", description: "Last 7 days summary" },
              { title: "Monthly Report", icon: "📈", description: "Last 30 days analysis" },
            ].map((template, index) => (
              <Card
                key={index}
                className="p-6 hover:shadow-lg transition-smooth cursor-pointer group border-2 border-border hover:border-primary/50"
              >
                <p className="text-4xl mb-3">{template.icon}</p>
                <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                  {template.title}
                </h3>
                <p className="text-sm text-foreground/60 mb-4">{template.description}</p>
                <Button size="sm" className="w-full bg-gradient-to-r from-primary to-secondary">
                  Generate
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* Recent Reports */}
        <div>
          <h2 className="text-2xl font-bold mb-6">Recent Reports</h2>

          <div className="space-y-4">
            {reports.map((report) => (
              <Card key={report.id} className="p-6 hover:shadow-lg transition-smooth group">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4 flex-grow">
                    <FileText
                      size={32}
                      className="text-primary/50 group-hover:text-primary transition-smooth flex-shrink-0"
                    />
                    <div className="flex-grow">
                      <h3 className="font-semibold text-lg mb-1 group-hover:text-primary transition-smooth">
                        {report.title}
                      </h3>
                      <p className="text-sm text-foreground/60 mb-2">{report.period}</p>
                      <div className="flex items-center gap-2 text-xs text-foreground/50">
                        <Calendar size={14} />
                        <span>{report.generatedAt.toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                      <Eye size={16} className="mr-2" />
                      View
                    </Button>
                    <Button variant="outline" size="sm">
                      <Download size={16} className="mr-2" />
                      Export
                    </Button>
                    <Button variant="destructive" size="sm">
                      <Trash2 size={16} />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
