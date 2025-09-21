import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Target, TrendingUp, Zap, Shield } from "lucide-react"

export function ModelMetrics() {
  const metrics = [
    {
      name: "Accuracy",
      value: 94.2,
      description: "Overall prediction accuracy",
      icon: Target,
      color: "text-green-600",
    },
    {
      name: "Sensitivity",
      value: 91.8,
      description: "True positive rate",
      icon: TrendingUp,
      color: "text-blue-600",
    },
    {
      name: "Specificity",
      value: 96.1,
      description: "True negative rate",
      icon: Shield,
      color: "text-purple-600",
    },
    {
      name: "AUC-ROC",
      value: 95.7,
      description: "Area under ROC curve",
      icon: Zap,
      color: "text-orange-600",
    },
  ]

  const getPerformanceLevel = (value: number) => {
    if (value >= 95) return { label: "Excellent", variant: "default" as const }
    if (value >= 90) return { label: "Very Good", variant: "secondary" as const }
    if (value >= 85) return { label: "Good", variant: "outline" as const }
    return { label: "Fair", variant: "destructive" as const }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Performance</CardTitle>
        <CardDescription>Key performance metrics for the Alzheimer's prediction model</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {metrics.map((metric) => {
          const Icon = metric.icon
          const performance = getPerformanceLevel(metric.value)

          return (
            <div key={metric.name} className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Icon className={`h-5 w-5 ${metric.color}`} />
                  <div>
                    <p className="font-medium text-foreground">{metric.name}</p>
                    <p className="text-sm text-muted-foreground">{metric.description}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-foreground">{metric.value}%</p>
                  <Badge variant={performance.variant} className="text-xs">
                    {performance.label}
                  </Badge>
                </div>
              </div>
              <Progress value={metric.value} className="h-2" />
            </div>
          )
        })}

        <div className="mt-6 p-4 bg-muted/50 rounded-lg">
          <h4 className="font-medium text-foreground mb-2">Model Details</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">Algorithm</p>
              <p className="font-medium text-foreground">Random Forest</p>
            </div>
            <div>
              <p className="text-muted-foreground">Features</p>
              <p className="font-medium text-foreground">485,577 CpG sites</p>
            </div>
            <div>
              <p className="text-muted-foreground">Training Samples</p>
              <p className="font-medium text-foreground">1,247</p>
            </div>
            <div>
              <p className="text-muted-foreground">Cross-validation</p>
              <p className="font-medium text-foreground">10-fold CV</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
