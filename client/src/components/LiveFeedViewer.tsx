import React from 'react';
import { Camera, Video } from 'lucide-react';
import { CameraData } from '@/types/type';

interface LiveFeedViewerProps {
  camera: CameraData | null;
}

export const LiveFeedViewer: React.FC<LiveFeedViewerProps> = ({ camera }) => {
  if (!camera) {
    return (
      <div className="card shadow-sm border-0">
        <div className="card-body text-center py-5">
          <Camera size={64} className="text-muted mb-3" />
          <h5 className="text-muted">Select a camera to view live feed</h5>
        </div>
      </div>
    );
  }

  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <div className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">{camera.name} - Live Feed</h5>
          <span className={`badge ${camera.status === 'active' ? 'bg-success' : 'bg-danger'}`}>
            {camera.status === 'active' ? 'LIVE' : 'OFFLINE'}
          </span>
        </div>
      </div>
      <div className="card-body">
        <div className="bg-dark rounded d-flex align-items-center justify-content-center" style={{ height: '450px' }}>
          {camera.status === 'active' ? (
            <div className="text-center text-white">
              <Video size={64} className="mb-3 opacity-50" />
              <p className="mb-1">Live Stream</p>
              <small className="text-white-50">{camera.streamUrl}</small>
              <div className="mt-3">
                <small className="text-white-50">Resolution: {camera.resolution} @ {camera.fps} FPS</small>
              </div>
            </div>
          ) : (
            <div className="text-center text-white-50">
              <Camera size={64} className="mb-3" />
              <p>Camera Offline</p>
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
              <div>{camera.resolution}</div>
            </div>
            <div className="col">
              <small className="text-muted d-block">Frame Rate</small>
              <div>{camera.fps} FPS</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};