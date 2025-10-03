import React from 'react';
import { CameraData } from '@/types/type';

interface CameraSettingsCardProps {
  camera: CameraData;
  onUpdate: <K extends keyof CameraData>(id: number, field: K, value: CameraData[K]) => void;
}

export const CameraSettingsCard: React.FC<CameraSettingsCardProps> = ({ camera, onUpdate }) => {
  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white">
        <div className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">{camera.name}</h5>
          <span className={`badge ${camera.status === 'active' ? 'bg-success' : 'bg-danger'}`}>
            {camera.status}
          </span>
        </div>
        <small className="text-muted">{camera.location}</small>
      </div>
      <div className="card-body">
        <div className="mb-3">
          <label className="form-label">Resolution</label>
          <select 
            className="form-select"
            value={camera.resolution}
            onChange={(e) => onUpdate(camera.id, 'resolution', e.target.value)}
          >
            <option value="1920x1080">1920x1080 (Full HD)</option>
            <option value="1280x720">1280x720 (HD)</option>
            <option value="640x480">640x480 (SD)</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Frame Rate (FPS)</label>
          <select 
            className="form-select"
            value={camera.fps}
            onChange={(e) => onUpdate(camera.id, 'fps', parseInt(e.target.value))}
          >
            <option value="60">60 FPS</option>
            <option value="30">30 FPS</option>
            <option value="25">25 FPS</option>
            <option value="15">15 FPS</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Brightness: {camera.brightness}%</label>
          <input 
            type="range" 
            className="form-range"
            min="0"
            max="100"
            value={camera.brightness}
            onChange={(e) => onUpdate(camera.id, 'brightness', parseInt(e.target.value))}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Contrast: {camera.contrast}%</label>
          <input 
            type="range" 
            className="form-range"
            min="0"
            max="100"
            value={camera.contrast}
            onChange={(e) => onUpdate(camera.id, 'contrast', parseInt(e.target.value))}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Stream URL</label>
          <input 
            type="text" 
            className="form-control"
            value={camera.streamUrl}
            onChange={(e) => onUpdate(camera.id, 'streamUrl', e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Status</label>
          <select 
            className="form-select"
            value={camera.status}
            onChange={(e) => onUpdate(camera.id, 'status', e.target.value as 'active' | 'inactive')}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        <button className="btn btn-primary w-100">Apply Settings</button>
      </div>
    </div>
  );
};