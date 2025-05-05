# -*- coding: utf-8 -*-
"""
Created on Mon May 05 11:47 2025
@author: kevinathom
Purpose: Render output from the process
"""

# Dependencies
import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser
import sys

def render_markdown_pyqt(content=markdown_content, title="Markdown Content Viewer"):
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)
    
    # Display the HTML using PyQt
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle(title)
    window.setGeometry(100, 100, 800, 600)
    
    browser = QTextBrowser(window)
    browser.setHtml(html_content)
    window.setCentralWidget(browser)
    
    window.show()
    sys.exit(app.exec_())

render_markdown_pyqt(content=completion.choices[0].message.content, title="Virtual Business Library Response")
