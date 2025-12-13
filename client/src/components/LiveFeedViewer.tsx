import React from 'react';
import { Camera } from 'lucide-react';
import { CameraData } from '@/types/type';
import { trafficLightApi } from '@/services/api';

interface LiveFeedViewerProps {
  camera: CameraData | null;
}

export const LiveFeedViewer: React.FC<LiveFeedViewerProps> = ({ camera }) => {
  if (!camera) {
    return (
      <div className="card shadow-sm border-0">
        <div className="card-body text-center py-5">
          <Camera size={64} className="text-muted mb-3" />
          <h5 className="text-muted">Chọn camera để xem trực tiếp</h5>
        </div>
      </div>
    );
  }

  const cameraStreamUrl = trafficLightApi.getCameraStream();

  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <div className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">{camera.name} - Trực tiếp</h5>
          <span className={`badge ${camera.status === 'active' ? 'bg-success' : 'bg-danger'}`}>
            {camera.status === 'active' ? 'LIVE' : 'OFFLINE'}
          </span>
        </div>
      </div>
      <div className="card-body">
        <div className="bg-dark rounded overflow-hidden" style={{ height: '450px' }}>
          {camera.status === 'active' ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img 
              src={cameraStreamUrl} 
              alt="Camera Live Stream"
              className="w-100 h-100"
              style={{ objectFit: 'cover' }}
              onError={(e) => {
                // Fallback nếu không load được ảnh
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
                target.parentElement?.classList.add('d-flex', 'align-items-center', 'justify-content-center');
              }}
            />
          ) : (
            <div className="text-center text-white-50 d-flex align-items-center justify-content-center h-100">
              <div>
                <Camera size={64} className="mb-3" />
                <p>Camera Offline</p>
              </div>
            </div>
          )}
        </div>
        <div className="mt-3">
          <div className="row g-2">
            <div className="col">
              <small className="text-muted d-block">Location</small>
              <div>{camera.location}</div>
            </div>
            <div className="col">
              <small className="text-muted d-block">Resolution</small>
              <div>416x416</div>
            </div>
            <div className="col">
              <small className="text-muted d-block">Frame Rate</small>
              <div>5 FPS</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};