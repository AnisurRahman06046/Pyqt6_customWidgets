from PyQt6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal

"""
- We are creating a class called SearchableComboBox which inherits QCombobox cause we are extending QComboBox to add custom behavior
- Inside the class we define a emitter called pyqtsingnal which transmits the string whenever users types in the search bar

- super().__init__(parent) → Calls the parent class (QComboBox) constructor.
self.setPlaceholderText("Brand") → Sets a default title for the combo box.
self.setEditable(False) → Prevents direct text input in the combo box.
"""


class SearchableComboBox(QComboBox):
    textChanged = pyqtSignal(str)

    # Initializing the cusotm combo box
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Brand")
        self.setEditable(False)

        # creating a popup frame to hold the search bar and list
        self.popup_frame = QFrame(
            self
        )  # creates a floating frame as a child of combo box
        self.popup_frame.setWindowFlags(
            Qt.WindowType.Popup
        )  # makes the frame behave like a popup
        self.popup_frame.setLayout(
            QVBoxLayout()
        )  # the elements inside the pop up will be arranged vertically

        # adding search bar
        self.search_bar = QLineEdit(self)  # creates a text input field
        self.search_bar.setPlaceholderText(
            "Search..."
        )  # sets a default title for the search bar
        self.search_bar.textChanged.connect(
            self.textChanged.emit
        )  # Connects the textChanged signal of QLineEdit to the custom signal we defined earlier (textChanged), so that the main program knows when the user types.

        # adding list widgets
        self.list_widget = QListWidget(
            self
        )  # Creates a list that will hold selectable items.
        self.list_widget.itemClicked.connect(
            self.select_item
        )  # Connects the itemClicked signal to the select_item method (which handles what happens when a user selects an item).

        # adding widgets to the pop up
        self.popup_frame.layout().addWidget(self.search_bar)
        self.popup_frame.layout().addWidget(self.list_widget)

        # showing the pop up

    def show_popup(self):
        self.popup_frame.setMinimumWidth(
            self.width()
        )  # Ensures the popup matches the width of the combo box.
        self.popup_frame.move(
            self.mapToGlobal(self.rect().bottomLeft())
        )  # Positions the popup right below the combo box.
        self.popup_frame.show()
        self.search_bar.setFocus()  # Automatically places the cursor in the search bar when the popup opens.

    def hidePopup(self):
        self.popup_frame.hide()

    def update_items(self, items):
        """Update the list dynamically when data is fetched from PosTerminalPage."""
        self.list_widget.clear()
        for item in items:
            list_item = QListWidgetItem(item)
            self.list_widget.addItem(list_item)

    def select_item(self, item):
        """Handle item selection and emit a signal."""
        selected_text = item.text()
        self.setPlaceholderText(f"{self.title}: {selected_text}")  # Temporary selection
        self.itemSelected.emit(selected_text)  # Emit selection signal
        self.hidePopup()
        self.search_bar.clear()
