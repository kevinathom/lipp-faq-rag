# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
Purpose: Functions to build a prompt and run the LLM
"""

# Dependencies
from huggingface_hub import InferenceClient


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
  # Select LLM
  client = InferenceClient(model='meta-llama/Llama-3.1-405B-Instruct', provider='nebius') # Llama 3.1-405B-Instruct
  
  # Retrieve LLM completion
  completion = client.chat.completions.create(messages=[{'role': 'user', 'content': ragful_prompt}],)
  completion_markdown = completion.choices[0].message.content
  return(completion_markdown)
