import { FileUploadSection } from "@/components/file-upload-section"
import { StatsCards } from "@/components/stats-cards"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground">NeuroPredict</h1>
              <p className="text-muted-foreground">Advanced Alzheimer's Disease Prediction Platform</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Platform Overview */}
        <div className="text-center space-y-4 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-foreground text-balance">
            DNA Methylation Analysis for Alzheimer's Risk Prediction
          </h2>
          <p className="text-muted-foreground text-pretty leading-relaxed">
            Upload your CSV methylation data files and receive comprehensive analysis with feature importance scores,
            biomarker identification, and risk predictions using cutting-edge machine learning algorithms.
          </p>
        </div>

        {/* Statistics Cards */}
        <StatsCards />

        {/* File Upload Section */}
        <div className="max-w-4xl mx-auto">
          <FileUploadSection />
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Advanced ML Models</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                State-of-the-art machine learning algorithms trained on large-scale methylation datasets for accurate
                Alzheimer's risk prediction.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Biomarker Discovery</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Identify key CpG sites and methylation patterns associated with Alzheimer's disease progression and
                cognitive decline.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Comprehensive Reports</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Detailed analysis reports with visualizations, feature importance scores, and actionable insights for
                research and clinical applications.
              </p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
