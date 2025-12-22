'use client';

import React, { useState, useEffect } from 'react';
import { Activity, Video, Settings, Sliders } from 'lucide-react';
import Layout from './layout';
import OverviewPage from './dashboard/page';
import MonitorPage from './monitor/page';
import SettingsPage from './settings/page';
import ControlPage from './control/page';
import { CameraData, TrafficLight, VehicleStats } from '@/types/type';
import { trafficLightApi } from '@/services/api';

// Initial data
const initialCameras: CameraData[] = [
  { 
    id: 1, 
    name: 'Camera Cụm 1', 
    location: 'Cluster 1', 
    status: 'active', 
    resolution: '1920x1080', 
    fps: 30, 
    brightness: 50, 
    contrast: 50, 
    streamUrl: 'https://congregative-pathognomonically-madelene.ngrok-free.dev/camera' 
  },
  { 
    id: 2, 
    name: 'Camera Cụm 2', 
    location: 'Cluster 2', 
    status: 'active', 
    resolution: '1920x1080', 
    fps: 30, 
    brightness: 50, 
    contrast: 50, 
    streamUrl: 'https://congregative-pathognomonically-madelene.ngrok-free.dev/camera' 
  },
];

const mockVehicleStats: VehicleStats[] = [
  { date: '2025-12-07', count: 12543 },
  { date: '2025-12-08', count: 13201 },
  { date: '2025-12-09', count: 11876 },
  { date: '2025-12-10', count: 14032 },
  { date: '2025-12-11', count: 13654 },
  { date: '2025-12-12', count: 12987 },
  { date: '2025-12-13', count: 8234 },
];

export default function Home() {
  const [activeTab, setActiveTab] = useState<'overview' | 'monitor' | 'control' | 'settings'>('overview');
  const [cameras, setCameras] = useState<CameraData[]>(initialCameras);
  const [trafficLights, setTrafficLights] = useState<TrafficLight[]>([]);
  const [vehicleCounts, setVehicleCounts] = useState<{c1: number | null, c2: number | null}>({c1: null, c2: null});
  const [mounted, setMounted] = useState(false);
  const [loading, setLoading] = useState(true);

  // Fetch traffic light status từ API
  const fetchTrafficLightStatus = async () => {
    try {
      const status = await trafficLightApi.getStatus();
      console.log('API Response:', status); // Debug log
      
      // Lưu vehicle counts
      setVehicleCounts({
        c1: status.traffic_light_1.vehicles,
        c2: status.traffic_light_2.vehicles
      });
      
      // Cập nhật traffic lights với dữ liệu từ API - CHỈ dùng dữ liệu thực tế
      const updatedLights: TrafficLight[] = [
        {
          id: 1,
          location: 'Cụm đèn 1',
          redTime: status.traffic_light_1.red_time,
          yellowTime: status.traffic_light_1.yellow_time,
          greenTime: status.traffic_light_1.green_time,
          vehicles: status.traffic_light_1.vehicles,
        },
        {
          id: 2,
          location: 'Cụm đèn 2',
          redTime: status.traffic_light_2.red_time,
          yellowTime: status.traffic_light_2.yellow_time,
          greenTime: status.traffic_light_2.green_time,
          vehicles: status.traffic_light_2.vehicles,
        },
      ];
      
      console.log('Updated Traffic Lights:', updatedLights); // Debug log
      setTrafficLights(updatedLights);
    } catch (error) {
      console.error('Error fetching traffic light status:', error);
    }
  };

  useEffect(() => {
    setMounted(true);
    
    // Load Bootstrap CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css';
    document.head.appendChild(link);

    // Fetch initial data
    fetchTrafficLightStatus().finally(() => setLoading(false));

    // Poll API mỗi 2 giây để cập nhật trạng thái đèn
    const interval = setInterval(fetchTrafficLightStatus, 2000);

    return () => {
      document.head.removeChild(link);
      clearInterval(interval);
    };
  }, []);

  const handleCameraUpdate = (id: number, field: keyof CameraData, value: unknown) => {
    setCameras(cameras.map(cam => cam.id === id ? { ...cam, [field]: value } : cam));
  };

  if (!mounted || loading) {
    return (
      <Layout>
        <div className="d-flex justify-content-center align-items-center min-vh-100">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container-fluid mt-3">
        <ul className="nav nav-tabs">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              <Activity size={16} className="me-1" />
              Overview
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'monitor' ? 'active' : ''}`}
              onClick={() => setActiveTab('monitor')}
            >
              <Video size={16} className="me-1" />
              Camera Monitor
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'control' ? 'active' : ''}`}
              onClick={() => setActiveTab('control')}
            >
              <Sliders size={16} className="me-1" />
              Traffic Control
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'settings' ? 'active' : ''}`}
              onClick={() => setActiveTab('settings')}
            >
              <Settings size={16} className="me-1" />
              Camera Settings
            </button>
          </li>
        </ul>
      </div>

      <div className="container-fluid mt-4 pb-4">
        {activeTab === 'overview' && (
          <OverviewPage
            cameras={cameras}
            trafficLights={trafficLights}
            vehicleStats={mockVehicleStats}
            vehicleCounts={vehicleCounts}
          />
        )}
        {activeTab === 'monitor' && <MonitorPage cameras={cameras} />}
        {activeTab === 'control' && (
          <ControlPage
            trafficLights={trafficLights}
            vehicleCounts={vehicleCounts}
            onUpdate={fetchTrafficLightStatus}
          />
        )}
        {activeTab === 'settings' && (
          <SettingsPage cameras={cameras} onUpdateCamera={handleCameraUpdate} />
        )}
      </div>
    </Layout>
  );
}