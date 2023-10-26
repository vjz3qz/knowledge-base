import React, { useState } from 'react';
import { Document, Page } from 'react-pdf';
import '../styles/DocumentSearch.css';
import DocumentCard from '../components/DocumentCard';  // Make sure to import the DocumentCard component

const DocumentSearch = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [results, setResults] = useState([]);
    const [selectedDocument, setSelectedDocument] = useState(null);

    function handleSearch() {
        const fakeResults = [
            { name: 'Document 1', date: '2023-10-25', summary: 'Summary for Document 1.' },
            { name: 'Document 2', date: '2023-10-24', summary: 'Summary for Document 2. Detailed overview of the topics covered.' },
            { name: 'Document 3', date: '2023-10-23', summary: 'Summary for Document 3. Insights into the subject matter.' },
            { name: 'Document 4', date: '2023-10-22', summary: 'Summary for Document 4. Key findings and important notes.' },
            { name: 'Document 5', date: '2023-10-21', summary: 'Summary for Document 5. Final remarks and conclusions.' }
        ];
        setResults(fakeResults);
    }

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
                        <Document
                            file="/Users/rahulkumar/Desktop/trace-ai/knowledge-base/frontend/public/report.pdf"
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
