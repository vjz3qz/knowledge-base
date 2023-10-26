import React, { useState } from "react";
import axios from 'axios';
import "../styles/DocumentChat.css";
import { Document, Page } from 'react-pdf';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;



function OperatorChat() {
    const [pdfFile, setPdfFile] = useState(null);
    const [pdfFileName, setPdfFileName] = useState("");
    const [pdfId, setPdfId] = useState("");
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [summary, setSummary] = useState("");
  
    const sendMessage = async () => {
      const payload = {
        current_message: inputValue,
        conversation_history: messages.map(m => m.content),
        id: pdfId
      };
      const result = await axios.post("http://localhost:5001/api/v1/document-chat", payload);
      const responseMessage = result.data.response;
      setMessages([...messages, { type: 'user', content: inputValue }, { type: 'server', content: responseMessage }]);
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
          <hr className='section-divider'></hr>
          <div class="chat-input">
            <div class="row">
              <div class="col-md-9">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type a message..."
                  class="form-control chat-input-field"
                />
              </div>
              <div class="col-md-3">
                <button class="btn btn-primary btn-sm" style={{fontSize: '18px'}}>Send</button>
                <button class="btn btn-primary btn-sm ml-1" style={{ marginLeft: '5px', fontSize: '18px'}}>Finish</button>
              </div>
            </div>
          </div>
          </div>
        </div>
    );
  }


export default OperatorChat;
