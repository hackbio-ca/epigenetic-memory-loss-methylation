import { type NextRequest, NextResponse } from "next/server"

// Mock database - in production, use a real database
const mockAnalyses = new Map()

export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const analysisId = params.id

    // In production, fetch from database
    const analysis = mockAnalyses.get(analysisId)

    if (!analysis) {
      return NextResponse.json({ error: "Analysis not found" }, { status: 404 })
    }

    return NextResponse.json({
      success: true,
      analysis,
    })
  } catch (error) {
    console.error("Analysis fetch error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
