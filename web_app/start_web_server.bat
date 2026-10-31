@echo off
title GlassyPrint Hub - Development Server
echo ========================================================
echo  Launching GlassyPrint Hub Web Server (Windows Mode)
echo ========================================================
cd /d "%~dp0"
python app.py
pause
