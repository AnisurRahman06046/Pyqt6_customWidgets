from PyQt6.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    product_added = pyqtSignal(dict)  # Signal for adding products to cart

event_bus = EventBus()  # Global instance
