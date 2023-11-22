import Summary from "../subcomponents/Summary";
import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/DocumentViewer.css";

function DocumentViewer({ id }) {
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
    setFileUrl("https://www.clickdimensions.com/links/TestPDFfile.pdf");
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
    <div className='sidebar'>
        <div className="holder"></div>
        
        <iframe width="100%" height="60%" src={fileUrl} title="YouTube video player" frameBorder="0" allow="accelerometer;"
    style={{ border: '2px solid #ddd', borderRadius: '10px' }}></iframe>
        <Summary id={id} metadata={metadata} />
    </div>
  );
}

export default DocumentViewer;
