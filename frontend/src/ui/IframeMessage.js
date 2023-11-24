import React from "react";
import PropTypes from "prop-types";
import "../styles/IframeMessage.css"; // You'll need to create this CSS file

const IframeMessage = ({ src, timestamp, isUserMessage }) => {
  return (
    <div className={`iframe-message ${isUserMessage ? "user-message" : ""}`}>
      <div className="timestamp">{timestamp}</div>
      <iframe src={src} title="File Preview" frameBorder="0"></iframe>
    </div>
  );
};

IframeMessage.propTypes = {
  src: PropTypes.string.isRequired,
  timestamp: PropTypes.string.isRequired,
  isUserMessage: PropTypes.bool.isRequired,
};

export default IframeMessage;
