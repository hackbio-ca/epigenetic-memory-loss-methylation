import { DashboardHeader } from "@/components/dashboard-header"
import { FileUploadSection } from "@/components/file-upload-section"
import { RecentAnalyses } from "@/components/recent-analyses"
import { StatsCards } from "@/components/stats-cards"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto px-4 py-8 space-y-8">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-foreground">Research Dashboard</h1>
          <p className="text-muted-foreground">Upload methylation data and analyze Alzheimer's disease risk patterns</p>
        </div>

        <StatsCards />

        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <FileUploadSection />
          </div>
          <div>
            <RecentAnalyses />
          </div>
        </div>
      </main>
    </div>
  )
}
