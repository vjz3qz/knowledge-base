import React, { useState } from "react";
import axios from 'axios';
import "../styles/DocumentChat.css";
import { Document, Page } from 'react-pdf';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;



function DocumentChat() {
    const [pdfFile, setPdfFile] = useState(null);
    const [pdfFileName, setPdfFileName] = useState("");
    const [pdfId, setPdfId] = useState("");
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [summary, setSummary] = useState("");
  
    const onFileChange = (e) => {
      setPdfFile(e.target.files[0]);
    };
  
    const onUpload = async () => {
      const formData = new FormData();
      formData.append('file', pdfFile);
      const result = await axios.post("http://localhost:5001/upload", formData);
      if (result.data.id) {
        setPdfId(result.data.id);
        setSummary(result.data.summary);  // Set the summary after uploading
        setPdfFileName(result.data.filename);
      }
    };
  
    const sendMessage = async () => {
      const payload = {
        current_message: inputValue,
        conversation_history: messages.map(m => m.content),
        id: pdfId
      };
      const result = await axios.post("http://localhost:5001/chat_interact", payload);
      const responseMessage = result.data.response;
      setMessages([...messages, { type: 'user', content: inputValue }, { type: 'server', content: responseMessage }]);
      setInputValue("");
    };
  
    return (
      <div className="app">
        <div className="chat-panel">
          <div className="chat-header">Trace AI</div>
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
          <div className="chat-input">
            {!pdfId && (
              <div>
                <input type="file" onChange={onFileChange} accept=".pdf" />
                <button onClick={onUpload}>Upload PDF</button>
              </div>
            )}
            {pdfId && (
              <>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type a message..."
                  className="chat-input-field"
                />
                <button onClick={sendMessage} className="chat-send-button">
                  Send
                </button>
              </>
            )}
          </div>
        </div>
        <div className="document-panel">
          <div className="document-header">
            {pdfFileName}
          </div>
          <div className="document-content">
            {/* ADD DOCUMENT ITSELF HERE TO VIEW */}
            <Document file={pdfFile} onLoadError={error => console.error(error)}>
  <Page pageNumber={1} onRenderError={error => console.error(error)} />
</Document>

          </div>
        </div>
        {/* If there's a summary after uploading the PDF, display it */}
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
