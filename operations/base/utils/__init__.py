

import os
import shutil

def library_create(name):
    if library_exists(name): return

    if not os.path.isdir(library_path(name)):
        shutil.copytree(library_template_path(), library_path(name))
    return library_path

def library_exists(name):
    library_path = os.path.join(os.getcwd(), 'operations', name)
    return os.path.isdir(library_path)

def library_path(name):
    return os.path.join(os.getcwd(), 'operations', name)

def library_template_path():
    return os.path.join(os.getcwd(), 'templates', 'library')