import { TrafficLightStatus, ManualAdjustResponse } from '@/types/type';

const API_BASE_URL = 'https://sniffy-dramatizable-jagger.ngrok-free.dev';

// Fetch options with ngrok header
const getFetchOptions = (method: string = 'GET'): RequestInit => ({
  method,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
  },
});

export const trafficLightApi = {
  // Lấy trạng thái đèn giao thông
  getStatus: async (): Promise<TrafficLightStatus> => {
    const response = await fetch(`${API_BASE_URL}/status`, getFetchOptions());
    if (!response.ok) {
      throw new Error('Failed to fetch traffic light status');
    }
    return response.json();
  },

  // Điều chỉnh đèn giao thông thủ công
  manualAdjust: async (cluster: number, seconds: number): Promise<ManualAdjustResponse> => {
    const response = await fetch(
      `${API_BASE_URL}/manual_adjust/${cluster}/${seconds}`,
      getFetchOptions('POST')
    );
    if (!response.ok) {
      throw new Error('Failed to adjust traffic light');
    }
    return response.json();
  },

  // Reset đèn về thời gian ban đầu và tắt AI
  manualReset: async (): Promise<{ message: string }> => {
    const response = await fetch(
      `${API_BASE_URL}/manual_reset`,
      getFetchOptions('POST')
    );
    if (!response.ok) {
      throw new Error('Failed to reset traffic lights');
    }
    return response.json();
  },

  // Bật lại chức năng điều chỉnh đèn tự động
  enableAI: async (): Promise<{ message: string }> => {
    const response = await fetch(
      `${API_BASE_URL}/enable_ai`,
      getFetchOptions('POST')
    );
    if (!response.ok) {
      throw new Error('Failed to enable AI mode');
    }
    return response.json();
  },

  // Lấy camera stream URL
  getCameraStream: (): string => {
    return `${API_BASE_URL}/camera`;
  },
};
