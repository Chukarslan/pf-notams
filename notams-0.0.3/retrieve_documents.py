from typing import List
from promptflow import tool
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import CognitiveSearchConnection

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def retrieve_documents(question:str, index_name:str, embedding:List[float], search: CognitiveSearchConnection) -> str:
    """
    Retrieve documents from the search index.
    """
    search_client = SearchClient(endpoint=search.api_base, 
                                 index_name=index_name, 
                                 credential=AzureKeyCredential(search.api_key))
    
    vector = Vector(value=embedding, k=50, fields="contentVector")

    results = search_client.search(
        search_text=question,
        top=1,
        search_fields=["content"],
        vectors=[vector],
    )

    docs = [{"id": doc["id"], "title": doc["title"], "content": doc["content"], "url": doc["url"]} 
            for doc in results]

    return docs