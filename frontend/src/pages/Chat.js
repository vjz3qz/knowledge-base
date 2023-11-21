// Home.js

import React, { useState, useRef, useEffect } from 'react';
import '../styles/Home.css';
import FeatureBox from '../components/FeatureBox';
import ExampleBox from '../components/ExampleBox';
import Header from '../components/Header';
import ChatBubble from '../components/ChatBubble';
import FileMessage from '../components/FileMessage';
import SidePanel from '../components/SidePanel';
import IframeMessage from '../components/IframeMessage';

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

   const [messages, setMessages] = useState([
     { text: "Hello I'm Tracy, how can I help?", isUserMessage: false },
  ]);

  const [showChat, setShowChat] = useState(false); // State to manage whether chat is shown

  // Event handler for the Answer Question button
  const handleAnswerQuestion = () => {
    setShowChat(true);
  };

  const renderChatBubbles = () => {
    return showChat && (
      <div className="chat-container">
        {messages.map((message, index) => {
          if (message.type === 'file') {
            return (
              <FileMessage
                key={index}
                fileName={message.fileName}
                fileSize={message.fileSize}
                timestamp={message.timestamp}
                isUserMessage={message.isUserMessage} // Pass isUserMessage prop to FileMessage if needed
              />
            );
          }
          if (message.type === 'iframe') {
          return (
            <IframeMessage
              key={index}
              src={message.src}
              timestamp={message.timestamp}
              isUserMessage={message.isUserMessage}
            />
          );
          }
          else {
            return (
              <ChatBubble
                key={index}
                message={message.text}
                isUserMessage={message.isUserMessage}
                timestamp={message.timestamp || '2:03 PM'} // Replace with actual timestamp data
              />
            );
          }
        })}
      </div>
    );
  }

  const [inputValue, setInputValue] = useState(''); // Add this line to manage user input

  const handleSendMessage = () => {
    if (inputValue.trim()) { // Check if the input is not just whitespace
      const newMessage = {
        text: inputValue,
        isUserMessage: true // This will be a user message
      };
      setMessages([...messages, newMessage]); // Add the new message to the messages list
      setInputValue(''); // Clear the input field after sending a message
    }
  };

  const fileInputRef = useRef(null);

  const handleFileUpload = (file) => {

    const newFileMessage = {
      type: 'file',
      fileName: file.name,
      fileSize: (file.size / 1024 / 1024).toFixed(2), // Convert bytes to MB
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), // Use actual timestamp
      isUserMessage: true, // This file message is from the user
    };
    setMessages(prevMessages => [...prevMessages, newFileMessage]);
  };
  // Function to trigger the hidden file input click
  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  // Function to handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Call the function to handle the file upload and message creation
      handleFileUpload(file);
    }
  };

  const [showSidePanel, setShowSidePanel] = useState(false);

  const toggleSidePanel = () => {
    setShowSidePanel(!showSidePanel);
  };

  const handleIframeMessage = (url) => {
    const newIframeMessage = {
      type: 'iframe',
      src: 'https://www.eecs70.org/assets/pdf/notes/n2.pdf', // URL of the file to be displayed in the iframe
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isUserMessage: true,
    };
  setMessages(prevMessages => [...prevMessages, newIframeMessage]);
  };


  const { id } = useParams();

  const [fileUrl, setFileUrl] = useState("");
  const [metadata, setMetadata] = useState({});





  return (
    <div className={`app-container ${showChat ? 'chat-active' : ''}`}>
      <Header user={user} />
      <main className={`main-content ${showChat ? 'show-chat' : ''}`}>
        {!showChat && (
          <>
            <h1>Hi, I'm Tracy</h1>
            <p>How can I help you today?</p>
            <div className="features-container">
              <div className="feature-wrapper">
                <FeatureBox
                  icon={<FaRegLightbulb />}
                  title="Examples"
                  description="Can interpret the P&ID from Highline Industries."
                />
                <ExampleBox text="Secondary example content 1" />
              </div>
              <div className="feature-wrapper">
                <FeatureBox
                  icon={<MdOutlineRememberMe />}
                  title="Capabilities"
                  description="Remembers what user said earlier in the conversation."
                />
                <ExampleBox text="Secondary example content 2" />
              </div>
              <div className="feature-wrapper">
                <FeatureBox
                  icon={<AiOutlineExclamationCircle />}
                  title="Limitations"
                  description="May occasionally generate incorrect information."
                />
                <ExampleBox text="Secondary example content 3" />
              </div>
            </div>
          </>
        )}
        {renderChatBubbles()}
        {/* This will conditionally render the chat bubbles */}
        
      </main>
      {showSidePanel && <SidePanel onClose={() => setShowSidePanel(false)} />}

      <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }} // Make the file input invisible
        />

      <div className='bottom-container'>
        <div className="action-buttons">
          <button className="action-button" onClick={handleUploadClick}>Upload</button>
          <button className="action-button" onClick={handleAnswerQuestion}>Answer Question</button>
          <button className="action-button" onClick={toggleSidePanel}>Extract Data</button>
          <button className="action-button">Incident Capture</button>
        </div>
        <div className="chat-bar">
          <input
            type="text"
            className="chat-input"
            placeholder="Send a message..."
            value={inputValue} // Bind the input value to the state
            onChange={(e) => setInputValue(e.target.value)} // Update the state when the input changes
          />
          <button className="chat-send-button" onClick={handleSendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
