#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Create a Davai experiment to test an IAL bundle.
"""

import os
import argparse
import sys

from .. import config, DAVAI_HOST
from ..experiment import XPmaker
from ..util import expandpath

__all__ = ['main']


def main():

    # get args
    args = get_args()

    # create new experiment
    XPmaker.new_xp(args.sources_to_test,
                   editable=args.editable,
                   davai_version=args.davai_version,
                   davai_remote_repo=args.davai_remote_repo,
                   usecase=args.usecase,
                   host=args.host,
                   genesis_commandline=" ".join(sys.argv),
                   bundle_src_dir=args.bundle_src_dir)


def get_args():
    parser = argparse.ArgumentParser(description='Create a Davai experiment to test an IAL bundle.')
    parser.add_argument('bundle',
                        help=" ".join([
                            "An IAL bundle, either as a local bundle file (.yml or .yaml) or",
                            "a git ref (tag, commit) in the IAL-bundle repository.",
                            "First guess will be to check if the local file exists,",
                            "if not will assume the provided 'bundle' argument is a reference",
                            "in the IAL-bundle repository, in which case",
                            "the repository has to be specified via arg -r."]))
    parser.add_argument('-e', '--editable',
                        action='store_true',
                        help="Editable: use an editable version of Davai sources (hence a brand new venv).")
    parser.add_argument('-r', '--IAL_bundle_repo',
                        default=None,
                        dest='IAL_bundle_repository',
                        help="URL or path of IAL-bundle repository in which to find the given reference of bundle. " +
                             "E.g. 'https://github.com/ACCORD-NWP/IAL-bundle' or '~/repositories/IAL-bundle'.")
    parser.add_argument('-v', '--davai_version',
                        dest='davai_version',
                        help="Version of the Davai test bench to be used.")
    parser.add_argument('-c', '--comment',
                        default=None,
                        help="Comment about experiment. Defaults to 'bundle' argument.")
    parser.add_argument('-u', '--usecase',
                        default=config['defaults']['usecase'],
                        help="Usecase: NRV (restrained set of canonical tests) or ELP (extended elementary tests); " +
                             "More to come (PC, ...). Defaults to: '{}'".format(config['defaults']['usecase']))
    parser.add_argument('-o', '--origin', '--davai_remote_repo',
                        default=config['defaults']['davai_remote_repo'],
                        dest='davai_remote_repo',
                        help=" ".join([
                            "URL of the DAVAI-tests origin repository to be cloned in XP.",
                            "Default ({})".format(config['defaults']['davai_remote_repo']),
                            "can be set through section [defaults] of user config file."]))
    parser.add_argument('--host',
                        default=DAVAI_HOST,
                        help="Generic name of host machine, in order to find paths to necessary packages. " +
                             ("Default is guessed ({}), or can be set through " +
                              "section 'hosts' of user config file").format(DAVAI_HOST))
    parser.add_argument('-b', '--bundle_src_dir',
                        default='$HOME/bundle_cache',
                        dest='bundle_src_dir',
                        help=" ".join(["In case davai_version is not specified:",
                                       "cache directory where to download/update bundle repositories,",
                                       "in search for the davai_version, potentially stored in IAL."]))
    args = parser.parse_args()

    # pre-process args
    local_file = os.path.abspath(args.bundle)
    if os.path.exists(local_file):
        # local bundle file
        sources_to_test = dict(IAL_bundle_file=os.path.abspath(args.bundle))
    else:
        if args.IAL_bundle_repository is None:
            if args.bundle.endswith('.yml') or args.bundle.endswith('.yaml'):
                # seems like an invalid path
                raise IOError("Bundle '{}' is not a path to an existing file".format(args.bundle))
            else:
                # git ref in an IAL-bundle repo
                raise IOError("If 'bundle' is an IAL-bundle git ref, you must provide a repository (-r) where to find it.")
        local_repo = os.path.abspath(args.IAL_bundle_repository)
        if os.path.isdir(local_repo):
            IAL_bundle_repository = local_repo
        else:
            IAL_bundle_repository = args.IAL_bundle_repository
        sources_to_test = dict(IAL_bundle_ref=args.bundle,
                               IAL_bundle_repository=IAL_bundle_repository)
    sources_to_test['comment'] = args.comment
    args.sources_to_test = sources_to_test
    args.bundle_src_dir = os.path.expanduser(os.path.expandvars(args.bundle_src_dir))
    return args

