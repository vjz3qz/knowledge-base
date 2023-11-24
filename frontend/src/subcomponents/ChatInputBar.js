import React from "react";

function ChatInputBar({
  inputValue,
  uploadingStatus,
  setInputValue,
  handleSendMessage,
}) {
  return (
    <div className="chat-bar">
      <input
        type="text"
        className="chat-input"
        placeholder={uploadingStatus ? "uploading..." : "Send a message..."}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={uploadingStatus} // Disable input when uploading
      />
      <button
        className="chat-send-button"
        onClick={handleSendMessage}
        disabled={uploadingStatus} // Disable button when uploading
      >
        Send
      </button>
    </div>
  );
}

export default ChatInputBar;
