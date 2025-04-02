// src/components/FraudDetector.jsx
import { useState, useEffect } from 'react';
import { checkApiHealth, detectFraud } from '../services/api';

export default function FraudDetector() {
  const [apiStatus, setApiStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    checkApiHealth()
      .then(data => setApiStatus(data))
      .catch(err => setApiStatus({ status: 'error', message: err.message }));
  }, []);

  const handleSubmit = async (formData) => {
    setLoading(true);
    try {
      const detectionResult = await detectFraud(formData);
      setResult(detectionResult);
    } catch (error) {
      console.error('Detection failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Fraud Detection System</h2>
      
      <div className="mb-6 p-4 bg-blue-50 rounded">
        <h3 className="font-semibold">API Status:</h3>
        <pre className="text-sm mt-2">{JSON.stringify(apiStatus, null, 2)}</pre>
      </div>

      {/* Your fraud detection form would go here */}
      {loading && <p>Analyzing transaction...</p>}
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-semibold">Detection Result:</h3>
          <pre className="text-sm mt-2">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}