# Check Printer Application

A professional PyQt6 application for printing checks with support for multiple check templates (BDR, BNA, CCP). Features a modern Fluent Design UI and works on both Linux and Windows.

## Features

- 🎨 Modern Fluent Design UI using qfluentwidgets
- 📋 Support for multiple check templates (BDR, BNA, CCP)
- 💰 Automatic amount-to-words conversion (French)
- 🖨️ Print functionality with preview
- 🎯 Draggable text elements for position adjustment
- 🔄 Cross-platform support (Linux & Windows)
- 📦 Modular architecture with separated concerns

## Project Structure

```
check-printer/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── run_linux.sh           # Linux startup script
├── run_windows.bat        # Windows startup script
├── README.md              # This file
├── src/
│   ├── __init__.py        # Package initialization
│   ├── app.py             # Main application window
│   ├── models.py          # Data models and templates
│   ├── renderers.py       # Check rendering logic
│   ├── utils.py           # Utility functions
│   └── widgets.py         # Custom PyQt6 widgets
├── bdr_1.jpg              # BDR check template
├── bna_1.jpg              # BNA check template
└── chèque-ccp.png         # CCP check template
```

## Requirements

- Python 3.8 or higher
- PyQt6 6.7.1+
- qfluentwidgets 0.4.0+
- num2words 0.5.14+

## Installation

### Linux

1. **Clone or download the project**
   ```bash
   cd check-printer
   ```

2. **Make the startup script executable**
   ```bash
   chmod +x run_linux.sh
   ```

3. **Run the application**
   ```bash
   ./run_linux.sh
   ```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Launch the application

### Windows

1. **Download the project**
   - Extract the ZIP file to your desired location

2. **Run the startup script**
   - Double-click `run_windows.bat`

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Launch the application

### Manual Installation (Both Platforms)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

1. **Select a Check Template**
   - Choose from: None, BDR, BNA, or CCP
   - The preview will update with the selected template

2. **Enter Check Information**
   - **Amount (DA)**: Enter the check amount in Dinars
   - **Beneficiary**: Enter the recipient's name
   - **Location**: Enter the location (default: Alger)
   - **Date**: Select the check date

3. **Preview**
   - The right panel shows a live preview of the check
   - You can drag text elements to adjust their positions
   - Positions are logged to the console for reference

4. **Print**
   - Click the "Imprimer (Print)" button
   - Select your printer and print settings
   - Click "Print" to send to printer

## Architecture

### Modular Design

The application is split into logical modules:

- **`models.py`**: Data structures and template configurations
- **`renderers.py`**: Check rendering logic for both preview and printing
- **`widgets.py`**: Custom PyQt6 widgets (CheckPreviewWidget)
- **`utils.py`**: Utility functions (path resolution, amount conversion, platform detection)
- **`app.py`**: Main application window and business logic

### Key Classes

#### `CheckData`
Data structure for check information.

#### `CheckTemplate`
Configuration for check templates including positions and file paths.

#### `CheckRenderer`
Renders check data onto a QPainter surface.

#### `CheckPreviewWidget`
Custom widget for previewing checks with draggable elements.

#### `CheckPrinterApp`
Main application window with UI controls.

## Configuration

### Check Templates

Templates are defined in `src/models.py` under `CheckTemplate.POSITIONS`. Each template has specific positions for:
- Amount (numeric)
- Amount (words)
- Beneficiary
- Location
- Date

Positions are specified as percentages (0.0 to 1.0) of the check dimensions.

### Fonts

Fonts are configured in `src/renderers.py`:
- Amount (numeric): Arial, 10pt, Bold
- Text: Courier New, 11pt
- Date: Courier New, 6pt

## Troubleshooting

### Python not found
- **Linux**: Install Python 3 using your package manager
  ```bash
  sudo apt-get install python3 python3-venv
  ```
- **Windows**: Download from https://www.python.org/ and ensure "Add Python to PATH" is checked

### Virtual environment issues
- Delete the `venv` folder and run the startup script again
- Ensure you have write permissions in the project directory

### Missing dependencies
- Run: `pip install -r requirements.txt`
- Ensure your internet connection is active

### Image not loading
- Verify that check template images (bdr_1.jpg, bna_1.jpg, chèque-ccp.png) are in the project root
- Check file permissions

### Print dialog not appearing
- Ensure you have at least one printer configured on your system
- On Linux, you may need to install CUPS: `sudo apt-get install cups`

## Development

### Adding a New Check Template

1. Add the template image to the project root
2. Update `CheckTemplate.TEMPLATES` in `src/models.py`
3. Add positions to `CheckTemplate.POSITIONS`
4. Update the combo box in `src/app.py`

### Modifying Positions

Positions can be adjusted by:
1. Running the application
2. Dragging text elements in the preview
3. Checking the console output for position values
4. Updating `CheckTemplate.POSITIONS` with new values

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check:
1. The troubleshooting section above
2. Console output for error messages
3. Ensure all dependencies are correctly installed

## Version

- **Version**: 1.0.0
- **Last Updated**: 2026-01-16
- **Python**: 3.8+
- **PyQt6**: 6.7.1+

## Credits

- Built with PyQt6 and qfluentwidgets
- Uses num2words for amount conversion
- Supports French language localization
