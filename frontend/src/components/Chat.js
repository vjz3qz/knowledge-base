// Chat.js

import React, { useState, useRef } from "react";
import ChatBubble from "../ui/ChatBubble";
import FileMessage from "../ui/FileMessage";
import IframeMessage from "../ui/IframeMessage";
import ActionButton from '../ui/ActionButton'; // Import the new ActionButton component
import ChatInputBar from "../subcomponents/ChatInputBar";
import FeatureSection from "../subcomponents/FeatureSection";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const Chat = ({ user, setFileAndOpenDocumentViewer, showSidePanel, setSearchTerm }) => {
  // State Declarations
  const [messages, setMessages] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [highlightUploadButton, setHighlightUploadButton] = useState(false);
  const [highlightAnswerQuestionButton, setHighlightAnswerQuestionButton] = useState(false);
  const [highlightExtractDataButton, setHighlightExtractDataButton] = useState(false);
  const [highlightIncidentCaptureButton, setHighlightIncidentCaptureButton] = useState(false);

  // SUPPORT QUESTION ANSWER ONLY WITHOUT DOCS
  //const [highlightAnswerQuestionButton, setHighlightAnswerQuestionButton] = useState(false);

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
      // TODO send message to backend
      // TODO conditionally render the right thing for each button
      if (highlightAnswerQuestionButton) {
        setSearchTerm(inputValue);
        setHighlightAnswerQuestionButton(false);
      } else if (highlightExtractDataButton) {
        setHighlightExtractDataButton(false);
      } else if (highlightIncidentCaptureButton) {
        setHighlightIncidentCaptureButton(false);
      }
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
    setShowChat(true);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      handleFileUpload(file);
      setFileAndOpenDocumentViewer(file);
    }
  };

  // Render Functions
  const renderChatBubbles = () => {
    return (
      showChat && (
        <div className={`chat-container ${showSidePanel ? 'full-width' : 'half-width'}`}>
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
    <div className="chat-component">
      <main className={`main-content ${showChat ? "show-chat" : ""}`}>
        {!showChat && <FeatureSection />}
        {showChat && renderChatBubbles()}
      </main>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <div className={`bottom-container ${showSidePanel ? 'full-width' : 'half-width'}`}>
        <div className="action-buttons">
          <ActionButton
            onClick={handleUploadClick}
            highlight={highlightUploadButton}
            label="Upload"
          />
          <ActionButton
            onClick={handleAnswerQuestionClick}
            highlight={highlightAnswerQuestionButton}
            label="Answer Question"
          />
          <ActionButton
            onClick={handleExtractDataClick}
            highlight={highlightExtractDataButton}
            label="Extract Data"
          />
          <ActionButton
            onClick={handleIncidentCaptureClick}
            highlight={highlightIncidentCaptureButton}
            label="Incident Capture"
          />
        </div>
        <ChatInputBar
          inputValue={inputValue}
          setInputValue={setInputValue}
          handleSendMessage={handleSendMessage}
        />
        
      </div>
    </div>
  );
};

export default Chat;
