from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


def summarize_document(texts, llm):
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)


