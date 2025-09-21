"use client"

import React from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Progress } from "@/components/ui/progress"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Brain, FileText, BarChart3, TrendingUp, Loader2 } from "lucide-react"

interface AnalysisLoadingDialogProps {
  isOpen: boolean
  onOpenChange: (open: boolean) => void
  progress: number
  stage: 'uploading' | 'processing' | 'analyzing' | 'finalizing'
  fileName?: string
  fileCount?: number
  onCancel?: () => void
}

const stages = {
  uploading: {
    title: "Uploading Files",
    description: "Securely transferring your methylation data...",
    icon: FileText,
    color: "text-blue-500"
  },
  processing: {
    title: "Processing Data", 
    description: "Validating and preparing methylation profiles...",
    icon: Brain,
    color: "text-purple-500"
  },
  analyzing: {
    title: "AI Analysis",
    description: "Running machine learning models and SHAP analysis...",
    icon: BarChart3,
    color: "text-green-500"
  },
  finalizing: {
    title: "Generating Results",
    description: "Creating visualizations and feature importance rankings...",
    icon: TrendingUp,
    color: "text-orange-500"
  }
}

export function AnalysisLoadingDialog({ 
  isOpen, 
  onOpenChange, 
  progress, 
  stage,
  fileName,
  fileCount = 1,
  onCancel
}: AnalysisLoadingDialogProps) {
  const currentStage = stages[stage]
  const StageIcon = currentStage.icon

  // Prevent closing during analysis by only allowing close when progress is 100%
  const handleOpenChange = (open: boolean) => {
    if (!open && progress < 100) {
      // Don't allow closing during analysis
      return
    }
    onOpenChange(open)
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent 
        className="sm:max-w-[500px]" 
        aria-describedby="loading-description"
        // Hide close button during analysis
        showCloseButton={progress >= 100}
      >
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <div className={`p-2 rounded-full bg-primary/10 ${currentStage.color}`}>
              <StageIcon className="h-5 w-5" />
            </div>
            {currentStage.title}
          </DialogTitle>
          <DialogDescription id="loading-description">
            {currentStage.description}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Overall Progress</span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {/* File Info */}
          {fileName && (
            <div className="flex items-center gap-3 p-3 bg-secondary/50 rounded-lg">
              <FileText className="h-4 w-4 text-muted-foreground" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{fileName}</p>
                <p className="text-xs text-muted-foreground">
                  {fileCount === 1 ? "Single file analysis" : `${fileCount} files being processed`}
                </p>
              </div>
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
            </div>
          )}

          {/* Stage Progress Indicators */}
          <div className="grid grid-cols-4 gap-2">
            {Object.entries(stages).map(([key, stageInfo], index) => {
              const isActive = key === stage
              const isCompleted = Object.keys(stages).indexOf(key) < Object.keys(stages).indexOf(stage)
              const StageIconComponent = stageInfo.icon
              
              return (
                <div
                  key={key}
                  className={`flex flex-col items-center gap-1 p-2 rounded-lg transition-colors ${
                    isActive 
                      ? 'bg-primary/10 border border-primary/20' 
                      : isCompleted 
                        ? 'bg-green-50 text-green-600' 
                        : 'bg-secondary/30 text-muted-foreground'
                  }`}
                >
                  <StageIconComponent className={`h-4 w-4 ${
                    isActive 
                      ? stageInfo.color 
                      : isCompleted 
                        ? 'text-green-600'
                        : 'text-muted-foreground'
                  }`} />
                  <span className="text-xs font-medium text-center">
                    {stageInfo.title.split(' ')[0]}
                  </span>
                </div>
              )
            })}
          </div>

          {/* Analysis Preview Skeleton */}
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Skeleton className="h-4 w-4 rounded-full" />
                <Skeleton className="h-4 w-32" />
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="space-y-2">
                <Skeleton className="h-3 w-full" />
                <Skeleton className="h-3 w-4/5" />
                <Skeleton className="h-3 w-3/5" />
              </div>
              <div className="grid grid-cols-3 gap-3">
                <Skeleton className="h-16 w-full" />
                <Skeleton className="h-16 w-full" />
                <Skeleton className="h-16 w-full" />
              </div>
            </CardContent>
          </Card>

          {/* Estimated Time & Cancel */}
          <div className="text-center p-4 bg-blue-50/50 rounded-lg border border-blue-100">
            <p className="text-sm text-blue-700 font-medium">
              🧬 Processing your methylation data...
            </p>
            <p className="text-xs text-blue-600 mt-1">
              This may take 2-5 minutes depending on file size and complexity
            </p>
            
            {/* Cancel button only during early stages */}
            {(stage === 'uploading' || stage === 'processing') && onCancel && progress < 50 && (
              <div className="mt-3">
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={onCancel}
                  className="text-xs"
                >
                  Cancel Analysis
                </Button>
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}