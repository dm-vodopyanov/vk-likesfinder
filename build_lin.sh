#!/bin/bash

VERSION=2.0.0

# CLI
/usr/local/bin/pyinstaller vk_likesfinder_cli.py --distpath ./bin --clean --onefile --name vk-likesfinder-$VERSION-cli-lin
