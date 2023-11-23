import React, { useState, useRef } from 'react';
import '../styles/FileUpload.css';

function FileUpload() {
    const [fileType, setFileType] = useState('diagram');
    const fileInputRef = useRef(null);

    const handleTypeChange = (event) => {
        setFileType(event.target.value);
    };

    const handleFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        console.log(selectedFile);
    };

    const getAcceptedFileTypes = () => {
        if (fileType === 'document') {
            return ".pdf,.txt,.docx";
        } else if (fileType === 'diagram') {
            return ".pdf,.jpeg,.png";
        } else {
            return "*";
        }
    }

    return (
        <div className="d-flex flex-column align-items-center justify-content-center vh-100">
            <div 
                id="drop-area" 
                className="border rounded p-5 mb-4 d-flex flex-column align-items-center justify-content-center" 
                style={{ width: '600px', height: '400px' }}
            >
                <div className="text-center">
                    Drag and drop your file here
                    <br />
                    or
                    <br />
                    <button 
                        className="btn btn-outline-primary mt-2"
                        onClick={() => fileInputRef.current.click()}
                    >
                        Select File
                    </button>
                    <input 
                        type="file" 
                        ref={fileInputRef} 
                        style={{ display: 'none' }}
                        onChange={handleFileSelect}
                        accept={getAcceptedFileTypes()}
                    />
                </div>
            </div>
            <div className="btn-group btn-group-toggle mb-4" data-toggle="buttons">
                <label 
                    className={`btn btn-secondary ${fileType === 'diagram' ? 'active' : ''}`}
                    onClick={() => setFileType('diagram')}
                >
                    <input 
                        type="radio" 
                        name="options" 
                        id="option1" 
                        autoComplete="off"
                    />
                    Diagram
                </label>
                <label 
                    className={`btn btn-secondary ${fileType === 'document' ? 'active' : ''}`}
                    onClick={() => setFileType('document')}
                >
                    <input 
                        type="radio" 
                        name="options" 
                        id="option2" 
                        autoComplete="off"
                    />
                    Document
                </label>
            </div>
            <button className="btn btn-primary">Upload</button>
        </div>
    );
}


export default FileUpload;