#!/bin/bash

echo "Installing Production QR Code Generator Dependencies..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed"
        echo "Please install Python from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found. Installing required packages..."
echo

# Install required packages
$PYTHON_CMD -m pip install qrcode[pil]==7.4.2
if [ $? -ne 0 ]; then
    echo "Error installing qrcode"
    exit 1
fi

$PYTHON_CMD -m pip install Pillow==10.1.0
if [ $? -ne 0 ]; then
    echo "Error installing Pillow"
    exit 1
fi

echo
echo "✅ Installation complete!"
echo
echo "You can now run:"
echo "  • GUI: $PYTHON_CMD qr_generator_gui.py"
echo "  • CLI: $PYTHON_CMD qr_generator_cli.py --help"
echo "  • Examples: $PYTHON_CMD examples.py"
echo