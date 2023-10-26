import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DocumentChat from './pages/DocumentChat';
import OperatorChat from './pages/OperatorChat';
import DocumentSearch from './pages/DocumentSearch';
import './styles/App.css'; // Assuming you have an App.css file for the styles



function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="sidebar-wrapper">
          <Sidebar />
        </div>
        <div className="content-wrapper">
          <Routes>
            <Route path="/document-search" element={<DocumentSearch />}/>
            <Route path="/document-chat" element={<DocumentChat />} />
            <Route path="/incident-reports" element={<OperatorChat/>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
