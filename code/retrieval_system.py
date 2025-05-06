# -*- coding: utf-8 -*-
"""
Created on Mon May 05 18:01 2025
@author: kevinathom
Purpose: Build the retrieval system.
         (Can run once per session.)
"""

# Dependencies
from huggingface_hub import login
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
#from llama_index.core.node_parser import HTMLNodeParser # For HTML parser
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


# Load documents
docs = SimpleDirectoryReader(dir_project / 'data' / 'docs_lipp-faq').load_data()


# Create embeddings
model_embed = 'BAAI/bge-small-en-v1.5'

Settings.embed_model = HuggingFaceEmbedding(model_name=model_embed)
Settings.llm = None

## Based on fixed context window
Settings.chunk_size = 600
Settings.chunk_overlap = 50
index = VectorStoreIndex.from_documents(docs)

"""
## Based on HTML tags
parser = HTMLNodeParser(tags = ['title', 'p', 'ul', 'ol'])

def create_html_based_index(docs):#: List[Document]):
    # Extract nodes from all documents
    all_nodes = []
    for doc in docs:
        nodes = parser.get_nodes_from_documents([doc])
        all_nodes.extend(nodes)
    
    # Create vector index from nodes instead of documents
    index = VectorStoreIndex(all_nodes)
    return index

index = create_html_based_index(docs)
"""

# Retrieval system
top_k = 4 # Documents to retrieve
similarity_cutoff = .6 # Minimum document similarity

retriever = VectorIndexRetriever(
  index=index,
  similarity_top_k=top_k,
  similarity_cutoff=similarity_cutoff,
  )
query_engine = RetrieverQueryEngine(
  retriever=retriever,
  node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)],
  )
