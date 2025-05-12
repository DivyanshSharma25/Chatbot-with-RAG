import requests,json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from llama_index.readers.mongodb import SimpleMongoReader
from llama_index.core import VectorStoreIndex,Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader
class RAG_pipeline():
    
    def __init__(self,dir_to_doc=None):        
        self.set_params()      
        if(dir_to_doc!=None):
            self.load_document(dir_to_doc)
            self.make_index()
            self.make_query_engine()
        
       
        
    def set_params(self):
        Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
         ) 
        Settings.llm = Ollama(model="llama3.1:latest", request_timeout=60.0)
    def get_rag_query(self, query):
        response = self.query_engine.query(query)
        print("response type",type(response.response))
        return response.response
    
    def load_document(self,dir_to_doc):
        reader = SimpleDirectoryReader(input_files=[dir_to_doc])
        documents = reader.load_data()
        self.documents=documents
        print("Documents loaded.")
    
    def make_index(self):
        self.index=VectorStoreIndex.from_documents(self.documents)
        print("Index created from documents.")
        
    def make_query_engine(self):
        self.query_engine = self.index.as_query_engine(similarity_top_k=3)
        print("Query engine created from index.")
    

    
