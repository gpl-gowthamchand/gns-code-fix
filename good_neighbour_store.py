import tkinter as tk
from tkinter import ttk, messagebox

# Sample products (name, category, original price, discount %)
PRODUCTS = [
    ("Apples", "Fruits", 120, 10),
    ("Carrots", "Vegetables", 40, 5),
    ("Cabbage", "Vegetables", 20, 0),
    ("Spinach", "Vegetables", 30, 0),
    ("Milk (1L)", "Dairy", 60, 0),
    ("Curd (500g)", "Dairy", 45, 5),
    ("Butter (200g)", "Dairy", 90, 10),
    ("Cheese (200g)", "Dairy", 120, 0),
    ("Paneer (200g)", "Dairy", 80, 0),
    ("Rice (1kg)", "Grains", 65, 0),
    ("Wheat Flour (1kg)", "Grains", 45, 5),
    ("Bananas", "Fruits", 50, 0)
]

CATEGORIES = ["All", "Fruits", "Vegetables", "Dairy", "Grains"]

class Product:
    def __init__(self, name, category, price, discount):
        self.name = name
        self.category = category
        self.price = price
        self.discount = discount

    def discounted_price(self):
        return round(self.price * (1 - self.discount / 100), 2)

class CartItem:
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        return round(self.product.discounted_price() * self.quantity, 2)

class BillingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Good Neighbour Store - Offline POS")
        self.configure(bg="#f8fbfc")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.products = [Product(*p) for p in PRODUCTS]
        self.cart = {}
        self.selected_category = "All"

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#17a2b8", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Good Neighbour Store", font=("Segoe UI", 20, "bold"), fg="white", bg="#17a2b8").pack(side="left", padx=25)
        tk.Label(header, text="Offline Point of Sale", font=("Segoe UI", 12), fg="white", bg="#17a2b8").pack(side="left", padx=10)
        tk.Label(header, text="● Offline", font=("Segoe UI", 12, "bold"), fg="white", bg="#17a2b8").pack(side="right", padx=25)

        # Search and Category Bar
        search_cat = tk.Frame(self, bg="#f8fbfc")
        search_cat.pack(fill="x", pady=(10, 0), padx=20)
        self.search_var = tk.StringVar()
        # Search entry with placeholder synced to StringVar
        self.search_var.set("Search products...")
        search_entry = tk.Entry(search_cat, textvariable=self.search_var, font=("Segoe UI", 14), width=28, fg="#666")
        search_entry.pack(side="left", padx=(0, 20))
        # Clear placeholder on focus, restore on focus out if empty
        def on_focus_in(e):
            if self.search_var.get().lower() == "search products...":
                self.search_var.set("")
                search_entry.config(fg="#000")
        def on_focus_out(e):
            if not self.search_var.get().strip():
                self.search_var.set("Search products...")
                search_entry.config(fg="#666")
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_products())

        # Category Buttons
        for cat in CATEGORIES:
            btn = tk.Button(search_cat, text=cat, font=("Segoe UI", 12), bg="#e3f6fd", fg="#17a2b8", bd=0, padx=12, pady=6,
                            command=lambda c=cat: self.set_category(c))
            btn.pack(side="left", padx=(0, 10))

        # Main Area
        main_area = tk.Frame(self, bg="#f8fbfc")
        main_area.pack(fill="both", expand=True, padx=(20, 0), pady=10)

        # Product Grid
        self.product_frame = tk.Frame(main_area, bg="#f8fbfc")
        self.product_frame.place(relx=0, rely=0, relwidth=0.7, relheight=1)
        self.refresh_products()

        # Cart Sidebar
        self.cart_frame = tk.Frame(main_area, bg="white", bd=2, relief="groove")
        self.cart_frame.place(relx=0.72, rely=0, relwidth=0.28, relheight=1)
        tk.Label(self.cart_frame, text="🛒 Shopping Cart", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=18)
        self.cart_items_frame = tk.Frame(self.cart_frame, bg="white")
        self.cart_items_frame.pack(fill="both", expand=True)
        self.cart_total_label = tk.Label(self.cart_frame, text="Your cart is empty.\nAdd items to get started.", font=("Segoe UI", 14), bg="white", fg="#aaa")
        self.cart_total_label.pack(pady=10)
        tk.Button(self.cart_frame, text="Checkout", font=("Segoe UI", 14, "bold"), bg="#17a2b8", fg="white", bd=0, padx=10, pady=8,
                  command=self.checkout).pack(side="bottom", pady=18)

    def set_category(self, cat):
        self.selected_category = cat
        self.refresh_products()

    def refresh_products(self):
        for widget in self.product_frame.winfo_children():
            widget.destroy()
        search_term = self.search_var.get().lower()
        filtered = []
        for p in self.products:
            if self.selected_category != "All" and p.category != self.selected_category:
                continue
            if search_term and search_term != "search products..." and search_term not in p.name.lower():
                continue
            filtered.append(p)

        # Grid Layout
        for idx, prod in enumerate(filtered):
            card = tk.Frame(self.product_frame, bg="white", bd=2, relief="ridge", padx=10, pady=10)
            card.grid(row=idx // 3, column=idx % 3, padx=17, pady=15, sticky="nsew")
            name = tk.Label(card, text=prod.name, font=("Segoe UI", 15, "bold"), bg="white")
            name.pack(anchor="w")
            cat = tk.Label(card, text=prod.category, font=("Segoe UI", 11), bg="white", fg="#17a2b8")
            cat.pack(anchor="w")

            # Price & Discount
            price_frame = tk.Frame(card, bg="white")
            price_frame.pack(anchor="w", pady=(7, 0))
            if prod.discount > 0:
                old_price = tk.Label(price_frame, text=f"₹{prod.price:.2f}", font=("Segoe UI", 11, "overstrike"), fg="#999", bg="white")
                old_price.pack(side="left")
                discount_tag = tk.Label(price_frame, text=f"{prod.discount}% OFF", font=("Segoe UI", 9, "bold"), bg="#17a2b8", fg="white", padx=6, pady=2)
                discount_tag.pack(side="left", padx=(8,0))
            curr_price = tk.Label(card, text=f"₹{prod.discounted_price():.2f}", font=("Segoe UI", 14, "bold"), fg="#17a2b8", bg="white")
            curr_price.pack(anchor="w", pady=(2,0))

            # Add to Cart
            add_btn = tk.Button(card, text="Add to Cart", font=("Segoe UI", 12), bg="#e3f6fd", fg="#17a2b8", bd=0, padx=8, pady=4,
                                command=lambda p=prod: self.add_to_cart(p))
            add_btn.pack(fill="x", pady=(10,0))

    def add_to_cart(self, product):
        # Use product object as the dict key to avoid name collisions
        if product in self.cart:
            self.cart[product].quantity += 1
        else:
            self.cart[product] = CartItem(product, 1)
        self.refresh_cart()

    def refresh_cart(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        if not self.cart:
            self.cart_total_label.config(text="Your cart is empty.\nAdd items to get started.", fg="#aaa")
            return
        total = 0
        # iterate key, item so remove can reference the exact product object
        for idx, (key, item) in enumerate(list(self.cart.items())):
            row = tk.Frame(self.cart_items_frame, bg="white")
            row.pack(fill="x", pady=5, padx=7)
            tk.Label(row, text=f"{item.product.name}", font=("Segoe UI", 12), bg="white", width=15, anchor="w").pack(side="left")
            tk.Label(row, text=f"₹{item.product.discounted_price():.2f}", font=("Segoe UI", 12), bg="white", width=8).pack(side="left")
            tk.Label(row, text=f"x{item.quantity}", font=("Segoe UI", 12), bg="white", width=5).pack(side="left")
            tk.Label(row, text=f"₹{item.subtotal():.2f}", font=("Segoe UI", 12, "bold"), bg="white", width=8).pack(side="left")
            # Remove button references the product object key
            tk.Button(row, text="−", font=("Segoe UI", 12, "bold"), bg="#e3f6fd", fg="#17a2b8", bd=0,
                      command=lambda k=key: self.remove_from_cart(k)).pack(side="right", padx=5)
            total += item.subtotal()
        self.cart_total_label.config(text=f"Total: ₹{total:.2f}", fg="#17a2b8")

    def remove_from_cart(self, key):
        # key is the product object when using object keys
        if key in self.cart:
            self.cart[key].quantity -= 1
            if self.cart[key].quantity <= 0:
                del self.cart[key]
            self.refresh_cart()

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return
        total = sum(item.subtotal() for item in self.cart.values())
        pay = messagebox.askquestion("Checkout", f"Total amount: ₹{total:.2f}\n\nProcess payment?")
        if pay == "yes":
            self.cart.clear()
            self.refresh_cart()
            messagebox.showinfo("Payment Successful", "Thank you for shopping at Good Neighbour Store!")

if __name__ == "__main__":
    BillingSystem().mainloop()