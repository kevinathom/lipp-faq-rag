# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
Purpose: Functions to build a prompt and run the LLM
"""

# Dependencies
#from huggingface_hub import InferenceClient # For HuggingFace API
from openai import OpenAI # For Nebius API
import os # For Nebius API


def llm_query(query):
  """Take a query, retrieve context, and compile a prompt,
  and retrieve a response from the LLM"""
  # Vector query response
  response = query_engine.query(query)
  
  # RAG context for LLM prompt
  context = 'Context:\n'
  for k in range(top_k):
    context = context + response.source_nodes[k].text + '\n\n'
  
  # LLM prompt
  ragless_prompt = f'[INST] As a virtual business research librarian, communicate in clear, concise, accessible language. Include a link from the provided context for each suggested resource. If the provided context is irrelevant, suggest sending business research questions to a Lippincott Business Librarian instead of suggesting resources.\n\nPlease respond to this request: {query}[/INST]'
  ragful_prompt = ragless_prompt + context
  return(ragful_prompt)


def llm_completion(ragful_prompt):
  """Submit a prompt to and retrieve a response from the LLM"""

  # Select completion service
  #client = InferenceClient(model=meta-llama/Llama-3.1-405B-Instruct, provider='nebius') # Nebius via HuggingFace
  client = OpenAI(base_url="https://api.studio.nebius.com/v1/", api_key=os.environ.get("NEBIUS_API_KEY"),) # Nebius direct
  
  # Retrieve LLM completion
  completion = client.chat.completions.create(
    model='meta-llama/Meta-Llama-3.1-405B-Instruct', # Omit when using Nebius via HuggingFace
    messages=[{'role': 'user', 'content': ragful_prompt}],
    )
  completion_markdown = completion.choices[0].message.content
  return(completion_markdown)
