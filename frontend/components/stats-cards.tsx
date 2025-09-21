import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, TrendingUp, Users, Clock } from "lucide-react"

export function StatsCards() {
  const stats = [
    {
      title: "Total Analyses",
      value: "24",
      description: "Completed studies",
      icon: FileText,
      trend: "+12% from last month",
    },
    {
      title: "Accuracy Rate",
      value: "94.2%",
      description: "Model performance",
      icon: TrendingUp,
      trend: "Validated on 1,200+ samples",
    },
    {
      title: "Samples Processed",
      value: "3,847",
      description: "Total methylation profiles",
      icon: Users,
      trend: "+156 this month",
    },
    {
      title: "Avg. Processing Time",
      value: "2.3 min",
      description: "Per analysis",
      icon: Clock,
      trend: "15% faster than baseline",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
              <Icon className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">{stat.description}</p>
              <p className="text-xs text-accent mt-1">{stat.trend}</p>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
