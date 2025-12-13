'use client';

import React from 'react';
import { Car, TrendingUp, TrendingDown } from 'lucide-react';

interface VehicleCountDisplayProps {
  cluster1Count: number | null;
  cluster2Count: number | null;
}

export const VehicleCountDisplay: React.FC<VehicleCountDisplayProps> = ({
  cluster1Count,
  cluster2Count
}) => {
  const getTrafficLevel = (count: number | null) => {
    if (count === null || count === undefined) return { level: 'unknown', color: 'secondary', text: 'Chờ dữ liệu' };
    if (count <= 5) return { level: 'low', color: 'success', text: 'Thông thoáng' };
    if (count <= 10) return { level: 'medium', color: 'warning', text: 'Bình thường' };
    return { level: 'high', color: 'danger', text: 'Đông đúc' };
  };

  const level1 = getTrafficLevel(cluster1Count);
  const level2 = getTrafficLevel(cluster2Count);

  return (
    <div className="row g-3 mb-4">
      <div className="col-md-6">
        <div className="card shadow-sm border-0">
          <div className="card-body">
            <div className="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h6 className="text-muted mb-1">Cụm đèn 1</h6>
                <div className="d-flex align-items-center">
                  <Car size={24} className="text-primary me-2" />
                  <span className="fs-2 fw-bold">
                    {cluster1Count !== null && cluster1Count !== undefined ? cluster1Count : '--'}
                  </span>
                  <span className="text-muted ms-2">xe</span>
                </div>
              </div>
              <span className={`badge bg-${level1.color} fs-6`}>
                {level1.text}
              </span>
            </div>
            <div className="progress" style={{ height: '8px' }}>
              <div 
                className={`progress-bar bg-${level1.color}`}
                style={{ width: `${Math.min((cluster1Count || 0) * 5, 100)}%` }}
              />
            </div>
            <small className="text-muted mt-2 d-block">
              Cập nhật mỗi 10 giây từ AI
            </small>
          </div>
        </div>
      </div>

      <div className="col-md-6">
        <div className="card shadow-sm border-0">
          <div className="card-body">
            <div className="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h6 className="text-muted mb-1">Cụm đèn 2</h6>
                <div className="d-flex align-items-center">
                  <Car size={24} className="text-primary me-2" />
                  <span className="fs-2 fw-bold">
                    {cluster2Count !== null && cluster2Count !== undefined ? cluster2Count : '--'}
                  </span>
                  <span className="text-muted ms-2">xe</span>
                </div>
              </div>
              <span className={`badge bg-${level2.color} fs-6`}>
                {level2.text}
              </span>
            </div>
            <div className="progress" style={{ height: '8px' }}>
              <div 
                className={`progress-bar bg-${level2.color}`}
                style={{ width: `${Math.min((cluster2Count || 0) * 5, 100)}%` }}
              />
            </div>
            <small className="text-muted mt-2 d-block">
              Cập nhật mỗi 10 giây từ AI
            </small>
          </div>
        </div>
      </div>

      {/* So sánh mật độ */}
      {cluster1Count !== null && cluster2Count !== null && (
        <div className="col-12">
          <div className="alert alert-info mb-0">
            <div className="d-flex align-items-center">
              {cluster1Count > cluster2Count ? (
                <>
                  <TrendingUp className="me-2" size={20} />
                  <span>
                    <strong>Cụm 1</strong> đông hơn <strong>Cụm 2</strong> ({cluster1Count - cluster2Count} xe)
                    {cluster1Count > 10 && ' - AI sẽ tự động tăng thời gian đèn xanh'}
                  </span>
                </>
              ) : cluster2Count > cluster1Count ? (
                <>
                  <TrendingUp className="me-2" size={20} />
                  <span>
                    <strong>Cụm 2</strong> đông hơn <strong>Cụm 1</strong> ({cluster2Count - cluster1Count} xe)
                    {cluster2Count > 10 && ' - AI sẽ tự động tăng thời gian đèn xanh'}
                  </span>
                </>
              ) : (
                <>
                  <TrendingDown className="me-2" size={20} />
                  <span>Mật độ xe <strong>cân bằng</strong> ở cả 2 cụm</span>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
