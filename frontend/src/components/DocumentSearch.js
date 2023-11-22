import React from "react";
import DocumentCard from "../subcomponents/DocumentCard";
import "../styles/DocumentSearch.css";

const DocumentSearch = ({ results, setFileAndOpenDocumentViewer }) => {

  return (
    <div className="container">
      <div className="search-panel">
        <div className="results">
          {results.map((result, index) => (
            <DocumentCard
              key={index}
              documentName={result.name}
              date={result.date}
              summary={result.summary}
              onClick={() => setFileAndOpenDocumentViewer(result.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DocumentSearch;
