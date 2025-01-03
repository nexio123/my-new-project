import React from 'react';

interface StoreHeatmapProps {
  data: Array<{ store: string; price: number }>;
}

export const StoreHeatmap: React.FC<StoreHeatmapProps> = ({ data }) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {data.map(item => (
        <div key={item.store} className="p-4 rounded" style={{ backgroundColor: `rgba(66, 135, 245, ${item.price / 100})` }}>
          {item.store}
        </div>
      ))}
    </div>
  );
};
