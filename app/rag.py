from app.store import vector_store
from app.llm import generate_answer

def rag_query(query: str):
    docs = vector_store.search(query, k=3)

    if not docs:
        return "No knowledge has been ingested yet."

    context = "\n\n".join(docs)
    return generate_answer(context, query)
