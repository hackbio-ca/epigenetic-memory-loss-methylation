import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FileText, Eye } from "lucide-react"

export function RecentAnalyses() {
  const analyses = [
    {
      id: 1,
      name: "Cohort Study A",
      date: "2024-01-15",
      samples: 156,
      status: "completed",
      riskScore: "High Risk: 23%",
    },
    {
      id: 2,
      name: "Longitudinal Study B",
      date: "2024-01-12",
      samples: 89,
      status: "completed",
      riskScore: "Moderate Risk: 45%",
    },
    {
      id: 3,
      name: "Control Group Analysis",
      date: "2024-01-10",
      samples: 203,
      status: "processing",
      riskScore: "Processing...",
    },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "default"
      case "processing":
        return "secondary"
      default:
        return "outline"
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-accent" />
          Recent Analyses
        </CardTitle>
        <CardDescription>Your latest methylation studies and results</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {analyses.map((analysis) => (
          <div key={analysis.id} className="border border-border rounded-lg p-4 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="font-medium text-foreground">{analysis.name}</h4>
                <p className="text-sm text-muted-foreground">
                  {analysis.samples} samples • {analysis.date}
                </p>
              </div>
              <Badge variant={getStatusColor(analysis.status)}>{analysis.status}</Badge>
            </div>

            <div className="text-sm">
              <p className="text-muted-foreground">{analysis.riskScore}</p>
            </div>

            {analysis.status === "completed" && (
              <Button variant="outline" size="sm" className="w-full bg-transparent">
                <Eye className="mr-2 h-4 w-4" />
                View Results
              </Button>
            )}
          </div>
        ))}

        <Button variant="ghost" className="w-full">
          View All Analyses
        </Button>
      </CardContent>
    </Card>
  )
}
