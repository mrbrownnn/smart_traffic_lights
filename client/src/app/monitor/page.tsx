'use client';

import React, { useState } from 'react';
import { CameraListSidebar } from '@/components/CameraListSidebar';
import { LiveFeedViewer } from '@/components/LiveFeedViewer';
import { CameraData } from '@/types/type';

interface MonitorPageProps {
  cameras: CameraData[];
}

export default function MonitorPage({ cameras }: MonitorPageProps) {
  const [selectedCamera, setSelectedCamera] = useState<CameraData | null>(null);

  return (
    <div className="row">
      <div className="col-md-3">
        <CameraListSidebar
          cameras={cameras}
          selectedCamera={selectedCamera}
          onSelectCamera={setSelectedCamera}
        />
      </div>
      <div className="col-md-9">
        <LiveFeedViewer camera={selectedCamera} />
      </div>
    </div>
  );
}