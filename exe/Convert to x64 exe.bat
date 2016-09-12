@echo off
cd %~dp0
"%SystemDrive%\python35x64\Scripts\pyinstaller.exe" --console -F -i "%~dp0\VP.ico" -m "%~dp0\manifest.xml" --upx-dir "%~dp0\upx" --distpath "%~dp0\Build\x64" "%~dp0\DecoraterBot.py"
"%~dp0\Build\x64\DecoraterBot.exe"
"%~dp0\Build\x64\DecoraterBot.x64.win32.cpython-351.exe"
pause