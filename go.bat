@echo off
cd /d "D:\claude projects folder\Agents Team UI"
echo.
echo === Git Push to GitHub ===
echo.
git --version
if %errorlevel% neq 0 (
    echo ERROR: git not found in PATH
    pause
    exit /b 1
)
echo.
echo Initialising repo...
git init
git remote remove origin 2>nul
git remote add origin https://github.com/anuj123345/Agents-Team-.git
git branch -M main
echo.
echo Adding files...
git add .
echo.
echo Committing...
git diff --cached --quiet
if %errorlevel% neq 0 (
    git commit -m "Content calendar: AI-powered 12-week calendar with parse from strategy, add/delete items, platform color coding"
) else (
    echo Nothing new to commit.
)
echo.
echo Pushing to GitHub...
git push -u origin main --force
echo.
echo Done. Exit code: %errorlevel%
pause
