#!/bin/bash
cd "$(dirname "$0")"
echo "📦 Setting up SPFMUI for Mac..."
echo ""
echo "Installing Python dependencies..."
pip3 install customtkinter pillow
echo ""
echo "Installing SP Font Maker..."
cd ~/Desktop
if [ -d "sp-font-maker" ]; then
    echo "sp-font-maker already exists, updating..."
    cd sp-font-maker
    git pull
else
    git clone https://github.com/KelseyHigham/sp-font-maker
    cd sp-font-maker
fi
pip3 install -e .
echo ""
echo "✅ Setup complete!"
echo "You can now double-click 'launch_mac.command' to run SPFMUI"
read -p "Press Enter to close..."
