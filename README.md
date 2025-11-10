# QR Code Generator

A production-level Python application for generating static QR codes that never expire.

## Features

- **Static QR Codes**: Generated QR codes are permanent and never expire
- **High Quality**: Production-level QR codes with optimal error correction
- **Multiple Formats**: Support for URLs, text, email, phone numbers, WiFi, and more
- **Customizable**: Adjustable size, error correction level, and border
- **User-friendly GUI**: Simple and intuitive interface
- **Export Options**: Save as PNG, JPEG, or other image formats
- **Batch Generation**: Generate multiple QR codes at once

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Application
Run the main application:
```bash
python qr_generator_gui.py
```

### Command Line Interface
```bash
python qr_generator_cli.py --text "Your content here" --output "qr_code.png"
```

## QR Code Types Supported

- **URL/Website**: Direct links to websites
- **Plain Text**: Any text content
- **Email**: Email addresses with optional subject/body
- **Phone Numbers**: Phone numbers for direct calling
- **SMS**: SMS with phone number and message
- **WiFi**: WiFi network credentials
- **vCard**: Contact information

## Technical Details

- **Error Correction**: Uses HIGH level error correction (Level H - ~30% recovery)
- **Format**: Generates standard QR codes compatible with all scanners
- **Quality**: High resolution output suitable for print and digital use
- **Static Nature**: QR codes contain the actual data, not links to external services

## File Structure

```
qr_generator/
├── qr_generator_gui.py      # Main GUI application
├── qr_generator_cli.py      # Command line interface
├── qr_core.py              # Core QR generation logic
├── requirements.txt        # Dependencies
├── README.md              # This file
└── output/                # Generated QR codes (created automatically)
```

## Why These QR Codes Never Expire

Unlike dynamic QR codes that redirect through third-party services, this generator creates **static QR codes** that directly contain your data. This means:

- ✅ No dependency on external services
- ✅ No expiration dates
- ✅ Works offline once generated
- ✅ Full control over your data
- ✅ No tracking or analytics
- ✅ Production-ready quality

## License

This project is open source and available under the MIT License.