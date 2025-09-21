
import React, { useState } from "react";
import { axiosInstance } from "@/lib/axios";

export default function ResultsPage() {
  const [studyName, setStudyName] = useState("");
  const [studyDescription, setStudyDescription] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiles(e.target.files);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResult("");
    if (!studyName.trim() || !files || files.length === 0) {
      setError("Please provide a study name and at least one CSV file.");
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("studyName", studyName);
      formData.append("studyDescription", studyDescription);
      Array.from(files).forEach((file, idx) => {
        formData.append(`file_${idx}`, file);
      });
      const res = await axiosInstance.post("/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(JSON.stringify(res.data, null, 2));
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: "2rem", maxWidth: 600, margin: "0 auto" }}>
      <h1>Alzheimer's Risk Analysis Results</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="studyName">Study Name *</label>
          <input
            id="studyName"
            type="text"
            value={studyName}
            onChange={(e) => setStudyName(e.target.value)}
            required
            style={{ width: "100%", padding: "0.5rem", marginTop: "0.5rem" }}
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="studyDescription">Study Description</label>
          <textarea
            id="studyDescription"
            value={studyDescription}
            onChange={(e) => setStudyDescription(e.target.value)}
            rows={3}
            style={{ width: "100%", padding: "0.5rem", marginTop: "0.5rem" }}
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="csvFiles">CSV File(s) *</label>
          <input
            id="csvFiles"
            type="file"
            accept=".csv"
            multiple
            onChange={handleFileChange}
            required
            style={{ marginTop: "0.5rem" }}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{ padding: "0.75rem 1.5rem", fontWeight: "bold", background: "#0070f3", color: "white", border: "none", borderRadius: "4px" }}
        >
          {loading ? "Analyzing..." : "Submit"}
        </button>
      </form>
      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>{error}</div>
      )}
      {result && (
        <pre style={{ background: "#f4f4f4", padding: "1rem", borderRadius: "8px" }}>
          {result}
        </pre>
      )}
    </main>
  );
}
