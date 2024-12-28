import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface FlaggedItem {
  id: string;
  type: string;
  content: string;
  reason: string;
  timestamp: string;
  status: string;
}

export const FlaggedContent: React.FC = () => {
  const [flaggedItems, setFlaggedItems] = useState<FlaggedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFlaggedContent = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/v1/content/flagged`);
        setFlaggedItems(response.data);
      } catch (err) {
        setError('Failed to fetch flagged content');
        console.error('Error fetching flagged content:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchFlaggedContent();
  }, []);

  const handleStatusUpdate = async (id: string, newStatus: string) => {
    try {
      await axios.patch(`${import.meta.env.VITE_API_URL}/api/v1/content/${id}/status`, {
        status: newStatus
      });
      setFlaggedItems(items =>
        items.map(item =>
          item.id === id ? { ...item, status: newStatus } : item
        )
      );
    } catch (err) {
      console.error('Error updating content status:', err);
      setError('Failed to update content status');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Flagged Content</h1>
      <div className="space-y-4">
        {flaggedItems.length === 0 ? (
          <p>No flagged content found.</p>
        ) : (
          flaggedItems.map(item => (
            <div key={item.id} className="border p-4 rounded">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">{item.type}</h3>
                  <p className="text-sm text-gray-600">Reason: {item.reason}</p>
                  <p className="text-sm text-gray-600">
                    Date: {new Date(item.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="space-x-2">
                  <button
                    onClick={() => handleStatusUpdate(item.id, 'resolved')}
                    className="bg-green-500 text-white px-3 py-1 rounded"
                    disabled={item.status === 'resolved'}
                  >
                    Resolve
                  </button>
                  <button
                    onClick={() => handleStatusUpdate(item.id, 'rejected')}
                    className="bg-red-500 text-white px-3 py-1 rounded"
                    disabled={item.status === 'rejected'}
                  >
                    Reject
                  </button>
                </div>
              </div>
              <div className="mt-2">
                <p className="text-sm">{item.content}</p>
              </div>
              <div className="mt-2">
                <span className={`text-sm px-2 py-1 rounded ${
                  item.status === 'resolved' ? 'bg-green-100 text-green-800' :
                  item.status === 'rejected' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {item.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
