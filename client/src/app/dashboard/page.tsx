'use client';

import React from 'react';
import { Camera, TrafficCone, Car } from 'lucide-react';
import { StatCard } from '@/components/StatCard';
import { VehicleChart } from '@/components/VehicleChart';
import { CameraStatusList } from '@/components/CameraStatusList';
import { TrafficLightStatusList } from '@/components/TrafficLightStatusList';
import { VehicleCountDisplay } from '@/components/VehicleCountDisplay';
import { CameraData, TrafficLight, VehicleStats } from '@/types/type';

interface OverviewPageProps {
  cameras: CameraData[];
  trafficLights: TrafficLight[];
  vehicleStats: VehicleStats[];
  vehicleCounts?: {c1: number | null, c2: number | null};
}

export default function OverviewPage({ 
  cameras, 
  trafficLights, 
  vehicleStats,
  vehicleCounts
}: OverviewPageProps) {
  const activeCameras = cameras.filter(c => c.status === 'active').length;
  const totalVehicles = (vehicleCounts?.c1 || 0) + (vehicleCounts?.c2 || 0);

  return (
    <>
      {/* Vehicle Count Display - Real-time từ AI */}
      {vehicleCounts && (
        <VehicleCountDisplay 
          cluster1Count={vehicleCounts.c1}
          cluster2Count={vehicleCounts.c2}
        />
      )}

      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <StatCard
            title="Cameras hoạt động"
            value={activeCameras.toString()}
            total={cameras.length.toString()}
            icon={<Camera size={32} className="text-primary" />}
            color="primary"
            progress={(activeCameras / cameras.length) * 100}
          />
        </div>
        <div className="col-md-4">
          <StatCard
            title="Cụm đèn giao thông"
            value={trafficLights.length.toString()}
            total={trafficLights.length.toString()}
            icon={<TrafficCone size={32} className="text-success" />}
            color="success"
            progress={100}
          />
        </div>
        <div className="col-md-4">
          <StatCard
            title="Tổng xe hiện tại"
            value={totalVehicles.toString()}
            icon={<Car size={32} className="text-warning" />}
            color="warning"
            subtitle="Cập nhật từ AI mỗi 10s"
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