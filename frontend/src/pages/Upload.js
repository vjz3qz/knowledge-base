import React, { useState } from 'react';
import axios from 'axios';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploadType, setUploadType] = useState('text'); // 'text' or 'diagram'
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadStatus('');
  };

  const handleUploadTypeChange = (event) => {
    setUploadType(event.target.checked ? 'diagram' : 'text');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setUploadStatus('Please select a file to upload.');
      return;
    }
    setUploadStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('content_type', file.type);
    formData.append('file_type', uploadType);

    try {
      const response = await axios.post('http://localhost:5001/api/v2/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Check response status code
      if (response.status === 200) {
        setUploadStatus('Upload successful!');
      } else {
        setUploadStatus(`Upload failed with status: ${response.status}`);
      }
    } catch (error) {
      setUploadStatus(`Upload error: ${error.message}`);
    }
  };

  return (
    <div className="upload-page">
      <h1>Upload Page</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Upload as Text:
          <input
            type="radio"
            name="uploadType"
            checked={uploadType === 'text'}
            onChange={() => setUploadType('text')}
          />
        </label>
        <label>
          Upload as Diagram:
          <input
            type="radio"
            name="uploadType"
            checked={uploadType === 'diagram'}
            onChange={() => setUploadType('diagram')}
          />
        </label>

        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {uploadStatus && <p>{uploadStatus}</p>}
    </div>
  );
};

export default Upload;
