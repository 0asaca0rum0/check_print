# Check Printing Guide - Positioning & Configuration

## Overview

This guide explains how to properly position text on checks and configure your printer for accurate printing using the Check Printer application.

## Understanding the Coordinate System

### How Positions Work in the Application

The application uses a **percentage-based coordinate system** (0.0 to 1.0) for text positioning:

```
(0.0, 0.0) ─────────────────────────────── (1.0, 0.0)
   │                                           │
   │                                           │
   │         Check Area (175mm × 80mm)        │
   │                                           │
   │                                           │
(0.0, 1.0) ─────────────────────────────── (1.0, 1.0)
```

**Example:**
- `(0.5, 0.5)` = Center of the check
- `(0.0, 0.0)` = Top-left corner
- `(1.0, 1.0)` = Bottom-right corner
- `(0.820, 0.009)` = Near top-right (amount position for BDR)

### Why Percentages?

Percentages ensure that text positions scale correctly regardless of:
- Check size variations
- Printer resolution
- Screen DPI
- Preview widget size

## Check Template Positions

### BDR Check Template

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Amount (words)                                 │
│  (0.289, 0.264)                                │
│                                                 │
│                                                 │
│  Beneficiary                                    │
│  (0.246, 0.416)                                │
│                                                 │
│  Location              Date                     │
│  (0.623, 0.508)        (0.750, 0.516)         │
│                                                 │
│                                    Amount (num) │
│                                    (0.820, 0.009)
│                                                 │
└─────────────────────────────────────────────────┘
```

**BDR Positions in src/models.py:**
```python
"BDR": {
    "amount_num": (0.820, 0.009),      # Top-right: numeric amount
    "amount_words": (0.289, 0.264),    # Upper-left: amount in words
    "beneficiary": (0.246, 0.416),     # Middle-left: recipient name
    "location": (0.623, 0.508),        # Lower-right: location
    "date": (0.750, 0.516)             # Lower-right: date
}
```

### BNA Check Template

```
┌─────────────────────────────────────────────────┐
│                                                 │
│                                    Amount (num) │
│                                    (0.831, 0.044)
│                                                 │
│  Amount (words)                                 │
│  (0.044, 0.375)                                │
│                                                 │
│  Beneficiary                                    │
│  (0.263, 0.440)                                │
│                                                 │
│  Location              Date                     │
│  (0.580, 0.567)        (0.771, 0.567)         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**BNA Positions in src/models.py:**
```python
"BNA": {
    "amount_num": (0.831, 0.044),      # Top-right: numeric amount
    "amount_words": (0.044, 0.375),    # Left-middle: amount in words
    "beneficiary": (0.263, 0.440),     # Left-middle: recipient name
    "location": (0.580, 0.567),        # Bottom-right: location
    "date": (0.771, 0.567)             # Bottom-right: date
}
```

### CCP Check Template

```
┌─────────────────────────────────────────────────┐
│                                                 │
│                                    Amount (num) │
│                                    (0.804, 0.028)
│                                                 │
│  Amount (words)                                 │
│  (0.272, 0.244)                                │
│                                                 │
│  Beneficiary                                    │
│  (0.180, 0.424)                                │
│                                                 │
│  Location              Date                     │
│  (0.639, 0.472)        (0.765, 0.480)         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**CCP Positions in src/models.py:**
```python
"CCP": {
    "amount_num": (0.804, 0.028),      # Top-right: numeric amount
    "amount_words": (0.272, 0.244),    # Upper-left: amount in words
    "beneficiary": (0.180, 0.424),     # Middle-left: recipient name
    "location": (0.639, 0.472),        # Lower-right: location
    "date": (0.765, 0.480)             # Lower-right: date
}
```

## Adjusting Positions in the Application

### Step-by-Step Position Adjustment

1. **Launch the application**
   ```bash
   ./run_linux.sh  # Linux
   # or
   run_windows.bat  # Windows
   ```

2. **Select a check template**
   - Choose "BDR", "BNA", or "CCP" from the dropdown

3. **View the preview**
   - The right panel shows the check preview
   - Text elements are displayed with their current positions

4. **Drag text elements**
   - Click and drag any text element in the preview
   - The cursor changes to indicate draggable elements:
     - 🖐️ Open hand = hovering over element
     - ✊ Closed hand = dragging element

5. **Check console output**
   - When you release the mouse, the console shows:
   ```
   [POSITION] amount_num: (0.820, 0.009)
   [ALL POSITIONS for BDR]:
       self.pos_amount_num = (0.820, 0.009)
       self.pos_amount_words = (0.289, 0.264)
       self.pos_beneficiary = (0.246, 0.416)
       self.pos_location = (0.623, 0.508)
       self.pos_date = (0.750, 0.516)
   ```

6. **Update the code**
   - Copy the new positions from console
   - Update src/models.py in the CheckTemplate.POSITIONS dictionary

## Printer Configuration

### Understanding Print Settings

When you click "Imprimer (Print)", a print dialog appears with these key settings:

#### 1. **Printer Selection**
- Choose your physical printer
- Ensure it's connected and online
- Test print if available

#### 2. **Paper Size**
- **Recommended**: A4 (210mm × 297mm)
- Check templates are 175mm × 80mm
- Plenty of space for positioning

#### 3. **Orientation**
- **Portrait** (default): Check prints vertically
- **Landscape**: Check prints horizontally
- Choose based on your check template

#### 4. **Margins**
- **Top Margin**: 10-20mm (space before check)
- **Left Margin**: 10-20mm (space from left edge)
- **Right Margin**: 10-20mm (space from right edge)
- **Bottom Margin**: 10-20mm (space after check)

### Printer Configuration Code

The printing logic is in src/app.py:

```python
def print_check(self):
    """Print the check."""
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    dialog = QPrintDialog(printer, self)
    
    if dialog.exec():
        painter = QPainter(printer)
        rect = printer.pageRect(QPrinter.Unit.DevicePixel)
        renderer = CheckRenderer(
            self.get_current_data(),
            self.current_background,
            self.current_check_type
        )
        renderer.draw(painter, rect, draw_background=True)
        painter.end()
```

**Key Components:**
- `QPrinter.PrinterMode.HighResolution` = Best quality printing
- `QPrintDialog` = User-friendly printer selection
- `painter.pageRect()` = Gets the printable area
- `renderer.draw()` = Renders the check on the printer

### Advanced Printer Settings

#### Linux (CUPS)

1. **Open CUPS Web Interface**
   ```
   http://localhost:631
   ```

2. **Configure Printer**
   - Go to "Administration" → "Manage Printers"
   - Select your printer
   - Set default paper size to A4
   - Configure margins

3. **Test Print**
   ```bash
   lp -d printer_name test_file.txt
   ```

#### Windows

1. **Open Printer Settings**
   - Settings → Devices → Printers & scanners
   - Select your printer
   - Click "Manage"

2. **Configure Defaults**
   - Click "Printing preferences"
   - Set paper size to A4
   - Set orientation (Portrait/Landscape)
   - Configure margins

3. **Test Print**
   - Right-click printer → "Printer properties"
   - Click "Print test page"

## Physical Check Positioning

### Aligning Checks in the Printer

#### For Single Check Printing

1. **Measure the check**
   - Width: 175mm
   - Height: 80mm

2. **Position on paper**
   - Place check on A4 paper (210mm × 297mm)
   - Leave 10-20mm margins on all sides
   - Align with top-left corner for consistency

3. **Mark reference points**
   - Use a ruler to mark where the check should be
   - This helps with consistent positioning

#### For Multiple Checks

1. **Create a template**
   - Print a test page with grid lines
   - Mark check positions
   - Use as a guide for manual placement

2. **Batch printing**
   - Print multiple checks in sequence
   - Stack them in the printer tray
   - Ensure consistent orientation

### Printer Tray Setup

1. **Load paper**
   - Use A4 paper (standard 80gsm)
   - Ensure paper is not wrinkled
   - Fill tray completely for consistent feeding

2. **Adjust guides**
   - Align paper guides to paper width
   - Ensure paper sits flat

3. **Test feed**
   - Print a test page first
   - Check for paper jams or misfeeds

## Troubleshooting Print Issues

### Text Appears in Wrong Position

**Problem**: Text is offset from expected position

**Solutions**:
1. Verify positions in src/models.py
2. Check printer margins in print dialog
3. Test with different paper size
4. Adjust positions using the preview drag feature

### Text is Too Small or Too Large

**Problem**: Text size doesn't match expectations

**Solutions**:
1. Check font sizes in src/renderers.py:
   ```python
   self.font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
   self.font_text = QFont("Courier New", 11)
   self.font_date = QFont("Courier New", 6)
   ```
2. Adjust font sizes as needed
3. Test print to verify

### Image Background Not Printing

**Problem**: Check template image doesn't appear

**Solutions**:
1. Verify image file exists in project root
2. Check file permissions
3. Ensure image format is supported (JPG, PNG)
4. Test with "Aucun (None)" template first

### Printer Not Responding

**Problem**: Print dialog appears but nothing prints

**Solutions**:
1. Check printer is online and connected
2. Verify printer drivers are installed
3. Clear print queue:
   - **Linux**: `lpstat -o` then `cancel job_id`
   - **Windows**: Settings → Devices → Printers → Clear queue
4. Restart printer

## Best Practices

### For Accurate Printing

1. **Always test first**
   - Print a test page before production
   - Verify text alignment
   - Check image quality

2. **Use consistent paper**
   - Same paper type for all checks
   - Same paper size (A4)
   - Same paper quality

3. **Maintain printer**
   - Clean printer regularly
   - Replace ink/toner as needed
   - Update printer drivers

4. **Document your settings**
   - Save printer configuration
   - Document position adjustments
   - Keep test prints for reference

### For Production Printing

1. **Batch processing**
   - Print multiple checks in one session
   - Reduces setup time
   - Ensures consistency

2. **Quality control**
   - Inspect first check from each batch
   - Verify text alignment
   - Check image quality

3. **Storage**
   - Store printed checks in secure location
   - Keep in original order
   - Protect from damage

## Code Reference

### Rendering Logic (src/renderers.py)

```python
def draw(self, painter: QPainter, rect: QRectF, draw_background=False):
    """Draw the check on the painter."""
    painter.save()
    
    if draw_background:
        self._draw_background(painter, rect)
    
    painter.setPen(Qt.GlobalColor.black)
    self._draw_text_elements(painter, rect)
    
    painter.restore()
```

### Position Calculation

```python
def get_pos(pct_tuple):
    """Convert percentage position to pixel position."""
    return (rect.x() + rect.width() * pct_tuple[0],
            rect.y() + rect.height() * pct_tuple[1])
```

### Font Configuration

```python
# In CheckRenderer.__init__()
self.font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
self.font_text = QFont("Courier New", 11)
self.font_date = QFont("Courier New", 6)
```

## Summary

| Aspect | Details |
|--------|---------|
| **Coordinate System** | Percentage-based (0.0 to 1.0) |
| **Check Size** | 175mm × 80mm |
| **Paper Size** | A4 (210mm × 297mm) |
| **Margins** | 10-20mm on all sides |
| **Resolution** | HighResolution mode |
| **Adjustment Method** | Drag in preview, copy from console |
| **Configuration File** | src/models.py |

---

**For more information**, see:
- README.md - Full documentation
- SETUP_GUIDE.md - Setup instructions
- src/models.py - Position definitions
- src/renderers.py - Rendering logic
- src/app.py - Print implementation
