"""
Custom print dialog for better check printing experience.
"""
from PyQt6.QtGui import QPageLayout
from PyQt6.QtCore import Qt,QMarginsF
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSpinBox
from qfluentwidgets import BodyLabel, PrimaryPushButton


class CheckPrintDialog(QDialog):
    """Wrapper around standard print dialog with additional options."""
    
    def __init__(self, printer: QPrinter, parent=None):
        super().__init__(parent)
        self.printer = printer
        self.setWindowTitle("Imprimer le Chèque")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Configure printer defaults
        self.printer.setPageOrientation(QPageLayout.Orientation.Portrait)
        self.printer.setPageMargins(QMarginsF(10, 10, 10, 10), QPageLayout.Unit.Millimeter)
        
        self.init_ui()
        self.result_code = QDialog.DialogCode.Rejected
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = BodyLabel("Configuration d'impression")
        layout.addWidget(title)
        
        # Copies
        copies_layout = QHBoxLayout()
        copies_label = BodyLabel("Nombre de copies:")
        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 100)
        self.copies_spin.setValue(1)
        copies_layout.addWidget(copies_label)
        copies_layout.addWidget(self.copies_spin)
        copies_layout.addStretch()
        layout.addLayout(copies_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.print_button = PrimaryPushButton("Imprimer")
        self.print_button.clicked.connect(self.accept)
        
        self.cancel_button = PrimaryPushButton("Annuler")
        self.cancel_button.setStyleSheet("background-color: #f3f3f3; color: black;")
        self.copies_spin.setStyleSheet("background-color: #f3f3f3; color: black;")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def get_printer(self) -> QPrinter:
        """Get configured printer."""
        # Set copies
        self.printer.setCopyCount(self.copies_spin.value())
        return self.printer
    
    def exec(self) -> int:
        """Execute the dialog."""
        result = super().exec()
        if result == QDialog.DialogCode.Accepted:
            self.get_printer()
            
            # Verify printer is valid
            if not self.printer:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "Erreur d'imprimante",
                    "Aucune imprimante n'a pu être initialisée."
                )
                return QDialog.DialogCode.Rejected
            
            # Set output format explicitly
            self.printer.setOutputFormat(QPrinter.OutputFormat.NativeFormat)
            
            # Show standard print dialog for final printer selection
            print_dialog = QPrintDialog(self.printer, self)
            print_dialog.setWindowTitle("Imprimer le Chèque")
            print_dialog.setStyleSheet("""
                QDialog {
                    background-color: #f9f9f9;
                }
                QLabel {
                    color: #201f1e;
                    font-size: 13px;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: 1px solid #0078d4;
                    padding: 8px 20px;
                    border-radius: 2px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                    border: 1px solid #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                    border: 1px solid #005a9e;
                }
                QPushButton:disabled {
                    background-color: #f3f2f1;
                    color: #a19f9d;
                    border: 1px solid #edebe9;
                }
                QComboBox {
                    background-color: white;
                    color: #201f1e;
                    border: 1px solid #8a8886;
                    border-radius: 2px;
                    padding: 6px;
                    font-size: 13px;
                }
                QComboBox:hover {
                    border: 1px solid #323130;
                }
                QComboBox:focus {
                    border: 1px solid #0078d4;
                    outline: none;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QGroupBox {
                    color: #323130;
                    font-weight: 600;
                    border: 1px solid #edebe9;
                    border-radius: 2px;
                    margin-top: 12px;
                    padding-top: 12px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px;
                }
                QRadioButton, QCheckBox {
                    color: #201f1e;
                    spacing: 8px;
                }
                QRadioButton::indicator, QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid #8a8886;
                    border-radius: 2px;
                    background-color: white;
                }
                QRadioButton::indicator:hover, QCheckBox::indicator:hover {
                    border: 1px solid #323130;
                }
                QRadioButton::indicator:checked, QCheckBox::indicator:checked {
                    background-color: #1b6f78;
                    border: 1px solid #1b6f78;
                }
                QSpinBox, QLineEdit {
                    background-color: white;
                    color: #201f1e;
                    border: 1px solid #8a8886;
                    border-radius: 2px;
                    padding: 6px;
                    font-size: 13px;
                }
                QSpinBox:hover, QLineEdit:hover {
                    border: 1px solid #323130;
                }
                QSpinBox:focus, QLineEdit:focus {
                    border: 1px solid #1b6f78;
                    outline: none;
                }
            """)
            return print_dialog.exec()
        return result
