from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QLineEdit,
    QPushButton,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QDateEdit,
)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont, QIcon


class PaymentProcess(QWidget):
    def __init__(self):
        super().__init__()
        self.payment_rows = []  # Store references to payment rows
        self.payment_container = None  # Will hold payment rows
        self.initUI()

    def initUI(self):
        main_container = QVBoxLayout()
        totalAmountValue = 5000

        # Header Section
        header_label = QLabel(f"Total Amount:{totalAmountValue}")
        header_label.setStyleSheet(
            "background-color:#7A8882;color:#FFFFFF;font-weight:bold;"
        )
        header_label.setFixedHeight(50)
        header_label.setFont(QFont("Arial", 15))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Columns Header Section
        cols_header_Container = QWidget()
        cols_header_Container.setStyleSheet(
            "background-color: white; padding: 8px; border:1px solid #D3D3D3; border-radius: 5px;"
        )
        cols_header_Container.setFixedHeight(50)
        cols_header_layout = QHBoxLayout()
        cols_header_layout.setSpacing(20)

        paymentProcess_cols = [
            "Payment Type",
            "Payment Options",
            "Amount Received",
            "Action",
        ]
        for col in paymentProcess_cols:
            label = QLabel(col)
            label.setStyleSheet(
                "font-weight: bold; padding: 5px; background-color: white;border:none;"
            )
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cols_header_layout.addWidget(label)
        cols_header_Container.setLayout(cols_header_layout)

        # Payment Methods Container
        payment_section = QVBoxLayout()
        self.payment_container = payment_section
        self.add_payment_row(is_first=True)

        # Additional Fields Section
        additional_fields = QGridLayout()

        delivery_charge_label = QLabel("Delivery charge")
        delivery_charge_value = QLineEdit("0")

        due_date_label = QLabel("Due date")
        due_date_value = QDateEdit()
        due_date_value.setDisplayFormat("yyyy-MM-dd")
        due_date_value.setDate(QDate.currentDate())
        due_date_value.setCalendarPopup(True)

        receiveCash_label = QLabel("Receive Cash")
        receiveCash_value = QLineEdit("")

        change_label = QLabel("Change")
        change_value = QLineEdit()
        change_value.setReadOnly(True)
        change_value.setStyleSheet("background-color:#E9ECEF")

        remark_label = QLabel("Remark")
        remark_value = QLineEdit("")

        additional_fields.addWidget(delivery_charge_label, 0, 0, 1, 1)
        additional_fields.addWidget(delivery_charge_value, 0, 1, 1, 3)
        additional_fields.addWidget(due_date_label, 1, 0, 1, 1)
        additional_fields.addWidget(due_date_value, 1, 1, 1, 3)
        additional_fields.addWidget(receiveCash_label, 2, 0, 1, 1)
        additional_fields.addWidget(receiveCash_value, 2, 1, 1, 3)
        additional_fields.addWidget(change_label, 3, 0, 1, 1)
        additional_fields.addWidget(change_value, 3, 1, 1, 3)
        additional_fields.addWidget(remark_label, 4, 0, 1, 1)
        additional_fields.addWidget(remark_value, 4, 1, 1, 3)
        additional_fields.setColumnStretch(0, 3)
        additional_fields.setColumnStretch(1, 7)
        additional_fields.setVerticalSpacing(15)

        # Cancel and Checkout Buttons
        cancelCheckOutBtnLayout = QHBoxLayout()
        cancelCheckOutBtnLayout.setSpacing(25)
        cancelCheckOutBtnLayout.setContentsMargins(0, 20, 50, 0)

        cancelBtn = QPushButton("Cancel")
        cancelBtn.setStyleSheet(
            "background-color:red;color:white;padding:6px;font-weight:bold;"
        )

        checkoutBtn = QPushButton("Checkout")
        checkoutBtn.setStyleSheet(
            "background-color:green;color:white;padding:6px;font-weight:bold"
        )

        cancelCheckOutBtnLayout.addStretch(1)
        cancelCheckOutBtnLayout.addWidget(cancelBtn, stretch=1)
        cancelCheckOutBtnLayout.addWidget(checkoutBtn, stretch=1)
        cancelCheckOutBtnLayout.setAlignment(Qt.AlignmentFlag.AlignJustify)

        # Add all sections to main container
        main_container.addWidget(header_label)
        main_container.addWidget(cols_header_Container)
        main_container.addLayout(payment_section)
        main_container.addLayout(additional_fields)
        main_container.addLayout(cancelCheckOutBtnLayout)

        self.setLayout(main_container)

    def add_payment_row(self, is_first=False):
        row_container = QWidget()
        row_layout = QVBoxLayout(row_container)

        # Main payment row
        payment_row = QHBoxLayout()

        # Payment Method Dropdown
        paymentMethod = QComboBox()
        paymentMethod.addItems(["Cash", "Bank Cheque"])

        # Payment Option
        paymentOption = QLineEdit()
        paymentOption.setReadOnly(True)
        paymentOption.setText(paymentMethod.currentText())
        paymentOption.setStyleSheet("background-color:#E9ECEF")

        paymentMethod.currentTextChanged.connect(
            lambda text, opt=paymentOption: opt.setText(text)
        )

        # Amount Received
        amountReceived = QLineEdit("0")

        # Action Buttons
        action_buttons = QHBoxLayout()
        action_buttons.setSpacing(5)

        deleteBtn = QPushButton()
        deleteBtn.setIcon(QIcon("assets/trash.png"))
        deleteBtn.setStyleSheet("background-color:#FF0000;")
        deleteBtn.clicked.connect(lambda: self.remove_payment_row(row_container))

        if is_first:
            deleteBtn.setDisabled(True)

        addBtn = QPushButton()
        addBtn.setIcon(QIcon("assets/add.png"))
        addBtn.setStyleSheet("background-color:blue;")
        addBtn.clicked.connect(self.add_payment_row)

        action_buttons.addWidget(deleteBtn)
        action_buttons.addWidget(addBtn)

        # Add widgets to payment row
        payment_row.addWidget(paymentMethod)
        payment_row.addWidget(paymentOption)
        payment_row.addWidget(amountReceived)
        payment_row.addLayout(action_buttons)

        # Extra Fields for Bank Cheque
        extra_fields = QWidget()
        extra_layout = QGridLayout(extra_fields)

        # Bank Cheque fields
        chequeAmountLabel = QLabel("Cheque Amount")
        chequeAmountInput = QLineEdit("0")

        bankNameLabel = QLabel("Client Bank Name")
        bankNameInput = QLineEdit()
        bankNameInput.setPlaceholderText("Bank Name")

        bankChequeNoLabel = QLabel("Bank Cheque No:")
        bankChequeNoInput = QLineEdit()
        bankChequeNoInput.setPlaceholderText("Cheque Number")

        issueDateLabel = QLabel("Issue Date")
        issueDateInput = QDateEdit()
        issueDateInput.setDisplayFormat("yyyy-MM-dd")
        issueDateInput.setDate(QDate.currentDate())
        issueDateInput.setCalendarPopup(True)

        activeDateLabel = QLabel("Active Date")
        activeDateInput = QDateEdit()
        activeDateInput.setDisplayFormat("yyyy-MM-dd")
        activeDateInput.setDate(QDate.currentDate())
        activeDateInput.setCalendarPopup(True)

        issueToHome_label = QLabel("Issue To Home")
        issueToHomeInput = QLineEdit()
        issueToHomeInput.setPlaceholderText("Issue To Home")

        # Add fields to extra layout
        extra_layout.addWidget(chequeAmountLabel, 0, 0)
        extra_layout.addWidget(chequeAmountInput, 0, 1)
        extra_layout.addWidget(bankNameLabel, 1, 0)
        extra_layout.addWidget(bankNameInput, 1, 1)
        extra_layout.addWidget(bankChequeNoLabel, 2, 0)
        extra_layout.addWidget(bankChequeNoInput, 2, 1)
        extra_layout.addWidget(issueDateLabel, 3, 0)
        extra_layout.addWidget(issueDateInput, 3, 1)
        extra_layout.addWidget(activeDateLabel, 4, 0)
        extra_layout.addWidget(activeDateInput, 4, 1)
        extra_layout.addWidget(issueToHome_label, 5, 0)
        extra_layout.addWidget(issueToHomeInput, 5, 1)

        # Store references
        row_container.extra_fields = extra_fields
        row_container.row_layout = row_layout

        extra_fields.setParent(None)  # Initially hidden

        # Toggle extra fields based on payment method
        def update_payment_fields(text):
            if text == "Bank Cheque":
                if extra_fields.parent() is None:
                    row_layout.addWidget(extra_fields)
            else:
                row_layout.removeWidget(extra_fields)
                extra_fields.setParent(None)

            QTimer.singleShot(100, self.delayed_resize)

        paymentMethod.currentTextChanged.connect(update_payment_fields)

        # Add to layouts
        row_layout.addLayout(payment_row)
        self.payment_rows.append(row_container)
        self.payment_container.addWidget(row_container)
        self.delayed_resize()

    def remove_payment_row(self, row_container):
        if len(self.payment_rows) > 1:
            self.payment_container.removeWidget(row_container)
            self.payment_rows.remove(row_container)

            while row_container.row_layout.count():
                item = row_container.row_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()

            row_container.setParent(None)
            row_container.deleteLater()
            self.delayed_resize()

    def delayed_resize(self):
        """Helper method to resize the window with proper geometry calculation"""
        self.adjustSize()
        self.updateGeometry()
        if self.parent():
            self.parent().adjustSize()