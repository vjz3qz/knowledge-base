import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/sidebar/Sidebar';
import ChatPage from './components/chat/ChatPage';
import IncidentReporting from './components/IncidentReporting';
import Dashboard from './components/dashboard/Dashboard';
import './App.css'; // Assuming you have an App.css file for the styles

function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="sidebar-wrapper">
          <Sidebar />
        </div>
        <div className="content-wrapper">
          <Routes>
            <Route path="/dashboard" element={<Dashboard/>}/>
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/incident-reports" element={<IncidentReporting/>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
