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
  redTime: number;
  yellowTime: number;
  greenTime: number;
  vehicles: number | null;
}

export interface VehicleStats {
  date: string;
  count: number;
}

// API Response Types
export interface TrafficLightStatus {
  traffic_light_1: {
    red_time: number;
    yellow_time: number;
    green_time: number;
    vehicles: number | null;
  };
  traffic_light_2: {
    red_time: number;
    yellow_time: number;
    green_time: number;
    vehicles: number | null;
  };
}

export interface ManualAdjustResponse {
  status: string;
  "Cụm điều chỉnh": number;
  "Tăng số giây đèn xanh": number;
}
