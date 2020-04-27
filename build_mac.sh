#!/bin/bash

VK_LIKESFINDER_VERSION=2.0.0

/Library/Frameworks/Python.framework/Versions/3.5/bin/pyinstaller vk_likesfinder_cli.py --distpath ./bin --clean --onefile --name vk-likesfinder-$VK_LIKESFINDER_VERSION-cli-mac
