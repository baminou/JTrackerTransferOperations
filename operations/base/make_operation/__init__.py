

from operations.operation import Operation
import shutil
import os
from ..utils import library_create, library_path

class MakeOperation(Operation):
    def _run(self, args):

        #Retrieve the library name and path
        library = args.library

        #Retrieve the operation name and path
        operation = args.operation
        operation_path = os.path.join(library_path(library),operation)

        template_path = os.path.join(os.getcwd(),'templates','operation')
        new_init_path = os.path.join(operation_path,'__init__.py')

        library_create(library)

        if os.path.isdir(operation_path) and os.path.isfile(new_init_path):
            raise FileExistsError("The module already exists: "+operation)

        shutil.copytree(template_path,operation_path)
        with open(new_init_path,'r') as f:
            new_text = f.read().replace('NewOperation', MakeOperation.to_camel_case(operation).capitalize())

        with open(new_init_path,'w') as f:
            f.write(new_text)

    @staticmethod
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
