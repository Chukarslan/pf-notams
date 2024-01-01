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
    
    vector = Vector(value=embedding, k=25)

    results = search_client.search(
        search_text=question,
        top=20,
        # search_fields=["message", "location"],
        # vectors=[vector],
    )

    docs = [{"content": doc["content"]} 
            for doc in results]

    return docs