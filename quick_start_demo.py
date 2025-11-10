"""
Quick Start Demo for Production QR Code Generator

This script demonstrates the key features and generates sample QR codes
to show the production-level quality and various use cases.
"""

import os
from qr_core import QRGenerator

def main():
    print("🚀 Production QR Code Generator - Quick Start Demo")
    print("=" * 60)
    print()
    
    # Initialize generator
    qr_gen = QRGenerator()
    
    # Create demo directory
    demo_dir = "demo_output"
    os.makedirs(demo_dir, exist_ok=True)
    
    print("📱 Generating production-level static QR codes...")
    print()
    
    # Demo 1: Your website/link
    print("1. 🌐 Website QR Code")
    website_url = input("   Enter your website URL (or press Enter for demo): ").strip()
    if not website_url:
        website_url = "https://github.com"
    
    website_path = qr_gen.create_url_qr(
        website_url,
        output_dir=demo_dir,
        error_correction='H',  # Maximum error correction for production
        box_size=12,
        border=4
    )
    print(f"   ✅ Generated: {os.path.basename(website_path)}")
    print(f"   📁 Location: {website_path}")
    print()
    
    # Demo 2: Contact information
    print("2. 📇 Contact vCard QR Code")
    name = input("   Enter your name (or press Enter for demo): ").strip()
    if not name:
        name = "John Doe"
    
    email = input("   Enter your email (or press Enter for demo): ").strip()
    if not email:
        email = "john.doe@example.com"
    
    phone = input("   Enter your phone (or press Enter for demo): ").strip()
    if not phone:
        phone = "+1-555-123-4567"
    
    contact_path = qr_gen.create_vcard_qr(
        name=name,
        email=email,
        phone=phone,
        output_dir=demo_dir,
        error_correction='H'
    )
    print(f"   ✅ Generated: {os.path.basename(contact_path)}")
    print(f"   📁 Location: {contact_path}")
    print()
    
    # Demo 3: WiFi sharing
    print("3. 📶 WiFi QR Code")
    wifi_name = input("   Enter WiFi name (or press Enter for demo): ").strip()
    if not wifi_name:
        wifi_name = "MyNetwork"
    
    wifi_pass = input("   Enter WiFi password (or press Enter for demo): ").strip()
    if not wifi_pass:
        wifi_pass = "password123"
    
    wifi_path = qr_gen.create_wifi_qr(
        ssid=wifi_name,
        password=wifi_pass,
        security="WPA",
        output_dir=demo_dir,
        error_correction='H'
    )
    print(f"   ✅ Generated: {os.path.basename(wifi_path)}")
    print(f"   📁 Location: {wifi_path}")
    print()
    
    # Demo 4: Custom text/message
    print("4. 💬 Custom Text QR Code")
    custom_text = input("   Enter your custom text (or press Enter for demo): ").strip()
    if not custom_text:
        custom_text = "This is a production-level static QR code that never expires!"
    
    text_path = qr_gen.create_text_qr(
        custom_text,
        output_dir=demo_dir,
        error_correction='H'
    )
    print(f"   ✅ Generated: {os.path.basename(text_path)}")
    print(f"   📁 Location: {text_path}")
    print()
    
    # Demo 5: High-resolution for printing
    print("5. 🖨️  High-Resolution Print QR Code")
    print_url = input("   Enter URL for print QR (or press Enter for demo): ").strip()
    if not print_url:
        print_url = "https://your-business-website.com"
    
    print_path = qr_gen.save_qr_code(
        print_url,
        "high_resolution_print_qr",
        output_dir=demo_dir,
        error_correction='H',  # Maximum error correction
        box_size=20,           # Large boxes for high resolution
        border=8,              # Large border for print safety
        fill_color='black',
        back_color='white'
    )
    print(f"   ✅ Generated: {os.path.basename(print_path)}")
    print(f"   📁 Location: {print_path}")
    print()
    
    # Show QR information
    print("📊 QR Code Technical Details:")
    info = qr_gen.get_qr_info(custom_text)
    print(f"   • Error Correction: Level H (~30% damage recovery)")
    print(f"   • Format: Standard QR Code (ISO/IEC 18004)")
    print(f"   • Compatibility: Universal (works with any QR scanner)")
    print(f"   • Resolution: Scalable vector-based generation")
    print(f"   • File Format: High-quality PNG with optimization")
    print()
    
    print("🔒 Why These QR Codes Are Production-Ready:")
    print("   ✅ STATIC - Contains actual data, not redirect links")
    print("   ✅ NEVER EXPIRE - No dependency on external services")
    print("   ✅ OFFLINE CAPABLE - Works without internet connection")
    print("   ✅ HIGH ERROR CORRECTION - Recovers from up to 30% damage")
    print("   ✅ UNIVERSAL COMPATIBILITY - Works with any QR scanner")
    print("   ✅ PRIVACY-FRIENDLY - No tracking or analytics")
    print("   ✅ PRODUCTION QUALITY - Suitable for business use")
    print("   ✅ PRINT-READY - High resolution output")
    print()
    
    print(f"🎉 Demo complete! All QR codes saved in: {os.path.abspath(demo_dir)}")
    print()
    print("🛠️  Next Steps:")
    print("   • GUI Application: python qr_generator_gui.py")
    print("   • CLI Help: python qr_generator_cli.py --help")
    print("   • Batch Processing: python qr_generator_cli.py --batch batch_example.txt")
    print()
    print("💡 Pro Tips:")
    print("   • Use Error Correction Level H for production")
    print("   • Use larger box_size (15-20) for print materials")
    print("   • Include larger borders (6-8) for print safety")
    print("   • Test QR codes with multiple scanners before deployment")


if __name__ == "__main__":
    main()