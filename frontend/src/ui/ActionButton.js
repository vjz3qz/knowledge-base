import React from 'react';

const ActionButton = ({ onClick, highlight, label, disabled }) => {
  let buttonClass = 'action-button-white';
  if (highlight) {
    buttonClass = 'action-button-black';
  }
  if (disabled) {
    buttonClass += ' disabled'; // Assuming you have appropriate styles for the disabled state
  }

  return (
    <button className={buttonClass} onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};

export default ActionButton;
