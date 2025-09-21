import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { AlertTriangle, CheckCircle, TrendingUp, Users } from "lucide-react"

export function PredictionOverview() {
  const overviewStats = [
    {
      title: "High Risk Samples",
      value: 36,
      percentage: 23.1,
      icon: AlertTriangle,
      color: "text-red-600",
      bgColor: "bg-red-50",
      description: "Samples with >70% Alzheimer's risk probability",
    },
    {
      title: "Moderate Risk Samples",
      value: 71,
      percentage: 45.5,
      icon: TrendingUp,
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
      description: "Samples with 30-70% risk probability",
    },
    {
      title: "Low Risk Samples",
      value: 49,
      percentage: 31.4,
      icon: CheckCircle,
      color: "text-green-600",
      bgColor: "bg-green-50",
      description: "Samples with <30% risk probability",
    },
  ]

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5 text-accent" />
            Prediction Overview
          </CardTitle>
          <CardDescription>Summary of Alzheimer's risk predictions across all analyzed samples</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            {overviewStats.map((stat) => {
              const Icon = stat.icon
              return (
                <div key={stat.title} className="space-y-3">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                      <Icon className={`h-5 w-5 ${stat.color}`} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                      <div className="flex items-baseline gap-2">
                        <span className="text-2xl font-bold text-foreground">{stat.value}</span>
                        <Badge variant="secondary">{stat.percentage}%</Badge>
                      </div>
                    </div>
                  </div>
                  <Progress value={stat.percentage} className="h-2" />
                  <p className="text-xs text-muted-foreground">{stat.description}</p>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Key Findings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-accent rounded-full mt-2 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">23.1%</strong> of samples show high Alzheimer's risk, indicating
                potential early-stage biomarkers
              </p>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-accent rounded-full mt-2 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Top 5 CpG sites</strong> contribute to 67% of the predictive power
                in the model
              </p>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-accent rounded-full mt-2 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Model accuracy:</strong> 94.2% with high confidence intervals across
                all risk categories
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Analysis Parameters</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Total Samples</span>
              <span className="text-sm font-medium text-foreground">156</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">CpG Sites Analyzed</span>
              <span className="text-sm font-medium text-foreground">485,577</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Processing Time</span>
              <span className="text-sm font-medium text-foreground">2.3 minutes</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Model Version</span>
              <span className="text-sm font-medium text-foreground">v2.1.4</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Analysis Date</span>
              <span className="text-sm font-medium text-foreground">Jan 15, 2024</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
