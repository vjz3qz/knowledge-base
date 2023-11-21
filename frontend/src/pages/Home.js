// Home.js

import React, { useState, useRef, useEffect } from 'react';
import '../styles/Home.css';
import FeatureBox from '../ui/FeatureBox';
import ExampleBox from '../ui/ExampleBox';
import Header from '../ui/Header';
import ChatBubble from '../ui/ChatBubble';
import FileMessage from '../ui/FileMessage';
import SidePanel from '../ui/SidePanel';
import IframeMessage from '../ui/IframeMessage';

import Chat from '../components/Chat';
import { FaRegLightbulb } from 'react-icons/fa'; // Example icon for "Examples"
import { MdOutlineRememberMe } from 'react-icons/md'; // Example icon for "Capabilities"
import { AiOutlineExclamationCircle } from 'react-icons/ai'; // Example icon for "Limitations"

import axios from "axios";
import { useParams } from "react-router-dom";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;




const Home = () => {

  const user = {
    name: 'Rahul Kumar',
    avatar: 'path-to-avatar-image.png'
  };



  const [file, setFile] = useState(null);
  const [showSidePanel, setShowSidePanel] = useState(false);

  const toggleSidePanel = () => {
    setShowSidePanel(!showSidePanel);
  };

  const setFileAndToggleSidePanel = (file) => {
    toggleSidePanel();
    setFile(file);
  }

  const { id } = useParams();

  const [fileUrl, setFileUrl] = useState("");
  const [metadata, setMetadata] = useState({});





  return (
    <div className={`app-container`}>
      <Header user={user} />
      <Chat user={user} setFileAndToggleSidePanel={setFileAndToggleSidePanel} />
    </div>
  );
};

export default Home;
