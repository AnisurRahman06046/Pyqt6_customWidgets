from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal


class ProductCard(QFrame):
    product_clicked = pyqtSignal(str)

    def __init__(self, image_path: str, title: str, parent=None):
        super().__init__(parent)
        # print(image_path)

        # Set fixed size for the product card
        self.setFixedSize(180, 180)  # Adjust the size as per your design

        self.setStyleSheet(
            "QFrame {"
            "   border: 1px solid #ccc;"
            "   border-radius: 10px;"
            "   background-color: white;"
            "   padding: 2px;"
            "}"
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(3)

        # Product Image
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(
            pixmap.scaled(
                150,
                140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Product Title
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("padding: 2px;")
        self.title_label.setMaximumHeight(30)

        # Add widgets to layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.title_label)

    def mousePressEvent(self, event):
        """Detect when the product card is clicked."""
        self.product_clicked.emit(
            self.title_label.text()
        )  # Emit signal with product name
