// App.js or main file
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/sidebar/Sidebar';
import ChatPage from './components/chat/ChatPage';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <Routes>
          <Route path="/chat" component={<ChatPage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
