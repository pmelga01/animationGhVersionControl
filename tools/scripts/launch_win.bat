@echo off
:: Find where THIS script is located
set "REPO_ROOT=%~dp0..\..\"
:: Path to team's specialized config and scripts inside the repo
set "BLENDER_USER_CONFIG=%REPO_ROOT%tools\config"
set "BLENDER_USER_SCRIPTS=%REPO_ROOT%tools\scripts"

:: Search common Steam installation paths
set "STEAM_C=C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"
set "STEAM_D=D:\SteamLibrary\steamapps\common\Blender\blender.exe"

echo Launching Project Blender via Steam (LTS)...
if exist "%STEAM_C%" (
    start "" /b "%STEAM_C%"
    exit
) else if exist "%STEAM_D%" (
    start "" /b "%STEAM_D%"
    exit
) else (
    echo [ERROR] Blender not found.
    pause
)
