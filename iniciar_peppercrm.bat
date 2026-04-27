@echo off
title PepperCRM
echo.
echo  Iniciando PepperCRM...
echo.

cd /d C:\Users\welov\PycharmProjects\WebSolution\peppercrm

call ..\venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    call venv\Scripts\activate.bat 2>nul
)

streamlit run crm_app.py --server.port 8501

pause