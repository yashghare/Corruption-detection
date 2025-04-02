// src/services/api.js
const API_BASE = 'http://localhost:8000';

export const checkApiHealth = async () => {
  const response = await fetch(`${API_BASE}/api/test`);
  return await response.json();
};

export const detectFraud = async (transactionData) => {
  const response = await fetch(`${API_BASE}/api/detect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(transactionData)
  });
  return await response.json();
};

export const testConnection = async () => {
    console.log("[API] Attempting to connect to /api/test");  // 👈 Log start
    try {
      const response = await fetch('http://localhost:8000/api/test');
      console.log("[API] Response status:", response.status); // 👈 Log status
      
      if (!response.ok) {
        console.error("[API] Error status:", response.status);
        throw new Error('API connection failed');
      }
      
      const data = await response.json();
      console.log("[API] Successful response:", data);  // 👈 Log success
      return data;
      
    } catch (error) {
      console.error("[API] Connection failed:", error);  // 👈 Log failure
      throw error;
    }
  };