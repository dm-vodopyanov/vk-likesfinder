@echo off

set VK_LIKESFINDER_VERSION=2.0.0

C:\Python35\Scripts\pyinstaller.exe vk_likesfinder_cli.py --distpath .\bin --clean --onefile --icon .\images\icon.ico --name vk-likesfinder-%VK_LIKESFINDER_VERSION%-cli-win
