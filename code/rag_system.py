# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 11:54:17 2025
@author: kevinathom
Purpose: Initialize each component of the RAG system
"""

# Dependencies
from dotenv import load_dotenv
from pathlib import Path

dir_project = Path('./GitHub/lipp-faq-rag') # Repository directory
load_dotenv(dotenv_path=dir_project / '.env') # See HF_TOKEN


# Generate retrieval system
exec(open(dir_project / 'code' / 'llm_func.py').read())

# Create functions for prompt generation and LLM call
exec(open(dir_project / 'code' / 'llm_func.py').read())

# Run user interface
exec(open(dir_project / 'code' / 'user_interface.py').read())
