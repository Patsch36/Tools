@echo off
setlocal enabledelayedexpansion

:: Erstelle das .tools Verzeichnis im Benutzerverzeichnis
set TOOLSDIR=%USERPROFILE%\.tools
mkdir %TOOLSDIR%

:: Dynamischen Pfad zu den Skripten und der requirements.txt ermitteln
set SCRIPTSDIR=%~dp0
set SCRIPTSDIR=%SCRIPTSDIR:~0,-14%
echo Script-Directory: %SCRIPTSDIR%
set REQUIREMENTS=%SCRIPTSDIR%\requirements.txt
echo Requirements-File: %REQUIREMENTS%

echo ===Installing Python===========================================

:: Erstelle eine Python Umgebung im .tools Ordner
cd %TOOLSDIR%
python -m venv .env
%TOOLSDIR%\.env\Scripts\python.exe -m pip install --upgrade pip

:: Installiere die Bibliotheken aus requirements.txt
%TOOLSDIR%\.env\Scripts\python.exe -m pip install -r "%REQUIREMENTS%"

echo ===Creating Custom Scripts=====================================

:: Erstelle die Skripte für jedes Python-Skript im Skripte-Ordner
for %%f in ("%SCRIPTSDIR%\*") do (
    if "%%~xf" == ".py" (
        set "SCRIPTNAME=%%f"

        set "SCRIPTNAME=!SCRIPTNAME:%SCRIPTSDIR%=!"
        set "SCRIPTNAME=!SCRIPTNAME:.py=!"
        set "SCRIPTNAME=!SCRIPTNAME:\=!"
        
        echo Creating Tool !SCRIPTNAME!

        echo @echo off > %TOOLSDIR%\!SCRIPTNAME!.bat
        echo %TOOLSDIR%\.env\Scripts\python.exe %SCRIPTSDIR%!SCRIPTNAME!.py %%* >> %TOOLSDIR%\!SCRIPTNAME!.bat
    )
)
echo ===Adding .tools to PATH=======================================

:: Fügt das .tools Verzeichnis zur PATH-Umgebungsvariable hinzu
setx PATH "%TOOLSDIR%;%PATH%"

echo Setup abgeschlossen!
endlocal
