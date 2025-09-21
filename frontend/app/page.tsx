import { FileUploadSection } from "@/components/file-upload-section"
import { StatsCards } from "@/components/stats-cards"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, Database, BarChart3, Shield } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-foreground/10 rounded-lg">
                <Brain className="h-8 w-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Epigenetic Markers of Memory Loss</h1>
                <p className="text-primary-foreground/80">Advanced Alzheimer's Disease Prediction Platform</p>
              </div>
            </div>
            <Badge variant="secondary" className="bg-accent text-accent-foreground">
              Research Platform
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-12">
        {/* Hero Section */}
        <div className="text-center space-y-6 max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-foreground text-balance">
            DNA Methylation Analysis for Alzheimer's Risk Prediction
          </h2>
          <p className="text-xl text-muted-foreground text-pretty leading-relaxed">
            Upload your CSV methylation data files and receive comprehensive analysis with feature importance scores,
            biomarker identification, and risk predictions using cutting-edge machine learning algorithms.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <CardTitle className="text-lg">Advanced ML Models</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                State-of-the-art machine learning algorithms trained on large-scale methylation datasets for accurate
                Alzheimer's risk prediction.
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                <Database className="h-6 w-6 text-primary" />
              </div>
              <CardTitle className="text-lg">Biomarker Discovery</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Identify key CpG sites and methylation patterns associated with Alzheimer's disease progression and
                cognitive decline.
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                <BarChart3 className="h-6 w-6 text-primary" />
              </div>
              <CardTitle className="text-lg">Comprehensive Reports</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Detailed analysis reports with visualizations, feature importance scores, and actionable insights for
                research and clinical applications.
              </p>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <CardTitle className="text-lg">Secure & Private</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                HIPAA-compliant data processing with end-to-end encryption ensuring your research data remains secure
                and confidential.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* File Upload Section */}
        <div className="max-w-4xl mx-auto">
          <FileUploadSection />
        </div>

        {/* Statistics Cards */}
        <StatsCards />

        {/* API Integration Info */}
        <div className="max-w-4xl mx-auto">
          <Card className="bg-secondary">
            <CardHeader>
              <CardTitle className="text-center">Ready for Backend Integration</CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-muted-foreground">
                This platform is designed to connect seamlessly with your backend API endpoints for data processing and
                analysis.
              </p>
              <div className="grid md:grid-cols-3 gap-4 text-sm">
                <div className="p-3 bg-background rounded-lg">
                  <code className="text-primary font-mono">POST /api/upload</code>
                  <p className="text-muted-foreground mt-1">File upload endpoint</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <code className="text-primary font-mono">POST /api/analyze</code>
                  <p className="text-muted-foreground mt-1">Analysis processing</p>
                </div>
                <div className="p-3 bg-background rounded-lg">
                  <code className="text-primary font-mono">GET /api/results</code>
                  <p className="text-muted-foreground mt-1">Retrieve results</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-muted mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-muted-foreground">
            <p>&copy; 2024 Epigenetic Markers of Memory Loss. Advanced Alzheimer's Disease Prediction Platform.</p>
            <p className="text-sm mt-2">Built for scientific research and clinical applications.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
