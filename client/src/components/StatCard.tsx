import React from 'react';

interface StatCardProps {
  title: string;
  value: string;
  total?: string;
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning';
  subtitle?: string;
  progress?: number;
}

export const StatCard: React.FC<StatCardProps> = ({ 
  title, 
  value, 
  total, 
  icon, 
  color, 
  subtitle, 
  progress 
}) => {
  return (
    <div className="card shadow-sm border-0 h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <h6 className="text-muted mb-1">{title}</h6>
            <h2 className="mb-0">
              {value}
              {total && <span className="fs-5 text-muted">/{total}</span>}
            </h2>
          </div>
          <div className={`bg-${color} bg-opacity-10 p-3 rounded`}>
            {icon}
          </div>
        </div>
        {progress !== undefined && (
          <div className="progress mt-3" style={{ height: '6px' }}>
            <div className={`progress-bar bg-${color}`} style={{ width: `${progress}%` }} />
          </div>
        )}
        {subtitle && <small className="text-muted mt-2 d-block">{subtitle}</small>}
      </div>
    </div>
  );
};
