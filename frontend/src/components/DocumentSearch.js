import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import DocumentCard from "../subcomponents/DocumentCard";
import "../styles/DocumentSearch.css";

const DocumentSearch = ({ searchTerm, setFileAndOpenDocumentViewer }) => {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const payload = {
      query: searchTerm,
    };
    // const result = await axios.post(
    //   "http://localhost:5001/api/v2/search/3",
    //   payload
    // );

    const result = {
      data: {
        sources: {
          source1: {
            metadata: {
              file_type: "pdf",
              content_type: "research_paper",
              name: "Impact of Climate Change on Marine Life",
              summary:
                "This research paper discusses the various impacts of climate change on marine biodiversity, including rising sea temperatures and ocean acidification.",
              url: "http://example.com/research/climate_change_marine_life.pdf",
            },
          },
          source2: {
            metadata: {
              file_type: "image",
              content_type: "photograph",
              name: "Aurora Borealis in Norway",
              summary:
                "A breathtaking photograph capturing the Aurora Borealis over the Norwegian landscape during the winter season.",
              url: "http://example.com/images/aurora_borealis_norway.jpg",
            },
          },
        },
      },
    };

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
  });

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
