import React from 'react';

interface ShareListModalProps {
  isOpen: boolean;
  onClose: () => void;
  listId: string;
}

export const ShareListModal: React.FC<ShareListModalProps> = ({ isOpen, onClose, listId }) => {
  return (
    <div className={`modal ${isOpen ? 'block' : 'hidden'}`}>
      <div className="modal-content">
        <h2>Share Shopping List</h2>
        {/* Sharing form content */}
      </div>
    </div>
  );
};
