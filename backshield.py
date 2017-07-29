#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import subprocess
from distutils.dir_util import copy_tree
from datetime import datetime
from pytz import timezone

def run():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Parse arguments
    parser = argparse.ArgumentParser(description="Backshield is simple backup tool for server configurations with git.")
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init", help="Initialize with git repository url")
    parser_init.add_argument('repository', type=str, metavar="REPOSITORY", help="git repository for backup")
    parser_init.set_defaults(handler=command_init)

    parser_add = subparsers.add_parser("add", help="Add file to backup targets")
    parser_add.add_argument('file', type=str, metavar="FILE", help="filename")
    parser_add.set_defaults(handler=command_add)

    parser_remove = subparsers.add_parser("remove", help="Remove file in backup targets")
    parser_remove.add_argument('file', type=str, metavar="FILE", help="filename")
    parser_remove.set_defaults(handler=command_remove)

    parser_list = subparsers.add_parser("list", help="Print backup targets")
    parser_list.set_defaults(handler=command_list)

    parser_backup = subparsers.add_parser("backup", help="Backup now")
    parser_backup.add_argument('message', type=str, nargs="?", default="-", metavar="COMMIT_MESSAGE", help="commit message")
    parser_backup.set_defaults(handler=command_backup)

    # Run the command
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

def command_init(args):
    # Git clone
    print("Run git clone: %s" % args.repository)
    p = subprocess.Popen("git clone %s data" % args.repository, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err.decode("utf-8"))
        sys.exit(1)

    # Create config files if not exist
    hostname = os.uname()[1]
    print("Create config file and directory")
    os.makedirs("data/%s" % hostname, exist_ok=True)
    os.makedirs("data/_backshield", exist_ok=True)
    open("data/%s/.gitkeep" % hostname, "a").close()
    open("data/_backshield/%s.conf" % hostname, "a").close()

    print("Initialized.")

def command_add(args):
    # Get fullpath
    abspath = os.path.abspath(args.file)

    # Add file to config
    hostname = os.uname()[1]
    with open("data/_backshield/%s.conf" % hostname, "r+") as f:
        watches = f.readlines()
        if abspath in watches:
            print("Already exist in configuration")
            sys.exit(0)
        f.write("%s\n" % abspath)

    print("Added %s" % abspath)

def command_remove(args):
    # Get fullpath
    abspath = os.path.abspath(args.file)

    # Remove file to config
    hostname = os.uname()[1]
    with open("data/_backshield/%s.conf" % hostname, "r+") as f:
        watches = f.readlines()
        f.seek(0)
        f.truncate()
        for watch in watches:
            if watch.rstrip() == abspath:
                os.remove("data/%s%s" % (hostname, abspath))
                print("Removed %s" % abspath)
                continue

            f.write("%s\n" % watch.rstrip())

def command_list(args):    
    hostname = os.uname()[1]
    with open("data/_backshield/%s.conf" % hostname, "r") as f:
        watches = f.readlines()
        watches.sort()
        for watch in watches:
            print(watch.rstrip())

def command_backup(args):
    hostname = os.uname()[1]
    with open("data/_backshield/%s.conf" % hostname, "r+") as f:
        watches = f.readlines()
        for watch in watches:
            watch = watch.rstrip()

            # Check exist file
            if os.path.exists(watch) == False:
                print("Warning: %s is not found." % watch)
                continue

            # Create Directory
            os.makedirs("data/%s%s" % (hostname, os.path.split(watch)[0]), exist_ok=True)

            # Copy directory/file
            if os.path.isdir(watch):
                copy_tree(watch, "data/%s%s" % (hostname, watch))
            else:
                shutil.copy(watch, "data/%s%s" % (hostname, watch))

    # Git commit     
    timestr = datetime.now(timezone("Asia/Tokyo")).strftime("%Y/%m/%d %H:%M:%S")
    p = subprocess.Popen("cd data && git add -A; git diff-index --quiet HEAD || (git commit -m \"[%s] %s: %s\" ;git push origin master) && cd .." % (timestr, hostname, args.message), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print("git add/commit/push failed: ", err.decode("utf-8"), out.decode("utf-8"))
        sys.exit(1)

    print("Completed.")

run()