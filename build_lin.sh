#!/bin/bash

VERSION=1.0.0

# CLI
/usr/local/bin/pyinstaller vk_likechecker_cli.py --distpath ./bin --clean --onefile --name vk-likechecker-$VERSION-cli-lin
