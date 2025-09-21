"use client"

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface SimpleShapVisualizationProps {
  topFeatures: Array<{
    feature_name: string
    feature_index: number
    mean_abs_shap: number
  }>
  featureNames: string[]
}

export function SimpleShapVisualization({ topFeatures, featureNames }: SimpleShapVisualizationProps) {
  const [selectedFeatures, setSelectedFeatures] = React.useState<number>(20)

  // Prepare data for feature importance bar chart
  const chartData = topFeatures.slice(0, selectedFeatures).map((feature, index) => ({
    feature_name: feature.feature_name.length > 12 
      ? feature.feature_name.substring(0, 12) + '...' 
      : feature.feature_name,
    full_name: feature.feature_name,
    importance: feature.mean_abs_shap,
    rank: index + 1
  }))

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border rounded shadow-lg">
          <p className="font-medium">{`${data.full_name}`}</p>
          <p className="text-sm">{`Rank: #${data.rank}`}</p>
          <p className="text-sm">{`Mean |SHAP|: ${data.importance.toFixed(6)}`}</p>
        </div>
      )
    }
    return null
  }

  if (!topFeatures || topFeatures.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>SHAP Feature Importance</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No SHAP feature importance data available</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>SHAP Feature Importance Analysis</CardTitle>
          <div className="flex items-center gap-2">
            <label className="text-sm">Show top:</label>
            <Select value={selectedFeatures.toString()} onValueChange={(value) => setSelectedFeatures(parseInt(value))}>
              <SelectTrigger className="w-20">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="10">10</SelectItem>
                <SelectItem value="15">15</SelectItem>
                <SelectItem value="20">20</SelectItem>
                <SelectItem value="25">25</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        <p className="text-sm text-muted-foreground">
          Features ranked by their average absolute impact on model predictions across all samples
        </p>
      </CardHeader>
      <CardContent>
        {/* Bar Chart */}
        <div className="h-[500px] w-full mb-6">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart 
              data={chartData} 
              margin={{ top: 20, right: 30, bottom: 100, left: 20 }}
              layout="horizontal"
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number"
                domain={[0, 'dataMax']}
                label={{ value: 'Mean Absolute SHAP Value', position: 'insideBottom', offset: -10 }}
              />
              <YAxis 
                type="category"
                dataKey="feature_name"
                width={100}
                fontSize={9}
                interval={0}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="importance" 
                fill="#3b82f6"
                radius={[0, 2, 2, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        {/* Feature importance table */}
        <div className="mt-6">
          <h4 className="text-lg font-semibold mb-3">Top Features by SHAP Importance</h4>
          <p className="text-sm text-muted-foreground mb-3">
            Features (CpG sites or columns) from your uploaded CSV ranked by their impact on predictions
          </p>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-200">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 px-4 py-2 text-left">Rank</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Feature Name</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Mean |SHAP|</th>
                  <th className="border border-gray-200 px-4 py-2 text-left">Relative Impact</th>
                </tr>
              </thead>
              <tbody>
                {topFeatures.slice(0, selectedFeatures).map((feature, idx) => {
                  const maxImpact = topFeatures[0]?.mean_abs_shap || 1
                  const relativeImpact = (feature.mean_abs_shap / maxImpact) * 100
                  
                  return (
                    <tr key={feature.feature_index} className={idx % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                      <td className="border border-gray-200 px-4 py-2 font-medium">
                        #{idx + 1}
                      </td>
                      <td className="border border-gray-200 px-4 py-2 font-mono text-sm break-all">
                        {feature.feature_name}
                      </td>
                      <td className="border border-gray-200 px-4 py-2">
                        <Badge variant="secondary">{feature.mean_abs_shap.toFixed(6)}</Badge>
                      </td>
                      <td className="border border-gray-200 px-4 py-2">
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full" 
                              style={{width: `${relativeImpact}%`}}
                            ></div>
                          </div>
                          <span className="text-xs text-gray-600">{relativeImpact.toFixed(1)}%</span>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Summary stats */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-blue-200 bg-blue-50">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">
                {topFeatures.length}
              </div>
              <div className="text-sm text-blue-800">Total Features Analyzed</div>
            </CardContent>
          </Card>
          
          <Card className="border-green-200 bg-green-50">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-600">
                {topFeatures[0]?.mean_abs_shap.toFixed(4) || "N/A"}
              </div>
              <div className="text-sm text-green-800">Highest SHAP Impact</div>
            </CardContent>
          </Card>
          
          <Card className="border-purple-200 bg-purple-50">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">
                {selectedFeatures}
              </div>
              <div className="text-sm text-purple-800">Features Displayed</div>
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  )
}