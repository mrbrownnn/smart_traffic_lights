import React from 'react';
import { TrafficLight } from '@/types/type';

interface TrafficLightStatusListProps {
  trafficLights: TrafficLight[];
}

export const TrafficLightStatusList: React.FC<TrafficLightStatusListProps> = ({ trafficLights }) => {
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <h5 className="mb-0">Traffic Light Status</h5>
      </div>
      <div className="card-body p-0">
        <div className="list-group list-group-flush">
          {trafficLights.map(light => (
            <div key={light.id} className="list-group-item">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="mb-1">Traffic Light {light.id}</h6>
                  <small className="text-muted">{light.location}</small>
                </div>
                <div>
                  <span className={`badge ${light.status === 'active' ? 'bg-success' : 'bg-danger'} me-1`}>
                    {light.status}
                  </span>
                  <span className="badge bg-secondary">{light.mode}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};