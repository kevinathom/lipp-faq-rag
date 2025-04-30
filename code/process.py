# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
"""

# Dependencies
from dotenv import load_dotenv
from huggingface_hub import login
from huggingface_hub import InferenceClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import HTMLNodeParser
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from transformers import pipeline
import urllib.request
from pathlib import Path

dir_project = Path('./GitHub/lipp-faq-rag') # Repository directory
load_dotenv(dotenv_path=dir_project / '.env') # See HF_TOKEN


# Load documents
docs = SimpleDirectoryReader(dir_project / 'data' / 'docs_lipp-faq').load_data()


# Create embeddings based on HTML tags
## Based on fixed window
model_embed = 'BAAI/bge-small-en-v1.5'

Settings.embed_model = HuggingFaceEmbedding(model_name=model_embed)
Settings.llm = None
Settings.chunk_size = 150
Settings.chunk_overlap = 20

index = VectorStoreIndex.from_documents(docs) # Creates vector store object
"""
## Based on HTML tags
parser = HTMLNodeParser(tags = ['title', 'p', 'ul', 'ol', 'li'])
#What output format is needed for nodes from all docs?
nodes = parser.get_nodes_from_documents([docs[40]]) # one doc
"""

# Retrieval system
top_k = 3 # Documents to retrieve
similarity_cutoff = .5 # Minimum document similarity

retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)
query_engine = RetrieverQueryEngive(retriever=retriever, node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)],)
