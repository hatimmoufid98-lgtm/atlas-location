@echo off
echo ========================================
echo   Atlas Location - Demarrage du site
echo ========================================

cd /d "%~dp0"

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Appliquer les migrations si necessaire
python manage.py migrate --run-syncdb

REM Lancer le serveur
echo.
echo  Site disponible sur : http://localhost:8000
echo  Admin disponible sur : http://localhost:8000/admin
echo  Appuyez sur CTRL+C pour arreter
echo.
python manage.py runserver
