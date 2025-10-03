export interface CameraData {
  id: number;
  name: string;
  location: string;
  status: 'active' | 'inactive';
  resolution: string;
  fps: number;
  brightness: number;
  contrast: number;
  streamUrl: string;
}

export interface TrafficLight {
  id: number;
  location: string;
  status: 'active' | 'inactive';
  mode: 'automatic' | 'manual';
}

export interface VehicleStats {
  date: string;
  count: number;
}
