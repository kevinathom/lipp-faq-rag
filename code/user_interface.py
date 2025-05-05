# -*- coding: utf-8 -*-
"""
Created on Mon May 05 11:47 2025
@author: kevinathom
Purpose: Provide a user interface for the RAG system
"""

# Dependencies
## Environment
from pathlib import Path

dir_project = Path('./GitHub/lipp-faq-rag') # Repository directory

## User interface
import markdown
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QTextEdit, QSplitter)
import sys


# Query input
class InputResponseWindow(QMainWindow):
  """Window for collecting multi-line input and displaying responses"""
  
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Virtual Lippincott Business Research Agent")
    self.setGeometry(100, 100, 800, 600)  # Wider window for better readability
    
    # Central widget and main layout
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)
    
    # Create a splitter to allow resizing between input and output areas
    splitter = QSplitter(Qt.Vertical)
    main_layout.addWidget(splitter)
    
    # Input section
    input_widget = QWidget()
    input_layout = QVBoxLayout(input_widget)
    
    # Input label
    input_label = QLabel("Enter your business research query:")
    input_layout.addWidget(input_label)
    
    # Multi-line input (QTextEdit)
    self.text_input = QTextEdit()
    self.text_input.setPlaceholderText("How can I find...?")
    input_layout.addWidget(self.text_input)
    
    # Submit button
    self.submit_button = QPushButton("Submit")
    self.submit_button.clicked.connect(self.process_input)
    input_layout.addWidget(self.submit_button)
    
    splitter.addWidget(input_widget)
    
    # Response section
    response_widget = QWidget()
    response_layout = QVBoxLayout(response_widget)
    
    # Response label
    response_label = QLabel("Virtual agent response:")
    response_layout.addWidget(response_label)
    
    # Response display area (read-only QTextEdit)
    self.response_display = QTextEdit()
    self.response_display.setReadOnly(True)
    self.response_display.setPlaceholderText("A response based on human librarian recommendations will appear here.")
    response_layout.addWidget(self.response_display)
    
    splitter.addWidget(response_widget)
    
    # Set initial splitter sizes (50% each)
    splitter.setSizes([300, 300])
  
  def process_input(self):
    """Process the submitted text and display a response"""
    # Get the input text
    input_text = self.text_input.toPlainText()
    
    if not input_text.strip():
        self.response_display.setHtml("<p style='color:red'>Please enter some text first.</p>")
        return
    
    # Run the user's input throught the RAG system and store the RAG's response
    exec(open(dir_project / 'code' / 'rag_system.py').read())
    completion_markdown = your_processing_function(completion.choices[0].message.content)
    #completion_markdown = '*test* **test** test' # For standalone testing
    
    # Convert Markdown to HTML and display
    self.response_display.setHtml(markdown.markdown(completion_markdown))

def main():
  app = QApplication(sys.argv)
  window = InputResponseWindow()
  window.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
