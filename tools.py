

from retrieval import Retriever
from langchain_tavily import TavilySearch



def get_tools():


    print("Initializing tools")
    retriever = Retriever()

    # create retrievers for audit(dummy) and chat(rag)
    rag_retriver = retriever.retriver_sim

    def get_rag_documents(query: str) -> str:  
        """Query a vector database of University of Michigan course documents. Write a precise query to retrieve relevant documents.
                THIS IS YOUR PRIMARY TOOL CALL IT OFTEN WHEN GIVING ADVICE ON CIRRICLUM AND CLUBS FOR UMICH, DEFAULT TO THIS.
                Split queries by `|` to get results for each query. Don't include multiple courses, clubs, or majors in the same query, split them with pipe (|)."""
        queries = query.split("|")
        print("Queries to vector database: ", queries)
        response = ""
        for q in queries:
            print("Querying vector database with query: ", q)
            response += f"\n\nQuery: {q}\n\nDocuments: \n"
            response += str(rag_retriver.invoke(q))
        print("Response from vector database: ", response)
        return f"Documents: \n{response}"

    search_tool = TavilySearch(
        max_results=10,
        topic="general",)
    
    return [
        get_rag_documents,
        search_tool,
    ]