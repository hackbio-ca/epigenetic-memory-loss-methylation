"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Upload, FileText, CheckCircle, AlertCircle, X, Send } from "lucide-react"
import { axiosInstance } from "@/lib/axios"
import { AnalysisLoadingDialog } from "@/components/analysis-loading-dialog"

interface UploadedFile {
  name: string
  size: number
  type: string
  lastModified: number
  file: File
}

interface FileUploadSectionProps {
  onAnalysisComplete?: (result: any) => void
}

export function FileUploadSection({ onAnalysisComplete }: FileUploadSectionProps) {
  const [dragActive, setDragActive] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [studyName, setStudyName] = useState("")
  const [studyDescription, setStudyDescription] = useState("")
  const [error, setError] = useState("")
  const [loadingStage, setLoadingStage] = useState<'uploading' | 'processing' | 'analyzing' | 'finalizing'>('uploading')
  const [showLoadingDialog, setShowLoadingDialog] = useState(false)
  const [abortController, setAbortController] = useState<AbortController | null>(null)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    setError("")

    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    handleFiles(files)
  }

  const handleFiles = (files: File[]) => {
    if (files.length === 0) return

    const validFiles: UploadedFile[] = []
    let hasError = false

    files.forEach((file) => {
      // Validate file type
      if (!file.name.toLowerCase().endsWith(".csv")) {
        setError("Please upload CSV files containing methylation data.")
        hasError = true
        return
      }

      // Validate file size (max 100MB)
      if (file.size > 100 * 1024 * 1024) {
        setError("File size must be less than 100MB.")
        hasError = true
        return
      }

      validFiles.push({
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
        file,
      })
    })

    if (!hasError) {
      setUploadedFiles((prev) => [...prev, ...validFiles])
      setError("")
    }
  }

  const removeFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index))
    setUploadProgress(0)
  }

  const handleAnalyze = async () => {
    if (uploadedFiles.length === 0 || !studyName.trim()) {
      setError("Please provide a study name and upload at least one file.")
      return
    }

    // Immediately show loading dialog
    setShowLoadingDialog(true)
    setIsUploading(true)
    setError("")
    setUploadProgress(0)
    setLoadingStage('uploading')

    try {
      console.log("[v0] Starting analysis with backend integration points")

      // Prepare form data
      const formData = new FormData()
      formData.append("studyName", studyName)
      formData.append("studyDescription", studyDescription)
      uploadedFiles.forEach((file, index) => {
        formData.append(`file_${index}`, file.file)
      })

      // Stage 1: Uploading (0-25%)
      setLoadingStage('uploading')
      const uploadProgressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev < 25) return prev + 2
          return prev
        })
      }, 100)

      // Debug FormData contents
      console.log("=== FormData Debug ===")
      console.log("studyName:", formData.get("studyName"))
      console.log("studyDescription:", formData.get("studyDescription"))
      uploadedFiles.forEach((file, index) => {
        console.log(`file_${index}:`, formData.get(`file_${index}`))
      })

      // Start the API call
      const apiPromise = axiosInstance.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      // Stage 2: Processing (25-50%)
      setTimeout(() => {
        setLoadingStage('processing')
        setUploadProgress(25)
        const processingInterval = setInterval(() => {
          setUploadProgress((prev) => {
            if (prev < 50) return prev + 1
            clearInterval(processingInterval)
            return prev
          })
        }, 150)
      }, 1000)

      // Stage 3: Analyzing (50-85%)
      setTimeout(() => {
        setLoadingStage('analyzing')
        setUploadProgress(50)
        const analyzingInterval = setInterval(() => {
          setUploadProgress((prev) => {
            if (prev < 85) return prev + 1
            clearInterval(analyzingInterval)
            return prev
          })
        }, 100)
      }, 3000)

      // Stage 4: Finalizing (85-95%)
      setTimeout(() => {
        setLoadingStage('finalizing')
        setUploadProgress(85)
        const finalizingInterval = setInterval(() => {
          setUploadProgress((prev) => {
            if (prev < 95) return prev + 0.5
            clearInterval(finalizingInterval)
            return prev
          })
        }, 200)
      }, 8000)

      // Wait for API response
      const res = await apiPromise

      console.log("Upload response:", res.data)

      // Clear all intervals
      clearInterval(uploadProgressInterval)
      
      // Complete progress
      setUploadProgress(100)

      // Debug: Log the full response
      console.log('API Response:', res.data)
      console.log('SHAP Analysis:', res.data?.shap_analysis)

      // Small delay to show completion
      await new Promise(resolve => setTimeout(resolve, 500))

      // Hide loading dialog
      setShowLoadingDialog(false)

      // Call the callback with the API response
      if (onAnalysisComplete) {
        onAnalysisComplete(res.data)
      }

      // Reset form after a short delay
      setTimeout(() => {
        setUploadedFiles([])
        setStudyName("")
        setStudyDescription("")
        setUploadProgress(0)
      }, 1000)

    } catch (err) {
      // Hide loading dialog on error
      setShowLoadingDialog(false)
      setError(err instanceof Error ? err.message : "Analysis failed. Please try again.")
      setUploadProgress(0)
    } finally {
      setIsUploading(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5 text-primary" />
          Upload Methylation Data
        </CardTitle>
        <CardDescription>
          Upload single or multiple CSV files containing DNA methylation profiles for Alzheimer's risk analysis
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Study Information */}
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="studyName">Study Name *</Label>
            <Input
              id="studyName"
              placeholder="e.g., Alzheimer's Cohort Study 2024"
              value={studyName}
              onChange={(e) => setStudyName(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="studyDescription">Study Description</Label>
            <Textarea
              id="studyDescription"
              placeholder="Brief description of the study, sample characteristics, and methodology..."
              value={studyDescription}
              onChange={(e) => setStudyDescription(e.target.value)}
              rows={3}
            />
          </div>
        </div>

        {/* File Upload Area */}
        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".csv"
            multiple
            onChange={handleFileInput}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />

          {uploadedFiles.length === 0 ? (
            <div className="space-y-4">
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                <Upload className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-lg font-medium text-foreground">Drop your CSV files here, or click to browse</p>
                <p className="text-sm text-muted-foreground mt-1">Supports multiple CSV files up to 100MB each</p>
              </div>
              <div className="text-xs text-muted-foreground">
                <p>Expected format: CpG sites as columns, samples as rows</p>
                <p>Include sample IDs and methylation beta values (0-1)</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="space-y-2">
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-center gap-3 p-3 bg-secondary rounded-lg">
                    <FileText className="h-6 w-6 text-primary" />
                    <div className="text-left flex-1">
                      <p className="font-medium text-foreground">{file.name}</p>
                      <p className="text-sm text-muted-foreground">{formatFileSize(file.size)} • CSV file</p>
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => removeFile(index)}>
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>

              {isUploading && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Processing {uploadedFiles.length} file(s)...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                </div>
              )}
            </div>
          )}
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* File Requirements */}
        <div className="bg-secondary rounded-lg p-4">
          <h4 className="font-medium text-foreground mb-2">File Requirements:</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• CSV format with methylation beta values (0-1 range)</li>
            <li>• First column: Sample IDs</li>
            <li>• Subsequent columns: CpG site methylation values</li>
            <li>• Header row with CpG site identifiers (e.g., cg00000029)</li>
            <li>• Maximum file size: 100MB per file</li>
          </ul>
        </div>

        {/* Action Button */}
        <Button
          onClick={handleAnalyze}
          disabled={uploadedFiles.length === 0 || !studyName.trim() || isUploading}
          className="w-full"
          size="lg"
        >
          {isUploading ? (
            <>
              <CheckCircle className="mr-2 h-4 w-4" />
              Processing Analysis...
            </>
          ) : (
            <>
              <Send className="mr-2 h-4 w-4" />
              Start Alzheimer's Risk Analysis ({uploadedFiles.length} file{uploadedFiles.length !== 1 ? "s" : ""})
            </>
          )}
        </Button>
      </CardContent>

      {/* Loading Dialog */}
      <AnalysisLoadingDialog
        isOpen={showLoadingDialog}
        onOpenChange={setShowLoadingDialog}
        progress={uploadProgress}
        stage={loadingStage}
        fileName={uploadedFiles[0]?.name}
        fileCount={uploadedFiles.length}
      />
    </Card>
  )
}
