# Rectangular Mosaic Desktop

<p align="center">
  <strong>English | <a href="./README_zh-CN.md">简体中文</a></strong>
</p>

<div align="center">
  <img src="assets/icon.png" alt="Rectangular Mosaic Desktop" width="128" height="128">
  <h3>Rectangular Mosaic Desktop</h3>
  <a href="https://apps.apple.com/us/app/rectangular-mosaic-desktop/id6754189038" target="_blank">
    <img src="https://developer.apple.com/app-store/marketing/guidelines/images/badge-download-on-the-mac-app-store.svg" alt="Download on the Mac App Store">
  </a>
</div>

## Project Overview

This project is a PySide6-based image mosaic tool that supports rectangular area selection via mouse drag and one-click mosaic processing, perfect for quickly handling sensitive information in images.

## Key Features
- Support for image upload and display
- Mouse drag rectangular area selection
- One-click mosaic processing for selected areas
- Image saving functionality
- Clean and intuitive interface

## Installation and Running

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the main program

```bash
python main.py
```

## Building Executable

### Interactive Build (Recommended)

Use the interactive build script:

```bash
python build.py
```

This will guide you through:
- Target architecture selection
- Build mode (onedir/onefile) selection  
- Platform-specific packaging options

### Direct PyInstaller Command

For onedir build (generates folder with multiple files):

```bash
pyinstaller --onedir --name "RectangularMosaic" --add-data "assets;assets" --icon="assets/icon.ico" --noconsole main.py
```

For onefile build (generates single executable):

```bash
pyinstaller --onefile --name "RectangularMosaic" --add-data "assets;assets" --icon="assets/icon.ico" --noconsole main.py
```

The built executable will be in the `dist/` directory.

## Directory Structure

```
/src
  /features
    mosaic_tool.py      # Main interface and feature entry
    image_mosaic.py     # Mosaic processing logic
    image_loader.py     # Image loading and saving
  /utils
    rect_selector.py    # Selection tool
  /constants
    config.py           # Configuration constants
main.py                # Startup entry point
requirements.txt       # Dependencies file
.gitignore             # Git ignore file
README.md              # Project documentation
```

## Usage Instructions

1. After starting the program, click "Upload Image" to select a local image.
2. Drag the mouse on the image to select the area that needs mosaic processing.
3. Click the "Area Mosaic" button to apply mosaic processing to the selected area.
4. To save the processed image, click the "Save Image" button.

## Development Standards
- High cohesion and low coupling, modular design for easy maintenance and extension
- Detailed Chinese comments for each module, function, and class
- Clear directory structure for easy navigation and management

## Environment Requirements
- Python 3.7 or higher
- PySide6 6.5.0 or higher

## Contributing and Feedback
For suggestions or issues, please submit an issue or PR.

- **Join our QQ group for discussion:** [SK Open Source Discussion Group](https://qm.qq.com/q/fGavz3UxCo)
- **Join our Discord server:** [SK Open Source Community](https://discord.gg/thWGWq7CwA)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sihuangtech/rectangular-mosaic-desktop&type=Date)](https://www.star-history.com/#sihuangtech/rectangular-mosaic-desktop&Date)