# lipp-faq-rag algorithm and development

## Resources  
- [Convert Python Script to .exe File](https://www.geeksforgeeks.org/convert-python-script-to-exe-file/)
- [Examples of using the Nebius AI Studio API](https://docs.nebius.com/studio/api/examples)
- [GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)
- [Language Models 3: 🤗 Hugging Face with RAG and Open AI Web Search](https://github.com/ithaka/constellate-notebooks/blob/master/Applying-large-language-models/language-models-3.ipynb)
- [LlamaIndex: Chunking Strategies for Large Language Models. Part — 1](https://medium.com/@bavalpreetsinghh/llamaindex-chunking-strategies-for-large-language-models-part-1-ded1218cfd30)
- [Markdown Live Preview](https://markdownlivepreview.com/)

## Executable version 
This line, run in the terminal, may make an executable file via PyInstaller: `python -m PyInstaller --add-data ".env;." --add-data "data/docs_lipp-faq/*.html;data/docs_lipp-faq" --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --onefile --noconsole "code/rag_system.py"`

## Algorithm  
Note: parse.py can split a LibAnswers FAQ export into distinct HTML files for each Q. I used it to create the files that form the RAG context.

1. rag_system.py
   1. Sets directory and environment
   1. Executes each script in turn
1. retrieval_system.py
	1. Loads data
	1. Creates embeddings (based on fixed context window, although it has code for parsing HTML)
	1. Builds a retrieval system
1. llm_func.py
   1. Defines the function llm_query
      1. Takes a query string
      1. Retrieves context
	  1. Adds static instructions
	  1. Appends the above components into a RAG prompt
   1. Defines the function llm_completion
	  1. Submits a prompt to the LLM of choice
	  1. Returns the prompt completion
1. user_interface (can run repeatedly in one session)
   1. Creates a user interface for submitting a free-text query and displaying HTML-formatted completion
   1. Runs llm_query and llm_completion
   1. Displays the LLM's completion

## Aspirations  
- Refine the fixed prompt
- Tune the context parameters
- Try other models
- Construct a web app
