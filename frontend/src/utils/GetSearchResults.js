// import axios
import axios from "axios";
async function getSearchResults(searchTerm) {
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
  const answer = result.data.answer;
  return [answer, results];
}

export default getSearchResults;
