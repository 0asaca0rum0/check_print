import sys
import os
from PyQt6.QtCore import Qt, QDate, QRectF
from PyQt6.QtGui import QPainter, QFont, QColor, QPixmap, QTransform
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect

# Added InfoBarPosition to imports
from qfluentwidgets import (SubtitleLabel, LineEdit, DoubleSpinBox, 
                            CalendarPicker, PrimaryPushButton, StrongBodyLabel, 
                            CardWidget, BodyLabel, InfoBar, InfoBarPosition, ComboBox)
from num2words import num2words

# --- CONSTANTS FOR LAYOUT ---
CHECK_WIDTH_MM = 175
CHECK_HEIGHT_MM = 80

class CheckRenderer:
    def __init__(self, data, background_image=None, check_type=None):
        self.data = data
        self.background_image = background_image
        self.check_type = check_type
        self.font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
        self.font_text = QFont("Courier New", 11)
        self.font_date = QFont("Courier New", 6)  # Smaller font for date
        
        # Different position sets for different check types
        # Coordinates (X, Y) in Percentages (0.0 to 1.0)
        if check_type == "BDR":
            self.pos_amount_num = (0.820, 0.009)
            self.pos_amount_words = (0.289, 0.264)
            self.pos_beneficiary =  (0.246, 0.416)
            self.pos_location = (0.623, 0.508)
            self.pos_date = (0.750, 0.516)
        elif check_type == "BNA":
            self.pos_amount_num = (0.831, 0.044)
            self.pos_amount_words = (0.044, 0.375)
            self.pos_beneficiary = (0.263, 0.440)
            self.pos_location = (0.580, 0.567)
            self.pos_date = (0.771, 0.567)
        elif check_type == "CCP":
            self.pos_amount_num = (0.804, 0.028)
            self.pos_amount_words = (0.272, 0.244)
            self.pos_beneficiary = (0.180, 0.424)
            self.pos_location = (0.639, 0.472)
            self.pos_date = (0.765, 0.480)
        else:
            # Default positions
            self.pos_amount_num = (0.78, 0.05)
            self.pos_amount_words = (0.25, 0.28)
            self.pos_beneficiary = (0.20, 0.50)
            self.pos_location = (0.15, 0.65)
            self.pos_date = (0.50, 0.65)

    def draw(self, painter: QPainter, rect: QRectF, draw_background=False):
        painter.save()
        
        if draw_background:
            # Draw background image if available
            if self.background_image and not self.background_image.isNull():
                painter.drawPixmap(rect.toRect(), self.background_image)
            else:
                # Fallback to simple background
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(240, 248, 255))
                painter.drawRect(rect)
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(QRectF(
                    rect.x() + rect.width()*0.75, rect.y() + rect.height()*0.02, 
                    rect.width()*0.22, rect.height()*0.12
                ))
                painter.drawLine(
                    int(rect.x() + rect.width()*0.1), int(rect.y() + rect.height()*0.35),
                    int(rect.x() + rect.width()*0.9), int(rect.y() + rect.height()*0.35)
                )

        painter.setPen(Qt.GlobalColor.black)
        
        def get_pos(pct_tuple):
            return (rect.x() + rect.width() * pct_tuple[0], 
                    rect.y() + rect.height() * pct_tuple[1])

        # Draw Numeric Amount
        painter.setFont(self.font_amount_num)
        x, y = get_pos(self.pos_amount_num)
        amount_str = f"{self.data['amount']:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
        painter.drawText(int(x), int(y + 20), amount_str)  # Removed # symbols

        # Draw Words
        painter.setFont(self.font_text)
        x, y = get_pos(self.pos_amount_words)
        painter.drawText(int(x), int(y), self.data['words'])

        # Draw Beneficiary
        x, y = get_pos(self.pos_beneficiary)
        painter.drawText(int(x), int(y), f"{self.data['beneficiary']}")

        # Draw Location
        x, y = get_pos(self.pos_location)
        painter.drawText(int(x), int(y), self.data['location'])
        
        # Draw Date (with smaller font)
        painter.setFont(self.font_date)
        x, y = get_pos(self.pos_date)
        date_str = self.data['date'].toString("dd/MM/yyyy")
        painter.drawText(int(x), int(y), f"le {date_str}")

        painter.restore()

class CheckPreviewWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {"amount": 0, "words": "", "beneficiary": "", "location": "", "date": QDate.currentDate()}
        self.background_image = None
        self.check_type = None
        self.setMinimumHeight(300)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
        
        # Draggable positions (in percentages 0.0-1.0)
        self.draggable_positions = {
            "amount_num": (0.820, 0.009),
            "amount_words": (0.289, 0.264),
            "beneficiary": (0.120, 0.480),
            "location": (0.623, 0.508),
            "date": (0.750, 0.516)
        }
        self.dragging = None
        self.drag_offset = (0, 0)
        self.setMouseTracking(True)

    def update_data(self, data, background_image=None, check_type=None):
        self.data = data
        if background_image is not None:
            self.background_image = background_image
            # Log image size
            print(f"[IMAGE SIZE] {self.background_image.width()} x {self.background_image.height()}")
        if check_type is not None:
            self.check_type = check_type
            # Update default positions based on check type
            if check_type == "BDR":
                self.draggable_positions = {
                    "amount_num": (0.820, 0.009),
                    "amount_words": (0.289, 0.264),
                    "beneficiary":  (0.246, 0.416),
                    "location": (0.623, 0.508),
                    "date": (0.750, 0.516)
                }
            elif check_type == "BNA":
                self.draggable_positions = {
                    "amount_num": (0.831, 0.044),
                    "amount_words":(0.044, 0.375),
                    "beneficiary": (0.263, 0.440),
                    "location": (0.580, 0.567),
                    "date": (0.771, 0.567)
                }
            elif check_type == "CCP":
                self.draggable_positions = {
                    "amount_num": (0.804, 0.028),
                    "amount_words": (0.272, 0.244),
                    "beneficiary": (0.180, 0.424),
                    "location": (0.639, 0.472),
                    "date": (0.765, 0.480)
                }
        self.update()
    
    def get_target_rect(self):
        available_w = self.width()
        aspect_ratio = CHECK_HEIGHT_MM / CHECK_WIDTH_MM
        draw_h = available_w * aspect_ratio
        offset_y = (self.height() - draw_h) / 2
        return QRectF(10, offset_y, available_w - 20, draw_h)
    
    def get_element_at(self, pos):
        """Find which text element is at the given position"""
        rect = self.get_target_rect()
        for name, pct in self.draggable_positions.items():
            x = rect.x() + rect.width() * pct[0]
            y = rect.y() + rect.height() * pct[1]
            # Create larger hit boxes - amount_words needs a bigger one
            if name == "amount_words":
                hit_rect = QRectF(x - 20, y - 20, 350, 40)
            elif name == "amount_num":
                hit_rect = QRectF(x - 20, y - 10, 150, 50)
            else:
                hit_rect = QRectF(x - 20, y - 20, 200, 40)
            if hit_rect.contains(pos.x(), pos.y()):
                return name
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            element = self.get_element_at(event.pos())
            if element:
                self.dragging = element
                rect = self.get_target_rect()
                pct = self.draggable_positions[element]
                x = rect.x() + rect.width() * pct[0]
                y = rect.y() + rect.height() * pct[1]
                self.drag_offset = (event.pos().x() - x, event.pos().y() - y)
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            rect = self.get_target_rect()
            new_x = (event.pos().x() - self.drag_offset[0] - rect.x()) / rect.width()
            new_y = (event.pos().y() - self.drag_offset[1] - rect.y()) / rect.height()
            # Clamp values
            new_x = max(0.0, min(1.0, new_x))
            new_y = max(0.0, min(1.0, new_y))
            self.draggable_positions[self.dragging] = (new_x, new_y)
            self.update()
        else:
            # Change cursor when hovering over draggable elements
            element = self.get_element_at(event.pos())
            if element:
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            # Log the final position
            pos = self.draggable_positions[self.dragging]
            print(f"[POSITION] {self.dragging}: ({pos[0]:.3f}, {pos[1]:.3f})")
            print(f"[ALL POSITIONS for {self.check_type}]:")
            for name, p in self.draggable_positions.items():
                print(f"    self.pos_{name} = ({p[0]:.3f}, {p[1]:.3f})")
            self.dragging = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.get_target_rect()
        
        # Draw background
        if self.background_image and not self.background_image.isNull():
            painter.drawPixmap(rect.toRect(), self.background_image)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(240, 248, 255))
            painter.drawRect(rect)
        
        # Draw text elements using draggable positions
        painter.setPen(Qt.GlobalColor.black)
        font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
        font_text = QFont("Courier New", 11)
        
        def get_pos(name):
            pct = self.draggable_positions[name]
            return (rect.x() + rect.width() * pct[0], 
                    rect.y() + rect.height() * pct[1])
        
        # Draw Numeric Amount
        painter.setFont(font_amount_num)
        x, y = get_pos("amount_num")
        amount_str = f"{self.data['amount']:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
        painter.drawText(int(x), int(y + 20), amount_str)
        
        # Draw Words
        painter.setFont(font_text)
        x, y = get_pos("amount_words")
        painter.drawText(int(x), int(y), self.data['words'])
        
        # Draw Beneficiary
        x, y = get_pos("beneficiary")
        painter.drawText(int(x), int(y), self.data['beneficiary'])
        
        # Draw Location
        x, y = get_pos("location")
        painter.drawText(int(x), int(y), self.data['location'])
        
        # Draw Date (with smaller font)
        font_date = QFont("Courier New", 9)
        painter.setFont(font_date)
        x, y = get_pos("date")
        date_str = self.data['date'].toString("dd/MM/yyyy")
        painter.drawText(int(x), int(y), f"le {date_str}")
        
        # Draw drag handles (small circles) for visual feedback
        if self.dragging:
            painter.setBrush(QColor(0, 120, 215, 100))
            painter.setPen(QColor(0, 120, 215))
            for name, pct in self.draggable_positions.items():
                x = rect.x() + rect.width() * pct[0]
                y = rect.y() + rect.height() * pct[1]
                if name == self.dragging:
                    painter.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)

# --- CHANGED CLASS INHERITANCE HERE ---
class CheckPrinterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Check Printer (French Demo)")
        self.resize(900, 600)
        
        # Apply a white background for better contrast with Fluent widgets
        self.setStyleSheet("background-color: white;")
        
        # Check templates
        self.check_templates = {
            "BDR": "bdr_1.jpg",
            "BNA": "bna_1.jpg",
            "CCP": "chèque-ccp.png"
        }
        self.current_background = None
        self.current_check_type = None

        # Main Layout (Directly on self)
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(20, 20, 20, 20)

        # --- LEFT PANEL: CONTROLS ---
        self.panel_controls = QWidget()
        self.v_layout = QVBoxLayout(self.panel_controls)
        self.v_layout.setSpacing(15)
        
        self.v_layout.addWidget(SubtitleLabel("Informations du Chèque"))
        
        # Check Template Selector
        self.lbl_template = BodyLabel("Modèle de chèque (Check Template):")
        self.combo_template = ComboBox()
        self.combo_template.addItems(["Aucun (None)", "BDR", "BNA", "CCP"])
        self.combo_template.currentTextChanged.connect(self.on_template_changed)
        self.v_layout.addWidget(self.lbl_template)
        self.v_layout.addWidget(self.combo_template)

        self.lbl_amount = BodyLabel("Montant (DA):")
        self.spin_amount = DoubleSpinBox()
        self.spin_amount.setRange(0, 999999999)
        self.spin_amount.setValue(11800.00)
        self.spin_amount.valueChanged.connect(self.update_preview)
        
        self.v_layout.addWidget(self.lbl_amount)
        self.v_layout.addWidget(self.spin_amount)

        self.lbl_ben = BodyLabel("À l'ordre de (Beneficiary):")
        self.txt_ben = LineEdit()
        self.txt_ben.setPlaceholderText("ex: Mohammed Benali")
        self.txt_ben.textChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_ben)
        self.v_layout.addWidget(self.txt_ben)

        self.lbl_loc = BodyLabel("Fait à (Location):")
        self.txt_loc = LineEdit()
        self.txt_loc.setText("Alger")
        self.txt_loc.textChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_loc)
        self.v_layout.addWidget(self.txt_loc)

        self.lbl_date = BodyLabel("Le (Date):")
        self.date_picker = CalendarPicker()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.dateChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_date)
        self.v_layout.addWidget(self.date_picker)

        self.v_layout.addStretch(1)

        self.btn_print = PrimaryPushButton("Imprimer (Print)")
        self.btn_print.clicked.connect(self.print_check)
        self.v_layout.addWidget(self.btn_print)

        # --- RIGHT PANEL: PREVIEW ---
        self.panel_preview = QWidget()
        self.prev_layout = QVBoxLayout(self.panel_preview)
        self.prev_layout.addWidget(StrongBodyLabel("Aperçu (Preview)"))
        
        self.preview_widget = CheckPreviewWidget()
        self.prev_layout.addWidget(self.preview_widget)
        self.prev_layout.addStretch(1)

        self.h_layout.addWidget(self.panel_controls, 1)
        self.h_layout.addWidget(self.panel_preview, 2)

        self.update_preview()

    def get_amount_in_words(self, amount):
        try:
            words = num2words(amount, lang='fr')
            return f"{words} Dinars".capitalize()
        except Exception:
            return "Erreur de conversion"

    def get_current_data(self):
        return {
            "amount": self.spin_amount.value(),
            "words": self.get_amount_in_words(self.spin_amount.value()),
            "beneficiary": self.txt_ben.text(),
            "location": self.txt_loc.text(),
            "date": self.date_picker.date
        }

    def on_template_changed(self, template_name):
        """Load the selected check template image"""
        if template_name == "Aucun (None)":
            self.current_background = None
            self.current_check_type = None
        elif template_name in self.check_templates:
            image_path = os.path.join(os.path.dirname(__file__), self.check_templates[template_name])
            if os.path.exists(image_path):
                self.current_background = QPixmap(image_path)
                if self.current_background.isNull():
                    InfoBar.error(
                        title='Erreur',
                        content=f"Impossible de charger l'image: {template_name}",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3000,
                        parent=self
                    )
                    self.current_background = None
                    self.current_check_type = None
                else:
                    # Rotate BDR image 90 degrees counterclockwise
                    if template_name == "BDR":
                        transform = QTransform().rotate(-90)
                        self.current_background = self.current_background.transformed(transform)
                    self.current_check_type = template_name
            else:
                InfoBar.warning(
                    title='Attention',
                    content=f"Fichier non trouvé: {self.check_templates[template_name]}",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                self.current_background = None
                self.current_check_type = None
        self.update_preview()

    def update_preview(self):
        data = self.get_current_data()
        self.preview_widget.update_data(data, self.current_background, self.current_check_type)

    def print_check(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec():
            painter = QPainter(printer)
            rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            renderer = CheckRenderer(self.get_current_data(), self.current_background, self.current_check_type)
            # Print with background if available
            renderer.draw(painter, rect, draw_background=True)
            painter.end()
            
            InfoBar.success(
                title='Succès',
                content="L'impression a été envoyée.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckPrinterApp()
    window.show()
    sys.exit(app.exec())