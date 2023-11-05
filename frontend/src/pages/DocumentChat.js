import Summary from "../components/Summary";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "../styles/DocumentChat.css";
import { Document, Page } from "react-pdf";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;


function DocumentChat() {
  const { id } = useParams();

  const [fileUrl, setFileUrl] = useState("");
  const [metadata, setMetadata] = useState({});

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  // Function to initialize chat when component mounts or when document ID changes
  useEffect(() => {
    const fetchMessages = async () => {
      const result = await axios.get(`http://localhost:5001/api/v2/view/${id}`);
      setFileUrl(result.data.url);
    };

    const fetchMetadata = async () => {
      const result = await axios.get(
        `http://localhost:5001/api/v2/view-metadata/${id}`
      );
      // Here you would load the document's details, including fetching the summary and setting the file name
      setMetadata(result.data);
      
    };
    try {
      fetchMessages();
      fetchMetadata();
    } catch (error) {
      console.log(error);
    }
  }, [id]);

  const sendMessage = async () => {
    const payload = {
      user_message: inputValue,
      conversation_history: messages.map((m) => m.content),
      id: id,
      file_type: metadata["file_type"],
    };
    const result = await axios.post(
      "http://localhost:5001/api/v2/document-chat",
      payload
    );
    const responseMessage = result.data.response;
    setMessages([
      ...messages,
      { type: "user", content: inputValue },
      { type: "server", content: responseMessage },
    ]);
    setInputValue("");
  };

  return (
    <div className="container">
      <div className="chat-panel">
        <div className="chat-content">
          {messages.map((message, index) => (
            <div
              key={index}
              className={
                message.type === "user" ? "user-input" : "model-response"
              }
            >
              {message.content}
            </div>
          ))}
        </div>
        <hr className="section-divider"></hr>
        <div className="chat-input">
          {id && (
            <div className="row">
              <div className="col-md-8">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type a message..."
                  className="chat-input-field form-control"
                />
              </div>
              <div className="col-md-4">
                <button
                  onClick={sendMessage}
                  className="chat-send-button btn btn-primary"
                >
                  Send
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="document-panel">
        {/* ADD DOCUMENT ITSELF HERE TO VIEW */}
        {id && fileUrl && metadata && (
          <div>
            <div className="document-header">{metadata['name']}</div>
            <div className="document-content">
              {metadata["content_type"] === "application/pdf" ? (
                <Document
                  file={fileUrl}
                  onLoadError={(error) => console.error(error)}
                >
                  <Page
                    pageNumber={1}
                    onRenderError={(error) => console.error(error)}
                  />
                </Document>
              ) : (
                <img src={fileUrl} alt={metadata['name']} />
              )}
            </div>
          </div>
        )}
      </div>
      {/* If there's a summary after uploading the doc, display it */}
      {id && fileUrl && metadata && <Summary id={id} metadata={metadata} />}
    </div>
  );
}

export default DocumentChat;
