import { useState } from 'react';
import FraudDetectionSystem from './FraudDetectionSystem';
import { ArrowRightIcon, DocumentChartBarIcon, ChartPieIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';

export default function HomePage() {
  const [showDetection, setShowDetection] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Hero Section */}
      <div className="relative bg-blue-700 text-white py-20 px-4 text-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-800/10 to-blue-600/10"></div>
      <div className="relative max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
            Advanced <span className="text-blue-300">Fraud Detection</span> Platform
          </h1>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            AI-powered transaction analysis with real-time risk assessment
          </p>
          <button
            onClick={() => setShowDetection(!showDetection)}
            className="px-8 py-4 bg-white text-blue-700 rounded-xl font-bold text-lg
                     hover:bg-blue-50 transition-all shadow-lg hover:shadow-xl
                     flex items-center gap-2 mx-auto"
          >
            {showDetection ? (
              <>
                <ArrowDownTrayIcon className="h-5 w-5" />
                Hide Analysis Panel
              </>
            ) : (
              <>
                <ArrowRightIcon className="h-5 w-5" />
                Launch Detection Tool
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {showDetection ? (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="p-1 bg-gradient-to-r from-blue-500 to-blue-700"></div>
            <div className="p-8">
              <FraudDetectionSystem />
            </div>
          </div>
        ) : (
          <>
            <div className="text-center mb-16">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Key Features</h2>
              <div className="w-24 h-1 bg-blue-600 mx-auto"></div>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <FeatureCard 
                icon={<DocumentChartBarIcon className="h-10 w-10 text-blue-600" />}
                title="Comprehensive Analysis"
                description="Deep transaction scanning with machine learning models"
              />
              <FeatureCard 
                icon={<ChartPieIcon className="h-10 w-10 text-blue-600" />}
                title="Visual Analytics"
                description="Interactive dashboards with confidence metrics"
              />
              <FeatureCard 
                icon={<ArrowDownTrayIcon className="h-10 w-10 text-blue-600" />}
                title="Export Ready"
                description="Generate audit-ready PDF/CSV reports"
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

const FeatureCard = ({ icon, title, description }) => (
  <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
    <div className="flex items-center justify-center h-12 w-12 rounded-full bg-blue-50 mb-4">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);