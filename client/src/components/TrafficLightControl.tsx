'use client';

import React, { useState } from 'react';
import { trafficLightApi } from '@/services/api';
import { TrafficLight } from '@/types/type';
import { Car } from 'lucide-react';

interface TrafficLightControlProps {
  trafficLight: TrafficLight;
  vehicleCount?: number | null;
  onUpdate?: () => void;
}

export const TrafficLightControl: React.FC<TrafficLightControlProps> = ({ 
  trafficLight,
  vehicleCount,
  onUpdate 
}) => {
  const [adjusting, setAdjusting] = useState(false);
  const [seconds, setSeconds] = useState(5);
  const [message, setMessage] = useState('');

  const handleAdjust = async () => {
    try {
      setAdjusting(true);
      setMessage('');
      await trafficLightApi.manualAdjust(trafficLight.id, seconds);
      setMessage(`Đã điều chỉnh cụm ${trafficLight.id}: tăng ${seconds}s đèn xanh`);
      if (onUpdate) onUpdate();
    } catch (error) {
      setMessage('Lỗi khi điều chỉnh đèn');
      console.error(error);
    } finally {
      setAdjusting(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const handleReset = async () => {
    try {
      setAdjusting(true);
      setMessage('');
      await trafficLightApi.manualReset();
      setMessage('Đã reset về thời gian ban đầu và tắt AI');
      if (onUpdate) onUpdate();
    } catch (error) {
      setMessage('Lỗi khi reset đèn');
      console.error(error);
    } finally {
      setAdjusting(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const handleEnableAI = async () => {
    try {
      setAdjusting(true);
      setMessage('');
      await trafficLightApi.enableAI();
      setMessage('Đã bật chế độ AI tự động');
      if (onUpdate) onUpdate();
    } catch (error) {
      setMessage('Lỗi khi bật AI');
      console.error(error);
    } finally {
      setAdjusting(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  return (
    <div className="card shadow-sm">
      <div className="card-header bg-white">
        <div className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">
            <span className="badge bg-primary me-2">Cụm {trafficLight.id}</span>
            {trafficLight.location}
          </h5>
          <div className="d-flex align-items-center gap-2">
            {vehicleCount !== null && vehicleCount !== undefined && (
              <span className="badge bg-info">
                <Car size={14} className="me-1" />
                {vehicleCount} xe
              </span>
            )}
          </div>
        </div>
      </div>
      <div className="card-body">
        {/* Hiển thị thời gian đèn - TỪ API */}
        <div className="mb-4">
          <h6 className="text-muted mb-3">⏱️ Cấu hình thời gian (từ API)</h6>
          <div className="row g-3">
            <div className="col-4">
              <div className="text-center p-3 rounded" style={{ backgroundColor: '#f8d7da' }}>
                <div className="text-danger fw-bold mb-1">🔴 Đỏ</div>
                <div className="fs-4 fw-bold">{trafficLight.redTime}s</div>
              </div>
            </div>
            <div className="col-4">
              <div className="text-center p-3 rounded" style={{ backgroundColor: '#fff3cd' }}>
                <div className="text-warning fw-bold mb-1">🟡 Vàng</div>
                <div className="fs-4 fw-bold">{trafficLight.yellowTime}s</div>
              </div>
            </div>
            <div className="col-4">
              <div className="text-center p-3 rounded" style={{ backgroundColor: '#d1e7dd' }}>
                <div className="text-success fw-bold mb-1">🟢 Xanh</div>
                <div className="fs-4 fw-bold">{trafficLight.greenTime}s</div>
              </div>
            </div>
          </div>
          <div className="mt-2 text-center">
            <small className="text-muted">
              Tổng chu kỳ: {trafficLight.redTime + trafficLight.yellowTime + trafficLight.greenTime}s
            </small>
          </div>
        </div>

        {/* Điều chỉnh thủ công */}
        <div className="mb-3">
          <label className="form-label fw-bold">
            Điều chỉnh thủ công (tăng thời gian đèn xanh)
          </label>
          <div className="input-group">
            <input
              type="number"
              className="form-control"
              value={seconds}
              onChange={(e) => setSeconds(Math.max(1, Math.min(60, parseInt(e.target.value) || 1)))}
              min="1"
              max="60"
            />
            <span className="input-group-text">giây</span>
          </div>
          <small className="text-muted">Giá trị từ 1-60 giây</small>
        </div>

        {/* Buttons điều khiển */}
        <div className="d-grid gap-2">
          <button
            className="btn btn-primary btn-lg"
            onClick={handleAdjust}
            disabled={adjusting}
          >
            {adjusting ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Đang xử lý...
              </>
            ) : (
              `⏱️ Tăng ${seconds}s cho cụm ${trafficLight.id}`
            )}
          </button>

          {trafficLight.id === 1 && (
            <>
              <button
                className="btn btn-warning btn-lg"
                onClick={handleReset}
                disabled={adjusting}
              >
                🔄 Reset về ban đầu & Tắt chế độ điều chỉnh đèn tự động
              </button>
              <button
                className="btn btn-success btn-lg"
                onClick={handleEnableAI}
                disabled={adjusting}
              >
                🤖 Bật chế độ điều chỉnh đèn tự động
              </button>
            </>
          )}
        </div>

        {/* Thông báo */}
        {message && (
          <div className={`alert ${message.includes('Lỗi') ? 'alert-danger' : 'alert-success'} mt-3 mb-0`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
};
