'use client';

import React from 'react';
import { Camera, TrafficCone, Car } from 'lucide-react';
import { StatCard } from '@/components/StatCard';
import { VehicleChart } from '@/components/VehicleChart';
import { CameraStatusList } from '@/components/CameraStatusList';
import { TrafficLightStatusList } from '@/components/TrafficLightStatusList';
import { CameraData, TrafficLight, VehicleStats } from '@/types/type';

interface OverviewPageProps {
  cameras: CameraData[];
  trafficLights: TrafficLight[];
  vehicleStats: VehicleStats[];
}

export default function OverviewPage({ 
  cameras, 
  trafficLights, 
  vehicleStats 
}: OverviewPageProps) {
  const activeCameras = cameras.filter(c => c.status === 'active').length;
  const activeTrafficLights = trafficLights.filter(t => t.status === 'active').length;
  const todayVehicles = vehicleStats[vehicleStats.length - 1]?.count || 0;

  return (
    <>
      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <StatCard
            title="Active Cameras"
            value={activeCameras.toString()}
            total={cameras.length.toString()}
            icon={<Camera size={32} className="text-primary" />}
            color="primary"
            progress={(activeCameras / cameras.length) * 100}
          />
        </div>
        <div className="col-md-4">
          <StatCard
            title="Active Traffic Lights"
            value={activeTrafficLights.toString()}
            total={trafficLights.length.toString()}
            icon={<TrafficCone size={32} className="text-success" />}
            color="success"
            progress={(activeTrafficLights / trafficLights.length) * 100}
          />
        </div>
        <div className="col-md-4">
          <StatCard
            title="Vehicles Today"
            value={todayVehicles.toLocaleString()}
            icon={<Car size={32} className="text-warning" />}
            color="warning"
            subtitle="Updated in real-time"
          />
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12">
          <VehicleChart data={vehicleStats} />
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-md-6">
          <CameraStatusList cameras={cameras} />
        </div>
        <div className="col-md-6">
          <TrafficLightStatusList trafficLights={trafficLights} />
        </div>
      </div>
    </>
  );
}