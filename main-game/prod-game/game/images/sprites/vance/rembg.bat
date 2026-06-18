@echo off
title Batch Background Removal

set "REMBG_EXE=C:\Users\mikez\AppData\Local\Programs\Python\Python312\Scripts\rembg.exe"
set "INPUT_DIR=%~dp0input"
set "OUTPUT_DIR=%~dp0output"

if not exist "%REMBG_EXE%" (
    echo rembg.exe not found:
    echo "%REMBG_EXE%"
    echo.
    echo Check the path and update this BAT file if needed.
    pause
    exit /b 1
)

if not exist "%INPUT_DIR%" (
    echo Input folder not found:
    echo "%INPUT_DIR%"
    echo.
    echo Create a folder named "original" next to this BAT file and put your source images there.
    pause
    exit /b 1
)

echo.
echo Running background removal...
echo Input : "%INPUT_DIR%"
echo Output: "%OUTPUT_DIR%"
echo.

"%REMBG_EXE%" p "%INPUT_DIR%" "%OUTPUT_DIR%"

if errorlevel 1 (
    echo.
    echo rembg failed.
    pause
    exit /b 1
)

echo.
echo Done.
echo Output saved in:
echo "%OUTPUT_DIR%"
pause