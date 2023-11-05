import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Document, Page } from "react-pdf";
import "../styles/DocumentSearch.css";
import DocumentCard from "../components/DocumentCard";
import { pdfjs } from "react-pdf";
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const DocumentSearch = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);

  const handleSearch = async () => {
    const payload = {
      query: searchTerm,
    };
    const result = await axios.post(
      "http://localhost:5001/api/v2/search/3",
      payload
    );

    // TODO add this to the backend
    const data = result.data;
    let results = [];
    for (let id in data.sources) {
      let source = data.sources[id];
      results.push({
        id: id,
        file_type: source.metadata.file_type,
        content_type: source.metadata.content_type,
        name: source.metadata.name,
        date: "2023-10-25",
        summary: source.metadata.summary,
        url: source.url,
      });
    }
    setResults(results);
  };

  // This function will navigate to the DocumentChat component with the document's details
  const goToChat = (id) => {
    navigate(`/document-chat/${id}`); // Use navigate function with the path
  };

  return (
    <div className="container">
      <div className="search-panel">
        <div className="search-input row">
          <div className="col-md-9">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="col-md-3">
            <button onClick={handleSearch} className="btn btn-primary">
              Search
            </button>
          </div>
        </div>

        <div className="results">
          {results.map((result, index) => (
            <DocumentCard
              key={index}
              documentName={result.name}
              date={result.date}
              summary={result.summary}
              onClick={() => setSelectedDocument(result)}
            />
          ))}
        </div>
      </div>
      <div className="document-panel">
        {selectedDocument && (
          <div className="document-content">
            <h2>{selectedDocument.name}</h2>
            <p>{selectedDocument.date}</p>
            <p>{selectedDocument.summary}</p>
            {/* Add a chat button in the summary section */}
            <button
              onClick={() => goToChat(selectedDocument.id)}
              className="btn btn-secondary"
            >
              Go to Chat
            </button>
            {selectedDocument.content_type === "application/pdf" ? (
              <Document
                file={selectedDocument.url}
                onLoadError={(error) => console.error(error)}
              >
                <Page
                  pageNumber={1}
                  onRenderError={(error) => console.error(error)}
                />
              </Document>
            ) : (
              <img src={selectedDocument.url} alt={selectedDocument.name} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentSearch;
