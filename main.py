#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from kernel.console import libraries

def main():
    parser = argparse.ArgumentParser(description='Create and test re-usable tools')

    subparsers = parser.add_subparsers()

    for library_key, library in libraries().items():
        library_group = subparsers.add_parser(library_key, description=library.description())
        library_subparsers = library_group.add_subparsers()

        for command, operation in library.operations().items():
            operation_subparser = library_subparsers.add_parser(command, description=operation.description())
            operation.parser(operation_subparser)
            operation_subparser.set_defaults(function=operation.execute)

    results = parser.parse_args()
    results.function(results)

if __name__ == "__main__":
    main()