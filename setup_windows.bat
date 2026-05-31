@echo off
echo 📦 Setting up SPFMUI for Windows...
echo.
echo Installing Python dependencies...
pip install customtkinter pillow
echo.
echo Installing SP Font Maker...
cd %USERPROFILE%\Desktop
if exist "sp-font-maker" (
    echo sp-font-maker already exists, updating...
    cd sp-font-maker
    git pull
) else (
    git clone https://github.com/KelseyHigham/sp-font-maker
    cd sp-font-maker
)
pip install -e .
echo.
echo ✅ Setup complete!
echo You can now double-click 'launch_windows.bat' to run SPFMUI
pause
