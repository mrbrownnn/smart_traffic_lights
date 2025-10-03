'use client';

import React, { useState, useEffect } from 'react';
import { Activity, Video, Settings } from 'lucide-react';
import Layout from './layout';
import OverviewPage from './dashboard/page';
import MonitorPage from './monitor/page';
import SettingsPage from './settings/page';
import { mockCameras, mockTrafficLights, mockVehicleStats } from '@/data/mockData';
import { CameraData } from '@/types/type';



export default function Home() {
  const [activeTab, setActiveTab] = useState<'overview' | 'monitor' | 'settings'>('overview');
  const [cameras, setCameras] = useState<CameraData[]>(mockCameras);

  useEffect(() => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css';
    document.head.appendChild(link);
    return () => {
      document.head.removeChild(link);
    };
  }, []);

  const handleCameraUpdate = (id: number, field: keyof CameraData, value: unknown) => {
    setCameras(cameras.map(cam => cam.id === id ? { ...cam, [field]: value } : cam));
  };

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
            trafficLights={mockTrafficLights}
            vehicleStats={mockVehicleStats}
          />
        )}
        {activeTab === 'monitor' && <MonitorPage cameras={cameras} />}
        {activeTab === 'settings' && (
          <SettingsPage cameras={cameras} onUpdateCamera={handleCameraUpdate} />
        )}
      </div>
    </Layout>
  );
}