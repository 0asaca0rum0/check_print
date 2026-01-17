"""
Custom PyQt6 widgets for the Check Printer application.
"""
from PyQt6.QtCore import Qt, QRectF, QDate
from PyQt6.QtGui import QPainter, QFont, QColor, QPixmap
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import CardWidget
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from src.models import CheckTemplate
from src.renderers import CheckRenderer

# Constants
CHECK_WIDTH_MM = 175
CHECK_HEIGHT_MM = 80


class CheckPreviewWidget(CardWidget):
    """Widget for previewing check with draggable text elements."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {
            "amount": 0,
            "words": "",
            "beneficiary": "",
            "location": "",
            "date": QDate.currentDate()
        }
        self.background_image = None
        self.check_type = None
        self.setMinimumHeight(300)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
        
        # Draggable positions
        self.draggable_positions = CheckTemplate.DEFAULT_POSITIONS.copy()
        self.dragging = None
        self.drag_offset = (0, 0)
        self.setMouseTracking(True)

    def update_data(self, data, background_image=None, check_type=None):
        """Update preview data."""
        self.data = data
        if background_image is not None:
            self.background_image = background_image
            print(f"[IMAGE SIZE] {self.background_image.width()} x {self.background_image.height()}")
        if check_type is not None:
            self.check_type = check_type
            self.draggable_positions = CheckTemplate.get_positions(check_type).copy()
        self.update()
    
    def get_target_rect(self) -> QRectF:
        """Calculate the rectangle for drawing the check."""
        available_w = self.width()
        aspect_ratio = CHECK_HEIGHT_MM / CHECK_WIDTH_MM
        draw_h = available_w * aspect_ratio
        offset_y = (self.height() - draw_h) / 2
        return QRectF(10, offset_y, available_w - 20, draw_h)
    
    def get_element_at(self, pos):
        """Find which text element is at the given position."""
        rect = self.get_target_rect()
        for name, pct in self.draggable_positions.items():
            x = rect.x() + rect.width() * pct[0]
            y = rect.y() + rect.height() * pct[1]
            
            # Create larger hit boxes
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
        """Handle mouse press for dragging."""
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
        """Handle mouse move for dragging."""
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
            # Change cursor when hovering
            element = self.get_element_at(event.pos())
            if element:
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            pos = self.draggable_positions[self.dragging]
            print(f"[POSITION] {self.dragging}: ({pos[0]:.3f}, {pos[1]:.3f})")
            print(f"[ALL POSITIONS for {self.check_type}]:")
            for name, p in self.draggable_positions.items():
                print(f"    self.pos_{name} = ({p[0]:.3f}, {p[1]:.3f})")
            self.dragging = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """Paint the preview widget."""
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
        
        # Draw text elements
        painter.setPen(Qt.GlobalColor.black)
        font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
        font_text = QFont("Courier New", 11)
        font_date = QFont("Courier New", 9)
        
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
        
        # Draw Date
        painter.setFont(font_date)
        x, y = get_pos("date")
        date_str = self.data['date'].toString("dd/MM/yyyy")
        painter.drawText(int(x), int(y), f"le {date_str}")
        
        # Draw drag handles
        if self.dragging:
            painter.setBrush(QColor(0, 120, 215, 100))
            painter.setPen(QColor(0, 120, 215))
            for name, pct in self.draggable_positions.items():
                x = rect.x() + rect.width() * pct[0]
                y = rect.y() + rect.height() * pct[1]
                if name == self.dragging:
                    painter.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)
