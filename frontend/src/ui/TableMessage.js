// import React from "react";
// import PropTypes from "prop-types";
// import "../styles/IframeMessage.css"; // Make sure this CSS file exists and is styled

// const TableMessage = ({ data, timestamp, isUserMessage }) => {
//   // Function to generate table rows from data

//   // const generateTableRows = (data) => {
//   //   return data.map((row, index) => (
//   //     <tr key={index}>
//   //       <td>{row.symbolId}</td>
//   //       <td>{row.symbolType}</td>
//   //       <td>{row.associatedText}</td>
//   //       <td>{row.detectionMethod}</td>
//   //       <td>{row.connectedSymbols}</td>
//   //     </tr>
//   //   ));
//   // };

//   const generateTableRows = (data) => {
//     return data.map((row) => 
//       `<tr>
//         <td>${row.symbolId}</td>
//         <td>${row.symbolType}</td>
//         <td>${row.associatedText}</td>
//         <td>${row.detectionMethod}</td>
//         <td>${row.connectedSymbols}</td>
//       </tr>`
//     ).join('');
//   };
  

//   // Create a data URI for the iframe content
//   const tableHTML = `
//     <!DOCTYPE html>
//     <html lang="en">
//     <head>
//       <meta charset="UTF-8">
//       <meta name="viewport" content="width=device-width, initial-scale=1.0">
//       <style>
//         body { font-family: Arial, sans-serif; margin: 0; padding: 0; font-weight: 300; }
//         table { width: 100%; border-collapse: collapse; }
//         th, td { border: 1px solid #ddd; padding: 8px; text-align: left;font-weight: normal; }
//         th { background-color: #f2f2f2;font-weight: normal; }
//       </style>
//     </head>
//     <body>
//       <table>
//         <thead>
//           <tr>
//             <th>Symbol ID</th>
//             <th>Symbol Type</th>
//             <th>Associated Text</th>
//             <th>Detection Method</th>
//             <th>Connected Symbols</th>
//           </tr>
//         </thead>
//         <tbody>
//         ${generateTableRows(sampleData)}
//         </tbody>
//       </table>
//     </body>
//     </html>
//   `;
//         // ${generateTableRows(sampleData).join('')}

//   const iframeSrc = `data:text/html;charset=utf-8,${encodeURIComponent(tableHTML)}`;

//   return (
//     <div className={`iframe-message ${isUserMessage ? "user-message" : ""}`}>
//       <div className="timestamp">{timestamp}</div>
//       <iframe src={iframeSrc} title="File Preview" frameBorder="0"></iframe>
//     </div>
//   );
// };

// TableMessage.propTypes = {
//   data: PropTypes.arrayOf(PropTypes.shape({
//     symbolId: PropTypes.number.isRequired,
//     symbolType: PropTypes.string.isRequired,
//     associatedText: PropTypes.string.isRequired,
//     detectionMethod: PropTypes.string.isRequired,
//     connectedSymbols: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
//   })).isRequired,
//   timestamp: PropTypes.string.isRequired,
//   isUserMessage: PropTypes.bool.isRequired,
// };

// export default TableMessage;
import React from 'react';
import PropTypes from 'prop-types';
import '../styles/IframeMessage.css'; // Make sure this CSS file exists and is styled

const TableMessage = ({ data, timestamp, isUserMessage }) => {
  const sampleData = [
    {
      symbolId: 0,
      symbolType: "EQU",
      associatedText: "EQU_TK-583034",
      detectionMethod: "Manual",
      connectedSymbols: 43
    },
    {
      symbolId: 1,
      symbolType: "VAR",
      associatedText: "VAR_DX-920401",
      detectionMethod: "Automated",
      connectedSymbols: 27
    },
    {
      symbolId: 2,
      symbolType: "FUNC",
      associatedText: "FUNC_LM-840200",
      detectionMethod: "Semi-Automatic",
      connectedSymbols: 15
    },
    // Add more entries as needed
  ];
  
  return (
    <div className={`iframe-message ${isUserMessage ? 'user-message' : ''}`}>
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
          {sampleData.map((row, index) => (
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
