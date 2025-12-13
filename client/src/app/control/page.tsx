'use client';

import React from 'react';
import { TrafficLight } from '@/types/type';
import { TrafficLightControl } from '@/components/TrafficLightControl';
import { AlertCircle, Info } from 'lucide-react';

interface ControlPageProps {
  trafficLights: TrafficLight[];
  vehicleCounts?: {c1: number | null, c2: number | null};
  onRefresh?: () => void;
}

export default function ControlPage({ 
  trafficLights, 
  vehicleCounts,
  onRefresh
}: ControlPageProps) {
  
  if (trafficLights.length === 0) {
    return (
      <div className="alert alert-warning">
        <AlertCircle className="me-2" />
        Đang tải dữ liệu đèn giao thông...
      </div>
    );
  }

  return (
    <>
      {/* Header thông tin */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="alert alert-info">
            <Info className="me-2" size={20} />
            <strong>Hướng dẫn điều khiển:</strong>
            <ul className="mb-0 mt-2">
              <li><strong>Tăng thời gian đèn xanh:</strong> Nhập số giây (1-60) và nhấn "Tăng ... cho cụm"</li>
              <li><strong>Reset về mặc định:</strong> Đưa cả 2 cụm về thời gian ban đầu và tắt chế độ AI</li>
              <li><strong>Bật AI tự động:</strong> Cho phép AI điều chỉnh đèn dựa trên mật độ xe</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Thông tin số xe hiện tại */}
      {vehicleCounts && (vehicleCounts.c1 !== null || vehicleCounts.c2 !== null) && (
        <div className="row mb-4">
          <div className="col-12">
            <div className="card shadow-sm">
              <div className="card-header bg-primary text-white">
                <h5 className="mb-0">🚗 Mật độ xe hiện tại (từ AI)</h5>
              </div>
              <div className="card-body">
                <div className="row text-center">
                  <div className="col-md-6">
                    <h3 className="display-4 fw-bold text-primary">
                      {vehicleCounts.c1 ?? '--'}
                    </h3>
                    <p className="text-muted mb-0">Cụm 1</p>
                  </div>
                  <div className="col-md-6">
                    <h3 className="display-4 fw-bold text-primary">
                      {vehicleCounts.c2 ?? '--'}
                    </h3>
                    <p className="text-muted mb-0">Cụm 2</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Điều khiển từng cụm đèn */}
      <div className="row mb-4">
        <div className="col-12">
          <h4 className="mb-3">🎛️ Điều khiển đèn giao thông</h4>
        </div>
        {trafficLights.map((light, index) => (
          <div key={light.id} className="col-lg-6 mb-4">
            <TrafficLightControl 
              trafficLight={light} 
              vehicleCount={vehicleCounts ? (index === 0 ? vehicleCounts.c1 : vehicleCounts.c2) : null}
              onUpdate={onRefresh}
            />
          </div>
        ))}
      </div>

      {/* Ghi chú */}
      <div className="row">
        <div className="col-12">
          <div className="card bg-light">
            <div className="card-body">
              <h6 className="fw-bold mb-2">📝 Lưu ý:</h6>
              <ul className="mb-0 small">
                <li>Khi tăng thời gian đèn xanh cho 1 cụm, thời gian đèn đỏ của cụm kia sẽ tự động tăng tương ứng</li>
                <li>Chế độ AI sẽ tự động điều chỉnh đèn dựa trên mật độ xe (cập nhật mỗi 10 giây)</li>
                <li>Sử dụng "Reset" khi muốn quay về cài đặt ban đầu (17s xanh, 3s vàng, 20s đỏ)</li>
                <li>Thời gian hiển thị được cập nhật real-time từ Raspberry Pi</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
