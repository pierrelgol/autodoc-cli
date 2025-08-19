# PyInstaller hook for tree_sitter_languages
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import os
import tree_sitter_languages

# Collect all data files
datas = collect_data_files('tree_sitter_languages')

# Collect dynamic libraries
binaries = collect_dynamic_libs('tree_sitter_languages')

# Manually add the languages directory
tree_sitter_path = os.path.dirname(tree_sitter_languages.__file__)
languages_path = os.path.join(tree_sitter_path, 'languages')

if os.path.exists(languages_path):
    for file in os.listdir(languages_path):
        file_path = os.path.join(languages_path, file)
        if os.path.isfile(file_path):
            datas.append((file_path, f'tree_sitter_languages/languages/{file}'))
