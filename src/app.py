"""
Main application window for the Check Printer.
"""
import os
import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QTransform, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    SubtitleLabel, LineEdit, DoubleSpinBox, CalendarPicker,
    PrimaryPushButton, StrongBodyLabel, BodyLabel, InfoBar, InfoBarPosition, ComboBox
)

from src.models import CheckTemplate, CheckData
from src.renderers import CheckRenderer
from src.widgets import CheckPreviewWidget
from src.utils import get_resource_path, amount_to_words
from src.print_dialog import CheckPrintDialog


class CheckPrinterApp(QWidget):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Check Printer (French Demo)")
        self.resize(900, 600)
        
        # Apply white background
        self.setStyleSheet("background-color: white;")
        
        # Check templates
        self.check_templates = CheckTemplate.TEMPLATES
        self.current_background = None
        self.current_check_type = None

        # Main Layout
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

        # Amount
        self.lbl_amount = BodyLabel("Montant (DA):")
        self.spin_amount = DoubleSpinBox()
        self.spin_amount.setRange(0, 999999999)
        self.spin_amount.setValue(11800.00)
        self.spin_amount.valueChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_amount)
        self.v_layout.addWidget(self.spin_amount)

        # Beneficiary
        self.lbl_ben = BodyLabel("À l'ordre de (Beneficiary):")
        self.txt_ben = LineEdit()
        self.txt_ben.setPlaceholderText("ex: Mohammed Benali")
        self.txt_ben.textChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_ben)
        self.v_layout.addWidget(self.txt_ben)

        # Location
        self.lbl_loc = BodyLabel("Fait à (Location):")
        self.txt_loc = LineEdit()
        self.txt_loc.setText("Alger")
        self.txt_loc.textChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_loc)
        self.v_layout.addWidget(self.txt_loc)

        # Date
        self.lbl_date = BodyLabel("Le (Date):")
        self.date_picker = CalendarPicker()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.dateChanged.connect(self.update_preview)
        self.v_layout.addWidget(self.lbl_date)
        self.v_layout.addWidget(self.date_picker)

        self.v_layout.addStretch(1)

        # Print Button
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

    def get_amount_in_words(self, amount: float) -> str:
        """Convert amount to words."""
        return amount_to_words(amount, language='fr')

    def get_current_data(self) -> dict:
        """Get current check data."""
        return {
            "amount": self.spin_amount.value(),
            "words": self.get_amount_in_words(self.spin_amount.value()),
            "beneficiary": self.txt_ben.text(),
            "location": self.txt_loc.text(),
            "date": self.date_picker.date
        }

    def on_template_changed(self, template_name: str):
        """Load the selected check template image."""
        if template_name == "Aucun (None)":
            self.current_background = None
            self.current_check_type = None
        elif template_name in self.check_templates:
            image_path = get_resource_path(self.check_templates[template_name])
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
        """Update the preview widget."""
        data = self.get_current_data()
        self.preview_widget.update_data(data, self.current_background, self.current_check_type)

    def print_check(self):
        """Print the check."""
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        
        # Use custom print dialog
        dialog = CheckPrintDialog(printer, self)
        
        if dialog.exec():
            try:
                painter = QPainter(printer)
                if not painter.isActive():
                    raise Exception("Failed to initialize painter")
                
                rect = printer.pageRect(QPrinter.Unit.Millimeter)
                
                renderer = CheckRenderer(
                    self.get_current_data(),
                    self.current_background,
                    self.current_check_type
                )
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
            except Exception as e:
                InfoBar.error(
                    title='Erreur d\'impression',
                    content=f"Erreur lors de l'impression: {str(e)}",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = CheckPrinterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
