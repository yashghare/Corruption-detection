// src/components/DetectionForm.jsx
import { useState } from 'react';

export default function DetectionForm() {
  const [formData, setFormData] = useState({
    transaction_id: '',
    amount: 0,
    department: 'health'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    const result = await response.json();
    console.log('Detection Result:', result);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="Transaction ID"
        value={formData.transaction_id}
        onChange={(e) => setFormData({...formData, transaction_id: e.target.value})}
        className="block w-full p-2 border rounded"
      />
      <input
        type="number"
        placeholder="Amount"
        value={formData.amount}
        onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value)})}
        className="block w-full p-2 border rounded"
      />
      <select
        value={formData.department}
        onChange={(e) => setFormData({...formData, department: e.target.value})}
        className="block w-full p-2 border rounded"
      >
        <option value="health">Health</option>
        <option value="education">Education</option>
      </select>
      <button 
        type="submit" 
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Detect Fraud
      </button>
    </form>
  );
}