// Home.js

import React, { useState } from "react";
import "../styles/Home.css";
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
  }

  return (
    <div className={`app-container`}>
      <Header user={user} />
      <div className="main-container">
        <Chat
          user={user}
          setFileIdAndOpenDocumentViewer={setFileIdAndOpenDocumentViewer}
          showSidePanel={fileId || results.length > 0 } 
          setResultsAndOpenDocumentSearch={setResultsAndOpenDocumentSearch}
        />
        {fileId && <DocumentViewer id={fileId} />}
        {results.length > 0 && <DocumentSearch results={results} setFileIdAndOpenDocumentViewer={setFileIdAndOpenDocumentViewer} />}
      </div>
    </div>
  );
};

export default Home;
