# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
Purpose: Function to run the LLM,
         because calling the script from the UI fails
"""

# Dependencies
## Environment
#from dotenv import load_dotenv # For standalone testing
#from pathlib import Path # For standalone testing

#dir_project = Path('./GitHub/lipp-faq-rag') # Repository directory | # For standalone testing
#load_dotenv(dotenv_path=dir_project / '.env') # See HF_TOKEN | # For standalone testing

## Model
#from huggingface_hub import login # For standalone testing
from huggingface_hub import InferenceClient


def llm_query(query):
  """Take a query, retrieve context, compile a prompt,
  and retrieve a response from the LLM"""
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
  return(completion_markdown)
