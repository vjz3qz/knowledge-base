import React, { useState } from "react";
import "./ChatPage.css";

function ChatPage() {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);

  function giveInput() {
    if (inputValue.trim() !== "") {
      // This is the hardcoded response
      const responseText = "Thanks for your message! This is a hardcoded response.";

      const newMessage = { type: 'user', content: inputValue };
      const newResponse = { type: 'model', content: responseText };
      setMessages([...messages, newMessage, newResponse]);
      setInputValue("");
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      giveInput();
    }
  };

  return (
    <div className="app">
      <div className="chat-panel">
        <div className="chat-header">Trace AI</div>
        <div className="chat-content">
          {messages.map((message, index) => (
            <div key={index} className={message.type === 'user' ? 'user-input' : 'model-response'}>
                {message.content}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message..."
            className="chat-input-field"
          />
          <button onClick={giveInput} className="chat-send-button">
            Send
          </button>
        </div>
      </div>
      <div className="document-panel">
        <div className="document-header">
          production-plant-P&ID-2.14.2023.pdf
        </div>
        <div className="document-content">
          <img
            style={{
              width: "512px",
              height: "512px",
              border: "4px solid gray",
              borderRadius: "8px",
            }}
            alt="hero"
            src={`${process.env.PUBLIC_URL}/images/diagram.jpeg`}
          />
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
