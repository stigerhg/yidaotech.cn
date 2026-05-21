@echo off
echo ============================================
echo  yidaotech.xyz - Astro Build & Test
echo ============================================
echo.
cd /d C:\Users\stige\Desktop\yidaotech-new

echo [1/2] Running Astro build...
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo *** BUILD FAILED ***
    pause
    exit /b 1
)

echo.
echo [2/2] Build successful! Output in dist/
echo.
echo Ready to push to GitHub? Run:
echo   git add -A ^&^& git commit -m "content: full site rewrite" ^&^& git push
echo.
pause
