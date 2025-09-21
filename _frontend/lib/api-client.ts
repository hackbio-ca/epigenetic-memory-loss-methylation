export interface PredictionRequest {
  file: File
  studyName: string
  studyDescription?: string
}

export interface PredictionResult {
  analysisId: string
  totalSamples: number
  processingTime: number
  modelVersion: string
  accuracy: number
  predictions: Array<{
    sampleId: string
    riskScore: number
    confidence: number
    riskLevel: string
  }>
  featureImportance: Array<{
    cpg: string
    importance: number
    gene: string
    chromosome: string
  }>
  riskDistribution: {
    high: number
    moderate: number
    low: number
  }
  modelMetrics: {
    accuracy: number
    sensitivity: number
    specificity: number
    aucRoc: number
  }
}

export interface Analysis {
  id: string
  studyName: string
  fileName: string
  uploadedAt: string
  status: "processing" | "completed" | "failed"
  totalSamples: number
  highRiskCount: number | null
  processingTime: number | null
  results?: PredictionResult
}

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl = "/api") {
    this.baseUrl = baseUrl
  }

  async submitPrediction(request: PredictionRequest): Promise<{ analysisId: string }> {
    const formData = new FormData()
    formData.append("file", request.file)
    formData.append("studyName", request.studyName)
    if (request.studyDescription) {
      formData.append("studyDescription", request.studyDescription)
    }

    const response = await fetch(`${this.baseUrl}/predict`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || "Prediction failed")
    }

    const result = await response.json()
    return { analysisId: result.analysisId }
  }

  async getAnalysis(analysisId: string): Promise<Analysis> {
    const response = await fetch(`${this.baseUrl}/analysis/${analysisId}`)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || "Failed to fetch analysis")
    }

    const result = await response.json()
    return result.analysis
  }

  async getUserAnalyses(): Promise<Analysis[]> {
    const response = await fetch(`${this.baseUrl}/analyses`)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || "Failed to fetch analyses")
    }

    const result = await response.json()
    return result.analyses
  }

  async exportResults(analysisId: string, format: "csv" | "pdf" = "csv"): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/analysis/${analysisId}/export?format=${format}`)

    if (!response.ok) {
      throw new Error("Failed to export results")
    }

    return response.blob()
  }
}

// Export singleton instance
export const apiClient = new ApiClient()
