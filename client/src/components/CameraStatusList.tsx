import React from 'react';
import { CameraData } from '@/types/type';

interface CameraStatusListProps {
  cameras: CameraData[];
}

export const CameraStatusList: React.FC<CameraStatusListProps> = ({ cameras }) => {
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <h5 className="mb-0">Camera Status</h5>
      </div>
      <div className="card-body p-0">
        <div className="list-group list-group-flush">
          {cameras.map(camera => (
            <div key={camera.id} className="list-group-item">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="mb-1">{camera.name}</h6>
                  <small className="text-muted">{camera.location}</small>
                </div>
                <span className={`badge ${camera.status === 'active' ? 'bg-success' : 'bg-danger'}`}>
                  {camera.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
