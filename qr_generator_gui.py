"""
GUI Application for QR Code Generator

A user-friendly interface for generating production-level static QR codes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from PIL import Image, ImageTk
from qr_core import QRGenerator
import webbrowser


class QRGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Production QR Code Generator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize QR generator
        self.qr_gen = QRGenerator()
        
        # Variables
        self.qr_type = tk.StringVar(value="url")
        self.error_correction = tk.StringVar(value="H")
        self.box_size = tk.IntVar(value=10)
        self.border = tk.IntVar(value=4)
        self.fill_color = tk.StringVar(value="black")
        self.back_color = tk.StringVar(value="white")
        
        # Current QR image
        self.current_qr_image = None
        self.current_file_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Create main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generator Tab
        self.generator_frame = ttk.Frame(notebook)
        notebook.add(self.generator_frame, text="QR Generator")
        self.setup_generator_tab()
        
        # Batch Tab
        self.batch_frame = ttk.Frame(notebook)
        notebook.add(self.batch_frame, text="Batch Generator")
        self.setup_batch_tab()
        
        # About Tab
        self.about_frame = ttk.Frame(notebook)
        notebook.add(self.about_frame, text="About")
        self.setup_about_tab()
    
    def setup_generator_tab(self):
        """Setup the main generator tab."""
        # Main container
        main_container = ttk.PanedWindow(self.generator_frame, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for controls
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # Right panel for preview
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=1)
        
        # Setup left panel
        self.setup_controls(left_panel)
        
        # Setup right panel
        self.setup_preview(right_panel)
    
    def setup_controls(self, parent):
        """Setup control widgets."""
        # QR Type Selection
        type_frame = ttk.LabelFrame(parent, text="QR Code Type", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        qr_types = [
            ("URL/Website", "url"),
            ("Plain Text", "text"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("SMS", "sms"),
            ("WiFi", "wifi"),
            ("Contact (vCard)", "vcard")
        ]
        
        for i, (text, value) in enumerate(qr_types):
            ttk.Radiobutton(type_frame, text=text, variable=self.qr_type, 
                           value=value, command=self.update_input_fields).grid(
                               row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # Input Fields Frame
        self.input_frame = ttk.LabelFrame(parent, text="Content", padding=10)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(parent, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Error Correction
        ttk.Label(settings_frame, text="Error Correction:").grid(row=0, column=0, sticky=tk.W, pady=2)
        error_combo = ttk.Combobox(settings_frame, textvariable=self.error_correction, 
                                  values=["L (~7%)", "M (~15%)", "Q (~25%)", "H (~30%)"], 
                                  state="readonly", width=15)
        error_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        error_combo.bind('<<ComboboxSelected>>', lambda e: self.update_error_correction())
        
        # Box Size
        ttk.Label(settings_frame, text="Box Size:").grid(row=1, column=0, sticky=tk.W, pady=2)
        box_spin = ttk.Spinbox(settings_frame, from_=5, to=20, textvariable=self.box_size, width=15)
        box_spin.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Border
        ttk.Label(settings_frame, text="Border:").grid(row=2, column=0, sticky=tk.W, pady=2)
        border_spin = ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.border, width=15)
        border_spin.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Colors
        ttk.Label(settings_frame, text="Foreground:").grid(row=3, column=0, sticky=tk.W, pady=2)
        color_frame1 = ttk.Frame(settings_frame)
        color_frame1.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        ttk.Entry(color_frame1, textvariable=self.fill_color, width=10).pack(side=tk.LEFT)
        ttk.Button(color_frame1, text="Pick", command=lambda: self.pick_color(self.fill_color)).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(settings_frame, text="Background:").grid(row=4, column=0, sticky=tk.W, pady=2)
        color_frame2 = ttk.Frame(settings_frame)
        color_frame2.grid(row=4, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        ttk.Entry(color_frame2, textvariable=self.back_color, width=10).pack(side=tk.LEFT)
        ttk.Button(color_frame2, text="Pick", command=lambda: self.pick_color(self.back_color)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Action Buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(action_frame, text="Generate QR Code", 
                  command=self.generate_qr).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Save QR Code", 
                  command=self.save_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Open Output Folder", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=5)
        
        # Initialize input fields
        self.update_input_fields()
    
    def setup_preview(self, parent):
        """Setup preview panel."""
        preview_frame = ttk.LabelFrame(parent, text="Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg="white", width=400, height=400)
        self.preview_canvas.pack(expand=True)
        
        # Info text
        self.info_text = tk.Text(preview_frame, height=4, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, pady=(10, 0))
    
    def setup_batch_tab(self):
        """Setup batch generation tab."""
        # Instructions
        ttk.Label(self.batch_frame, text="Batch QR Code Generation", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.batch_frame, 
                 text="Enter one item per line. Format depends on type selected.").pack(pady=5)
        
        # Type selection for batch
        batch_type_frame = ttk.Frame(self.batch_frame)
        batch_type_frame.pack(pady=10)
        
        self.batch_type = tk.StringVar(value="url")
        ttk.Label(batch_type_frame, text="Type:").pack(side=tk.LEFT)
        batch_combo = ttk.Combobox(batch_type_frame, textvariable=self.batch_type,
                                  values=["url", "text", "email", "phone"], 
                                  state="readonly", width=10)
        batch_combo.pack(side=tk.LEFT, padx=5)
        
        # Text area for batch input
        ttk.Label(self.batch_frame, text="Items to generate:").pack(anchor=tk.W, padx=20)
        self.batch_text = scrolledtext.ScrolledText(self.batch_frame, height=15, width=60)
        self.batch_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Batch action buttons
        batch_buttons = ttk.Frame(self.batch_frame)
        batch_buttons.pack(pady=10)
        
        ttk.Button(batch_buttons, text="Generate All", 
                  command=self.generate_batch).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_buttons, text="Clear", 
                  command=lambda: self.batch_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
    
    def setup_about_tab(self):
        """Setup about tab."""
        about_text = """
Production QR Code Generator

This application generates static QR codes that never expire. Unlike dynamic QR codes 
that redirect through third-party services, these QR codes directly contain your data.

Features:
• Static QR codes - no expiration, no external dependencies
• High error correction for production quality
• Multiple data types supported
• Customizable appearance
• Batch generation capability
• High-resolution output suitable for print

Why Static QR Codes?
✓ Never expire
✓ Work offline
✓ No tracking
✓ Full data control
✓ Production ready
✓ No external service dependency

Technical Details:
• Error Correction: Up to 30% damage recovery
• Format: Standard QR codes compatible with all scanners
• Output: High-quality PNG/JPEG files
• Resolution: Scalable vector-based generation

Created with Python, qrcode library, and Tkinter.
        """
        
        about_label = tk.Label(self.about_frame, text=about_text, justify=tk.LEFT, 
                              wraplength=600, font=("Arial", 10))
        about_label.pack(pady=20, padx=20)
    
    def update_input_fields(self):
        """Update input fields based on selected QR type."""
        # Clear existing widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        qr_type = self.qr_type.get()
        
        if qr_type == "url":
            ttk.Label(self.input_frame, text="URL:").grid(row=0, column=0, sticky=tk.W)
            self.url_entry = ttk.Entry(self.input_frame, width=40)
            self.url_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            self.url_entry.insert(0, "https://")
            
        elif qr_type == "text":
            ttk.Label(self.input_frame, text="Text:").grid(row=0, column=0, sticky=tk.NW)
            self.text_entry = tk.Text(self.input_frame, width=40, height=4)
            self.text_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
        elif qr_type == "email":
            ttk.Label(self.input_frame, text="Email:").grid(row=0, column=0, sticky=tk.W)
            self.email_entry = ttk.Entry(self.input_frame, width=40)
            self.email_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Subject:").grid(row=1, column=0, sticky=tk.W)
            self.subject_entry = ttk.Entry(self.input_frame, width=40)
            self.subject_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Body:").grid(row=2, column=0, sticky=tk.NW)
            self.body_entry = tk.Text(self.input_frame, width=40, height=3)
            self.body_entry.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
            
        elif qr_type == "phone":
            ttk.Label(self.input_frame, text="Phone:").grid(row=0, column=0, sticky=tk.W)
            self.phone_entry = ttk.Entry(self.input_frame, width=40)
            self.phone_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
        elif qr_type == "sms":
            ttk.Label(self.input_frame, text="Phone:").grid(row=0, column=0, sticky=tk.W)
            self.sms_phone_entry = ttk.Entry(self.input_frame, width=40)
            self.sms_phone_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Message:").grid(row=1, column=0, sticky=tk.NW)
            self.sms_message_entry = tk.Text(self.input_frame, width=40, height=3)
            self.sms_message_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
            
        elif qr_type == "wifi":
            ttk.Label(self.input_frame, text="Network Name:").grid(row=0, column=0, sticky=tk.W)
            self.wifi_ssid_entry = ttk.Entry(self.input_frame, width=40)
            self.wifi_ssid_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
            self.wifi_password_entry = ttk.Entry(self.input_frame, width=40, show="*")
            self.wifi_password_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Security:").grid(row=2, column=0, sticky=tk.W)
            self.wifi_security = tk.StringVar(value="WPA")
            security_combo = ttk.Combobox(self.input_frame, textvariable=self.wifi_security,
                                        values=["WPA", "WEP", "nopass"], state="readonly", width=37)
            security_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
            
        elif qr_type == "vcard":
            ttk.Label(self.input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
            self.vcard_name_entry = ttk.Entry(self.input_frame, width=40)
            self.vcard_name_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
            self.vcard_phone_entry = ttk.Entry(self.input_frame, width=40)
            self.vcard_phone_entry.grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Email:").grid(row=2, column=0, sticky=tk.W)
            self.vcard_email_entry = ttk.Entry(self.input_frame, width=40)
            self.vcard_email_entry.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
            
            ttk.Label(self.input_frame, text="Organization:").grid(row=3, column=0, sticky=tk.W)
            self.vcard_org_entry = ttk.Entry(self.input_frame, width=40)
            self.vcard_org_entry.grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
    
    def update_error_correction(self):
        """Update error correction level."""
        combo_value = self.error_correction.get()
        self.error_correction.set(combo_value[0])  # Extract just the letter
    
    def pick_color(self, color_var):
        """Open color picker dialog."""
        try:
            from tkinter import colorchooser
            color = colorchooser.askcolor(title="Choose color")
            if color[1]:  # If user didn't cancel
                color_var.set(color[1])
        except ImportError:
            messagebox.showinfo("Info", "Color picker not available. Enter color name or hex code manually.")
    
    def generate_qr(self):
        """Generate QR code based on current settings."""
        try:
            # Get data based on type
            data = self.get_qr_data()
            if not data:
                messagebox.showerror("Error", "Please enter the required data.")
                return
            
            # Generate QR code
            qr = self.qr_gen.generate_qr_code(
                data,
                error_correction=self.error_correction.get(),
                box_size=self.box_size.get(),
                border=self.border.get()
            )
            
            # Create image
            img = self.qr_gen.create_qr_image(qr, self.fill_color.get(), self.back_color.get())
            
            # Store for saving later
            self.current_qr_image = img
            
            # Display preview
            self.display_preview(img)
            
            # Show info
            info = self.qr_gen.get_qr_info(data)
            info_text = f"""QR Code Information:
Version: {info['version']}
Error Correction: {self.error_correction.get()} level
Data Length: {info['data_length']} characters
Matrix Size: {info['box_count']}x{info['box_count']}
Estimated Size: {info['estimated_size_px']}x{info['estimated_size_px']} pixels

This is a STATIC QR code that will never expire!"""
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def get_qr_data(self):
        """Get QR data based on selected type."""
        qr_type = self.qr_type.get()
        
        try:
            if qr_type == "url":
                return self.url_entry.get().strip()
            elif qr_type == "text":
                return self.text_entry.get(1.0, tk.END).strip()
            elif qr_type == "email":
                email = self.email_entry.get().strip()
                subject = self.subject_entry.get().strip()
                body = self.body_entry.get(1.0, tk.END).strip()
                
                if not email:
                    return ""
                
                mailto_data = f"mailto:{email}"
                params = []
                if subject:
                    params.append(f"subject={subject}")
                if body:
                    params.append(f"body={body}")
                
                if params:
                    mailto_data += "?" + "&".join(params)
                
                return mailto_data
            elif qr_type == "phone":
                phone = self.phone_entry.get().strip()
                return f"tel:{phone}" if phone else ""
            elif qr_type == "sms":
                phone = self.sms_phone_entry.get().strip()
                message = self.sms_message_entry.get(1.0, tk.END).strip()
                
                if not phone:
                    return ""
                
                sms_data = f"sms:{phone}"
                if message:
                    sms_data += f"?body={message}"
                
                return sms_data
            elif qr_type == "wifi":
                ssid = self.wifi_ssid_entry.get().strip()
                password = self.wifi_password_entry.get().strip()
                security = self.wifi_security.get()
                
                if not ssid:
                    return ""
                
                return f"WIFI:T:{security};S:{ssid};P:{password};H:false;;"
            elif qr_type == "vcard":
                name = self.vcard_name_entry.get().strip()
                phone = self.vcard_phone_entry.get().strip()
                email = self.vcard_email_entry.get().strip()
                org = self.vcard_org_entry.get().strip()
                
                if not name:
                    return ""
                
                vcard_data = "BEGIN:VCARD\n"
                vcard_data += "VERSION:3.0\n"
                vcard_data += f"FN:{name}\n"
                if phone:
                    vcard_data += f"TEL:{phone}\n"
                if email:
                    vcard_data += f"EMAIL:{email}\n"
                if org:
                    vcard_data += f"ORG:{org}\n"
                vcard_data += "END:VCARD"
                
                return vcard_data
        except Exception:
            return ""
        
        return ""
    
    def display_preview(self, img):
        """Display QR code in preview canvas."""
        # Resize image to fit canvas
        canvas_size = 350
        img_size = img.size[0]
        
        if img_size > canvas_size:
            ratio = canvas_size / img_size
            new_size = (int(img_size * ratio), int(img_size * ratio))
            img = img.resize(new_size, Image.Resampling.NEAREST)
        
        # Convert to PhotoImage
        self.preview_image = ImageTk.PhotoImage(img)
        
        # Clear canvas and display image
        self.preview_canvas.delete("all")
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:  # Canvas is properly initialized
            x = canvas_width // 2
            y = canvas_height // 2
            self.preview_canvas.create_image(x, y, image=self.preview_image)
    
    def save_qr(self):
        """Save the current QR code."""
        if not self.current_qr_image:
            messagebox.showerror("Error", "Please generate a QR code first.")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    # Convert to RGB for JPEG
                    if self.current_qr_image.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', self.current_qr_image.size, 'white')
                        if self.current_qr_image.mode == 'P':
                            self.current_qr_image = self.current_qr_image.convert('RGBA')
                        background.paste(self.current_qr_image, 
                                       mask=self.current_qr_image.split()[-1] if self.current_qr_image.mode == 'RGBA' else None)
                        self.current_qr_image = background
                    self.current_qr_image.save(filename, 'JPEG', quality=95, optimize=True)
                else:
                    self.current_qr_image.save(filename, 'PNG', optimize=True)
                
                self.current_file_path = filename
                messagebox.showinfo("Success", f"QR code saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
    
    def generate_batch(self):
        """Generate batch QR codes."""
        batch_data = self.batch_text.get(1.0, tk.END).strip()
        if not batch_data:
            messagebox.showerror("Error", "Please enter items to generate.")
            return
        
        items = [line.strip() for line in batch_data.split('\n') if line.strip()]
        batch_type = self.batch_type.get()
        
        try:
            generated_files = []
            for i, item in enumerate(items):
                if batch_type == "url":
                    filepath = self.qr_gen.create_url_qr(item)
                elif batch_type == "text":
                    filepath = self.qr_gen.create_text_qr(item)
                elif batch_type == "email":
                    filepath = self.qr_gen.create_email_qr(item)
                elif batch_type == "phone":
                    filepath = self.qr_gen.create_phone_qr(item)
                
                generated_files.append(filepath)
            
            messagebox.showinfo("Success", 
                              f"Generated {len(generated_files)} QR codes in the 'output' folder.")
            self.open_output_folder()
            
        except Exception as e:
            messagebox.showerror("Error", f"Batch generation failed: {str(e)}")
    
    def open_output_folder(self):
        """Open the output folder."""
        output_dir = os.path.abspath("output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{output_dir}"' if sys.platform == 'darwin' else f'xdg-open "{output_dir}"')
        except Exception:
            messagebox.showinfo("Output Folder", f"Output folder location:\n{output_dir}")


def main():
    root = tk.Tk()
    app = QRGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()