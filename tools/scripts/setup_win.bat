@echo off
:: 1. Define Paths
set "REPO_ROOT=%~dp0..\.."
pushd "%REPO_ROOT%"
set "REPO_ROOT=%cd%"
popd
set "PROJECT_ROOT=%REPO_ROOT%\.."

echo --- PROJECT SETUP STARTING ---

:: 2. Create the 'local' folder if it doesn't exist
if not exist "%PROJECT_ROOT%\local" (
    mkdir "%PROJECT_ROOT%\local"
    mkdir "%PROJECT_ROOT%\local\temp"
    mkdir "%PROJECT_ROOT%\local\cache"
    echo [OK] Created local/ directories.
)

:: 3. Create the Symbolic Link to Google Drive
:: Adjust "G:\Shared drives\AnimationDrive\shared" if your team's drive name differs
set "SOURCE_DRIVE=G:\Shared drives\AnimationDrive\shared"
set "TARGET_LINK=%PROJECT_ROOT%\shared"

if exist "%TARGET_LINK%" (
    echo [INFO] 'shared' link already exists.
) else (
    mklink /D "%TARGET_LINK%" "%SOURCE_DRIVE%"
    if %errorlevel% neq 0 (
        echo [ERROR] mklink failed. Did you run this as Administrator?
        pause
        exit /b
    )
    echo [OK] Created link to Google Drive.
)

echo --- SETUP COMPLETE! ---
pause
