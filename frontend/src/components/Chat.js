// Chat.js

import React, { useState, useRef } from "react";
import ChatBubble from "../ui/ChatBubble";
import FileMessage from "../ui/FileMessage";
import IframeMessage from "../ui/IframeMessage";
import ActionButton from '../ui/ActionButton'; // Import the new ActionButton component
import ChatInputBar from "../subcomponents/ChatInputBar";
import FeatureSection from "../subcomponents/FeatureSection";
import getSearchResults from "../utils/GetSearchResults";
import { pdfjs } from "react-pdf";
import axios from "axios";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const Chat = ({ user, setFileIdAndOpenDocumentViewer, showSidePanel, setResultsAndOpenDocumentSearch }) => {

  // State Declarations
  const [messages, setMessages] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [uploadingStatus, setUploadingStatus] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [highlightUploadButton, setHighlightUploadButton] = useState(false);
  const [highlightAnswerQuestionButton, setHighlightAnswerQuestionButton] = useState(true);
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
    // setHighlightAnswerQuestionButton(false);
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
  async function handleSendMessage() {
    if (inputValue.trim()) {
      const newMessage = { text: inputValue, isUserMessage: true };
      
      if (highlightAnswerQuestionButton) {

        const [answer, results] = await getSearchResults(inputValue);
        const newAnswerMessage = { text: answer, isUserMessage: false };
        setMessages([...messages, newMessage, newAnswerMessage]);
        setResultsAndOpenDocumentSearch(results);
        // setHighlightAnswerQuestionButton(false);
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
  async function handleFileUpload(file) {
    const newFileMessage = {
      type: "file",
      fileName: file.name,
      fileSize: (file.size / 1024 / 1024).toFixed(2),
      fileType: file.type, // Accessing the MIME type of the file
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      isUserMessage: true,
    };
    const fileId = await uploadAndGetFileId(file);
    setMessages((prevMessages) => [...prevMessages, newFileMessage, { text: `Successfully uploaded ${file.name}.`, isUserMessage: false }]);
    setHighlightUploadButton(false);
    setShowChat(true);
    return fileId
  };




  const uploadAndGetFileId = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('content_type', file.type);
    // create an array with the mime types of txt, pdf, docx
    const fileTypes = ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    // create an array with the mime types of jpg, png, jpeg
    const imageTypes = ["image/jpg", "image/png", "image/jpeg"];
    // create an array with the mime types of mp4
    const videoTypes = ["video/mp4"];
    // decide what type of file it is, and set uploadType accordingly to text, image, or video
    let uploadType = "";
    if (fileTypes.includes(file.type)) {
      uploadType = "text";
    } else if (imageTypes.includes(file.type)) {
      uploadType = "diagram";
      // TODO support pdf diagrams
    } else if (videoTypes.includes(file.type)) { 
      uploadType = "video";
    } else {
      // if the file type is not one of the above, then it is unsupported
      // break out of the function
      return;
    }
    formData.append('file_type', uploadType);

    try {
      const response = await axios.post('http://localhost:5001/api/v2/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    
      // Check if response includes file_id
      if (response.status === 200 && response.data.file_id) {
        return response.data.file_id;
      } else {
        // Handle the case where file_id is not present in the response
        console.log('Upload successful, but no file ID returned.');
        return null;
      }
    } catch (error) {
      // Update error handling to include both response error or other errors
      const errorMessage = error.response?.data?.error || error.message;
      console.log(errorMessage);
      return null;
    }
    
  };





  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadingStatus(true);

      const fileId = await handleFileUpload(file);
      setUploadingStatus(false);
      // TODO fetch via file id
      //setFileIdAndOpenDocumentViewer(fileId);
      // fileInputRef = useRef(null);
      // WOnt upload if same, see if we want to change that
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
                timestamp={new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
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
          {/* <ActionButton
            onClick={handleAnswerQuestionClick}
            highlight={highlightAnswerQuestionButton}
            label="Answer Question"
          /> */}
          {/* <ActionButton
            onClick={handleExtractDataClick}
            highlight={highlightExtractDataButton}
            label="Extract Data"
          />
          <ActionButton
            onClick={handleIncidentCaptureClick}
            highlight={highlightIncidentCaptureButton}
            label="Incident Capture"
          /> */}
        </div>
        <ChatInputBar
          inputValue={inputValue}
          uploadingStatus={uploadingStatus}
          setInputValue={setInputValue}
          handleSendMessage={handleSendMessage}
        />
        
      </div>
    </div>
  );
};

export default Chat;
