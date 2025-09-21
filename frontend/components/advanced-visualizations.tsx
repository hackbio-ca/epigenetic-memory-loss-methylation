"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Area,
  AreaChart,
} from "recharts"
import { Activity } from "lucide-react"

// Mock data for advanced visualizations
const ageRiskData = [
  { age: 55, riskScore: 0.12, samples: 8 },
  { age: 60, riskScore: 0.18, samples: 12 },
  { age: 65, riskScore: 0.25, samples: 15 },
  { age: 70, riskScore: 0.42, samples: 18 },
  { age: 75, riskScore: 0.58, samples: 22 },
  { age: 80, riskScore: 0.71, samples: 16 },
  { age: 85, riskScore: 0.84, samples: 9 },
]

const methylationPatterns = [
  { position: 1, control: 0.45, mild: 0.52, severe: 0.68 },
  { position: 2, control: 0.38, mild: 0.48, severe: 0.72 },
  { position: 3, control: 0.42, mild: 0.55, severe: 0.75 },
  { position: 4, control: 0.35, mild: 0.51, severe: 0.69 },
  { position: 5, control: 0.41, mild: 0.58, severe: 0.78 },
  { position: 6, control: 0.39, mild: 0.54, severe: 0.71 },
  { position: 7, control: 0.44, mild: 0.59, severe: 0.82 },
  { position: 8, control: 0.37, mild: 0.53, severe: 0.74 },
]

const confidenceData = [
  { riskScore: 0.1, confidence: 0.92 },
  { riskScore: 0.2, confidence: 0.89 },
  { riskScore: 0.3, confidence: 0.85 },
  { riskScore: 0.4, confidence: 0.87 },
  { riskScore: 0.5, confidence: 0.84 },
  { riskScore: 0.6, confidence: 0.88 },
  { riskScore: 0.7, confidence: 0.91 },
  { riskScore: 0.8, confidence: 0.94 },
  { riskScore: 0.9, confidence: 0.96 },
]

export function AdvancedVisualizations() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-accent" />
          Advanced Analysis
        </CardTitle>
        <CardDescription>Deep dive into methylation patterns and risk correlations</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="age-correlation" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="age-correlation">Age Correlation</TabsTrigger>
            <TabsTrigger value="methylation-patterns">Methylation Patterns</TabsTrigger>
            <TabsTrigger value="confidence-analysis">Confidence Analysis</TabsTrigger>
          </TabsList>

          <TabsContent value="age-correlation" className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-foreground">Age vs Risk Score Correlation</h4>
              <p className="text-sm text-muted-foreground">
                Relationship between patient age and predicted Alzheimer's risk
              </p>
            </div>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart data={ageRiskData}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="age"
                    type="number"
                    domain={["dataMin - 2", "dataMax + 2"]}
                    className="text-xs"
                    label={{ value: "Age (years)", position: "insideBottom", offset: -5 }}
                  />
                  <YAxis
                    dataKey="riskScore"
                    type="number"
                    domain={[0, 1]}
                    className="text-xs"
                    label={{ value: "Risk Score", angle: -90, position: "insideLeft" }}
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "6px",
                    }}
                    formatter={(value: number, name: string) => [
                      name === "riskScore" ? `${(value * 100).toFixed(1)}%` : value,
                      name === "riskScore" ? "Risk Score" : name === "samples" ? "Sample Count" : name,
                    ]}
                  />
                  <Scatter dataKey="riskScore" fill="hsl(var(--accent))" />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-muted/50 rounded-lg p-3">
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Correlation coefficient: r = 0.87</strong> - Strong positive
                correlation between age and Alzheimer's risk, consistent with known epidemiological data.
              </p>
            </div>
          </TabsContent>

          <TabsContent value="methylation-patterns" className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-foreground">Methylation Level Comparison</h4>
              <p className="text-sm text-muted-foreground">
                Average methylation levels across top CpG sites by disease severity
              </p>
            </div>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={methylationPatterns}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="position"
                    className="text-xs"
                    label={{ value: "Top CpG Sites (ranked)", position: "insideBottom", offset: -5 }}
                  />
                  <YAxis
                    className="text-xs"
                    label={{ value: "Methylation Level", angle: -90, position: "insideLeft" }}
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "6px",
                    }}
                    formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, "Methylation"]}
                  />
                  <Area
                    type="monotone"
                    dataKey="control"
                    stackId="1"
                    stroke="#22c55e"
                    fill="#22c55e"
                    fillOpacity={0.3}
                    name="Control"
                  />
                  <Area
                    type="monotone"
                    dataKey="mild"
                    stackId="2"
                    stroke="#f59e0b"
                    fill="#f59e0b"
                    fillOpacity={0.3}
                    name="Mild Cognitive Impairment"
                  />
                  <Area
                    type="monotone"
                    dataKey="severe"
                    stackId="3"
                    stroke="#ef4444"
                    fill="#ef4444"
                    fillOpacity={0.3}
                    name="Alzheimer's Disease"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="space-y-1">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full" />
                  <span className="text-sm font-medium text-foreground">Control</span>
                </div>
                <p className="text-xs text-muted-foreground">Healthy individuals</p>
              </div>
              <div className="space-y-1">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                  <span className="text-sm font-medium text-foreground">MCI</span>
                </div>
                <p className="text-xs text-muted-foreground">Mild cognitive impairment</p>
              </div>
              <div className="space-y-1">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full" />
                  <span className="text-sm font-medium text-foreground">AD</span>
                </div>
                <p className="text-xs text-muted-foreground">Alzheimer's disease</p>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="confidence-analysis" className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-foreground">Prediction Confidence Analysis</h4>
              <p className="text-sm text-muted-foreground">
                Model confidence levels across different risk score ranges
              </p>
            </div>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={confidenceData}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis
                    dataKey="riskScore"
                    className="text-xs"
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                    label={{ value: "Risk Score", position: "insideBottom", offset: -5 }}
                  />
                  <YAxis
                    domain={[0.8, 1]}
                    className="text-xs"
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                    label={{ value: "Confidence", angle: -90, position: "insideLeft" }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "6px",
                    }}
                    formatter={(value: number, name: string) => [
                      `${(value * 100).toFixed(1)}%`,
                      name === "confidence" ? "Confidence" : "Risk Score",
                    ]}
                  />
                  <Line
                    type="monotone"
                    dataKey="confidence"
                    stroke="hsl(var(--accent))"
                    strokeWidth={3}
                    dot={{ fill: "hsl(var(--accent))", strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, stroke: "hsl(var(--accent))", strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-muted/50 rounded-lg p-3">
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">High confidence at extremes:</strong> The model shows highest
                confidence for very low risk (&lt;20%) and very high risk (&gt;80%) predictions, with slightly lower
                confidence in the moderate risk range.
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
