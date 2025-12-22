import { TrafficLightStatus, ManualAdjustResponse } from '@/types/type';

// Sử dụng Next.js API route để tránh CORS issues
const USE_PROXY = true;
const API_BASE_URL = USE_PROXY 
  ? '/api/traffic' 
  : 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

// Fetch options with ngrok header
const getFetchOptions = (method: string = 'GET'): RequestInit => ({
  method,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
  },
  cache: 'no-store',
});

export const trafficLightApi = {
  // Lấy trạng thái đèn giao thông
  getStatus: async (): Promise<TrafficLightStatus> => {
    if (USE_PROXY) {
      const response = await fetch('/api/traffic', { cache: 'no-store' });
      if (!response.ok) {
        throw new Error('Failed to fetch traffic light status');
      }
      return response.json();
    } else {
      const response = await fetch(`${API_BASE_URL}/status`, getFetchOptions());
      if (!response.ok) {
        throw new Error('Failed to fetch traffic light status');
      }
      return response.json();
    }
  },

  // Điều chỉnh đèn giao thông thủ công
  manualAdjust: async (cluster: number, seconds: number): Promise<ManualAdjustResponse> => {
    const endpoint = `/api/traffic/manual_adjust/${cluster}/${seconds}`;
    const response = await fetch(endpoint, {
      method: 'POST',
      cache: 'no-store',
    });
    if (!response.ok) {
      throw new Error('Failed to adjust traffic light');
    }
    return response.json();
  },

  // Reset đèn về thời gian ban đầu và tắt AI
  manualReset: async (): Promise<{ message: string }> => {
    const response = await fetch('/api/traffic/manual_reset', {
      method: 'POST',
      cache: 'no-store',
    });
    if (!response.ok) {
      throw new Error('Failed to reset traffic lights');
    }
    return response.json();
  },

  // Bật lại chức năng điều chỉnh đèn tự động
  enableAI: async (): Promise<{ message: string }> => {
    const response = await fetch('/api/traffic/enable_ai', {
      method: 'POST',
      cache: 'no-store',
    });
    if (!response.ok) {
      throw new Error('Failed to enable AI mode');
    }
    return response.json();
  },

  // Lấy camera stream URL
  getCameraStream: (): string => {
    return '/api/traffic/camera';
  },
};
