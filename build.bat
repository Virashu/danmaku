pyinstaller --onefile --clean --name danmaku --icon .\danmaku\resources\icon.ico .\danmaku\main.py
xcopy /s /mir .\danmaku\resources .\dist\resources
