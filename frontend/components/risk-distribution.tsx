"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"

const riskDistributionData = [
  { range: "0-10%", count: 12, label: "Very Low" },
  { range: "10-20%", count: 18, label: "Low" },
  { range: "20-30%", count: 19, label: "Low-Moderate" },
  { range: "30-40%", count: 23, label: "Moderate" },
  { range: "40-50%", count: 25, label: "Moderate" },
  { range: "50-60%", count: 23, label: "Moderate-High" },
  { range: "60-70%", count: 15, label: "High" },
  { range: "70-80%", count: 12, label: "High" },
  { range: "80-90%", count: 7, label: "Very High" },
  { range: "90-100%", count: 2, label: "Critical" },
]

const pieData = [
  { name: "Low Risk (<30%)", value: 49, color: "#22c55e" },
  { name: "Moderate Risk (30-70%)", value: 71, color: "#f59e0b" },
  { name: "High Risk (>70%)", value: 36, color: "#ef4444" },
]

export function RiskDistribution() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Distribution</CardTitle>
        <CardDescription>Distribution of Alzheimer's risk scores across all samples</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={riskDistributionData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="range" className="text-xs" angle={-45} textAnchor="end" height={60} />
              <YAxis className="text-xs" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "6px",
                }}
              />
              <Bar dataKey="count" fill="hsl(var(--accent))" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={40} outerRadius={80} paddingAngle={2} dataKey="value">
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "6px",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="grid grid-cols-3 gap-4 text-center">
          {pieData.map((item, index) => (
            <div key={index} className="space-y-1">
              <div className="flex items-center justify-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-sm font-medium text-foreground">{item.value}</span>
              </div>
              <p className="text-xs text-muted-foreground">{item.name}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
