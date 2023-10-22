import React from 'react';
import Message from './Message';

const ChatPanel = ({ messages, inputValue, setInputValue, sendMessage, handleKeyPress }) => {
  return (
    <div className="chat-panel">
      <div className="chat-header">Highline</div>
      <div className="chat-content">
        {messages.map((message, index) => (
          <Message key={index} type={message.type} content={message.content} />
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
        <button onClick={sendMessage} className="chat-send-button">Send</button> 
      </div>
    </div>
  );
};

export default ChatPanel;
