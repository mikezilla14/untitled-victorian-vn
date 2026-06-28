@echo off
if "%~1" == "" (
    echo Usage: fix_webp.bat ^<path_to_webp_file^>
    pause
    exit /b 1
)

python -c "import sys; from PIL import Image; img = Image.open(sys.argv[1]); img.save(sys.argv[1], 'WEBP')" "%~1"

echo Re-saved and fixed: %~1
pause
