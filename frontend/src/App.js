// import React from 'react';
// import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Sidebar from './components/sidebar/Sidebar';
// import ChatPage from './components/chat/ChatPage';
// import IncidentReporting from './components/IncidentReporting';
// import Dashboard from './components/dashboard/Dashboard';
// import './App.css'; // Assuming you have an App.css file for the styles

// function App() {
//   return (
//     <Router>
//       <div className="app-container">
//         <div className="sidebar-wrapper">
//           <Sidebar />
//         </div>
//         <div className="content-wrapper">
//           <Routes>
//             <Route path="/dashboard" element={<Dashboard/>}/>
//             <Route path="/chat" element={<ChatPage />} />
//             <Route path="/incident-reports" element={<IncidentReporting/>} />
//           </Routes>
//         </div>
//       </div>
//     </Router>
//   );
// }

// export default App;


import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [pageSelection, setPageSelection] = useState("Single page");
  const [page, setPage] = useState(1);
  const [question, setQuestion] = useState("");
  const [summary, setSummary] = useState("");

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('page_selection', pageSelection);
    formData.append('page_number', page);
    formData.append('question', question);
    
    const result = await axios.post("http://localhost:5001/upload", formData);
    setSummary(result.data.summary);
  }

  return (
    <div className="App">
      <h1>PDF Summarizer & QA</h1>
      <form onSubmit={onSubmit}>
        <input type="file" onChange={onFileChange} accept=".pdf" />
        <div>
          <label>
            <input type="radio" value="Single page" checked={pageSelection === "Single page"} onChange={(e) => setPageSelection(e.target.value)} />
            Single page
          </label>
          <label>
            <input type="radio" value="Overall Summary" checked={pageSelection === "Overall Summary"} onChange={(e) => setPageSelection(e.target.value)} />
            Overall Summary
          </label>
          <label>
            <input type="radio" value="Question" checked={pageSelection === "Question"} onChange={(e) => setPageSelection(e.target.value)} />
            Question
          </label>
        </div>
        {pageSelection === "Single page" && <input type="number" value={page} onChange={(e) => setPage(e.target.value)} />}
        {pageSelection === "Question" && <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />}
        <button type="submit">Run</button>
      </form>
      {summary && <div><h2>Summary</h2><p>{summary}</p></div>}
    </div>
  );
}

export default App;
