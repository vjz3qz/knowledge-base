import React, { useState } from "react";
import axios from "axios";
import "../styles/DocumentChat.css";
import { Document, Page } from "react-pdf";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

function DocumentChat() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [id, setId] = useState("");
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [summary, setSummary] = useState("");

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    let result;
    try {
      // check if image or  first
      if (
        file.type === "image/jpeg" ||
        file.type === "image/png" ||
        file.type === "image/jpg"
      ) {
        result = await axios.post(
          "http://localhost:5001/api/v1/upload-image",
          formData
        );
      } else {
        result = await axios.post(
          "http://localhost:5001/api/v1/upload",
          formData
        );
      }
    } catch (error) {
      console.error("Error uploading the file:", error);
    }
    if (result.data.id) {
      setId(result.data.id);
      setSummary(result.data.summary); // Set the summary after uploading
      setFileName(result.data.filename);
    }
  };

  const sendMessage = async () => {
    const payload = {
      current_message: inputValue,
      conversation_history: messages.map((m) => m.content),
      id: id,
    };
    const result = await axios.post(
      "http://localhost:5001/api/v1/document-chat",
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
          {!id && (
            <div className="row">
              <div className="col-md-8">
                <input
                  type="file"
                  onChange={onFileChange}
                  accept=".pdf,.jpeg,.jpg,.png" // TODO accept  and images
                  className="form-control choose-file"
                />
              </div>
              <div className="col-md-4">
                <button onClick={onUpload} className="btn btn-primary">
                  Upload
                </button>
              </div>
            </div>
          )}
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
        <div className="document-header">{fileName}</div>
        <div className="document-content">
          {/* ADD DOCUMENT ITSELF HERE TO VIEW */}
          {file && (file.type === "application/pdf" ? (
            <Document file={file} onLoadError={(error) => console.error(error)}>
              <Page
                pageNumber={1}
                onRenderError={(error) => console.error(error)}
              />
            </Document>
          ) : (
            <img src={URL.createObjectURL(file)} alt="uploaded file" />
          ))}
        </div>
      </div>
      {/* If there's a summary after uploading the doc, display it */}
      {summary && (
        <div className="document-panel">
          <div className="document-header">Summary</div>
          <div className="document-content">
            <p>{summary}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentChat;
