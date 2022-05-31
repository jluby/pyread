#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Read txt file, saving bookmarks at paragraph breaks. """

import argparse
import os
import re
import shutil
from pathlib import Path

from tqdm import tqdm

from pyread.helpers import process

# Initialize the argument parser.
parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path, nargs="?")
parser.add_argument("speed", type=float, default=1.15, nargs="?")
d = vars(parser.parse_args())


def main():
    text = open(d["file_path"], "r").read()[:2000]
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    output_file = os.path.join(os.getcwd(), f"{str(d['file_path'])[:-4]}.mp3")
    start_idx = 0
    chunklen = 2000
    i = 0
    pbar = tqdm(total=len(text))
    while start_idx < len(text):
        if start_idx + chunklen < len(text):
            end = re.search("(?s:.*)\n\n", text[: start_idx + chunklen]).span()[1]
            # handle case where paragraph is longer than 2000 characters
            if end == start_idx:
                end = re.search(". ", text[: start_idx + chunklen]).span()[1]
                # handle case where sentence is longer than 2000 characters
                if end == start_idx:
                    end = re.search(" ", text[: start_idx + chunklen]).span()[1]
        else:
            # handle end of file
            end = start_idx + chunklen
        temp_file = os.path.join(temp_dir, f"{start_idx}.mp3")
        process.cloud_tts(text[start_idx:end], d["speed"], temp_file)
        pbar.update(end - start_idx)
        start_idx = end
    pbar.close()
    for i, temp in enumerate(os.listdir(temp_dir)):
        temp_file = os.path.join(temp_dir, temp)
        if i == 0:
            mp3 = open(temp_file, "rb").read()
        else:
            mp3 += open(temp_file, "rb").read()
    open(output_file, "wb").write(mp3)
    shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
