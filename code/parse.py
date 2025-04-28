# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 12:12:27 2025
@author: kevinat
Purpose: Parse SpringShare FAQ export file into distinct files
"""

# Dependencies
import pandas as pd
from pathlib import Path


# Set FAQ export filename
file_export = 'la_faq_export2025-04-28_04_06_41_HTML.csv'

# Set directories
dir_onedrive = Path('./OneDrive - PennO365/Projects/Generative AI/FAQ_RAG_2025/FAQ_files')
dir_repodata = Path('./Documents/GitHub/lipp-faq-rag/data/docs_lipp-faq')

# Read FAQ export file
data_export = pd.read_csv(dir_onedrive / file_export)

# Save FAQ to HTML files
for row in range(len(data_export)):
    Id = data_export.loc[row, 'Id']
    Q = data_export.loc[row, 'Question']
    A = data_export.loc[row, 'Answer']
    with open(dir_repodata / f'{Id}.html', 'x') as file:
        file.write(f'<!doctype html><html><head><title>{Q}</title></head><body>{A}</body></html>')