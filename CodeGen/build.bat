@echo off
echo Building CodeGen (PyWebView app)...
python -m pip install setuptools pywebview pyinstaller
pyinstaller --noconsole --onefile --add-data "index.html;." --name CodeGen CodeGen.py

echo Moving Executable to current directory...
move /y dist\CodeGen.exe CodeGen.exe

echo Cleaning up temp folders...
rmdir /s /q build
rmdir /s /q dist
del CodeGen.spec

echo Build Complete! CodeGen.exe has been created.
