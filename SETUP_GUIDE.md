# Check Printer Application - Setup Guide

## Quick Start

### Linux
```bash
chmod +x run_linux.sh
./run_linux.sh
```

### Windows
```bash
run_windows.bat
```

## Project Structure

The application has been refactored into a modular architecture:

```
check-printer/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                    # Configuration
├── run_linux.sh           # Linux startup script
├── run_windows.bat        # Windows startup script
├── README.md              # Full documentation
├── SETUP_GUIDE.md         # This file
├── src/
│   ├── __init__.py        # Package initialization
│   ├── app.py             # Main application window (CheckPrinterApp)
│   ├── models.py          # Data models (CheckData, CheckTemplate)
│   ├── renderers.py       # Rendering logic (CheckRenderer)
│   ├── utils.py           # Utility functions
│   └── widgets.py         # Custom widgets (CheckPreviewWidget)
├── bdr_1.jpg              # BDR check template
├── bna_1.jpg              # BNA check template
└── chèque-ccp.png         # CCP check template
```

## Module Descriptions

### [`src/models.py`](src/models.py)
- **CheckData**: Dataclass for check information
- **CheckTemplate**: Configuration for check templates with positions

### [`src/renderers.py`](src/renderers.py)
- **CheckRenderer**: Renders check data onto QPainter surfaces
- Used for both preview and printing

### [`src/widgets.py`](src/widgets.py)
- **CheckPreviewWidget**: Custom PyQt6 widget with draggable elements
- Supports live preview with position adjustment

### [`src/utils.py`](src/utils.py)
- `get_resource_path()`: Cross-platform resource path resolution
- `amount_to_words()`: Convert amounts to French words
- `format_amount_display()`: Format amounts for display
- Platform detection functions

### [`src/app.py`](src/app.py)
- **CheckPrinterApp**: Main application window
- Handles UI controls and business logic
- Manages template loading and printing

## Features

✅ **Modular Architecture** - Clean separation of concerns
✅ **PyQt6 Fluent Design** - Modern UI with qfluentwidgets
✅ **Cross-Platform** - Works on Linux and Windows
✅ **Multiple Templates** - Support for BDR, BNA, CCP checks
✅ **Draggable Elements** - Adjust text positions in preview
✅ **French Localization** - Amount-to-words conversion
✅ **Print Support** - Direct printer integration
✅ **Automatic Setup** - Virtual environment creation

## Dependencies

- **PyQt6** 6.7.1+ - GUI framework
- **qfluentwidgets** 0.4.0+ - Fluent Design components
- **num2words** 0.5.14+ - Number to words conversion
- **darkdetect** 0.8.0+ - System theme detection

## Startup Scripts

### Linux (`run_linux.sh`)
- Creates virtual environment if needed
- Installs dependencies
- Activates venv and runs application
- Handles errors gracefully

### Windows (`run_windows.bat`)
- Creates virtual environment if needed
- Installs dependencies
- Activates venv and runs application
- Provides user-friendly error messages

## Configuration

Edit `.env` file to customize:
- Application name and version
- Default values (amount, location)
- UI settings (window size, theme)
- Logging configuration

## Troubleshooting

### Import Errors
- Ensure all files are in the correct locations
- Check that `src/__init__.py` exists
- Verify Python path includes project root

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Virtual Environment Issues
- Delete `venv` folder
- Run startup script again

### Image Loading Issues
- Verify check template images exist in project root
- Check file permissions
- Ensure correct file names in `CheckTemplate.TEMPLATES`

## Development

### Adding New Check Templates

1. Add image file to project root
2. Update `CheckTemplate.TEMPLATES` in [`src/models.py`](src/models.py)
3. Add positions to `CheckTemplate.POSITIONS`
4. Update combo box in [`src/app.py`](src/app.py)

### Modifying Text Positions

1. Run application
2. Drag text elements in preview
3. Check console for position values
4. Update `CheckTemplate.POSITIONS` with new values

### Extending Functionality

The modular design makes it easy to:
- Add new check types
- Modify rendering logic
- Extend UI components
- Add new utility functions

## Performance Notes

- Lazy loading of images
- Efficient rendering with QPainter
- Minimal memory footprint
- Fast startup time

## License

This project is provided as-is for educational and commercial use.

## Support

For issues:
1. Check README.md for detailed documentation
2. Review console output for error messages
3. Verify all dependencies are installed
4. Ensure check template images are present

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-16  
**Python**: 3.8+  
**PyQt6**: 6.7.1+
