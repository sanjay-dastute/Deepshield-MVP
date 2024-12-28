import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface User {
  id: string;
  email: string;
  role: string;
  isVerified: boolean;
  createdAt: string;
}

interface ContentFlag {
  id: string;
  type: string;
  reason: string;
  severity: string;
  status: string;
  createdAt: string;
}

const AdminPanel: React.FC = () => {
  const { user } = useAuth();
  // Use user object for admin verification
  console.log("Admin user:", user);
  const [users, setUsers] = useState<User[]>([]);
  const [flags, setFlags] = useState<ContentFlag[]>([]);
  const [activeTab, setActiveTab] = useState<'users' | 'flags'>('users');

  useEffect(() => {
    fetchUsers();
    fetchFlags();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/v1/admin/users');
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchFlags = async () => {
    try {
      const response = await fetch('/api/v1/admin/flags');
      if (response.ok) {
        const data = await response.json();
        setFlags(data);
      }
    } catch (error) {
      console.error('Error fetching flags:', error);
    }
  };

  const handleVerifyUser = async (userId: string) => {
    try {
      const response = await fetch(`/api/v1/admin/users/${userId}/verify`, {
        method: 'POST',
      });
      if (response.ok) {
        fetchUsers(); // Refresh user list
      }
    } catch (error) {
      console.error('Error verifying user:', error);
    }
  };

  const handleUpdateFlagStatus = async (flagId: string, status: string) => {
    try {
      const response = await fetch(`/api/v1/admin/flags/${flagId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });
      if (response.ok) {
        fetchFlags(); // Refresh flags list
      }
    } catch (error) {
      console.error('Error updating flag status:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Admin Panel</h1>
      
      <div className="mb-6">
        <div className="flex space-x-4">
          <button
            className={`px-4 py-2 rounded ${
              activeTab === 'users' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setActiveTab('users')}
          >
            Users
          </button>
          <button
            className={`px-4 py-2 rounded ${
              activeTab === 'flags' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
            onClick={() => setActiveTab('flags')}
          >
            Content Flags
          </button>
        </div>
      </div>

      {activeTab === 'users' && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">User Management</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300">
              <thead>
                <tr>
                  <th className="px-6 py-3 border-b">Email</th>
                  <th className="px-6 py-3 border-b">Role</th>
                  <th className="px-6 py-3 border-b">Status</th>
                  <th className="px-6 py-3 border-b">Created At</th>
                  <th className="px-6 py-3 border-b">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="px-6 py-4 border-b">{user.email}</td>
                    <td className="px-6 py-4 border-b">{user.role}</td>
                    <td className="px-6 py-4 border-b">
                      {user.isVerified ? 'Verified' : 'Pending'}
                    </td>
                    <td className="px-6 py-4 border-b">
                      {new Date(user.createdAt).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 border-b">
                      {!user.isVerified && (
                        <button
                          className="bg-green-500 text-white px-3 py-1 rounded"
                          onClick={() => handleVerifyUser(user.id)}
                        >
                          Verify
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'flags' && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">Content Flags</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300">
              <thead>
                <tr>
                  <th className="px-6 py-3 border-b">Type</th>
                  <th className="px-6 py-3 border-b">Reason</th>
                  <th className="px-6 py-3 border-b">Severity</th>
                  <th className="px-6 py-3 border-b">Status</th>
                  <th className="px-6 py-3 border-b">Created At</th>
                  <th className="px-6 py-3 border-b">Actions</th>
                </tr>
              </thead>
              <tbody>
                {flags.map((flag) => (
                  <tr key={flag.id}>
                    <td className="px-6 py-4 border-b">{flag.type}</td>
                    <td className="px-6 py-4 border-b">{flag.reason}</td>
                    <td className="px-6 py-4 border-b">{flag.severity}</td>
                    <td className="px-6 py-4 border-b">{flag.status}</td>
                    <td className="px-6 py-4 border-b">
                      {new Date(flag.createdAt).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 border-b">
                      <select
                        className="border rounded px-2 py-1"
                        value={flag.status}
                        onChange={(e) =>
                          handleUpdateFlagStatus(flag.id, e.target.value)
                        }
                      >
                        <option value="pending">Pending</option>
                        <option value="reviewing">Reviewing</option>
                        <option value="resolved">Resolved</option>
                        <option value="dismissed">Dismissed</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
