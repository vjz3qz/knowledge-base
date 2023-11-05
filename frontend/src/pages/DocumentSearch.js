import React, { useState } from 'react';
import axios from 'axios';
import { Document, Page } from 'react-pdf';
import '../styles/DocumentSearch.css';
import DocumentCard from '../components/DocumentCard';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;




const DocumentSearch = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [selectedDocument, setSelectedDocument] = useState(null);

    


    
    const handleSearch = async () => {
        const payload = {
          query: searchTerm,
        };
        const result = await axios.post("http://localhost:5001/api/v2/search/3", payload);

        // TODO add this to the backend
        const data = result.data;
        let results = []
        for (let id in data.sources) {
            let source = data.sources[id];
            results.push({
                name: source.metadata.name,
                date: '2023-10-25',
                summary: source.metadata.summary,
                url: source.url
            });
        }
        setResults(results);
      };

    // This function will navigate to the DocumentChat component with the document's details
    const goToChat = (document) => {
        // Assuming you're using React Router, you would navigate like this:
        // props.history.push(`/document-chat/${document.id}`);
        // For now, we're just logging it to the console:
        console.log(`Go to chat for document: ${document.id}`);
    };

    return (
        <div className="container">
            <div className="search-panel">
                <div className="search-input row">
                    <div className="col-md-9">
                        <input
                        type="text"
                        value={searchTerm}
                        onChange={e => setSearchTerm(e.target.value)}
                        className="form-control"
                        />
                    </div>
                    <div className="col-md-3">
                        <button onClick={handleSearch} className="btn btn-primary">Search</button>
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
                        <button onClick={() => goToChat(selectedDocument)} className="btn btn-secondary">
                            Go to Chat
                        </button>                     
                        <Document
                            file={selectedDocument.url}
                            onLoadError={error => console.error(error)}
                                >
                            <Page pageNumber={1} onRenderError={error => console.error(error)}/>
                        </Document>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DocumentSearch;
