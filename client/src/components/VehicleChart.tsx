import React from 'react';
import { VehicleStats } from '@/types/type';

interface VehicleChartProps {
  data: VehicleStats[];
}

export const VehicleChart: React.FC<VehicleChartProps> = ({ data }) => {
  const maxCount = Math.max(...data.map(s => s.count));
  
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <h5 className="mb-0">Vehicle Count - Last 7 Days</h5>
      </div>
      <div className="card-body">
        <div className="d-flex align-items-end justify-content-between" style={{ height: '200px' }}>
          {data.map((stat, idx) => (
            <div key={idx} className="d-flex flex-column align-items-center" style={{ flex: 1 }}>
              <small className="mb-2 fw-bold">{stat.count.toLocaleString()}</small>
              <div 
                className="bg-primary rounded-top w-75"
                style={{ 
                  height: `${(stat.count / maxCount) * 150}px`,
                  transition: 'height 0.3s'
                }}
              />
              <small className="mt-2 text-muted">
                {new Date(stat.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </small>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};