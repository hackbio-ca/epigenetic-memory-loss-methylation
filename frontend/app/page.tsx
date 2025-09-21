"use client"

import { useState } from "react"
import { FileUploadSection } from "@/components/file-upload-section"
import { StatsCards } from "@/components/stats-cards"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Brain, Database, BarChart3, Shield, X } from "lucide-react"

export default function HomePage() {
  const [showResults, setShowResults] = useState(false)
  const [analysisResults, setAnalysisResults] = useState<any>(null)

  const handleAnalysisComplete = (results: any) => {
    setAnalysisResults(results)
    setShowResults(true)
  }
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
          <FileUploadSection onAnalysisComplete={handleAnalysisComplete} />
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

      {/* Results Popup */}
      <Dialog open={showResults} onOpenChange={setShowResults}>
        <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">
              Alzheimer's Risk Analysis Results
            </DialogTitle>
            <DialogDescription className="text-lg">
              Analysis completed successfully. Here are the risk predictions for each sample:
            </DialogDescription>
          </DialogHeader>
          <div className="mt-6 space-y-6">
            {analysisResults?.results?.[0]?.predictions_with_ids ? (
              <>
                {/* Summary Cards */}
                <div className="grid grid-cols-3 gap-6 mb-8">
                  {(() => {
                    const predictions = analysisResults.results[0].predictions_with_ids;
                    const counts = { control: 0, mci: 0, alzheimer: 0 };
                    predictions.forEach((item: any) => {
                      if (item.prediction === 0) counts.control++;
                      else if (item.prediction === 1) counts.mci++;
                      else if (item.prediction === 2) counts.alzheimer++;
                    });
                    
                    return (
                      <>
                        <Card className="border-blue-300 bg-blue-50 shadow-lg">
                          <CardContent className="p-6 text-center">
                            <div className="text-3xl font-bold text-blue-700">{counts.control}</div>
                            <div className="text-lg font-semibold text-blue-600">Control</div>
                            <div className="text-sm text-blue-500 mt-2">Normal cognitive function</div>
                          </CardContent>
                        </Card>
                        <Card className="border-yellow-300 bg-yellow-50 shadow-lg">
                          <CardContent className="p-6 text-center">
                            <div className="text-3xl font-bold text-yellow-700">{counts.mci}</div>
                            <div className="text-lg font-semibold text-yellow-600">MCI</div>
                            <div className="text-sm text-yellow-500 mt-2">Mild Cognitive Impairment</div>
                          </CardContent>
                        </Card>
                        <Card className="border-orange-300 bg-orange-50 shadow-lg">
                          <CardContent className="p-6 text-center">
                            <div className="text-3xl font-bold text-orange-700">{counts.alzheimer}</div>
                            <div className="text-lg font-semibold text-orange-600">Alzheimer's</div>
                            <div className="text-sm text-orange-500 mt-2">High risk indication</div>
                          </CardContent>
                        </Card>
                      </>
                    );
                  })()}
                </div>

                {/* Results Table */}
                <div className="space-y-4">
                  <h3 className="text-xl font-bold">Sample Predictions:</h3>
                  <div className="border rounded-lg overflow-hidden shadow-sm">
                    <table className="w-full">
                      <thead className="bg-gray-50 border-b">
                        <tr>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Sample ID</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Classification</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Risk Level</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
                        {analysisResults.results[0].predictions_with_ids.map((item: any, index: number) => {
                          const getClassificationDetails = (pred: number) => {
                            switch (pred) {
                              case 0:
                                return {
                                  label: "Control",
                                  description: "Normal cognitive function",
                                  bgColor: "bg-blue-50",
                                  textColor: "text-blue-800",
                                  badgeColor: "bg-blue-200 text-blue-900",
                                  icon: "🔵"
                                };
                              case 1:
                                return {
                                  label: "MCI",
                                  description: "Mild Cognitive Impairment",
                                  bgColor: "bg-yellow-50", 
                                  textColor: "text-yellow-800",
                                  badgeColor: "bg-yellow-200 text-yellow-900",
                                  icon: "🟡"
                                };
                              case 2:
                                return {
                                  label: "Alzheimer's",
                                  description: "High risk indication",
                                  bgColor: "bg-orange-50",
                                  textColor: "text-orange-800", 
                                  badgeColor: "bg-orange-200 text-orange-900",
                                  icon: "🟠"
                                };
                              default:
                                return {
                                  label: "Unknown",
                                  description: "Unrecognized classification",
                                  bgColor: "bg-gray-50",
                                  textColor: "text-gray-800",
                                  badgeColor: "bg-gray-200 text-gray-900",
                                  icon: "⚪"
                                };
                            }
                          };

                          const details = getClassificationDetails(item.prediction);

                          return (
                            <tr key={index} className={`${details.bgColor} hover:opacity-75 transition-opacity`}>
                              <td className="px-6 py-4 text-sm font-medium text-gray-900">
                                {item.sample_id}
                              </td>
                              <td className="px-6 py-4">
                                <div className="flex items-center space-x-3">
                                  <span className="text-xl">{details.icon}</span>
                                  <Badge className={`${details.badgeColor} font-medium px-3 py-1`}>
                                    {details.label}
                                  </Badge>
                                </div>
                              </td>
                              <td className={`px-6 py-4 text-sm ${details.textColor} font-medium`}>
                                {details.description}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-xl text-gray-500 mb-4">No prediction data found in the response.</p>
                <p className="text-sm text-gray-400">Expected format: results[0].predictions_with_ids</p>
                <div className="mt-4 p-4 bg-gray-100 rounded text-left text-xs">
                  <strong>Actual response structure:</strong>
                  <pre>{JSON.stringify(analysisResults, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
