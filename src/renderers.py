"""
Check rendering logic for preview and printing.
"""
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QFont, QColor
from src.models import CheckTemplate


class CheckRenderer:
    """Renders check data onto a painter surface."""
    
    def __init__(self, data, background_image=None, check_type=None):
        self.data = data
        self.background_image = background_image
        self.check_type = check_type
        
        # Fonts
        self.font_amount_num = QFont("Arial", 10, QFont.Weight.Bold)
        self.font_text = QFont("Courier New", 11)
        self.font_date = QFont("Courier New", 6)
        
        # Get positions for this check type
        positions = CheckTemplate.get_positions(check_type)
        self.pos_amount_num = positions["amount_num"]
        self.pos_amount_words = positions["amount_words"]
        self.pos_beneficiary = positions["beneficiary"]
        self.pos_location = positions["location"]
        self.pos_date = positions["date"]

    def draw(self, painter: QPainter, rect: QRectF, draw_background=False):
        """Draw the check on the painter."""
        painter.save()
        
        if draw_background:
            self._draw_background(painter, rect)
        
        painter.setPen(Qt.GlobalColor.black)
        self._draw_text_elements(painter, rect)
        
        painter.restore()

    def _draw_background(self, painter: QPainter, rect: QRectF):
        """Draw the background image or fallback."""
        if self.background_image and not self.background_image.isNull():
            painter.drawPixmap(rect.toRect(), self.background_image)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(240, 248, 255))
            painter.drawRect(rect)
            painter.setPen(QColor(200, 200, 200))
            painter.drawRect(QRectF(
                rect.x() + rect.width() * 0.75, rect.y() + rect.height() * 0.02,
                rect.width() * 0.22, rect.height() * 0.12
            ))
            painter.drawLine(
                int(rect.x() + rect.width() * 0.1), int(rect.y() + rect.height() * 0.35),
                int(rect.x() + rect.width() * 0.9), int(rect.y() + rect.height() * 0.35)
            )

    def _draw_text_elements(self, painter: QPainter, rect: QRectF):
        """Draw all text elements on the check."""
        def get_pos(pct_tuple):
            return (rect.x() + rect.width() * pct_tuple[0],
                    rect.y() + rect.height() * pct_tuple[1])

        # Draw Numeric Amount
        painter.setFont(self.font_amount_num)
        x, y = get_pos(self.pos_amount_num)
        amount_str = f"{self.data['amount']:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
        painter.drawText(int(x), int(y + 20), amount_str)

        # Draw Words
        painter.setFont(self.font_text)
        x, y = get_pos(self.pos_amount_words)
        painter.drawText(int(x), int(y), self.data['words'])

        # Draw Beneficiary
        x, y = get_pos(self.pos_beneficiary)
        painter.drawText(int(x), int(y), self.data['beneficiary'])

        # Draw Location
        x, y = get_pos(self.pos_location)
        painter.drawText(int(x), int(y), self.data['location'])

        # Draw Date
        painter.setFont(self.font_date)
        x, y = get_pos(self.pos_date)
        date_str = self.data['date'].toString("dd/MM/yyyy")
        painter.drawText(int(x), int(y), f"le {date_str}")
