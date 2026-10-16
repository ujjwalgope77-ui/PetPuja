"""
PetPuja - starter Android food delivery app (Python + Kivy)
This is a front-end prototype. Real OTP, backend/database, restaurant approval,
live order notifications, and payment integration must be added before launch.
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

KV = r"""
#:import dp kivy.metrics.dp
ScreenManager:
    HomeScreen:
    CartScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: dp(14), dp(8)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 1, 0.42, 0.08, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "[b]পেটপূজা[/b]"
                markup: True
                font_size: "25sp"
                color: 1,1,1,1
                halign: "left"
            Button:
                text: "কার্ট (" + str(app.cart_count) + ")"
                size_hint_x: None
                width: dp(105)
                on_release: app.root.current = "cart"
        BoxLayout:
            size_hint_y: None
            height: dp(56)
            padding: dp(12), dp(8)
            TextInput:
                id: search
                hint_text: "খাবার বা রেস্টুরেন্ট খুঁজুন"
                multiline: False
                on_text: app.filter_products(self.text)
        Label:
            text: "আপনার এলাকার খাবার"
            size_hint_y: None
            height: dp(42)
            color: 0.05, 0.28, 0.16, 1
            bold: True
            font_size: "18sp"
        ScrollView:
            GridLayout:
                id: products
                cols: 1
                spacing: dp(8)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(104)
                row_force_default: True

<CartScreen>:
    name: "cart"
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            size_hint_y: None
            height: dp(58)
            padding: dp(10)
            canvas.before:
                Color:
                    rgba: 1, 0.42, 0.08, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "← খাবারে ফিরুন"
                size_hint_x: None
                width: dp(140)
                on_release: app.root.current = "home"
            Label:
                text: "[b]আপনার কার্ট[/b]"
                markup: True
                font_size: "20sp"
                color: 1,1,1,1
        ScrollView:
            GridLayout:
                id: cart_items
                cols: 1
                spacing: dp(8)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height
        Label:
            id: total_label
            text: "মোট: ₹0"
            size_hint_y: None
            height: dp(44)
            bold: True
            font_size: "18sp"
            color: 0.05, 0.28, 0.16, 1
        Button:
            text: "অর্ডার করতে এগিয়ে যান (ডেমো)"
            size_hint_y: None
            height: dp(52)
            background_color: 1, 0.42, 0.08, 1
            on_release: app.checkout_demo()
"""

class HomeScreen(Screen):
    pass

class CartScreen(Screen):
    pass

class PetPujaApp(App):
    cart = ListProperty([])
    cart_count = NumericProperty(0)
    products_data = ListProperty([
        {"name": "আলুর চিপস", "restaurant": "ডেমো দোকান", "price": 10},
        {"name": "ভেজ মোমো", "restaurant": "ডেমো রেস্টুরেন্ট", "price": 60},
        {"name": "ভেজ বিরিয়ানি", "restaurant": "ডেমো রেস্টুরেন্ট", "price": 90},
        {"name": "চিকেন রোল", "restaurant": "ডেমো হোটেল", "price": 50},
    ])

    def build(self):
        self.title = "PetPuja"
        root = Builder.load_string(KV)
        self.root_widget = root
        self.populate_products(self.products_data)
        return root

    def populate_products(self, items):
        grid = self.root_widget.get_screen("home").ids.products
        grid.clear_widgets()
        for item in items:
            row = BoxLayout(orientation="horizontal", spacing=dp(8), padding=dp(8))
            info = BoxLayout(orientation="vertical")
            info.add_widget(Label(text=f"[b]{item['name']}[/b]", markup=True,
                                  color=(0.08,0.16,0.1,1), halign="left"))
            info.add_widget(Label(text=f"{item['restaurant']}  •  ₹{item['price']}",
                                  color=(0.25,0.25,0.25,1), halign="left"))
            add = Button(text="যোগ করুন", size_hint_x=None, width=dp(100),
                         background_color=(0.05,0.38,0.2,1))
            add.bind(on_release=lambda _btn, product=item: self.add_to_cart(product))
            row.add_widget(info)
            row.add_widget(add)
            grid.add_widget(row)

    def filter_products(self, query):
        q = query.strip().lower()
        matches = [p for p in self.products_data
                   if q in p["name"].lower() or q in p["restaurant"].lower()]
        self.populate_products(matches)

    def add_to_cart(self, product):
        self.cart.append(product)
        self.cart_count = len(self.cart)

    def refresh_cart(self):
        screen = self.root_widget.get_screen("cart")
        grid = screen.ids.cart_items
        grid.clear_widgets()
        total = 0
        for item in self.cart:
            total += item["price"]
            grid.add_widget(Label(
                text=f"{item['name']} — ₹{item['price']}",
                size_hint_y=None, height=dp(42), color=(0.08,0.16,0.1,1)))
        screen.ids.total_label.text = f"মোট: ₹{total}"

    def on_start(self):
        self.root_widget.bind(current=self._screen_changed)

    def _screen_changed(self, _instance, screen_name):
        if screen_name == "cart":
            self.refresh_cart()

    def checkout_demo(self):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label as PopupLabel
        Popup(title="ডেমো চেকআউট",
              content=PopupLabel(text="এটি শুধু প্রোটোটাইপ। বাস্তব অর্ডারের জন্য OTP, ঠিকানা ও সার্ভার যোগ করতে হবে।"),
              size_hint=(0.88, 0.35)).open()

if __name__ == "__main__":
    PetPujaApp().run()
