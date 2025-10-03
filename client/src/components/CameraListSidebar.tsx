import React from 'react';
import { CameraData } from '@/types/type';

interface CameraListSidebarProps {
  cameras: CameraData[];
  selectedCamera: CameraData | null;
  onSelectCamera: (camera: CameraData) => void;
}

export const CameraListSidebar: React.FC<CameraListSidebarProps> = ({ 
  cameras, 
  selectedCamera, 
  onSelectCamera 
}) => {
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <h5 className="mb-0">Camera List</h5>
      </div>
      <div className="card-body p-0">
        <div className="list-group list-group-flush">
          {cameras.map(camera => (
            <button
              key={camera.id}
              className={`list-group-item list-group-item-action ${selectedCamera?.id === camera.id ? 'active' : ''}`}
              onClick={() => onSelectCamera(camera)}
            >
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <div className="fw-bold">{camera.name}</div>
                  <small className={selectedCamera?.id === camera.id ? 'text-white-50' : 'text-muted'}>
                    {camera.location}
                  </small>
                </div>
                <span className={`badge ${camera.status === 'active' ? 'bg-success' : 'bg-danger'}`}>
                  {camera.status === 'active' ? '●' : '○'}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
