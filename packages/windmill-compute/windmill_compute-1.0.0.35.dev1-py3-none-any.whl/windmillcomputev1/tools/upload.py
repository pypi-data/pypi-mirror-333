#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2025/3/12
# @Author  : zhoubohan
# @File    : upload.py
"""
import os
import re
import tarfile
from argparse import ArgumentParser

from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import upload_by_filesystem


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--name", required=True, type=str, default=None)
    parser.add_argument("--dest_uri", required=True, type=str, default=None)
    parser.add_argument("--source_uri", required=False, type=str, default=".")


    args, _ = parser.parse_known_args()

    return args


def extract_workspace_id(name):
    """
    extract workspace id from path.
    """
    match = re.search(r'workspaces/([^/]+)', name)
    return match.group(1) if match else None


def run():
    """
    upload file.
    """
    try:
        org_id = os.getenv("ORG_ID")
        user_id = os.getenv("USER_ID")
        windmill_endpoint = os.getenv("WINDMILL_ENDPOINT")

        args = parse_args()

        windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                         context={"OrgID": org_id, "UserID": user_id})

        workspace_id = extract_workspace_id(args.name)

        filesystem = windmill_client.suggest_first_filesystem(
            workspace_id=workspace_id,
            guest_name=args.name,
        )

        file_path = os.path.join(args.souce_uri, os.path.basename(args.dest_uri))
        extension = os.path.splitext(file_path)[1]

        if extension == ".tar":
            with tarfile.open(file_path, "w:") as tar:
                tar.add(args.source_uri, arcname=os.path.basename(args.source_uri))


        upload_by_filesystem(filesystem=filesystem, file_path=file_path, dest_path=args.dest_uri)
    except Exception as e:
        print(f"Upload File Failed {args}: {e}")
        raise e


if __name__ == "__main__":
    run()
