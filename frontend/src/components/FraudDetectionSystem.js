import { useState } from 'react';
import axios from 'axios';
import ConfidenceChart from './ConfidenceChart';
import ExportButton from './ExportButton';

export default function FraudDetectionSystem() {
  const [formData, setFormData] = useState({
    transactionId: '',
    amount: '',
    department: 'health',
    supplier: '',
    officerId: '',
    contractDuration: '12',
    biddingProcess: 'open',
    numBidders: '3',
    winningBidRatio: '0.85',
    previousContracts: '0',
    officerTenure: '2'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.endsWith('Ratio') || name.endsWith('Duration') || 
              name.endsWith('Bidders') || name.endsWith('Contracts') ||
              name.endsWith('Tenure') ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/detect-fraud', {
        transaction_id: formData.transactionId,
        amount: Number(formData.amount),
        department: formData.department,
        supplier: formData.supplier,
        officer_id: formData.officerId,
        contract_duration: formData.contractDuration,
        bidding_process: formData.biddingProcess,
        num_bidders: formData.numBidders,
        winning_bid_ratio: formData.winningBidRatio,
        previous_contracts: formData.previousContracts,
        officer_tenure: formData.officerTenure
      });
      
      setResult(response.data);
    } catch (error) {
      console.error('Detection error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-1 bg-gradient-to-r from-blue-500 to-blue-700"></div>
        
        <div className="p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Fraud Detection Analysis</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Basic Transaction Info */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-700 border-b pb-2">Transaction Details</h3>
                <FormField label="Transaction ID" name="transactionId" value={formData.transactionId} onChange={handleChange} required />
                <FormField label="Amount ($)" name="amount" type="number" value={formData.amount} onChange={handleChange} required min="0" step="0.01" />
                <FormField label="Department" name="department" type="select" value={formData.department} onChange={handleChange} options={['health', 'education', 'defense', 'infrastructure']} />
                <FormField label="Supplier" name="supplier" value={formData.supplier} onChange={handleChange} />
              </div>

              {/* Procurement Metadata */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-700 border-b pb-2">Procurement Parameters</h3>
                <FormField label="Officer ID" name="officerId" value={formData.officerId} onChange={handleChange} />
                <FormField label="Contract Duration (months)" name="contractDuration" type="number" value={formData.contractDuration} onChange={handleChange} min="1" />
                <FormField label="Bidding Process" name="biddingProcess" type="select" value={formData.biddingProcess} onChange={handleChange} options={['open', 'restricted', 'direct', 'negotiated']} />
                <FormField label="Number of Bidders" name="numBidders" type="number" value={formData.numBidders} onChange={handleChange} min="1" />
              </div>

              {/* Advanced Parameters */}
              <div className="space-y-4 md:col-span-2">
                <h3 className="font-semibold text-gray-700 border-b pb-2">Advanced Metrics</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <FormField label="Winning Bid Ratio" name="winningBidRatio" type="number" value={formData.winningBidRatio} onChange={handleChange} min="0" max="1" step="0.01" />
                  <FormField label="Previous Contracts with Supplier" name="previousContracts" type="number" value={formData.previousContracts} onChange={handleChange} min="0" />
                  <FormField label="Officer Tenure (years)" name="officerTenure" type="number" value={formData.officerTenure} onChange={handleChange} min="0" />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-6 rounded-lg font-medium text-white ${
                loading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
              } transition-colors shadow-md`}
            >
              {loading ? 'Analyzing Transaction...' : 'Submit for Fraud Analysis'}
            </button>
          </form>

          {result && (
            <div className="mt-8 space-y-6">
              <div className="border-b border-gray-200 pb-4">
                <h2 className="text-xl font-bold text-gray-800">Risk Assessment Results</h2>
              </div>
              
              <div className="grid md:grid-cols-2 gap-8">
                <ConfidenceChart confidence={result.confidence * 100} />
                
                <div className="space-y-4">
                  <RiskBadge isFraud={result.is_fraud} confidence={result.confidence} />
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-medium text-gray-700 mb-2">Transaction Summary</h3>
                    <DetailRow label="Transaction ID" value={result.transaction_id} />
                    <DetailRow label="Amount" value={`$${result.amount}`} />
                    <DetailRow label="Department" value={result.department} />
                  </div>
                  
                  {result.risk_factors?.length > 0 && (
                    <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                      <h3 className="font-medium text-red-700 mb-2">Identified Risk Factors</h3>
                      <ul className="space-y-2">
                        {result.risk_factors.map((factor, i) => (
                          <li key={i} className="flex items-start">
                            <span className="text-red-500 mr-2">•</span>
                            <span className="text-gray-700">{factor}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
              
              <ExportButton data={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Enhanced FormField Component (supports multiple input types)
const FormField = ({ label, type = 'text', options, ...props }) => (
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
    {type === 'select' ? (
      <select
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        {...props}
      >
        {options.map(option => (
          <option key={option} value={option}>
            {option.charAt(0).toUpperCase() + option.slice(1)}
          </option>
        ))}
      </select>
    ) : (
      <input
        type={type}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        {...props}
      />
    )}
  </div>
);

// Enhanced RiskBadge Component
const RiskBadge = ({ isFraud, confidence }) => (
  <div className={`p-3 rounded-lg ${
    isFraud ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
  }`}>
    <div className="flex justify-between items-center">
      <span className="font-medium">
        {isFraud ? 'High Risk Transaction' : 'Low Risk Transaction'}
      </span>
      <span className="text-sm">
        Confidence: {Math.round(confidence * 100)}%
      </span>
    </div>
  </div>
);

const DetailRow = ({ label, value }) => (
  <div className="flex justify-between py-2 border-b border-gray-100 last:border-0">
    <span className="text-gray-500">{label}</span>
    <span className="font-medium">{value}</span>
  </div>
);