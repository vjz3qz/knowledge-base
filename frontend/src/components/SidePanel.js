// SidePanel.js

import React from 'react';
import '../styles/SidePanel.css'; // Make sure to create this CSS file

const SidePanel = ({ onClose }) => {
  return (
    <div className="side-panel">
      {/* Your side panel content goes here */}
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default SidePanel;
