import React from 'react';

const ActionButton = ({ onClick, highlight, label }) => {
  const buttonClass = highlight ? 'action-button-black' : 'action-button-white';

  return (
    <button className={buttonClass} onClick={onClick}>
      {label}
    </button>
  );
};

export default ActionButton;
