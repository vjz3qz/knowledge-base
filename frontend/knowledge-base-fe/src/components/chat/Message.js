import React from 'react';

const Message = ({ type, content }) => {
  return (
    <div className={`message ${type}`}>
      {content}
    </div>
  );
};

export default Message;
