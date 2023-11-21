// Home.js

import React, { useState } from "react";
import "../styles/Home.css";
import Header from "../ui/Header";
import Chat from "../components/Chat";
import DocumentViewer from "../components/DocumentViewer";

import axios from "axios";
import { useParams } from "react-router-dom";

const Home = () => {
  const user = {
    name: "Rahul Kumar",
    avatar: "path-to-avatar-image.png",
  };

  const [file, setFile] = useState(null);
  const [showDocumentViewer, setShowDocumentViewer] = useState(false);

  const toggleDocumentViewer = () => {
    setShowDocumentViewer(!showDocumentViewer);
  };

  const setFileAndToggleDocumentViewer = (file) => {
    toggleDocumentViewer();
    setFile(file);
  };

  const { id } = useParams();
  // TODO send file to backend, get back id, pass to document viewer

  return (
    <div className={`app-container`}>
      <Header user={user} />
      <div className="main-container">
        <Chat
          user={user}
          setFileAndToggleDocumentViewer={setFileAndToggleDocumentViewer}
          showDocumentViewer={showDocumentViewer}
        />
        {showDocumentViewer && <DocumentViewer id={id} />}
        
      </div>
    </div>
  );
};

export default Home;
