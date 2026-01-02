"""FileRow widget for displaying individual file information"""

import os
import customtkinter as ctk
from .colors import COLORS


class FileRow(ctk.CTkFrame):
    """Widget for displaying one file row in the list"""
    
    def __init__(self, master, filepath, file_index, select_callback=None):
        super().__init__(master, fg_color="transparent", corner_radius=0, height=50)
        self.pack(fill="x", pady=1)
        self.select_callback = select_callback
        self.is_selected = False
        self.filepath = filepath
        
        filename = os.path.basename(filepath)
        dirname = os.path.dirname(filepath)
        if len(dirname) > 25:
            dirname = "..." + dirname[-25:]
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        ext = filename.split('.')[-1].upper()

        # Grid layout for the row
        self.grid_columnconfigure(1, weight=1)

        # 1. Icon
        self.icon = ctk.CTkLabel(
            self, text="🖼️", width=40, 
            text_color=COLORS["text_dark"]
        )
        self.icon.grid(row=0, column=0, padx=5, pady=10)

        # 2. Filename & Path
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="w", padx=5)
        
        self.lbl_name = ctk.CTkLabel(
            self.info_frame, text=filename, 
            font=("Segoe UI", 13, "bold"), 
            text_color=COLORS["text_main"]
        )
        self.lbl_name.pack(anchor="w")
        
        self.lbl_path = ctk.CTkLabel(
            self.info_frame, text=dirname, 
            font=("Segoe UI", 10), 
            text_color=COLORS["text_dark"]
        )
        self.lbl_path.pack(anchor="w")

        # 3. Size
        self.lbl_size = ctk.CTkLabel(
            self, text=f"{size_mb:.1f} MB", 
            font=("Segoe UI", 11), 
            text_color=COLORS["text_dark"], 
            width=80, anchor="w"
        )
        self.lbl_size.grid(row=0, column=2, padx=5)

        # 4. Conversion Flow (Ext -> Target)
        self.flow_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.flow_frame.grid(row=0, column=3, padx=10)
        
        self.badge_in = ctk.CTkLabel(
            self.flow_frame, text=ext, 
            fg_color=COLORS["bg_panel"], 
            text_color=COLORS["text_dim"], 
            corner_radius=4, padx=6, 
            font=("Segoe UI", 10, "bold")
        )
        self.badge_in.pack(side="left")
        
        ctk.CTkLabel(
            self.flow_frame, text="→", 
            text_color=COLORS["text_dark"], 
            font=("Segoe UI", 14)
        ).pack(side="left", padx=5)
        
        self.badge_out = ctk.CTkLabel(
            self.flow_frame, text="...", 
            fg_color="#312e81", 
            text_color="#818cf8", 
            corner_radius=4, padx=6, 
            font=("Segoe UI", 10, "bold")
        )
        self.badge_out.pack(side="left")

        # 5. Status
        self.lbl_status = ctk.CTkLabel(
            self, text="Pending", 
            font=("Segoe UI", 11), 
            text_color=COLORS["text_dark"], 
            width=80, anchor="e"
        )
        self.lbl_status.grid(row=0, column=4, padx=15)
        
        # Make row clickable
        self.bind("<Button-1>", self.on_click)
        for widget in [self.icon, self.info_frame, self.lbl_name, 
                       self.lbl_path, self.lbl_size, self.flow_frame, 
                       self.badge_in, self.badge_out, self.lbl_status]:
            widget.bind("<Button-1>", self.on_click)
    
    def on_click(self, event=None):
        """Handle click event"""
        if self.select_callback:
            self.select_callback(self, event)
    
    def set_selected(self, selected):
        """Set selection state"""
        self.is_selected = selected
        if selected:
            self.configure(fg_color=COLORS["border"])
        else:
            self.configure(fg_color="transparent")

    def update_target(self, target_fmt):
        """Update target format badge"""
        self.badge_out.configure(text=target_fmt)

    def set_status(self, status):
        """Update status label"""
        if status == "Done":
            self.lbl_status.configure(
                text="Complete ✓", 
                text_color=COLORS["accent_green"]
            )
        elif status == "Processing":
            self.lbl_status.configure(
                text="Converting...", 
                text_color=COLORS["accent_indigo"]
            )
        else:
            self.lbl_status.configure(
                text=status, 
                text_color=COLORS["text_dark"]
            )
