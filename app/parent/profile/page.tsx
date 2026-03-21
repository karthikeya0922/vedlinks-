"use client"

import { useAuth } from "@/lib/auth-context"
import { redirect } from "next/navigation"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mockParents } from "@/lib/mock-data"
import { Mail, Phone, MapPin, Edit } from "lucide-react"
import Link from "next/link"

export default function ParentProfilePage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || user?.role !== "parent") {
    redirect("/login")
  }

  const parent = mockParents.find((p) => p.id === user.id)
  if (!parent) redirect("/login")

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 to-secondary/10 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">Profile</h1>
              <p className="text-foreground/60">Manage your account settings</p>
            </div>
            <Link href="/parent/dashboard">
              <Button variant="outline">Back to Dashboard</Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Card className="p-8">
          <div className="flex justify-between items-start mb-8">
            <div>
              <h2 className="text-2xl font-bold mb-2">{parent.name}</h2>
              <p className="text-foreground/60">Parent Account</p>
            </div>
            <Button variant="outline">
              <Edit size={16} className="mr-2" />
              Edit Profile
            </Button>
          </div>

          <div className="space-y-6">
            <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
              <Mail size={20} className="text-primary" />
              <div>
                <p className="text-sm text-foreground/60">Email</p>
                <p className="font-medium">{parent.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
              <Phone size={20} className="text-primary" />
              <div>
                <p className="text-sm text-foreground/60">Phone</p>
                <p className="font-medium">+1 (555) 123-4567</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
              <MapPin size={20} className="text-primary" />
              <div>
                <p className="text-sm text-foreground/60">Location</p>
                <p className="font-medium">San Francisco, CA</p>
              </div>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-border">
            <h3 className="text-lg font-semibold mb-4">Preferences</h3>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                <div>
                  <p className="font-medium">Email Notifications</p>
                  <p className="text-sm text-foreground/60">Receive updates about your children's progress</p>
                </div>
                <input type="checkbox" defaultChecked className="w-5 h-5" />
              </div>

              <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                <div>
                  <p className="font-medium">Weekly Reports</p>
                  <p className="text-sm text-foreground/60">Get a summary of learning activities</p>
                </div>
                <input type="checkbox" defaultChecked className="w-5 h-5" />
              </div>

              <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                <div>
                  <p className="font-medium">Achievement Alerts</p>
                  <p className="text-sm text-foreground/60">Be notified when children unlock achievements</p>
                </div>
                <input type="checkbox" defaultChecked className="w-5 h-5" />
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
