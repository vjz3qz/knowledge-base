import React from "react";
import "../styles/FileMessage.css"; // Make sure to create this CSS file

const FileMessage = ({ fileName, fileSize, timestamp }) => {
  return (
    <div className="file-message">
      <div className="file-timestamp">{timestamp}</div>
      <div className="file-info">
        <div className="file-details">
          <span className="file-icon">📄 </span>
          <span className="file-name">{fileName} </span>
          <span className="file-size">{fileSize} mb</span>
        </div>
      </div>
    </div>
  );
};

export default FileMessage;
