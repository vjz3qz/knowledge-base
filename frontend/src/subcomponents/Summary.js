
import React from "react";
import "../styles/Summary.css";

  
  function Summary({ id, metadata }) {
    // if (metadata.file_type === "diagram") {
      // const classificationDataJsonUrl = await axios.get(`http://localhost:5001/api/v1/view/${id}?classification_data=true`);
    //   return <DiagramSummary />;
    // } else {
    //   return <TextSummary />;
    // }
    // Deserialize the classification data from the metadata
    // const classificationData = deserializeClassificationData(metadata.classification_data);
    
    // Extract summary and class counts from classification data
    const summary = metadata && metadata.summary ? metadata.summary : "No summary available.";
    // const classCounts = classificationData ? classificationData.class_counts : {};
  
    // // Format class counts for display
    // const formattedClassCounts = Object.entries(classCounts)
    //   .map(([className, count]) => `${count} instances of class ${className}`)
    //   .join(", ");
  
    return (
      <div className="document-panel">
        {/* <div className="document-header">Summary</div> */}
        <div className="document-content">
          <p>{summary}</p>
          {/* <p>{formattedClassCounts}</p> */}
        </div>
      </div>
    );
  }
  
  export default Summary;