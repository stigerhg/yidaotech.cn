@echo off
echo ============================================
echo  yidaotech.xyz - Git Push to GitHub
echo ============================================
echo.
cd /d C:\Users\stige\Desktop\yidaotech-new

echo Current status:
git status --short
echo.

echo Pushing to GitHub...
git push
if %errorlevel% neq 0 (
    echo.
    echo *** PUSH FAILED ***
    echo Check your network or GitHub authentication.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Push successful!
echo  Cloudflare Pages will auto-deploy.
echo  Check: https://yidaotech.pages.dev
echo ============================================
pause
