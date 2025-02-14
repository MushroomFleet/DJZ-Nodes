@echo off
rem PIP Manager for embedded Python
setlocal EnableDelayedExpansion

set "CONFIG_FILE=%~dp0python_path.cfg"

if exist "%CONFIG_FILE%" (
    set /p PYTHON_PATH=<"%CONFIG_FILE%"
) else (
    echo No saved Python path found.
    echo Please enter the full path to python.exe:
    set /p PYTHON_PATH="Python Path: "
    echo !PYTHON_PATH!>"%CONFIG_FILE%"
)

if not exist "!PYTHON_PATH!" (
    echo Python executable not found at: !PYTHON_PATH!
    del "%CONFIG_FILE%" 2>nul
    pause
    exit /b 1
)

:menu
cls
echo ===================================
echo            PIP MANAGER
echo ===================================
echo Current Python Path: !PYTHON_PATH!
echo.
echo 1. Update pip
echo 2. Remove package
echo 3. Install package
echo 4. Check version
echo 5. Check Packages
echo 6. List Packages
echo 7. Change path
echo 8. Exit
echo.
set /p CHOICE="Choose an option (1-8): "

if "!CHOICE!"=="1" (
    "!PYTHON_PATH!" -m pip install --upgrade pip
) else if "!CHOICE!"=="2" (
    set /p PKG="Package to remove: "
    "!PYTHON_PATH!" -m pip uninstall -y !PKG!
) else if "!CHOICE!"=="3" (
    set /p PKG="Package to install: "
    "!PYTHON_PATH!" -m pip install !PKG!
) else if "!CHOICE!"=="4" (
    set /p PKG="Package to check: "
    "!PYTHON_PATH!" -m pip show !PKG! | findstr "Version:" || echo Package not found
) else if "!CHOICE!"=="5" (
    "!PYTHON_PATH!" -m pip check
) else if "!CHOICE!"=="6" (
    "!PYTHON_PATH!" -m pip list
) else if "!CHOICE!"=="7" (
    set /p NEW_PATH="New Python path: "
    if exist "!NEW_PATH!" (
        echo !NEW_PATH!>"%CONFIG_FILE%"
        set "PYTHON_PATH=!NEW_PATH!"
        echo Path updated.
    ) else (
        echo Invalid path.
    )
) else if "!CHOICE!"=="8" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice.
)

pause
goto menu
