# 🌈 PRISM - Image Format Converter

A modern, sleek image format converter built with Python and CustomTkinter. Convert your images between multiple formats with ease and style.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎨 **Modern Dark UI** - Beautiful, professional interface with a dark theme
- 🔄 **Multiple Formats** - Support for PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF, ICO, PDF, HEIC
- 📦 **Batch Processing** - Convert multiple files at once
- 🎯 **Individual Format Selection** - Set different formats for different files
- 📊 **Multi-Select** - Select multiple files with Shift+Click for batch operations
- 💾 **Smart Destination** - Auto-sets destination to source folder, or choose your own
- 🔧 **Advanced Options** - Preserve metadata, adjust compression
- ⚡ **Fast & Efficient** - Multi-threaded conversion for better performance
- 📱 **HEIC Support** - Convert iPhone photos directly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prism-converter.git
cd prism-converter
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## 📖 Usage

1. **Add Files** - Click the "+  Add Files" button to select images
2. **Set Format** - Choose output format from the BATCH FORMAT dropdown
3. **Select Individual Files** (Optional):
   - Click on a file to select it
   - Hold Shift and click to select a range
   - Change format for selected files only
4. **Choose Destination** (Optional) - Click "..." to change the save location
5. **Configure Options**:
   - Toggle "Preserve Metadata" to keep EXIF data
   - Toggle "Max Compression" for smaller file sizes
6. **Convert** - Click "Convert All  →" to start conversion

## 🎯 Keyboard Shortcuts

- **Shift + Click** - Select a range of files
- **Click on file** - Select individual file

## 🛠️ Project Structure

```
Prism/
├── main.py              # Application entry point
├── ui/
│   ├── app.py          # Main application window
│   ├── file_row.py     # File list item widget
│   └── colors.py       # Color scheme
├── core/
│   └── converter.py    # Image conversion logic
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎨 Supported Formats

### Input Formats
- PNG
- JPG/JPEG
- WEBP
- HEIC (iPhone photos)
- TIFF
- BMP
- GIF
- ICO
- PSD

### Output Formats
- PNG
- JPG/JPEG
- WEBP
- GIF
- BMP
- TIFF
- ICO
- PDF
- HEIC

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Image processing by [Pillow](https://python-pillow.org/)
- HEIC support via [pillow-heif](https://github.com/bigcat88/pillow_heif)

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/prism-converter](https://github.com/yourusername/prism-converter)

## 🐛 Known Issues

If you encounter any issues, please report them on the [Issues](https://github.com/yourusername/prism-converter/issues) page.

## 🔮 Future Features

- [ ] Drag & drop support
- [ ] Image resize/crop options
- [ ] Watermark addition
- [ ] Batch rename functionality
- [ ] Format presets (e.g., "Web Optimized", "Print Quality")
- [ ] Dark/Light theme toggle
- [ ] Multi-language support

---

Made with ❤️ using Python
