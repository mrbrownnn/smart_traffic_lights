import { CameraData, TrafficLight, VehicleStats } from '../types/type';

export const mockCameras: CameraData[] = [
  { id: 1, name: 'Camera 01', location: 'Main St & 1st Ave', status: 'active', resolution: '1920x1080', fps: 30, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream1' },
  { id: 2, name: 'Camera 02', location: 'Highway 101 North', status: 'active', resolution: '1920x1080', fps: 30, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream2' },
];

export const mockTrafficLights: TrafficLight[] = [
  { id: 1, location: 'Main St & 1st Ave', status: 'active', mode: 'automatic' },
  { id: 2, location: 'Highway 101 North', status: 'active', mode: 'automatic' },
];

export const mockVehicleStats: VehicleStats[] = [
  { date: '2025-09-24', count: 12543 },
  { date: '2025-09-25', count: 13201 },
  { date: '2025-09-26', count: 11876 },
  { date: '2025-09-27', count: 14032 },
  { date: '2025-09-28', count: 13654 },
  { date: '2025-09-29', count: 12987 },
  { date: '2025-09-30', count: 8234 },
];
