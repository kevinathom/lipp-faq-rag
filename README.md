# lipp-faq-rag  
Exploring the value of developing a RAG system to support natural language querying of content in the [Lippincott Library Business FAQ](https://faq.library.upenn.edu/business/search/)

## Requirements  
- A Hugging Face API key (free access works) stored in the project's `.env` file
- A set of FAQs in individual HTML files (If you download SpringShare's default, HTML-included, FAQ extract, you can use `parse.py` to convert the extract to HTML files.)

## Instructions
1. Download the `.py` files from the `code` directory.
1. Adjust file paths and, as needed, any text/prompt/tuning details.
1. Run `rag_system.py`.
