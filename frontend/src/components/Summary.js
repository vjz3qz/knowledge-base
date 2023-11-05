import { deserializeClassificationData } from "../utils/ParseMetadata";

import React from "react";
import "../styles/DocumentChat.css";


  
  function Summary({ metadata }) {
    // Deserialize the classification data from the metadata
    const classificationData = deserializeClassificationData(metadata.classification_data);
    
    // Extract summary and class counts from classification data
    const summary = metadata.summary;
    const classCounts = classificationData ? classificationData.class_counts : {};
  
    // Format class counts for display
    const formattedClassCounts = Object.entries(classCounts)
      .map(([className, count]) => `${count} instances of class ${className}`)
      .join(", ");
  
    return (
      <div className="document-panel">
        <div className="document-header">Summary</div>
        <div className="document-content">
          <p>{summary}</p>
          <p>{formattedClassCounts}</p>
        </div>
      </div>
    );
  }
  
  export default Summary;
  