@echo off
echo ===============================
echo Autozuhändler Lagerverwaltung
echo ===============================

cd /d %~dp0

python -m src.main

echo.
echo Programm beendet
pause