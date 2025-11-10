"""
Command Line Interface for QR Code Generator

Generate production-level static QR codes from the command line.
"""

import argparse
import sys
import os
from qr_core import QRGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate production-level static QR codes that never expire",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate URL QR code
  python qr_generator_cli.py --url "https://example.com" --output "website.png"
  
  # Generate text QR code
  python qr_generator_cli.py --text "Hello World" --output "hello.png"
  
  # Generate email QR code
  python qr_generator_cli.py --email "test@example.com" --subject "Hello" --output "email.png"
  
  # Generate WiFi QR code
  python qr_generator_cli.py --wifi --ssid "MyNetwork" --password "mypass123" --output "wifi.png"
  
  # Generate with custom settings
  python qr_generator_cli.py --text "Custom QR" --error-correction H --box-size 15 --border 6 --output "custom.png"
        """
    )
    
    # Data type arguments (mutually exclusive)
    data_group = parser.add_mutually_exclusive_group(required=True)
    data_group.add_argument('--url', help='Generate QR code for URL')
    data_group.add_argument('--text', help='Generate QR code for plain text')
    data_group.add_argument('--email', help='Generate QR code for email address')
    data_group.add_argument('--phone', help='Generate QR code for phone number')
    data_group.add_argument('--wifi', action='store_true', help='Generate QR code for WiFi (requires --ssid and --password)')
    
    # Additional data for specific types
    parser.add_argument('--subject', help='Email subject (used with --email)')
    parser.add_argument('--body', help='Email body (used with --email)')
    parser.add_argument('--message', help='SMS message (used with --sms)')
    parser.add_argument('--ssid', help='WiFi network name (used with --wifi)')
    parser.add_argument('--password', help='WiFi password (used with --wifi)')
    parser.add_argument('--security', choices=['WPA', 'WEP', 'nopass'], default='WPA',
                       help='WiFi security type (default: WPA)')
    
    # vCard arguments
    parser.add_argument('--vcard', action='store_true', help='Generate vCard QR code (requires --name)')
    parser.add_argument('--name', help='Contact name (used with --vcard)')
    parser.add_argument('--organization', help='Organization (used with --vcard)')
    
    # Output settings
    parser.add_argument('--output', '-o', required=True, help='Output filename')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: output)')
    
    # QR code settings
    parser.add_argument('--error-correction', '-e', choices=['L', 'M', 'Q', 'H'], default='H',
                       help='Error correction level (default: H for production)')
    parser.add_argument('--box-size', type=int, default=10, help='Box size in pixels (default: 10)')
    parser.add_argument('--border', type=int, default=4, help='Border size in boxes (default: 4)')
    parser.add_argument('--fill-color', default='black', help='Foreground color (default: black)')
    parser.add_argument('--back-color', default='white', help='Background color (default: white)')
    
    # Utility arguments
    parser.add_argument('--info', action='store_true', help='Show QR code information without generating')
    parser.add_argument('--batch', help='Process batch file (one item per line)')
    parser.add_argument('--list-fonts', action='store_true', help='List available fonts for text QR codes')
    
    args = parser.parse_args()
    
    # Initialize QR generator
    qr_gen = QRGenerator()
    
    try:
        # Handle batch processing
        if args.batch:
            process_batch(qr_gen, args)
            return
        
        # Validate WiFi arguments
        if args.wifi:
            if not args.ssid or not args.password:
                parser.error("--wifi requires both --ssid and --password")
        
        # Validate vCard arguments
        if args.vcard:
            if not args.name:
                parser.error("--vcard requires --name")
        
        # Generate QR code based on type
        if args.url:
            data = args.url
            filename = args.output
        elif args.text:
            data = args.text
            filename = args.output
        elif args.email:
            data = create_email_data(args.email, args.subject, args.body)
            filename = args.output
        elif args.phone:
            data = f"tel:{args.phone}"
            filename = args.output
        elif args.wifi:
            data = f"WIFI:T:{args.security};S:{args.ssid};P:{args.password};H:false;;"
            filename = args.output
        elif args.vcard:
            data = create_vcard_data(args.name, args.phone, args.email, args.organization)
            filename = args.output
        else:
            parser.error("No data type specified")
        
        # Show info only if requested
        if args.info:
            info = qr_gen.get_qr_info(data)
            print("QR Code Information:")
            print(f"  Data: {data}")
            print(f"  Data Length: {info['data_length']} characters")
            print(f"  Version: {info['version']}")
            print(f"  Error Correction: {args.error_correction}")
            print(f"  Matrix Size: {info['box_count']}x{info['box_count']}")
            print(f"  Estimated Size: {info['estimated_size_px']}x{info['estimated_size_px']} pixels")
            print(f"  Static QR Code: Yes (never expires)")
            return
        
        # Generate and save QR code
        kwargs = {
            'error_correction': args.error_correction,
            'box_size': args.box_size,
            'border': args.border,
            'fill_color': args.fill_color,
            'back_color': args.back_color
        }
        
        # Remove extension from filename for save_qr_code function
        base_filename = os.path.splitext(args.output)[0]
        
        filepath = qr_gen.save_qr_code(data, base_filename, args.output_dir, **kwargs)
        
        print(f"✅ QR code generated successfully!")
        print(f"📁 File: {filepath}")
        print(f"📊 Data: {data}")
        print(f"🔒 Static QR code (never expires)")
        
        # Show additional info
        info = qr_gen.get_qr_info(data)
        print(f"📏 Size: {info['estimated_size_px']}x{info['estimated_size_px']} pixels")
        print(f"🛡️  Error Correction: {args.error_correction} level")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_email_data(email, subject=None, body=None):
    """Create mailto data string."""
    mailto_data = f"mailto:{email}"
    params = []
    if subject:
        params.append(f"subject={subject}")
    if body:
        params.append(f"body={body}")
    
    if params:
        mailto_data += "?" + "&".join(params)
    
    return mailto_data


def create_vcard_data(name, phone=None, email=None, organization=None):
    """Create vCard data string."""
    vcard_data = "BEGIN:VCARD\n"
    vcard_data += "VERSION:3.0\n"
    vcard_data += f"FN:{name}\n"
    if phone:
        vcard_data += f"TEL:{phone}\n"
    if email:
        vcard_data += f"EMAIL:{email}\n"
    if organization:
        vcard_data += f"ORG:{organization}\n"
    vcard_data += "END:VCARD"
    
    return vcard_data


def process_batch(qr_gen, args):
    """Process batch file."""
    if not os.path.exists(args.batch):
        raise FileNotFoundError(f"Batch file not found: {args.batch}")
    
    with open(args.batch, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        print("❌ Batch file is empty")
        return
    
    print(f"📋 Processing {len(lines)} items from batch file...")
    
    kwargs = {
        'error_correction': args.error_correction,
        'box_size': args.box_size,
        'border': args.border,
        'fill_color': args.fill_color,
        'back_color': args.back_color
    }
    
    generated_files = []
    
    for i, line in enumerate(lines, 1):
        try:
            # Determine data type and create appropriate QR
            if args.url or line.startswith(('http://', 'https://')):
                filepath = qr_gen.create_url_qr(line, output_dir=args.output_dir, **kwargs)
            elif args.email or '@' in line:
                filepath = qr_gen.create_email_qr(line, output_dir=args.output_dir, **kwargs)
            elif args.phone or line.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                filepath = qr_gen.create_phone_qr(line, output_dir=args.output_dir, **kwargs)
            else:
                filepath = qr_gen.create_text_qr(line, output_dir=args.output_dir, **kwargs)
            
            generated_files.append(filepath)
            print(f"  ✅ {i}/{len(lines)}: {os.path.basename(filepath)}")
            
        except Exception as e:
            print(f"  ❌ {i}/{len(lines)}: Failed - {e}")
    
    print(f"\n🎉 Batch processing complete!")
    print(f"📁 Generated {len(generated_files)} QR codes in: {os.path.abspath(args.output_dir)}")
    print(f"🔒 All QR codes are static and never expire")


if __name__ == "__main__":
    main()