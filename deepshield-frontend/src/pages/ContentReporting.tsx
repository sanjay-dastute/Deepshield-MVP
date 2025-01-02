import React, { useState } from 'react';
import axios from 'axios';

export const ContentReporting: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/v1/content/analyze`, formData);
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing content:', error);
      setResult({ error: 'Failed to analyze content' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Content Analysis</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-2">Upload Media for Analysis:</label>
          <input
            type="file"
            onChange={handleFileChange}
            accept="image/*,video/*"
            className="border p-2 rounded"
          />
        </div>
        <button
          type="submit"
          disabled={!file || loading}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze Content'}
        </button>
      </form>

      {result && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-4">Analysis Results:</h2>
          <pre className="bg-gray-100 p-4 rounded">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
