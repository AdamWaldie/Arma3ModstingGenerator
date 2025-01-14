@echo off
:: Auto-detect SteamCMD path
for /f "tokens=*" %%A in ('where steamcmd 2^>nul') do set "STEAMCMD_PATH=%%A"
if not defined STEAMCMD_PATH (
    echo ERROR: SteamCMD not found. Please set the path manually.
    set /p STEAMCMD_PATH="Enter the full path to steamcmd.exe: "
)

:: Auto-detect Arma 3 installation directory
for /f "tokens=*" %%A in ('reg query "HKCU\Software\Valve\Steam\Apps\107410" /v InstallDir 2^>nul ^| find /i "InstallDir"') do set "ARMA3_DIR=%%B"
if not defined ARMA3_DIR (
    echo ERROR: Arma 3 directory not found in registry. Please set the path manually.
    set /p ARMA3_DIR="Enter the full path to your Arma 3 installation directory: "
)

:: Set mods directory based on Arma 3 directory
set "ARMA3_MODS_DIR=%ARMA3_DIR%\!Workshop"
if not exist "%ARMA3_MODS_DIR%" mkdir "%ARMA3_MODS_DIR%"

:: Allow user to override directories
echo Current directories:
echo - SteamCMD: %STEAMCMD_PATH%
echo - Arma 3: %ARMA3_DIR%
echo - Mods: %ARMA3_MODS_DIR%
set /p CUSTOMIZE="Do you want to customize these paths? (Y/N): "
if /i "%CUSTOMIZE%"=="Y" (
    set /p STEAMCMD_PATH="Enter the full path to steamcmd.exe: "
    set /p ARMA3_DIR="Enter the full path to your Arma 3 installation directory: "
    set /p ARMA3_MODS_DIR="Enter the full path to your mods directory: "
)

:: Set workshop mods temporary download directory
set "INSTALL_DIR=%ARMA3_DIR%\WorkshopDownloads"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Check for workshop IDs file
set "WORKSHOP_ID_FILE=workshop_ids.txt"
if not exist "%WORKSHOP_ID_FILE%" (
    echo ERROR: %WORKSHOP_ID_FILE% not found.
    pause
    exit /b
)

:: Process each Workshop ID
for /f "usebackq tokens=*" %%i in ("%WORKSHOP_ID_FILE%") do (
    echo Downloading mod with Workshop ID: %%i
    %STEAMCMD_PATH% +login anonymous +force_install_dir "%INSTALL_DIR%" +workshop_download_item 107410 %%i +quit
    
    :: Move mod to Arma 3 mods directory
    if exist "%INSTALL_DIR%\steamapps\workshop\content\107410\%%i" (
        echo Moving mod %%i to Arma 3 mods directory.
        xcopy /E /I /Y "%INSTALL_DIR%\steamapps\workshop\content\107410\%%i" "%ARMA3_MODS_DIR%\%%i"
    ) else (
        echo ERROR: Mod %%i not found in the download directory.
    )
)

echo All mods processed.
pause
