// Simple test to verify the loading dialog component works
import { AnalysisLoadingDialog } from "@/components/analysis-loading-dialog"

export function LoadingTest() {
  return (
    <AnalysisLoadingDialog
      isOpen={true}
      onOpenChange={() => {}}
      progress={45}
      stage="analyzing"
      fileName="test_methylation_data.csv"
      fileCount={3}
    />
  )
}