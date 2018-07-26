#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from operations.ega_job import EGAJob
from operations.ega_to_stage import EGAStage
from operations.minibam_sync_files import MinibamSyncFiles
from operations.ega_to_delete import EgaToDelete
from operations.ega_dbox import EGADbox
import logging
import json


def run_ega_job(args):
    EGAJob().run(args)
    return

def run_ega_to_stage(args):
    EGAStage().run(args)
    return

def run_minibam_sync(args):
    MinibamSyncFiles().run(args)
    return

def run_ega_to_delete(args):
    EgaToDelete().run(args)
    return

def run_ega_dbox(args):
    EGADbox().run(args)
    return

def run_ega_job_schema(args):
    print(json.dumps(EGAJob()._schema(),indent=4))
    return

def run_ega_delete_schema(args):
    print(json.dumps(EgaToDelete()._schema(),indent=4))
    return

def run_ega_stage_schema(args):
    print(json.dumps(EGAStage()._schema(),indent=4))
    return

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Generate EGA jobs')
    subparsers = parser.add_subparsers(dest='subparser')

    parser_ega_job = subparsers.add_parser('ega:job')
    parser_ega_job.add_argument('-c', '--config', dest='config', required=True, help="A valid configuration yaml file",type=argparse.FileType('r'))
    parser_ega_job.add_argument('-a', '--audit', dest='audit', required=True)
    parser_ega_job.add_argument('-o', '--output', dest='output_dir', required=True)
    parser_ega_job.set_defaults(function=run_ega_job)

    parser_ega_job_schema = subparsers.add_parser('ega:job:schema')
    parser_ega_job_schema.set_defaults(function=run_ega_job_schema)

    parser_ega_dbox = subparsers.add_parser('ega:dbox')
    parser_ega_dbox.add_argument('-s','--aspera-server', dest='aspera_server',required=True)
    parser_ega_dbox.add_argument('-u','--aspera-user', dest='aspera_user', required=True)
    parser_ega_dbox.set_defaults(function=run_ega_dbox)

    parser_ega_stage = subparsers.add_parser('ega:stage')
    parser_ega_stage.add_argument('-c', '--config', dest='config', required=True, help="A valid configuration yaml file",type=argparse.FileType('r'))
    parser_ega_stage.add_argument('-a', '--audit', dest='audit', required=True)
    parser_ega_stage.add_argument('-o', '--output-file', dest='output_file', required=True)
    parser_ega_stage.set_defaults(function=run_ega_to_stage)

    parser_ega_stage_schema = subparsers.add_parser('ega:stage:schema')
    parser_ega_stage_schema.set_defaults(function=run_ega_stage_schema)

    parser_ega_delete = subparsers.add_parser('ega:delete')
    parser_ega_delete.add_argument('-c', '--config', dest='config', required=True, help="A valid configuration yaml file",type=argparse.FileType('r'))
    parser_ega_delete.add_argument('-o','--output-file', dest='output_file', required=True)
    parser_ega_delete.set_defaults(function=run_ega_to_delete)

    parser_ega_delete_schema = subparsers.add_parser('ega:delete:schema')
    parser_ega_delete_schema.set_defaults(function=run_ega_delete_schema)

    parser_minibam_sync = subparsers.add_parser('minibam:sync')
    parser_minibam_sync.add_argument('-c',
                                     '--config',
                                     dest='config',
                                     required=True,
                                     help="A valid configuration yaml file",
                                     type=argparse.FileType('r'))
    parser_minibam_sync.set_defaults(function=run_minibam_sync)

    results = parser.parse_args()
    results.function(results)

if __name__ == "__main__":
    main()