'use client';

import React from 'react';
import { CameraSettingsCard } from '@/components/CameraSettingsCard';
import { CameraData } from '@/types/type';

interface SettingsPageProps {
  cameras: CameraData[];
  onUpdateCamera: <K extends keyof CameraData>(id: number, field: K, value: CameraData[K]) => void;
}

export default function SettingsPage({ cameras, onUpdateCamera }: SettingsPageProps) {
  return (
    <div className="row">
      {cameras.map(camera => (
        <div key={camera.id} className="col-md-6 mb-4">
          <CameraSettingsCard camera={camera} onUpdate={onUpdateCamera} />
        </div>
      ))}
    </div>
  );
}