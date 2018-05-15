#!/usr/bin/env python
# coding=utf-8

import argparse
import collections
import datetime
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


def backup_tree(src, dst, prefix, file_action, dir_action):
    if not os.path.exists(src):
        raise Exception("Source directory does not exist: {}".format(dst))
    if not os.path.exists(dst):
        raise Exception("Destination directory does not exist: {}".format(dst))
    files_count = 0
    dirs_count = 0
    for root, subdirs, files in os.walk(src):
        dst_dir = os.path.join(dst, os.path.relpath(root, src))
        for file in files:
            dst_file = os.path.join(dst_dir, "{}{}".format(prefix, file))
            src_file = os.path.join(root, file)
            file_action(src_file, dst_file)
        for subdir in subdirs:
            dst_subdir = os.path.normpath(
                os.path.join(dst, os.path.relpath(root, src), subdir)
            )
            src_subdir = os.path.join(root, subdir)
            dir_action(src_subdir, dst_subdir)

if __name__ == "__main__":
    curdate = datetime.datetime.now().strftime("%Y-%m-%d_")
    argparser = argparse.ArgumentParser(
        description=(
            "Backup directory tree. "
            "Make the same directory structure in destination directory and "
            "add prefix (with current date by default) to each file name."
        )
    )
    argparser.add_argument(
        'src_path', metavar="SOURCE_PATH",
        help='source path (should exist)')
    argparser.add_argument(
        'dst_path', metavar="DEST_PATH",
        help='destination path (should exist)')
    argparser.add_argument(
        '-p', '--prefix', default=curdate,
        help='backup file prefix (default: system date in YYYY-MM-DD_ format)')
    argparser.add_argument(
        '-a', '--action', default="move", choices=("move", "copy"),
        help='perform one of the actions with each file (default: move)')
    argparser.add_argument(
        '--debug', action="store_true",
        help="debug output")
    argparser.add_argument(
        '--dry-run', action="store_true",
        help=(
            "don't preform real actions, "
            "use with --debug to test your settings"
        )
    )
    args = argparser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    count = collections.Counter()

    def move(src_file, dst_file):
        if os.path.exists(dst_file):
            raise Exception(
                "Move failed, file {} already exists".format(dst_file)
            )
        if not args.dry_run:
            shutil.move(src_file, dst_file)
        logging.debug("m {} -> {}".format(src_file, dst_file))
        count.update(files=1)

    def copy(src_file, dst_file):
        if os.path.exists(dst_file):
            raise Exception(
                "Copy failed, file {} already exists".format(dst_file)
            )
        if not args.dry_run:
            shutil.copy(src_file, dst_file)
        logging.debug("c {} -> {}".format(src_file, dst_file))
        count.update(files=1)

    actions = dict(move=move, copy=copy)

    def make_dirs(src_subdir, dst_subdir):
        if os.path.exists(dst_subdir):
            return
        if not args.dry_run:
            os.makedirs(dst_subdir)
        logging.debug("+ {}".format(dst_subdir))
        count.update(dirs=1)

    backup_tree(
        os.path.abspath(args.src_path),
        os.path.abspath(args.dst_path),
        prefix=args.prefix,
        file_action=actions[args.action],
        dir_action=make_dirs
    )
    logging.info(
        "{} files, {} directories processed".format(
            count["files"],
            count["dirs"]
        )
    )
