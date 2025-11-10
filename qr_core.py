"""
Core QR Code Generation Module

This module provides production-level QR code generation with static codes that never expire.
All QR codes generated are self-contained and do not rely on external services.
"""

import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_Q, ERROR_CORRECT_M, ERROR_CORRECT_L
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Optional, Tuple, Union
import re


class QRGenerator:
    """
    Production-level QR code generator that creates static, never-expiring QR codes.
    """
    
    def __init__(self):
        self.error_correction_levels = {
            'L': ERROR_CORRECT_L,  # ~7% recovery
            'M': ERROR_CORRECT_M,  # ~15% recovery  
            'Q': ERROR_CORRECT_Q,  # ~25% recovery
            'H': ERROR_CORRECT_H   # ~30% recovery (recommended for production)
        }
    
    def generate_qr_code(self, 
                        data: str, 
                        error_correction: str = 'H',
                        box_size: int = 10,
                        border: int = 4,
                        fill_color: str = 'black',
                        back_color: str = 'white') -> qrcode.QRCode:
        """
        Generate a QR code with the specified parameters.
        
        Args:
            data: The content to encode in the QR code
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
            box_size: Size of each box in pixels
            border: Border size in boxes
            fill_color: Foreground color
            back_color: Background color
            
        Returns:
            QRCode object ready for image generation
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Use high error correction by default for production quality
        error_level = self.error_correction_levels.get(error_correction, ERROR_CORRECT_H)
        
        qr = qrcode.QRCode(
            version=1,  # Auto-adjust based on data
            error_correction=error_level,
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr
    
    def create_qr_image(self, qr_code: qrcode.QRCode, 
                       fill_color: str = 'black', 
                       back_color: str = 'white') -> Image.Image:
        """
        Create PIL Image from QR code object.
        
        Args:
            qr_code: QRCode object
            fill_color: Foreground color
            back_color: Background color
            
        Returns:
            PIL Image object
        """
        img = qr_code.make_image(fill_color=fill_color, back_color=back_color)
        return img
    
    def save_qr_code(self, 
                    data: str, 
                    filename: str,
                    output_dir: str = "output",
                    **kwargs) -> str:
        """
        Generate and save QR code to file.
        
        Args:
            data: Content to encode
            filename: Output filename (without extension)
            output_dir: Output directory
            **kwargs: Additional parameters for QR generation
            
        Returns:
            Full path to saved file
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate QR code
        qr = self.generate_qr_code(data, **kwargs)
        img = self.create_qr_image(qr, 
                                  kwargs.get('fill_color', 'black'),
                                  kwargs.get('back_color', 'white'))
        
        # Determine file extension
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            filename += '.png'
        
        # Full path
        filepath = os.path.join(output_dir, filename)
        
        # Save with high quality
        if filename.lower().endswith('.png'):
            img.save(filepath, 'PNG', optimize=True)
        elif filename.lower().endswith(('.jpg', '.jpeg')):
            # Convert to RGB for JPEG (removes alpha channel)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, 'white')
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            img.save(filepath, 'JPEG', quality=95, optimize=True)
        else:
            img.save(filepath)
        
        return filepath
    
    def create_url_qr(self, url: str, **kwargs) -> str:
        """Create QR code for URL with validation."""
        if not self._is_valid_url(url):
            # Add https:// if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
        
        return self.save_qr_code(url, f"url_qr_{self._sanitize_filename(url)}", **kwargs)
    
    def create_text_qr(self, text: str, **kwargs) -> str:
        """Create QR code for plain text."""
        return self.save_qr_code(text, f"text_qr_{self._sanitize_filename(text)}", **kwargs)
    
    def create_email_qr(self, email: str, subject: str = "", body: str = "", **kwargs) -> str:
        """Create QR code for email with optional subject and body."""
        mailto_data = f"mailto:{email}"
        params = []
        if subject:
            params.append(f"subject={subject}")
        if body:
            params.append(f"body={body}")
        
        if params:
            mailto_data += "?" + "&".join(params)
        
        return self.save_qr_code(mailto_data, f"email_qr_{self._sanitize_filename(email)}", **kwargs)
    
    def create_phone_qr(self, phone: str, **kwargs) -> str:
        """Create QR code for phone number."""
        tel_data = f"tel:{phone}"
        return self.save_qr_code(tel_data, f"phone_qr_{self._sanitize_filename(phone)}", **kwargs)
    
    def create_sms_qr(self, phone: str, message: str = "", **kwargs) -> str:
        """Create QR code for SMS."""
        sms_data = f"sms:{phone}"
        if message:
            sms_data += f"?body={message}"
        
        return self.save_qr_code(sms_data, f"sms_qr_{self._sanitize_filename(phone)}", **kwargs)
    
    def create_wifi_qr(self, ssid: str, password: str, security: str = "WPA", hidden: bool = False, **kwargs) -> str:
        """Create QR code for WiFi connection."""
        wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
        return self.save_qr_code(wifi_data, f"wifi_qr_{self._sanitize_filename(ssid)}", **kwargs)
    
    def create_vcard_qr(self, name: str, phone: str = "", email: str = "", 
                       organization: str = "", **kwargs) -> str:
        """Create QR code for vCard contact."""
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
        
        return self.save_qr_code(vcard_data, f"vcard_qr_{self._sanitize_filename(name)}", **kwargs)
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use as filename."""
        # Remove or replace invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Limit length and remove extra spaces
        sanitized = sanitized.strip()[:50]
        return sanitized if sanitized else "qr_code"
    
    def get_qr_info(self, data: str) -> dict:
        """Get information about the QR code that would be generated."""
        qr = self.generate_qr_code(data)
        return {
            'version': qr.version,
            'error_correction': qr.error_correction,
            'box_count': qr.modules_count,
            'data_length': len(data),
            'estimated_size_px': qr.modules_count * 10 + (qr.border * 2 * 10)  # Assuming box_size=10
        }