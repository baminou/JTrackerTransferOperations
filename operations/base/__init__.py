

from ..library import Library
from .make_library import Makelibrary
from .make_operation import MakeOperation
from .make_operationtype import MakeOperationType
from .list_operation import Listoperation
from .yaml_to_json import Yamltojson
from .publish import Publish
from .install_operation import Installoperation
from .install import Install

class Base(Library):

    @staticmethod
    def name():
        return "base"

    @staticmethod
    def description():
        return "General operations"

    @staticmethod
    def operations():
        return {
            'make:library': Makelibrary,
            'make:operation': MakeOperation,
            'make:operation:type': MakeOperationType,
            'list:operations': Listoperation,
            'yaml_to_json': Yamltojson,
            'publish': Publish,
            'install:operation': Installoperation,
            'install': Install
        }