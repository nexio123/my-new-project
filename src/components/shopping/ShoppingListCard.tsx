import React from 'react';

interface ShoppingListCardProps {
  listName: string;
  items: Array<{ id: string; name: string; quantity: number }>;
}

export const ShoppingListCard: React.FC<ShoppingListCardProps> = ({ listName, items }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium">{listName}</h3>
      <ul className="mt-4 space-y-2">
        {items.map(item => (
          <li key={item.id}>{item.name} - {item.quantity}</li>
        ))}
      </ul>
    </div>
  );
};
