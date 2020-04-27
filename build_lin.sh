#!/bin/bash

VK_LIKESFINDER_VERSION=2.0.0

/usr/local/bin/pyinstaller vk_likesfinder_cli.py --distpath ./bin --clean --onefile --name vk-likesfinder-$VK_LIKESFINDER_VERSION-en-cli-lin
