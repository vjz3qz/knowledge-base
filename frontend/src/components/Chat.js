// Chat.js

import React, { useState, useRef, useEffect } from "react";
import ChatBubble from "../ui/ChatBubble";
import FileMessage from "../ui/FileMessage";
import IframeMessage from "../ui/IframeMessage";
import ActionButton from "../ui/ActionButton"; // Import the new ActionButton component
import ChatInputBar from "../subcomponents/ChatInputBar";
import FeatureSection from "../subcomponents/FeatureSection";
import getSearchResults from "../utils/GetSearchResults";
import axios from "axios";
import TableMessage from "../ui/TableMessage";

const Chat = ({
  user,
  setFileIdAndOpenDocumentViewer,
  showSidePanel,
  fileId,
  setResultsAndOpenDocumentSearch,
}) => {

  const data = [
    {
      symbolId: 0,
      symbolType: "EQU",
      associatedText: "EQU_TK-583034",
      detectionMethod: "Manual",
      connectedSymbols: 43,
    },
    {
      symbolId: 1,
      symbolType: "VAR",
      associatedText: "VAR_DX-920401",
      detectionMethod: "Automated",
      connectedSymbols: 27,
    },  
    {
      symbolId: 2,
      symbolType: "FUNC",
      associatedText: "FUNC_LM-840200",
      detectionMethod: "Semi-Automatic",
      connectedSymbols: 15,
    },  
    {
      symbolId: 3,
      symbolType: "EQU",
      associatedText: "EQU_TK-583034",
      detectionMethod: "Manual",
      connectedSymbols: 43,
    },
    {
      symbolId: 4,
      symbolType: "VAR",
      associatedText: "VAR_DX-920401",
      detectionMethod: "Automated",
      connectedSymbols: 27,
    },
    {
      symbolId: 5,
      symbolType: "FUNC",
      associatedText: "FUNC_LM-840200",
      detectionMethod: "Semi-Automatic",
      connectedSymbols: 15,
    },
    {
      symbolId: 6,
      symbolType: "EQU",
      associatedText: "EQU_TK-583034",
      detectionMethod: "Manual",
      connectedSymbols: 43,
    },
    {
      symbolId: 7,
      symbolType: "VAR",
      associatedText: "VAR_DX-920401",
      detectionMethod: "Automated",
      connectedSymbols: 27,
    },
  ];
  const newIframeMessage = {
    type: "table",
    src: data,
    timestamp: new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    isUserMessage: false,
  };
  
  // State Declarations
  const [messages, setMessages] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [uploadingStatus, setUploadingStatus] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [highlightUploadButton, setHighlightUploadButton] = useState(false);
  const [highlightDocumentSearchButton, setHighlightDocumentSearchButton] =
    useState(false);
  const [highlightExtractDataButton, setHighlightExtractDataButton] =
    useState(false);
  const [highlightIncidentCaptureButton, setHighlightIncidentCaptureButton] =
    useState(false);

  const [incidentQuestionResponseNumber, setIncidentQuestionResponseNumber] = useState(0);

  const incrementIncidentQuestionResponseNumber = () => {
    setIncidentQuestionResponseNumber((incidentQuestionResponseNumber + 1) % 7);
    return (incidentQuestionResponseNumber + 1) % 7;
  };

  const questions = [
    "What is the date/time of the incident?",
    "Who was involved in the incident?",
    "What components were involved?",
    "Were there any injuries?",
    "Can you tell me more about what happened?",
    "What was done to solve the issue?",
  ];

  // SUPPORT QUESTION ANSWER ONLY WITHOUT DOCS
  const [
    highlightAnswerGeneralQuestionButton,
    setHighlightAnswerGeneralQuestionButton,
  ] = useState(false);
  const [
    highlightAnswerDocumentQuestionButton,
    setHighlightAnswerDocumentQuestionButton,
  ] = useState(false);

  // Ref Declarations
  const fileInputRef = useRef(null);

  // Event Handling Functions

  const handleUploadClick = () => {
    setHighlightUploadButton(true);
    fileInputRef.current.click();
    setHighlightDocumentSearchButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);
    setHighlightAnswerDocumentQuestionButton(false);
    setHighlightAnswerGeneralQuestionButton(false);
  };
  const handleDocumentSearchClick = () => {
    setHighlightDocumentSearchButton(true);
    setHighlightUploadButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);
    setHighlightAnswerDocumentQuestionButton(false);
    setHighlightAnswerGeneralQuestionButton(false);
  };
  const handleExtractDataClick = () => {
    setHighlightExtractDataButton(true);
    setHighlightUploadButton(false);
    setHighlightDocumentSearchButton(false);
    setHighlightIncidentCaptureButton(false);
    setHighlightAnswerDocumentQuestionButton(false);
    setHighlightAnswerGeneralQuestionButton(false);
  };
  const handleIncidentCaptureClick = () => {
    setHighlightIncidentCaptureButton(true);
    setHighlightUploadButton(false);
    setHighlightDocumentSearchButton(false);
    setHighlightExtractDataButton(false);
    setHighlightAnswerDocumentQuestionButton(false);
    setHighlightAnswerGeneralQuestionButton(false);
  };

  // create click methods for general question and document question
  const handleAnswerGeneralQuestionClick = () => {
    setHighlightAnswerGeneralQuestionButton(true);
    setHighlightAnswerDocumentQuestionButton(false);
    setHighlightUploadButton(false);
    setHighlightDocumentSearchButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);
  };
  const handleAnswerDocumentQuestionClick = () => {
    setHighlightAnswerDocumentQuestionButton(true);
    setHighlightAnswerGeneralQuestionButton(false);
    setHighlightUploadButton(false);
    setHighlightDocumentSearchButton(false);
    setHighlightExtractDataButton(false);
    setHighlightIncidentCaptureButton(false);
  };

  const [metadata, setMetadata] = useState({});

  // create a use effect for fetching metadata with fileid as a dependency
  useEffect(() => {
    if (fileId) {
      fetchMetadata();
    }
  }, [fileId]);
  const fetchMetadata = async () => {
    const result = await axios.get(
      `http://localhost:5001/api/v2/view-metadata/${fileId}`
    );
    // Here you would load the document's details, including fetching the summary and setting the file name
    setMetadata(result.data);
  };

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Message Handling Functions
  async function handleSendMessage() {
    await sleep(3000);
    if (inputValue.trim()) {
      const newMessage = { text: inputValue, isUserMessage: true };
      if (highlightAnswerDocumentQuestionButton) {
        const payload = {
          user_message: inputValue,
          conversation_history: messages.map((m) => m.content),
          id: fileId,
          file_type: metadata["file_type"],
        };
        const result = await axios.post(
          "http://localhost:5001/api/v2/document-chat",
          payload
        );
        const responseMessage = result.data.response;
        setMessages([
          ...messages,
          { text: inputValue, isUserMessage: true },
          { text: responseMessage, isUserMessage: false },
        ]);
        setInputValue("");
      } else if (highlightDocumentSearchButton) {
        const [answer, results] = await getSearchResults(inputValue);
        const newAnswerMessage = {
          text: `Searched available documents. Found ${results.length} relevant documents.`,
          isUserMessage: false,
        };
        setMessages([...messages, newMessage, newAnswerMessage]);
        setResultsAndOpenDocumentSearch(results);
        setHighlightDocumentSearchButton(false);
      } else if (highlightExtractDataButton) {

        // TODO hard code with responses right now
        // iframe components response
        // iframe specific component response

        // add new iframe message to messages
        setMessages([...messages, newMessage, newIframeMessage]);




        setHighlightExtractDataButton(false);
      } else if (highlightIncidentCaptureButton) {


        // chat message
        const newAnswerMessage = { text: questions[incidentQuestionResponseNumber], isUserMessage: false };
        const newNumber = incrementIncidentQuestionResponseNumber();
        setMessages([...messages, newMessage, newAnswerMessage]);
        if (newNumber === 0) { // need to unhighlight after we get the last response
          // send messages to back end to generate the incident report, display here
          // for now, create a dummy incident report
          const incidentReport = {
            "date": "2021-09-15T00:00:00.000Z",
            "time": "2021-09-15T00:00:00.000Z",
            "location": "San Francisco",
            "people": "Rahul Kumar, John Doe",
            "components": "Engine, Wing",
            "injuries": "None",
            "description": "Engine failure",
            "resolution": "Replaced engine",
            "id": "613f4b6e3b7f1f0f8c8a9a9d"
          }
          // open document viewer with incident report
          setFileIdAndOpenDocumentViewer(incidentReport.id);
          const newResponseMessage = { text: "Incident report generated. Please let me know if you would like to make any edits!", isUserMessage: false };
          setMessages([...messages, newResponseMessage]);
          // TODO createa better sample incudent report
          setHighlightIncidentCaptureButton(false);
        }
      } else if (highlightAnswerGeneralQuestionButton) {
        setHighlightAnswerGeneralQuestionButton(false);
      }
      setInputValue("");
      setShowChat(true);
    }
  }
  const handleTableMessage = (data) => {
    const newTableMessage = {
      type: "table",
      src: data, // Updated to use the passed URL
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      isUserMessage: false,
    };
    setMessages((prevMessages) => [...prevMessages, newTableMessage]);
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
    setMessages((prevMessages) => [
      ...prevMessages,
      newFileMessage,
      { text: `Successfully uploaded ${file.name}.`, isUserMessage: false },
    ]);
    setHighlightUploadButton(false);
    setShowChat(true);
    return fileId;
  }

  const uploadAndGetFileId = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("content_type", file.type);
    // create an array with the mime types of txt, pdf, docx
    const fileTypes = [
      "text/plain",
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
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
    formData.append("file_type", uploadType);

    try {
      const response = await axios.post(
        "http://localhost:5001/api/v2/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Check if response includes file_id
      if (response.status === 200 && response.data.file_id) {
        return response.data.file_id;
      } else {
        // Handle the case where file_id is not present in the response
        console.log("Upload successful, but no file ID returned.");
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
      setFileIdAndOpenDocumentViewer(fileId);
      // fileInputRef = useRef(null);
      // WOnt upload if same, see if we want to change that
    }
  };

  // Render Functions
  const renderChatBubbles = () => {
    return (
      showChat && (
        <div
          className={`chat-container ${
            showSidePanel ? "full-width" : "half-width"
          }`}
        >
          {messages.map((message, index) =>
            message.type === "file" ? (
              <FileMessage key={index} {...message} />
            ) : message.type === "table" ? (
              <TableMessage key={index} {...message} />
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

      <div
        className={`bottom-container ${
          showSidePanel ? "full-width" : "half-width"
        }`}
      >
        <div className="action-buttons">
          {/* <ActionButton
            onClick={handleUploadClick}
            highlight={highlightUploadButton}
            label="Upload"
          /> */}
          <ActionButton
            onClick={handleDocumentSearchClick}
            highlight={highlightDocumentSearchButton}
            label="Document Search"
          />
          {/* <ActionButton
            onClick={handleAnswerGeneralQuestionClick}
            highlight={highlightAnswerGeneralQuestionButton}
            label="General Question"
          /> */}
          <ActionButton
            onClick={handleAnswerDocumentQuestionClick}
            highlight={highlightAnswerDocumentQuestionButton}
            label="Query Document"
            disabled={!fileId} // Disable the button if fileId is false or undefined
          />
          <ActionButton
            onClick={handleExtractDataClick}
            highlight={highlightExtractDataButton}
            label="Extract Data"
            disabled={!fileId} // Disable the button if fileId is false or undefined
          />
          {/* <ActionButton
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
