# PyQt6 Signal for communication

### What is Signal :

A signal is an event that is emitted when something happens.

- **For example**, clicking a button can emit a signal.

**Real World Example** :
Imagine you **press a doorbell-->** it rings inside the house.

- **Presssing the doorbell-->** Emits a signal
- **The doorbell is ringing**: Another part listening and responding to the signal

### What is Slot:

A slot is a function that runs when a signal is received.
It "listens" for specific signals and takes action.

**Example**:

- `button.clicked.connect(self.onBtnClick)`
- **clicked**: is a signal emitted by the button
- **self.onBtnClick** is a slot (function) that runs when the button is clicked

### Use Case 1:

Suppose, you have a product details modal widget which shows the product details. It has a **Add to Order** button.Now, you have another widget called **CartWindow** where the ordered items are listed. Now you want that when you click the **add to order** button from the modal, the product adds in the **CartWindow** itemlist. How to solve this problem ?

#### Solutions :

The problem can be solved using **pyqt signal slot mechanism**

**Sol 1:**

- Step 1: create a signal in your product details modal
- `
  from PyQt6.QtCore import pyqtSignal

class ProductDetailModal(QDialog):
product_added = pyqtSignal(dict) # Define a signal to send product data

    def __init__(self, product_name, parent=None):
        super().__init__(parent)
        ........................
        ........................

    def add_to_cart(self):
        """Emit the product details when 'Add to Order' is clicked"""
        product_data = {
            "name": self.product_name,
            "price": self.product_price,
            "quantity": self.quantity
        }
        self.product_added.emit(product_data)  # Emit signal with product data
        self.close()  # Close modal`

- Step 2 : Connect the signal to the slot in your cart window

---

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CartWidget(QWidget):
def **init**(self):
super().**init**()
self.setWindowTitle("Cart")

    def add_product(self, product_data):
        """add the product to the product list in the cart window"""
        self.product_added.connect(method to add the product in the cart)

---

**Sol 2** : Using Global Event Bus

- Step 1 : create a global event bus

```
from PyQt6.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    product_added = pyqtSignal(dict)  # Signal for sending product data to cart

event_bus = EventBus()  # Create a single instance
```

- Step 2 : Modify the Modal to Emit the Signal

```
from event_bus import event_bus  # Import the event bus

def add_to_cart(self):
    """Emit signal to add product to cart"""
    event_bus.product_added.emit(product_entry)  # Emit signal
    self.close()
```

**_Now, when "Add to Order" is clicked, the modal emits a signal with product data._**

- Step 3 : Connect the event to the cart window

`from event_bus import event_bus # Import event bus
class CartWindow(QWidget):
def **init**(self):
super().**init**()
event_bus.product_added.connect(self.add_product_to_cart) # Listen for event`

**If PyQt6’s signal-slot mechanism can handle communication between components, why would we need a global event bus?**

**Signal Slot(Local Communication )** :

- Works best when components are directly connected (like modal → cart).
- The sender (modal) and receiver (cart) must know each other.
- Limited to parent-child relationships or when both components exist in the same scope.

**_Best for_**:

- UI components that have a clear relationship (e.g., opening a modal from a button).
- Short-lived interactions (e.g., adding a product to a cart while the modal is open).

**Global Event Bus(Decoupled Communication)**:

- A **centralized** way to send and receive events across the entire application.
- Any component can **listen** for events **without direct connections**.
- Useful when components are **far apart** (e.g., modal in one window, cart in another).

**_Best for_**:

- **Large applications** where different parts need to communicate without being directly connected.
- **Background events** (e.g., real-time updates, network requests, multiple windows).

## Conclusion

- For simple cases → Use signal-slot (direct connection).
- For complex apps → Use a global event bus (decoupled & scalable).
  🔥 Which one do you want to practice more?
- Advanced signal-slot (e.g., passing more data, disconnecting signals)?
- More event bus use cases (e.g., multi-window apps, notifications)? 🚀
