"use client"

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface ShapVisualizationProps {
  shapData: Array<{
    sample_id: string
    base_value: number
    shap_values: number[]
    data_values: number[]
  }>
  topFeatures: Array<{
    feature_name: string
    feature_index: number
    mean_abs_shap: number
  }>
  featureNames: string[]
}

export function ShapVisualization({ shapData, topFeatures, featureNames }: ShapVisualizationProps) {
  const [selectedSample, setSelectedSample] = React.useState<string>("")
  const [selectedFeatures, setSelectedFeatures] = React.useState<number>(20)

  // Prepare data for SHAP summary plot (similar to your image)
  const prepareSummaryData = () => {
    if (!shapData || shapData.length === 0) return []

    const topFeatureIndices = topFeatures.slice(0, selectedFeatures).map(f => f.feature_index)
    const plotData: any[] = []

    topFeatureIndices.forEach((featureIdx, reverseIdx) => {
      const featureName = featureNames[featureIdx] || `Feature_${featureIdx}`
      
      shapData.forEach((sample, sampleIdx) => {
        const shapValue = sample.shap_values[featureIdx]
        const featureValue = sample.data_values[featureIdx]
        
        plotData.push({
          feature: featureName,
          featureIndex: reverseIdx, // For y-axis positioning (reversed)
          shapValue: shapValue,
          featureValue: featureValue,
          sampleId: sample.sample_id,
          // Normalize feature value for color scale (0-1)
          normalizedValue: featureValue // You might want to normalize this based on min/max
        })
      })
    })

    return plotData
  }

  const summaryData = prepareSummaryData()

  // Custom color function based on feature value (high = red, low = blue)
  const getPointColor = (value: number, allValues: number[]) => {
    const min = Math.min(...allValues)
    const max = Math.max(...allValues)
    const normalized = (value - min) / (max - min)
    
    // Create color scale from blue (low) to red (high)
    const red = Math.round(255 * normalized)
    const blue = Math.round(255 * (1 - normalized))
    return `rgb(${red}, 0, ${blue})`
  }

  // Get unique feature values for color scaling
  const allFeatureValues = summaryData.map(d => d.featureValue)

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border rounded shadow-lg">
          <p className="font-medium">{`${data.feature}`}</p>
          <p className="text-sm">{`Sample: ${data.sampleId}`}</p>
          <p className="text-sm">{`SHAP value: ${data.shapValue.toFixed(4)}`}</p>
          <p className="text-sm">{`Feature value: ${data.featureValue.toFixed(4)}`}</p>
        </div>
      )
    }
    return null
  }

  if (!shapData || shapData.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>SHAP Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No SHAP data available</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>SHAP Summary Plot</CardTitle>
          <div className="flex gap-4 items-center">
            <div className="flex items-center gap-2">
              <label className="text-sm">Features:</label>
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
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-500 rounded"></div>
              <span className="text-xs">Low</span>
              <div className="w-4 h-4 bg-red-500 rounded"></div>
              <span className="text-xs">High</span>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-[600px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 150 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number" 
                dataKey="shapValue"
                domain={['dataMin', 'dataMax']}
                label={{ value: 'SHAP value (impact on model output)', position: 'insideBottom', offset: -10 }}
              />
              <YAxis 
                type="number"
                dataKey="featureIndex"
                domain={[0, selectedFeatures - 1]}
                tickFormatter={(value) => {
                  const featureIdx = topFeatures[value]?.feature_index
                  return featureNames[featureIdx] || `Feature_${featureIdx}`
                }}
                width={140}
              />
              <Tooltip content={<CustomTooltip />} />
              <Scatter data={summaryData} fill="#8884d8">
                {summaryData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={getPointColor(entry.featureValue, allFeatureValues)}
                  />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
        
        {/* Feature importance ranking */}
        <div className="mt-6">
          <h4 className="text-lg font-semibold mb-3">Top Features by Mean |SHAP|</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {topFeatures.slice(0, selectedFeatures).map((feature, idx) => (
              <div key={feature.feature_index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <span className="text-sm font-medium">{feature.feature_name}</span>
                <Badge variant="secondary">{feature.mean_abs_shap.toFixed(4)}</Badge>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}