async function getSearchResults(searchTerm) {
  const payload = {
    query: searchTerm,
  };
//   const result = await axios.post(
//     "http://localhost:5001/api/v2/search/3",
//     payload
//   );

  const result = {
    data: {
      answer: "The impact of climate change on marine life is significant.",
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
  const answer = result.data.answer;
  return [answer, results];
}

export default getSearchResults;