// PARSE META DATA FROM DOCUMENTS
// deserialize the metadata from the document
// make a way to view summary nicely



//TODO:
// metadata['classification_data'] = urllib.parse.unquote(metadata['classification_data'])

// This function deserializes the classification_data from JSON string to an object
const deserializeClassificationData = (classificationDataString) => {
    try {
      return JSON.parse(classificationDataString);
    } catch (error) {
      console.error("Error deserializing classification data:", error);
      return null; // or a default empty object, depending on your error handling strategy
    }
  };

export { deserializeClassificationData };