"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Dna, Info } from "lucide-react"

const topFeatures = [
  {
    cpg: "cg00000029",
    importance: 0.087,
    gene: "RIN1",
    chromosome: "chr11",
    description: "Associated with neuronal function and synaptic plasticity",
  },
  {
    cpg: "cg00000165",
    importance: 0.074,
    gene: "APOE",
    chromosome: "chr19",
    description: "Major genetic risk factor for Alzheimer's disease",
  },
  {
    cpg: "cg00000236",
    importance: 0.069,
    gene: "TOMM40",
    chromosome: "chr19",
    description: "Linked to mitochondrial function and neurodegeneration",
  },
  {
    cpg: "cg00000321",
    importance: 0.063,
    gene: "BIN1",
    chromosome: "chr2",
    description: "Involved in tau pathology and neuroinflammation",
  },
  {
    cpg: "cg00000412",
    importance: 0.058,
    gene: "CLU",
    chromosome: "chr8",
    description: "Clusterin protein involved in amyloid clearance",
  },
  {
    cpg: "cg00000503",
    importance: 0.054,
    gene: "PICALM",
    chromosome: "chr11",
    description: "Regulates amyloid-beta production and clearance",
  },
  {
    cpg: "cg00000634",
    importance: 0.051,
    gene: "CR1",
    chromosome: "chr1",
    description: "Complement receptor involved in immune response",
  },
  {
    cpg: "cg00000745",
    importance: 0.048,
    gene: "CD33",
    chromosome: "chr19",
    description: "Microglial activation and neuroinflammation",
  },
]

export function FeatureImportance() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Dna className="h-5 w-5 text-accent" />
          Top Predictive Features
        </CardTitle>
        <CardDescription>
          Most important CpG methylation sites contributing to Alzheimer's risk prediction
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topFeatures} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis type="number" className="text-xs" tickFormatter={(value) => `${(value * 100).toFixed(1)}%`} />
              <YAxis type="category" dataKey="cpg" className="text-xs" width={80} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "6px",
                }}
                formatter={(value: number) => [`${(value * 100).toFixed(2)}%`, "Importance"]}
              />
              <Bar dataKey="importance" fill="hsl(var(--accent))" radius={[0, 2, 2, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-4">
          <h4 className="font-medium text-foreground flex items-center gap-2">
            <Info className="h-4 w-4" />
            Feature Details
          </h4>
          <div className="grid gap-3">
            {topFeatures.slice(0, 5).map((feature, index) => (
              <div key={feature.cpg} className="flex items-start gap-4 p-3 border border-border rounded-lg">
                <div className="flex-shrink-0">
                  <Badge variant="outline" className="font-mono text-xs">
                    #{index + 1}
                  </Badge>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-sm font-medium text-foreground">{feature.cpg}</span>
                    <Badge variant="secondary" className="text-xs">
                      {feature.gene}
                    </Badge>
                    <span className="text-xs text-muted-foreground">{feature.chromosome}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
                <div className="flex-shrink-0 text-right">
                  <p className="text-sm font-medium text-foreground">{(feature.importance * 100).toFixed(1)}%</p>
                  <p className="text-xs text-muted-foreground">importance</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-muted/50 rounded-lg p-4">
          <p className="text-sm text-muted-foreground">
            <strong className="text-foreground">Note:</strong> Feature importance scores represent the relative
            contribution of each CpG methylation site to the model's predictive power. Higher scores indicate stronger
            association with Alzheimer's disease risk.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
