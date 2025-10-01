import { CameraData, TrafficLight, VehicleStats } from '../types/type';

export const mockCameras: CameraData[] = [
  { id: 1, name: 'Camera 01', location: 'Main St & 1st Ave', status: 'active', resolution: '1920x1080', fps: 30, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream1' },
  { id: 2, name: 'Camera 02', location: 'Highway 101 North', status: 'active', resolution: '1920x1080', fps: 30, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream2' },
  { id: 3, name: 'Camera 03', location: 'Central Plaza', status: 'inactive', resolution: '1280x720', fps: 25, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream3' },
  { id: 4, name: 'Camera 04', location: '5th Ave Bridge', status: 'active', resolution: '1920x1080', fps: 30, brightness: 50, contrast: 50, streamUrl: 'rtsp://example.com/stream4' },
];

export const mockTrafficLights: TrafficLight[] = [
  { id: 1, location: 'Main St & 1st Ave', status: 'active', mode: 'automatic' },
  { id: 2, location: 'Main St & 2nd Ave', status: 'active', mode: 'automatic' },
  { id: 3, location: 'Highway 101 Exit', status: 'inactive', mode: 'manual' },
  { id: 4, location: 'Central Plaza', status: 'active', mode: 'automatic' },
  { id: 5, location: '5th Ave Bridge', status: 'active', mode: 'automatic' },
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
