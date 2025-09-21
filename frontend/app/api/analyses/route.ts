import { type NextRequest, NextResponse } from "next/server"

// Mock user analyses - in production, fetch from database based on user ID
const mockUserAnalyses = [
  {
    id: "analysis_1705123456789",
    studyName: "Cohort Study A",
    fileName: "methylation_data_cohort_a.csv",
    uploadedAt: "2024-01-15T10:30:00Z",
    status: "completed",
    totalSamples: 156,
    highRiskCount: 36,
    processingTime: 2.3,
  },
  {
    id: "analysis_1705023456789",
    studyName: "Longitudinal Study B",
    fileName: "longitudinal_methylation.csv",
    uploadedAt: "2024-01-12T14:15:00Z",
    status: "completed",
    totalSamples: 89,
    highRiskCount: 23,
    processingTime: 1.8,
  },
  {
    id: "analysis_1704923456789",
    studyName: "Control Group Analysis",
    fileName: "control_group_data.csv",
    uploadedAt: "2024-01-10T09:45:00Z",
    status: "processing",
    totalSamples: 203,
    highRiskCount: null,
    processingTime: null,
  },
]

export async function GET(request: NextRequest) {
  try {
    // In production, get user ID from authentication and fetch user's analyses
    const analyses = mockUserAnalyses

    return NextResponse.json({
      success: true,
      analyses,
    })
  } catch (error) {
    console.error("Analyses fetch error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
