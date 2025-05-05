# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
Purpose: Run the RAG system
"""

# Dependencies
## Environment
from dotenv import load_dotenv
#from pathlib import Path # For standalone testing

#dir_project = Path('./GitHub/lipp-faq-rag') # Repository directory | # For standalone testing
load_dotenv(dotenv_path=dir_project / '.env') # See HF_TOKEN

## Model
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


# Query (either text examples or from user_interface.py)
#query = 'Where can I find market research reports?'
#query = 'Get market size on medical implants for diabetes'
#query = """I’m a graduate student at Upenn, and I’m currently researching Orolay (the apparel company known for its “Amazon coat”). I’m trying to find the following information, ideally from 2012 to 2025 if available: Annual revenue (sales) of Orolay; Best-selling product(s); Information on Orolay’s main customer"""
#query = "can't access Pitchbook"
#query = 'microsoft'
#query = 'Am I an orange?'
query = input_text # from user_interface.py

# Vector query response
response = query_engine.query(query)


# RAG context for LLM prompt
context = 'Context:\n'
for k in range(top_k):
  context = context + response.source_nodes[k].text + '\n\n'

#print(context) # For standalone testing


# LLM prompt
ragless_prompt = f"""
[INST] As a virtual business research librarian, communicate in clear, concise, accessible language. Include a link from the provided context for each suggested resource. If the provided context is irrelevant, suggest sending business research questions to a Lippincott Business Librarian at lippincott@wharton.upenn.edu instead of suggesting resources.

Please respond to this request: {query}

End the response with this statement: "This response is model-generated, based on human librarian advice. For further assistance, please contact a Lippincott Business Librarian at lippincott@wharton.upenn.edu."
[/INST]
"""
ragful_prompt = ragless_prompt + context


# Prompt the LLM
client = InferenceClient(model='meta-llama/Llama-3.1-405B-Instruct', provider='nebius') # Llama 3.1-405B-Instruct

completion = client.chat.completions.create(messages=[{'role': 'user', 'content': ragful_prompt}],)
#print(completion.choices[0].message.content) # For standalone testing
