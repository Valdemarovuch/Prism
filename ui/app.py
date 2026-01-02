"""Main application window"""

import os
import threading
import customtkinter as ctk
from tkinter import filedialog

from .colors import COLORS
from .file_row import FileRow
from core.converter import ImageConverter


class PrismApp(ctk.CTk):
    """Main application class"""
    
    def __init__(self):
        super().__init__()

        self.title("Prism")
        self.geometry("950x650")
        self.configure(fg_color=COLORS["bg_body"])
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Data storage
        self.files = []
        self.file_rows = []
        self.selected_rows = []
        self.last_selected_index = None
        self.file_formats = {}

        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        self._create_header()
        self._create_toolbar()
        self._create_file_list()
        self._create_footer()

    def _create_header(self):
        """Create header with title"""
        self.header = ctk.CTkFrame(
            self, height=50, 
            fg_color=COLORS["bg_body"], 
            corner_radius=0
        )
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.header, text="PRISM", 
            font=("Segoe UI", 16, "bold"), 
            text_color=COLORS["text_main"]
        )
        title.grid(row=0, column=0, pady=12)

        # Separator
        ctk.CTkFrame(
            self, height=1, 
            fg_color=COLORS["border"]
        ).grid(row=0, column=0, sticky="ews")

    def _create_toolbar(self):
        """Create toolbar with buttons"""
        self.toolbar = ctk.CTkFrame(
            self, height=60, 
            fg_color="#121214", 
            corner_radius=0
        )
        self.toolbar.grid(row=1, column=0, sticky="ew")

        # Add Files Button
        self.btn_add = ctk.CTkButton(
            self.toolbar, text="+  Add Files",
            fg_color=COLORS["white"], 
            text_color="black", 
            hover_color="#d4d4d8",
            font=("Segoe UI", 12, "bold"), 
            height=32, corner_radius=6,
            command=self.add_files
        )
        self.btn_add.pack(side="left", padx=20, pady=12)

        # File Count
        self.lbl_count = ctk.CTkLabel(
            self.toolbar, text="0 files loaded", 
            font=("Segoe UI", 11), 
            text_color=COLORS["text_dark"]
        )
        self.lbl_count.pack(side="left", padx=10)

        # Clear Button
        self.btn_clear = ctk.CTkButton(
            self.toolbar, text="🗑 Clear All",
            fg_color="transparent", 
            text_color=COLORS["text_dark"], 
            hover_color=COLORS["hover"],
            font=("Segoe UI", 11), 
            width=80, height=32,
            command=self.clear_files
        )
        self.btn_clear.pack(side="right", padx=20)

        # Separator
        ctk.CTkFrame(
            self, height=1, 
            fg_color=COLORS["border"]
        ).grid(row=1, column=0, sticky="ews")

    def _create_file_list(self):
        """Create scrollable file list"""
        # Header
        self.table_header = ctk.CTkFrame(
            self, height=30, 
            fg_color=COLORS["bg_body"], 
            corner_radius=0
        )
        self.table_header.grid(row=2, column=0, sticky="new")
        
        ctk.CTkLabel(
            self.table_header, text="     FILENAME", 
            font=("Segoe UI", 10, "bold"), 
            text_color=COLORS["text_dark"]
        ).pack(side="left", padx=50, pady=5)
        
        # Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", 
            corner_radius=0
        )
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", pady=(30, 0))

    def _create_footer(self):
        """Create footer with settings and actions"""
        self.footer = ctk.CTkFrame(
            self, fg_color="#0f0f11", 
            corner_radius=0, border_width=1, 
            border_color=COLORS["border"]
        )
        self.footer.grid(row=3, column=0, sticky="ew")
        self.footer.grid_columnconfigure(1, weight=1)
        
        self._create_format_selector()
        self._create_destination_selector()
        self._create_toggles()
        self._create_action_bar()

    def _create_format_selector(self):
        """Create format selection controls"""
        f_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        f_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        ctk.CTkLabel(
            f_frame, text="BATCH FORMAT", 
            font=("Segoe UI", 9, "bold"), 
            text_color=COLORS["text_dark"]
        ).pack(anchor="w")
        
        self.combo_fmt = ctk.CTkComboBox(
            f_frame, 
            values=["PNG", "JPG", "JPEG", "WEBP", "GIF", "BMP", "TIFF", "ICO", "PDF", "HEIC"],
            fg_color=COLORS["bg_body"], 
            border_color=COLORS["border"],
            button_color=COLORS["border"], 
            text_color=COLORS["text_main"],
            font=("Segoe UI", 11),
            width=150, height=32, 
            command=self.on_format_changed
        )
        self.combo_fmt.pack(pady=5)
        self.combo_fmt.set("PNG")

    def _create_destination_selector(self):
        """Create destination path selector"""
        p_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        p_frame.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        ctk.CTkLabel(
            p_frame, text="DESTINATION", 
            font=("Segoe UI", 9, "bold"), 
            text_color=COLORS["text_dark"]
        ).pack(anchor="w")
        
        path_box = ctk.CTkFrame(
            p_frame, fg_color=COLORS["bg_body"], 
            border_width=1, border_color=COLORS["border"], 
            corner_radius=6
        )
        path_box.pack(fill="x", pady=5)
        
        self.lbl_dest = ctk.CTkLabel(
            path_box, text="Select files to set destination...",
            text_color=COLORS["text_dim"], 
            font=("Segoe UI", 11), anchor="w"
        )
        self.lbl_dest.pack(side="left", padx=10, pady=6, fill="x", expand=True)
        
        btn_browse = ctk.CTkButton(
            path_box, text="...", width=30, height=20,
            fg_color=COLORS["bg_panel"], 
            hover_color=COLORS["border"],
            command=self.browse_folder
        )
        btn_browse.pack(side="right", padx=5)

    def _create_toggles(self):
        """Create toggle switches"""
        t_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        t_frame.grid(row=0, column=2, padx=20, pady=20)
        
        self.sw_meta = ctk.CTkSwitch(
            t_frame, text="Preserve Metadata",
            font=("Segoe UI", 11), 
            text_color=COLORS["text_dim"],
            progress_color=COLORS["text_dark"], 
            fg_color=COLORS["border"]
        )
        self.sw_meta.pack(pady=2)
        self.sw_meta.select()
        
        self.sw_qual = ctk.CTkSwitch(
            t_frame, text="Max Compression",
            font=("Segoe UI", 11), 
            text_color=COLORS["text_dim"],
            progress_color=COLORS["text_dark"], 
            fg_color=COLORS["border"]
        )
        self.sw_qual.pack(pady=2)

    def _create_action_bar(self):
        """Create action bar with progress and convert button"""
        # Separator
        ctk.CTkFrame(
            self.footer, height=1, 
            fg_color=COLORS["border"]
        ).grid(row=1, column=0, columnspan=3, sticky="ew")

        action_area = ctk.CTkFrame(self.footer, fg_color="transparent")
        action_area.grid(row=2, column=0, columnspan=3, sticky="ew", padx=20, pady=15)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            action_area, height=6,
            progress_color=COLORS["accent_indigo"], 
            fg_color=COLORS["bg_panel"]
        )
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(0, 20))
        self.progress_bar.set(0)

        # Convert button
        self.btn_convert = ctk.CTkButton(
            action_area, text="Convert All  →",
            fg_color=COLORS["white"], 
            text_color="black", 
            hover_color="#d4d4d8",
            font=("Segoe UI", 12, "bold"), 
            height=36, width=140, 
            corner_radius=8,
            command=self.start_conversion_thread
        )
        self.btn_convert.pack(side="right")

    # --- File Management ---

    def add_files(self):
        """Add files to conversion list"""
        filetypes = [("Images", "*.png;*.jpg;*.jpeg;*.webp;*.heic;*.tiff;*.bmp;*.psd;*.gif;*.ico")]
        paths = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        
        if not paths:
            return
        
        default_format = self.combo_fmt.get()
        
        # Set destination to the folder of the first file
        if not self.files:
            first_file_dir = os.path.dirname(paths[0])
            self.lbl_dest.configure(text=first_file_dir)
        
        for path in paths:
            if path not in self.files:
                self.files.append(path)
                self.file_formats[path] = default_format
                
                row = FileRow(
                    self.scroll_frame, path, 
                    len(self.file_rows), 
                    select_callback=self.on_file_selected
                )
                row.update_target(default_format)
                self.file_rows.append(row)
                
        self.lbl_count.configure(text=f"{len(self.files)} files loaded")

    def clear_files(self):
        """Clear all files from list"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.files = []
        self.file_rows = []
        self.selected_rows = []
        self.last_selected_index = None
        self.file_formats = {}
        
        if hasattr(self, 'lbl_dest'):
            self.lbl_dest.configure(text="Select files to set destination...")
        
        self.lbl_count.configure(text="0 files loaded")
        self.progress_bar.set(0)

    def browse_folder(self):
        """Browse for destination folder"""
        folder = filedialog.askdirectory()
        if folder:
            self.lbl_dest.configure(text=folder)

    # --- Selection Management ---

    def on_file_selected(self, row, event=None):
        """Handle file row selection"""
        shift_pressed = event and (event.state & 0x0001)
        
        if shift_pressed and self.last_selected_index is not None:
            # Range selection
            current_index = self.file_rows.index(row)
            start = min(self.last_selected_index, current_index)
            end = max(self.last_selected_index, current_index)
            
            for r in self.selected_rows:
                r.set_selected(False)
            self.selected_rows = []
            
            for i in range(start, end + 1):
                self.file_rows[i].set_selected(True)
                self.selected_rows.append(self.file_rows[i])
        else:
            # Single selection
            for r in self.selected_rows:
                r.set_selected(False)
            self.selected_rows = [row]
            row.set_selected(True)
            self.last_selected_index = self.file_rows.index(row)
        
        # Update format combo
        if len(self.selected_rows) == 1:
            file_format = self.file_formats.get(self.selected_rows[0].filepath, "PNG")
            self.combo_fmt.set(file_format)
        elif len(self.selected_rows) > 1:
            formats = [self.file_formats.get(r.filepath, "PNG") for r in self.selected_rows]
            if len(set(formats)) == 1:
                self.combo_fmt.set(formats[0])
            else:
                self.combo_fmt.set("Mixed")

    def deselect_all(self):
        """Deselect all files"""
        for row in self.selected_rows:
            row.set_selected(False)
        self.selected_rows = []
        self.last_selected_index = None

    def on_format_changed(self, choice):
        """Handle format change"""
        if self.selected_rows:
            # Change format for selected files
            for row in self.selected_rows:
                self.file_formats[row.filepath] = choice
                row.update_target(choice)
            self.deselect_all()
        else:
            # Change format for all files
            for filepath in self.files:
                self.file_formats[filepath] = choice
            for row in self.file_rows:
                row.update_target(choice)

    # --- Conversion ---

    def start_conversion_thread(self):
        """Start batch conversion in background thread"""
        if not self.files:
            return
        
        self.btn_convert.configure(state="disabled")
        threading.Thread(target=self.convert_process, daemon=True).start()

    def convert_process(self):
        """Convert all files"""
        output_dir = self.lbl_dest.cget("text")
        
        if output_dir == "Select files to set destination...":
            print("Please select a destination folder first")
            self.btn_convert.configure(state="normal")
            return
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total = len(self.files)
        
        for i, filepath in enumerate(self.files):
            try:
                row = self.file_rows[i]
                row.set_status("Processing")
                
                target_format = self.file_formats.get(filepath, "png").lower()
                
                ImageConverter.convert_image(
                    filepath, target_format, output_dir,
                    preserve_metadata=self.sw_meta.get(),
                    max_compression=self.sw_qual.get()
                )
                
                row.set_status("Done")
            except Exception as e:
                print(str(e))
                if i < len(self.file_rows):
                    self.file_rows[i].set_status("Error")
            
            prog = (i + 1) / total
            self.progress_bar.set(prog)
        
        self.btn_convert.configure(state="normal")
        print("Batch complete.")
