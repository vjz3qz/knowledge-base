import Summary from "../subcomponents/Summary";
import React, { useState, useEffect } from "react";
import axios from "axios";

function DocumentViewer({ id}) {
  const [fileUrl, setFileUrl] = useState("");
  const [metadata, setMetadata] = useState({});

  // Function to initialize chat when component mounts or when document ID changes
  useEffect(() => {
    const fetchFile = async () => {
      const result = await axios.get(`http://localhost:5001/api/v2/view/${id}`);
      setFileUrl(result.data.url);
    };

    const fetchMetadata = async () => {
      const result = await axios.get(
        `http://localhost:5001/api/v2/view-metadata/${id}`
      );
      // Here you would load the document's details, including fetching the summary and setting the file name
      setMetadata(result.data);
    };
    try {
    //   fetchFile();
    //   fetchMetadata();
    setFileUrl("https://www.africau.edu/images/default/sample.pdf");
    setMetadata({
        "file_name": "sample.pdf",
        "file_type": "text",
        "summary": "This is a sample summary.",
        "classification_data": {
            "class_counts": {
                "class1": 1,
                "class2": 2
            }
        }
    });
    } catch (error) {
      console.log(error);
    }
  }, [id]);


  return (
    <div className="document-viewer">
      <div className="document-panel">
        <div className="document-header">Document</div>
        <div className="document-content">
          <iframe
            title="document"
            src={fileUrl}
            frameBorder="0"
            width="100%"
            height="100%"
          ></iframe>
        </div>
      </div>
      <Summary id={id} metadata={metadata} />
    </div>
  );
}

export default DocumentViewer;
