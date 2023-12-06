import React from 'react';
import PropTypes from 'prop-types';
import '../styles/IframeMessage.css'; // Make sure this CSS file exists and is styled

const TableMessage = ({ src, timestamp }) => {
  
  return (
    <div className={`iframe-message`}>
      <div className='timestamp'>{timestamp}</div>
      <table>
        <thead>
          <tr>
            <th>Symbol ID</th>
            <th>Symbol Type</th>
            <th>Associated Text</th>
            <th>Detection Method</th>
            <th>Connected Symbols</th>
          </tr>
        </thead>
        <tbody>
          {src.map((row, index) => (
            <tr key={index}>
              <td>{row.symbolId}</td>
              <td>{row.symbolType}</td>
              <td>{row.associatedText}</td>
              <td>{row.detectionMethod}</td>
              <td>{row.connectedSymbols}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

TableMessage.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    symbolId: PropTypes.number.isRequired,
    symbolType: PropTypes.string.isRequired,
    associatedText: PropTypes.string.isRequired,
    detectionMethod: PropTypes.string.isRequired,
    connectedSymbols: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  })).isRequired,
  timestamp: PropTypes.string.isRequired,
  isUserMessage: PropTypes.bool.isRequired,
};

export default TableMessage;
