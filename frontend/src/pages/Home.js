// Home.js

import React, { useState } from "react";
import "../styles/Home.css";
import "../styles/CloseButton.css";
import Header from "../ui/Header";
import Chat from "../components/Chat";
import DocumentViewer from "../components/DocumentViewer";
import DocumentSearch from "../components/DocumentSearch";

const Home = () => {
  const user = {
    name: "Rahul Kumar",
    avatar: "path-to-avatar-image.png",
  };
  const [fileId, setFileId] = useState(null);
  const [results, setResults] = useState([]);

  const setFileIdAndOpenDocumentViewer = (fileId) => {
    setFileId(fileId);
    setResults([]);
  };

  const setResultsAndOpenDocumentSearch = (results) => {
    setResults(results);
    setFileId(null);
  };

  const SidePanel = ({ onClose }) => {
    return (
      <div style={{ display: 'flex', 
      height: '100%' }}>
        {/* Your side panel content goes here */}
        <button onClick={onClose}
        className="close-button" />
        {fileId && <DocumentViewer id={fileId} />}
        {results.length > 0 && (
          <DocumentSearch
            results={results}
            setFileIdAndOpenDocumentViewer={setFileIdAndOpenDocumentViewer}
          />
        )}
      </div>
    );
  };

  return (
    <div className={`app-container`}>
      <Header user={user} />
      <div className="main-container">
        <Chat
          user={user}
          setFileIdAndOpenDocumentViewer={setFileIdAndOpenDocumentViewer}
          showSidePanel={fileId || results.length > 0}
          setResultsAndOpenDocumentSearch={setResultsAndOpenDocumentSearch}
        />
        {(fileId || results.length > 0) && (
          <SidePanel
            onClose={() => {
              setFileId(null);
              setResults([]);
            }}
          />
        )}
        {/* {(fileId || results.length > 0) && (
        <button onClick={() => {
              setFileId(null);
              setResults([]);}}>X</button>)}
        {fileId && <DocumentViewer id={fileId} />}
        {results.length > 0 && (
          <DocumentSearch
            results={results}
            setFileIdAndOpenDocumentViewer={setFileIdAndOpenDocumentViewer}
          />
        )} */}
      </div>
    </div>
  );
};

export default Home;
