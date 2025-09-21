import { DashboardHeader } from "@/components/dashboard-header"
import { PredictionOverview } from "@/components/prediction-overview"
import { RiskDistribution } from "@/components/risk-distribution"
import { FeatureImportance } from "@/components/feature-importance"
import { SampleAnalysis } from "@/components/sample-analysis"
import { ModelMetrics } from "@/components/model-metrics"
import { AdvancedVisualizations } from "@/components/advanced-visualizations"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download, Share } from "lucide-react"
import Link from "next/link"

export default function ResultsPage() {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto px-4 py-8 space-y-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="outline" size="sm">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Dashboard
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Analysis Results</h1>
              <p className="text-muted-foreground">Alzheimer's Cohort Study 2024 • 156 samples analyzed</p>
            </div>
          </div>

          <div className="flex gap-2">
            <Button variant="outline">
              <Share className="mr-2 h-4 w-4" />
              Share
            </Button>
            <Button>
              <Download className="mr-2 h-4 w-4" />
              Export Report
            </Button>
          </div>
        </div>

        <PredictionOverview />

        <div className="grid lg:grid-cols-2 gap-8">
          <RiskDistribution />
          <ModelMetrics />
        </div>

        <FeatureImportance />

        <AdvancedVisualizations />

        <SampleAnalysis />
      </main>
    </div>
  )
}
