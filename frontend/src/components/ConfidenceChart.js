import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js';

ChartJS.register(ArcElement, Tooltip);

export default function ConfidenceChart({ confidence }) {
  const data = {
    labels: ['Confidence', 'Remaining'],
    datasets: [{
      data: [confidence, 100 - confidence],
      backgroundColor: [
        confidence > 70 ? '#ef4444' : '#10b981',
        '#e5e7eb'
      ],
      borderWidth: 0
    }]
  };

  return (
    <div className="relative w-64 h-64 mx-auto">
      <Doughnut 
        data={data}
        options={{
          cutout: '70%',
          plugins: {
            legend: { display: false },
            tooltip: {
              displayColors: false,
              callbacks: {
                label: (ctx) => `${ctx.label}: ${ctx.raw}%`,
                title: () => null
              },
              bodyFont: {
                family: "'Inter', sans-serif",
                size: 14
              },
              padding: 10,
              backgroundColor: '#1f2937',
              cornerRadius: 4
            }
          }
        }}
      />
      <div 
        className="absolute inset-0 flex items-center justify-center"
        style={{ pointerEvents: 'none' }}
      >
        <span className="text-2xl font-bold text-gray-800">
          {confidence}%
        </span>
      </div>
    </div>
  );
}