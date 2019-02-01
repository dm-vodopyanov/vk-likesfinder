#!/bin/bash

VERSION=2.0.0

# CLI
/Library/Frameworks/Python.framework/Versions/3.5/bin/pyinstaller vk_likesfinder_cli.py --distpath ./bin --clean --onefile --name vk-likesfinder-$VERSION-cli-mac
