"use client"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { HeroSection } from "@/components/hero"
import { FeaturesSection } from "@/components/features"
import { GamificationShowcaseSection } from "@/components/gamification-showcase"
import { StakeholdersSection } from "@/components/stakeholders"
import { CTASection } from "@/components/cta"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <HeroSection />
        <FeaturesSection />
        <GamificationShowcaseSection />
        <StakeholdersSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  )
}
