# Backdrop-Off - Bulk Background Remover

A simple and powerful desktop application for removing backgrounds from images with custom background color options.

![Backdrop-Off](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- 🖼️ **Batch Processing**: Process multiple images at once
- 🎨 **Custom Background Colors**: Choose any background color using color picker or hex codes
- 📊 **Progress Tracking**: Real-time progress bar and image counter
- 📁 **Flexible Input**: Browse folders or manually enter paths
- 🚀 **Cross-Platform**: Works on Windows, macOS, and Linux
- 📂 **Quick Access**: Open output folder directly after processing
- 🎯 **User-Friendly**: Clean and intuitive interface

## Screenshots

<img width="702" height="531" alt="image" src="https://github.com/user-attachments/assets/aba179f2-6e31-406f-8bc7-cf330fae9712" />

## Demo

https://github.com/user-attachments/assets/47d54819-3c48-4fb4-8563-4742f9989991




## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Method 1: Install from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akhilsahuji/backdrop-off.git
   cd backdrop-off
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python bg_remover_ui.py
   ```

### Method 2: Download Executable

Pre-built executables for Windows, macOS, and Linux will be available in the [Releases](https://github.com/akhilsahuji/backdrop-off/releases) section.

## Usage

1. **Select Input Folder**: Choose the folder containing your images or type the path manually
2. **Select Output Folder**: Choose where to save processed images or type the path manually
3. **Choose Background Color**: 
   - Use the color picker button, or
   - Enter a hex color code (e.g., #FF0000 for red)
4. **Start Processing**: Click "Start Processing" and watch the progress
5. **View Results**: Click "Open Output Folder" when processing is complete

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)

### Popular Background Colors
- White: `#FFFFFF`
- Black: `#000000`
- Red: `#FF0000`
- Green: `#00FF00`
- Blue: `#0000FF`
- Transparent backgrounds are converted to your chosen solid color

## Development

### Setting up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akhilsahuji/backdrop-off.git
   cd backdrop-off
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Building Executables

To create standalone executables for distribution:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed bg_remover_ui.py
```

The executable will be created in the `dist/` folder.

## Dependencies

- **customtkinter**: Modern UI framework
- **rembg**: AI-powered background removal
- **Pillow (PIL)**: Image processing
- **onnxruntime**: AI model runtime

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Drag & drop support
- [ ] Batch rename options
- [ ] Custom output formats (PNG with transparency)
- [ ] Image quality settings

## Troubleshooting

### Common Issues

**"No module named 'customtkinter'"**
```bash
pip install customtkinter
```

**"No module named 'rembg'"**
```bash
pip install rembg
```

**Performance Issues**
- Processing time depends on image size and quantity
- Ensure sufficient RAM (4GB+ recommended)
- Close other heavy applications during processing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [rembg](https://github.com/danielgatis/rembg) - For the amazing background removal AI
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - For the modern UI framework

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/akhilsahuji/backdrop-off/issues) page
2. Create a new issue with detailed description
3. Include your OS, Python version, and error messages

---

⭐ **If you find this project helpful, please give it a star!** ⭐
