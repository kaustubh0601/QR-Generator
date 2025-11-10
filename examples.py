"""
Example script showing how to use the QR generator programmatically.
"""

from qr_core import QRGenerator
import os

def main():
    # Initialize the generator
    qr_gen = QRGenerator()
    
    print("🔧 Production QR Code Generator - Examples")
    print("=" * 50)
    
    # Create output directory
    output_dir = "examples_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Example 1: URL QR Code
    print("\n1. Generating URL QR Code...")
    url_path = qr_gen.create_url_qr(
        "https://github.com",
        output_dir=output_dir,
        error_correction='H',  # High error correction for production
        box_size=12,
        border=4
    )
    print(f"   ✅ Saved: {url_path}")
    
    # Example 2: Text QR Code
    print("\n2. Generating Text QR Code...")
    text_path = qr_gen.create_text_qr(
        "This is a static QR code that will never expire!",
        output_dir=output_dir,
        box_size=10
    )
    print(f"   ✅ Saved: {text_path}")
    
    # Example 3: Email QR Code
    print("\n3. Generating Email QR Code...")
    email_path = qr_gen.create_email_qr(
        "contact@example.com",
        subject="Hello from QR Code!",
        body="This email was triggered by scanning a static QR code.",
        output_dir=output_dir
    )
    print(f"   ✅ Saved: {email_path}")
    
    # Example 4: WiFi QR Code
    print("\n4. Generating WiFi QR Code...")
    wifi_path = qr_gen.create_wifi_qr(
        ssid="MyNetwork",
        password="mypassword123",
        security="WPA",
        output_dir=output_dir
    )
    print(f"   ✅ Saved: {wifi_path}")
    
    # Example 5: Phone QR Code
    print("\n5. Generating Phone QR Code...")
    phone_path = qr_gen.create_phone_qr(
        "+1-555-123-4567",
        output_dir=output_dir
    )
    print(f"   ✅ Saved: {phone_path}")
    
    # Example 6: vCard QR Code
    print("\n6. Generating vCard QR Code...")
    vcard_path = qr_gen.create_vcard_qr(
        name="John Doe",
        phone="+1-555-987-6543",
        email="john.doe@example.com",
        organization="Example Corp",
        output_dir=output_dir
    )
    print(f"   ✅ Saved: {vcard_path}")
    
    # Example 7: Custom colored QR Code
    print("\n7. Generating Custom Colored QR Code...")
    custom_path = qr_gen.save_qr_code(
        "Custom colored QR code!",
        "custom_colored_qr",
        output_dir=output_dir,
        fill_color="darkblue",
        back_color="lightgray",
        box_size=15,
        border=6
    )
    print(f"   ✅ Saved: {custom_path}")
    
    # Example 8: High-resolution QR Code for print
    print("\n8. Generating High-Resolution QR Code for Print...")
    print_path = qr_gen.save_qr_code(
        "https://printable-qr-code.example.com",
        "high_res_print_qr",
        output_dir=output_dir,
        box_size=20,  # Larger boxes for higher resolution
        border=8,     # Larger border for print safety
        error_correction='H'  # Maximum error correction
    )
    print(f"   ✅ Saved: {print_path}")
    
    # Show QR code information
    print("\n📊 QR Code Information Example:")
    sample_data = "https://example.com/very/long/url/path/with/parameters?id=123&name=test"
    info = qr_gen.get_qr_info(sample_data)
    print(f"   Data: {sample_data}")
    print(f"   Length: {info['data_length']} characters")
    print(f"   Version: {info['version']}")
    print(f"   Matrix Size: {info['box_count']}x{info['box_count']}")
    print(f"   Estimated Size: {info['estimated_size_px']}x{info['estimated_size_px']} pixels")
    
    print(f"\n🎉 All examples generated in: {os.path.abspath(output_dir)}")
    print("\n🔒 Key Benefits of These QR Codes:")
    print("   • Static - contain actual data, not redirects")
    print("   • Never expire - no external service dependency")
    print("   • Production quality - high error correction")
    print("   • Universal compatibility - work with any QR scanner")
    print("   • Offline capable - work without internet connection")
    print("   • Privacy-friendly - no tracking or analytics")

if __name__ == "__main__":
    main()