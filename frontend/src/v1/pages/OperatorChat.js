import React, { useState, useEffect } from "react";
import axios from 'axios';
import "../styles/DocumentChat.css";
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;


function OperatorChat() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const modelMessages = [
    { type: "model", content: "Hello Varun. Are you filing an incident report or a work report?" },
    { type: "model", content: "Where did the incident occur?" },
    { type: "model", content: "What happen in the incident?" },
    { type: "model", content: "Can you elaborate on that?" },
    { type: "model", content: "Approximately when did this incident occur?" },
    { type: "model", content: "Was this incident resolved?" },
    { type: "model", content: "How was it resolved?" },
    { type: "model", content: "Anything else I should know?" },
    { type: "model", content: "Thank you and have a great day." },
  ];

  const [modelMessageIndex, setModelMessageIndex] = useState(0);
  useEffect(() => {
      setMessages([modelMessages[0]]);
      setModelMessageIndex(1);
      },
      []
  );
  const sendMessage = () => {
    setMessages([...messages, { type: "user", content: inputValue }]);
    setInputValue("");
    
    if (modelMessageIndex < modelMessages.length) {
      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, modelMessages[modelMessageIndex]]);
        setModelMessageIndex(modelMessageIndex + 1);
      }, 1000);
    }
  }

  const submit = async () => {
    alert("Your report has been submitted.");
    
    const payload = modelMessages.reduce((acc, modelMessage, index) => {
      const userMessage = messages[index] ? messages[index].content : "";
      const combinedContent = `${modelMessage.content} ${userMessage}`;
      acc[`question${index + 1}`] = combinedContent;
      return acc;
    }, {});

    const result = await axios.post("http://localhost:5001/api/v1/upload-json", payload);

    setMessages([modelMessages[0]]);
    setInputValue("");
    setModelMessageIndex(1);
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
              <button class="btn btn-primary btn-sm"
                style={{ fontSize: '18px' }}
                onClick={sendMessage}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    sendMessage();
                  }
                }}
              >Send</button>
              <button class="btn btn-primary btn-sm ml-1"
                style={{ marginLeft: '5px', fontSize: '18px' }}
                onClick={submit}>Submit</button>
            </div>
          </div>
        </div>
        </div>
      </div>
  );
}


export default OperatorChat;
