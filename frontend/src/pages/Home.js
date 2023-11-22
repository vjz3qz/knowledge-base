// Home.js

import React, { useState } from "react";
import "../styles/Home.css";
import Header from "../ui/Header";
import Chat from "../components/Chat";
import DocumentViewer from "../components/DocumentViewer";
import DocumentSearch from "../components/DocumentSearch";

import axios from "axios";
import { useParams } from "react-router-dom";

const Home = () => {
  const user = {
    name: "Rahul Kumar",
    avatar: "path-to-avatar-image.png",
  };
  // TODO USE FILE URL, NOT FILE, USE INSTEAD OF DOCUMENT VIEWER
  const [file, setFile] = useState(null);
  const [showDocumentViewer, setShowDocumentViewer] = useState(false);
  const [results, setResults] = useState([]);

  const toggleDocumentViewer = () => {
    setShowDocumentViewer(!showDocumentViewer);
  };

  const setFileAndOpenDocumentViewer = (file) => {
    setFile(file);
    setShowDocumentViewer(true);
    setResults([]);
  };

  const setResultsAndOpenDocumentSearch = (results) => {
    setResults(results);
    setShowDocumentViewer(false);
    setFile(null);
  }

  const { id } = useParams();
  // TODO send file to backend, get back id, pass to document viewer
  return (
    <div className={`app-container`}>
      <Header user={user} />
      <div className="main-container">
        <Chat
          user={user}
          setFileAndOpenDocumentViewer={setFileAndOpenDocumentViewer}
          showSidePanel={showDocumentViewer || results.length } 
          setResultsAndOpenDocumentSearch={setResultsAndOpenDocumentSearch}
        />
        {showDocumentViewer && <DocumentViewer id={id} />}
        {results.length && <DocumentSearch results={results} setFileAndOpenDocumentViewer={setFileAndOpenDocumentViewer} />}
      </div>
    </div>
  );
};

export default Home;
