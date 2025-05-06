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
#from huggingface_hub import login # For standalone testing
from huggingface_hub import InferenceClient
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
#from llama_index.core.retrievers import VectorIndexRetriever
#from llama_index.core.query_engine import RetrieverQueryEngine
#from llama_index.core.postprocessor import SimilarityPostprocessor
#from transformers import pipeline
#import urllib.request

# Query (either text examples or from user_interface.py)
#query = 'Where can I find market research reports?'
#query = 'Get market size on medical implants for diabetes'
#query = """I’m a graduate student at Upenn, and I’m currently researching Orolay (the apparel company known for its “Amazon coat”). I’m trying to find the following information, ideally from 2012 to 2025 if available: Annual revenue (sales) of Orolay; Best-selling product(s); Information on Orolay’s main customer"""
#query = "can't access Pitchbook"
#query = 'microsoft'
#query = 'Am I an orange?'
query = input_text # from user_interface.py
print('query complete') # For UI crash testing

# Vector query response
response = query_engine.query(query)
print('response complete') # For UI crash testing


# RAG context for LLM prompt
context = 'Context:\n'
for k in range(top_k):
  context = context + response.source_nodes[k].text + '\n\n'
print('context complete') # For standalone testing


# LLM prompt
ragless_prompt = f'[INST] As a virtual business research librarian, communicate in clear, concise, accessible language. Include a link from the provided context for each suggested resource. If the provided context is irrelevant, suggest sending business research questions to a Lippincott Business Librarian instead of suggesting resources.\n\nPlease respond to this request: {query}[/INST]'
print('ragless_prompt complete') # For UI crash testing
ragful_prompt = ragless_prompt + context
print('ragful_prompt complete') # For UI crash testing


# Prompt the LLM
client = InferenceClient(model='meta-llama/Llama-3.1-405B-Instruct', provider='nebius') # Llama 3.1-405B-Instruct
print('specified client') # For UI crash testing

completion = client.chat.completions.create(messages=[{'role': 'user', 'content': ragful_prompt}],)
print('completion complete') # For UI crash testing
completion_markdown = completion.choices[0].message.content
#print(completion_markdown) # For standalone testing
