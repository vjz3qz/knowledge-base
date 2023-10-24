import React, { useState } from 'react';
import '../styles/Reporting.css';

const IncidentReporting = () => {
  const [reportType, setReportType] = useState(null);
  const [timeOfIncident, setTimeOfIncident] = useState('');
  const [location, setLocation] = useState('');
  const [typeOfIncident, setTypeOfIncident] = useState('');
  const [description, setDescription] = useState('');
  const [fix, setFix] = useState('');
  const [notes, setNotes] = useState('');
  const [workLocation, setWorkLocation] = useState('');
  const [workDescription, setWorkDescription] = useState('');
  const [workProblems, setWorkProblems] = useState('');
  const [workSolutions, setWorkSolutions] = useState('');

  const handleSubmit = async () => {
    const data = {
      name: "John Doe",
      employeeId: "12345",
      role: "Hydraulics Engineer",
      date: new Date().toLocaleDateString(),
      reportType,
      timeOfIncident,
      location,
      typeOfIncident,
      description,
      fix,
      notes,
      workLocation,
      workDescription,
      workProblems,
      workSolutions
    };

    try {
      const response = await fetch('YOUR_API_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      console.log(result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container">
      <h1>Report Form</h1>
      
      {/* Non-editable fields */}
      <div>
        <label>Name: </label>
        <input type="text" readOnly value="John Doe" className="read-only"/>
      </div>
      <div>
        <label>Employee ID: </label>
        <input type="text" readOnly value="12345" className="read-only"/>
      </div>
      <div>
        <label>Role: </label>
        <input type="text" readOnly value="Hydraulics Engineer" className="read-only"/>
      </div>
      <div>
        <label>Date: </label>
        <input type="text" readOnly value={new Date().toLocaleDateString()} className="read-only"/>
      </div>

      {/* Questions based on report type */}
      {reportType === 'incident' ? (
        <div>
          <div>
            <label>Time of Incident: </label>
            <input type="time" value={timeOfIncident} onChange={e => setTimeOfIncident(e.target.value)} />
          </div>
          <div>
            <label>Where have you been working: </label>
            <select value={location} onChange={e => setLocation(e.target.value)}>
              <option value="Location 1">Location 1</option>
              <option value="Location 2">Location 2</option>
              <option value="Location 3">Location 3</option>
            </select>
          </div>
          <div>
            <label>Type of Incident: </label>
            <input type="text" value={typeOfIncident} onChange={e => setTypeOfIncident(e.target.value)} />
          </div>
          <div>
            <label>Describe the Incident: </label>
            <textarea value={description} onChange={e => setDescription(e.target.value)}></textarea>
          </div>
          <div>
            <label>What did you do to fix it: </label>
            <textarea value={fix} onChange={e => setFix(e.target.value)}></textarea>
          </div>
          <div>
            <label>Additional Notes: </label>
            <textarea value={notes} onChange={e => setNotes(e.target.value)}></textarea>
          </div>
        </div>
      ) : reportType === 'work' ? (
        <div>
          <div>
            <label>Where have you been working: </label>
            <select value={workLocation} onChange={e => setWorkLocation(e.target.value)}>
              <option value="Location 1">Location 1</option>
              <option value="Location 2">Location 2</option>
              <option value="Location 3">Location 3</option>
            </select>
          </div>
          <div>
            <label>What have you been working on: </label>
            <textarea value={workDescription} onChange={e => setWorkDescription(e.target.value)}></textarea>
          </div>
          <div>
            <label>What problems did you encounter: </label>
            <textarea value={workProblems} onChange={e => setWorkProblems(e.target.value)}></textarea>
          </div>
          <div>
            <label>How did you fix or move past these problems: </label>
            <textarea value={workSolutions} onChange={e => setWorkSolutions(e.target.value)}></textarea>
          </div>
        </div>
      ) : null}

      {/* Buttons to select type of report */}
      <div className="button-group">
        <button onClick={() => setReportType('incident')}>Incident Report</button>
        <button onClick={() => setReportType('work')}>Work Report</button>
      </div>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default IncidentReporting;
