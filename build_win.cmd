@echo off

set VK_LIKESFINDER_VERSION=2.0.0
set VK_LIKESFINDER_LANG_PY=src\lang.py

echo VK_LIKESFINDER_VERSION=%VK_LIKESFINDER_VERSION%
echo VK_LIKESFINDER_LANG_PY=%VK_LIKESFINDER_LANG_PY%

echo Building CLI (English)...
if exist src\lang.py (erase %VK_LIKESFINDER_LANG_PY%)
break>"%VK_LIKESFINDER_LANG_PY%
echo lang = 0 > %VK_LIKESFINDER_LANG_PY%
C:\Python35\Scripts\pyinstaller.exe vk_likesfinder_cli.py --distpath .\bin --clean --onefile --icon .\images\icon.ico --name vk-likesfinder-%VK_LIKESFINDER_VERSION%-en-cli-win

echo Building CLI (Russian)...
if exist src\lang.py (erase %VK_LIKESFINDER_LANG_PY%)
break>"%VK_LIKESFINDER_LANG_PY%
echo lang = 1 > %VK_LIKESFINDER_LANG_PY%
C:\Python35\Scripts\pyinstaller.exe vk_likesfinder_cli.py --distpath .\bin --clean --onefile --icon .\images\icon.ico --name vk-likesfinder-%VK_LIKESFINDER_VERSION%-ru-cli-win
