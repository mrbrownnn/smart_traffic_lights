import React from 'react';
import { TrafficLight } from '@/types/type';

interface TrafficLightStatusListProps {
  trafficLights: TrafficLight[];
}

export const TrafficLightStatusList: React.FC<TrafficLightStatusListProps> = ({ trafficLights }) => {
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <h5 className="mb-0">🚦 Trạng thái đèn giao thông</h5>
      </div>
      <div className="card-body p-0">
        <div className="list-group list-group-flush">
          {trafficLights.map(light => (
            <div key={light.id} className="list-group-item">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="mb-1">
                    <span className="badge bg-primary me-2">#{light.id}</span>
                    {light.location}
                  </h6>
                  {light.vehicles !== null && (
                    <small className="text-muted">
                      🚗 {light.vehicles} xe đang chờ
                    </small>
                  )}
                </div>
                <div className="text-end">
                  <div className="mb-1">
                    <span className="badge bg-success">🟢 {light.greenTime}s</span>
                  </div>
                  <div>
                    <small className="text-muted">
                      🔴 {light.redTime}s | 🟡 {light.yellowTime}s
                    </small>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};