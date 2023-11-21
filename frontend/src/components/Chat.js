// Chat.js

import React, { useState, useRef } from "react";
import ChatBubble from "../ui/ChatBubble";
import FileMessage from "../ui/FileMessage";
import IframeMessage from "../ui/IframeMessage";
import FeatureBox from "../ui/FeatureBox";
import { ReactComponent as Logo } from "../assets/logo.svg";
import { FaRegLightbulb } from "react-icons/fa";
import { MdOutlineRememberMe } from "react-icons/md";
import { AiOutlineExclamationCircle } from "react-icons/ai";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const Chat = ({ user }) => {
  // State Declarations
  const [messages, setMessages] = useState([
    { text: "Hello I'm Tracy, how can I help?", isUserMessage: false },
  ]);
  const [showChat, setShowChat] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [showSidePanel, setShowSidePanel] = useState(false);
  const [highlightUploadButton, setHighlightUploadButton] = useState(false);
  const [highlightAnswerQuestionButton, setHighlightAnswerQuestionButton] =
    useState(false);
  const [highlightExtractDataButton, setHighlightExtractDataButton] =
    useState(false);
  const [highlightIncidentCaptureButton, setHighlightIncidentCaptureButton] =
    useState(false);

  // Ref Declarations
  const fileInputRef = useRef(null);

  // Event Handling Functions

  const handleUploadClick = () => {
    setHighlightUploadButton(true);
    fileInputRef.current.click();
    setHighlightAnswerQuestionButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);

  };
  const handleAnswerQuestionClick = () => {
    setHighlightAnswerQuestionButton(true);
    setHighlightUploadButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);
  };
  const handleExtractDataClick = () => {
    setHighlightExtractDataButton(true);
    setHighlightUploadButton(false);
    setHighlightAnswerQuestionButton(false);
    setHighlightIncidentCaptureButton(false);
  };
  const handleIncidentCaptureClick = () => {
    setHighlightIncidentCaptureButton(true);
    setHighlightUploadButton(false);
    setHighlightAnswerQuestionButton(false);
    setHighlightExtractDataButton(false);
  };

  // Message Handling Functions
  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const newMessage = { text: inputValue, isUserMessage: true };
      setMessages([...messages, newMessage]);
      setInputValue("");
      setShowChat(true);
    }
  };

  const handleIframeMessage = (url) => {
    const newIframeMessage = {
      type: "iframe",
      src: url, // Updated to use the passed URL
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      isUserMessage: true,
    };
    setMessages((prevMessages) => [...prevMessages, newIframeMessage]);
  };

  // File Handling Functions
  const handleFileUpload = (file) => {
    const newFileMessage = {
      type: "file",
      fileName: file.name,
      fileSize: (file.size / 1024 / 1024).toFixed(2),
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      isUserMessage: true,
    };
    setMessages((prevMessages) => [...prevMessages, newFileMessage]);
    setHighlightUploadButton(false);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) handleFileUpload(file);
  };

  // Render Functions
  const renderChatBubbles = () => {
    return (
      showChat && (
        <div className="chat-container">
          {messages.map((message, index) =>
            message.type === "file" ? (
              <FileMessage key={index} {...message} />
            ) : message.type === "iframe" ? (
              <IframeMessage key={index} {...message} />
            ) : (
              <ChatBubble
                key={index}
                message={message.text}
                isUserMessage={message.isUserMessage}
              />
            )
          )}
        </div>
      )
    );
  };

  // Main Render
  return (
    <div className={`app-container ${showChat ? "chat-active" : ""}`}>
      <main className={`main-content ${showChat ? "show-chat" : ""}`}>
        {!showChat && (
          <>
            <Logo className="logo-large" />
            <p>How can I help you today?</p>
            <div className="features-container">
              <FeatureBox
                icon={<FaRegLightbulb />}
                title="Examples"
                description="Can interpret the P&ID from Highline Industries."
              />
              <FeatureBox
                icon={<MdOutlineRememberMe />}
                title="Capabilities"
                description="Remembers what user said earlier in the conversation."
              />
              <FeatureBox
                icon={<AiOutlineExclamationCircle />}
                title="Limitations"
                description="May occasionally generate incorrect information."
              />
            </div>
          </>
        )}
        {renderChatBubbles()}
      </main>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <div className="bottom-container">
        <div className="action-buttons">
          <button
            className={`${
              highlightUploadButton
                ? "action-button-black"
                : "action-button-white"
            }`}
            onClick={handleUploadClick}
          >
            Upload
          </button>
          <button 
            className={`${
              highlightAnswerQuestionButton
                ? "action-button-black"
                : "action-button-white"
            }`} 
            onClick={handleAnswerQuestionClick}
            >
            Answer Question
          </button>
          <button 
            className={`${
              highlightExtractDataButton
                ? "action-button-black"
                : "action-button-white"
            }`} 
            onClick={handleExtractDataClick}
            >
            Extract Data
          </button>
          <button
            className={`${
              highlightIncidentCaptureButton
                ? "action-button-black"
                : "action-button-white"
            }`}
            onClick={handleIncidentCaptureClick}
          >
            Incident Capture
          </button>
        </div>
        <div className="chat-bar">
          <input
            type="text"
            className="chat-input"
            placeholder="Send a message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button className="chat-send-button" onClick={handleSendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
