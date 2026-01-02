"""
PRISM - Image Format Converter
A modern image conversion tool with batch processing support
"""

import customtkinter as ctk
from ui.app import PrismApp


def main():
    """Application entry point"""
    # Configure CustomTkinter
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create and run application
    app = PrismApp()
    app.mainloop()


if __name__ == "__main__":
    main()
