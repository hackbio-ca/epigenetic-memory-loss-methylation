"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Search, Download, Filter } from "lucide-react"

// Mock sample data
const sampleData = [
  { id: "S001", riskScore: 0.89, riskLevel: "High", age: 72, sex: "F", confidence: 0.94 },
  { id: "S002", riskScore: 0.23, riskLevel: "Low", age: 65, sex: "M", confidence: 0.91 },
  { id: "S003", riskScore: 0.67, riskLevel: "Moderate", age: 78, sex: "F", confidence: 0.88 },
  { id: "S004", riskScore: 0.91, riskLevel: "High", age: 81, sex: "M", confidence: 0.96 },
  { id: "S005", riskScore: 0.15, riskLevel: "Low", age: 59, sex: "F", confidence: 0.89 },
  { id: "S006", riskScore: 0.45, riskLevel: "Moderate", age: 69, sex: "M", confidence: 0.85 },
  { id: "S007", riskScore: 0.78, riskLevel: "High", age: 75, sex: "F", confidence: 0.92 },
  { id: "S008", riskScore: 0.32, riskLevel: "Moderate", age: 63, sex: "M", confidence: 0.87 },
]

export function SampleAnalysis() {
  const [searchTerm, setSearchTerm] = useState("")
  const [filteredData, setFilteredData] = useState(sampleData)

  const handleSearch = (term: string) => {
    setSearchTerm(term)
    const filtered = sampleData.filter(
      (sample) =>
        sample.id.toLowerCase().includes(term.toLowerCase()) ||
        sample.riskLevel.toLowerCase().includes(term.toLowerCase()),
    )
    setFilteredData(filtered)
  }

  const getRiskBadgeVariant = (level: string) => {
    switch (level) {
      case "High":
        return "destructive"
      case "Moderate":
        return "secondary"
      case "Low":
        return "default"
      default:
        return "outline"
    }
  }

  const getRiskColor = (score: number) => {
    if (score >= 0.7) return "text-red-600"
    if (score >= 0.3) return "text-yellow-600"
    return "text-green-600"
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Individual Sample Analysis</CardTitle>
        <CardDescription>Detailed risk predictions for each sample in your dataset</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by sample ID or risk level..."
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button variant="outline" size="sm">
            <Filter className="mr-2 h-4 w-4" />
            Filter
          </Button>
          <Button variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
        </div>

        <div className="border rounded-lg">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Sample ID</TableHead>
                <TableHead>Risk Score</TableHead>
                <TableHead>Risk Level</TableHead>
                <TableHead>Age</TableHead>
                <TableHead>Sex</TableHead>
                <TableHead>Confidence</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredData.map((sample) => (
                <TableRow key={sample.id}>
                  <TableCell className="font-mono font-medium">{sample.id}</TableCell>
                  <TableCell>
                    <span className={`font-medium ${getRiskColor(sample.riskScore)}`}>
                      {(sample.riskScore * 100).toFixed(1)}%
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge variant={getRiskBadgeVariant(sample.riskLevel)}>{sample.riskLevel}</Badge>
                  </TableCell>
                  <TableCell>{sample.age}</TableCell>
                  <TableCell>{sample.sex}</TableCell>
                  <TableCell>
                    <span className="text-sm text-muted-foreground">{(sample.confidence * 100).toFixed(1)}%</span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <p>
            Showing {filteredData.length} of {sampleData.length} samples
          </p>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded-full" />
              <span>High Risk ({sampleData.filter((s) => s.riskLevel === "High").length})</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full" />
              <span>Moderate Risk ({sampleData.filter((s) => s.riskLevel === "Moderate").length})</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full" />
              <span>Low Risk ({sampleData.filter((s) => s.riskLevel === "Low").length})</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
