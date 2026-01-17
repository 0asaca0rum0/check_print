# Print Dialog Guide - Custom Print Configuration

## Overview

The Check Printer application now includes a custom, user-friendly print dialog that provides better control over printer settings and a cleaner interface.

## Print Dialog Features

### 1. **Printer Selection**
- Automatically detects available printers on your system
- Dropdown menu to select your desired printer
- Shows all connected and configured printers

### 2. **Paper Size Options**
- **A4** (210mm × 297mm) - Default, recommended for checks
- **Letter** (8.5" × 11") - Standard US paper size
- **A5** (148mm × 210mm) - Smaller format option

### 3. **Orientation Settings**
- **Portrait** - Default, check prints vertically
- **Landscape** - Check prints horizontally
- Choose based on your check template layout

### 4. **Margin Configuration**
- Adjustable margins in millimeters
- Default: 10mm on all sides
- Range: 0-50mm
- Ensures proper spacing around the check

### 5. **Copy Count**
- Print multiple copies in one job
- Range: 1-100 copies
- Useful for batch printing

## How to Use the Print Dialog

### Step-by-Step

1. **Fill in Check Information**
   - Enter amount, beneficiary, location, and date
   - Select check template (BDR, BNA, or CCP)
   - Review preview on the right

2. **Click "Imprimer (Print)" Button**
   - The custom print dialog opens
   - Shows all available printers

3. **Configure Print Settings**
   - Select your printer from the dropdown
   - Choose paper size (usually A4)
   - Select orientation (usually Portrait)
   - Adjust margins if needed (default 10mm is fine)
   - Set number of copies

4. **Click "Imprimer" to Print**
   - Dialog closes
   - Check is sent to printer
   - Success message appears

5. **Or Click "Annuler" to Cancel**
   - Closes dialog without printing
   - Returns to main application

## Print Dialog Code Structure

### Location
[`src/print_dialog.py`](src/print_dialog.py)

### Main Class
```python
class CheckPrintDialog(QDialog):
    """Custom print dialog for check printing."""
```

### Key Methods

#### `__init__(printer, parent)`
Initializes the dialog with default printer settings:
- Page size: A4
- Orientation: Portrait
- Margins: 10mm on all sides

#### `init_ui()`
Creates the user interface with:
- Printer selection dropdown
- Paper size selector
- Orientation selector
- Margin spinner
- Copy count spinner
- Print and Cancel buttons

#### `get_printer()`
Applies user selections to the printer object:
- Sets paper size based on selection
- Sets orientation
- Applies margins
- Sets copy count

#### `_get_available_printers()`
Detects available printers on the system:
- Uses QPrinterInfo to find printers
- Returns list of printer names
- Falls back to "Default Printer" if none found

## Integration with Main Application

### In [`src/app.py`](src/app.py)

```python
from src.print_dialog import CheckPrintDialog

def print_check(self):
    """Print the check."""
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    
    # Use custom print dialog
    dialog = CheckPrintDialog(printer, self)
    
    if dialog.exec():
        # Printer is configured, proceed with printing
        painter = QPainter(printer)
        # ... render check ...
```

## Printer Configuration Details

### Default Settings

| Setting | Value | Range |
|---------|-------|-------|
| Paper Size | A4 | A4, Letter, A5 |
| Orientation | Portrait | Portrait, Landscape |
| Margins | 10mm | 0-50mm |
| Copies | 1 | 1-100 |
| Resolution | HighResolution | - |

### Recommended Settings for Checks

| Setting | Recommended | Reason |
|---------|-------------|--------|
| Paper Size | A4 | Standard size, plenty of space |
| Orientation | Portrait | Most check templates are vertical |
| Margins | 10-15mm | Ensures proper spacing |
| Copies | 1 | Print one at a time for quality control |

## Troubleshooting Print Dialog Issues

### Dialog Doesn't Appear

**Problem**: Print dialog doesn't open when clicking Print button

**Solutions**:
1. Check that printer is connected and online
2. Verify printer drivers are installed
3. Restart the application
4. Check system printer settings

### Printer Not Listed

**Problem**: Your printer doesn't appear in the dropdown

**Solutions**:
1. Ensure printer is connected
2. Install printer drivers
3. Add printer in system settings:
   - **Linux**: CUPS (http://localhost:631)
   - **Windows**: Settings → Devices → Printers
4. Restart application

### Wrong Paper Size Selected

**Problem**: Paper size doesn't match your printer

**Solutions**:
1. Check printer's paper tray
2. Select correct paper size in dialog
3. Verify printer supports selected size
4. Load correct paper before printing

### Margins Too Large/Small

**Problem**: Check position is off on printed page

**Solutions**:
1. Adjust margin value in dialog
2. Print test page to verify
3. Increase margins if text is cut off
4. Decrease margins if too much white space

## Advanced Configuration

### Modifying Default Margins

Edit [`src/print_dialog.py`](src/print_dialog.py):

```python
# In init_ui() method
self.margins_spin = QSpinBox()
self.margins_spin.setRange(0, 50)
self.margins_spin.setValue(10)  # Change this value
```

### Adding More Paper Sizes

Edit [`src/print_dialog.py`](src/print_dialog.py):

```python
# In init_ui() method
self.paper_combo.addItems(["A4", "Letter", "A5", "A3", "B4"])

# In get_printer() method
paper_sizes = {
    "A4": QPrinter.PageSize.A4,
    "Letter": QPrinter.PageSize.Letter,
    "A5": QPrinter.PageSize.A5,
    "A3": QPrinter.PageSize.A3,
    "B4": QPrinter.PageSize.B4
}
```

### Changing Default Orientation

Edit [`src/print_dialog.py`](src/print_dialog.py):

```python
# In init_ui() method
self.orientation_combo.setCurrentText("Landscape")  # Change default
```

## Print Dialog UI Layout

```
┌─────────────────────────────────────────┐
│  Imprimer le Chèque                     │
├─────────────────────────────────────────┤
│                                         │
│  Configuration d'impression             │
│                                         │
│  Imprimante:        [Dropdown ▼]       │
│  Format de papier:  [A4 ▼]             │
│  Orientation:       [Portrait ▼]       │
│  Marges (mm):       [10]                │
│  Nombre de copies:  [1]                 │
│                                         │
│                                         │
│                    [Imprimer] [Annuler] │
└─────────────────────────────────────────┘
```

## Fluent Design Integration

The print dialog uses qfluentwidgets components:
- **PrimaryPushButton**: "Imprimer" button (blue, primary action)
- **SecondaryPushButton**: "Annuler" button (secondary action)
- **BodyLabel**: Labels for settings
- **QComboBox**: Dropdown selectors
- **QSpinBox**: Numeric input fields

This ensures consistent Fluent Design styling throughout the application.

## Error Handling

The print dialog includes error handling for:
- Missing printer drivers
- Unavailable printers
- Invalid printer configuration
- Printer communication failures

Errors are displayed in the main application using InfoBar notifications.

## Performance Notes

- Dialog loads instantly
- Printer detection is cached
- No blocking operations
- Responsive UI during printing

## Summary

The custom print dialog provides:
✅ Clean, intuitive interface
✅ Full printer configuration control
✅ Fluent Design styling
✅ Error handling
✅ Cross-platform compatibility
✅ Easy customization

---

**For more information**, see:
- [`PRINTING_GUIDE.md`](PRINTING_GUIDE.md) - Detailed printing guide
- [`src/print_dialog.py`](src/print_dialog.py) - Source code
- [`src/app.py`](src/app.py) - Integration code
- [`README.md`](README.md) - Full documentation
