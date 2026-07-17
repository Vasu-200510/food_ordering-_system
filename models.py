import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "foodies.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            address TEXT
        );

        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            category TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(item_id) REFERENCES food_items(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'Placed',
            name TEXT,
            address TEXT,
            phone TEXT,
            pincode TEXT,
            payment_method TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES food_items(id)
        );
        """
    )
    conn.commit()
    conn.close()


def seed_food_items():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) AS c FROM food_items").fetchone()["c"]
    if count > 0:
        conn.close()
        return
    items = [
        ("Margherita Pizza", 199, "Pizza", "Stone-baked, san marzano tomato, fior di latte"),
        ("Veg Supreme Pizza", 249, "Pizza", "Bell pepper, olive, mushroom, sweet corn"),
        ("Pepperoni Pizza", 299, "Pizza", "Double pepperoni, mozzarella, oregano"),
        ("Classic Cheese Burger", 149, "Burger", "Grilled patty, cheddar, house sauce"),
        ("Smoky BBQ Burger", 179, "Burger", "Charred patty, smoked bbq glaze, onion crisp"),
        ("Paneer Tikka Burger", 159, "Burger", "Spiced paneer patty, mint mayo"),
        ("Creamy Alfredo Pasta", 189, "Pasta", "Penne, mushroom, parmesan cream"),
        ("Arrabbiata Pasta", 169, "Pasta", "Penne, chilli tomato, basil"),
        ("Peri Peri Fries", 99, "Sides", "Crisp fries, peri peri dust"),
        ("Fresh Lime Soda", 69, "Drinks", "Sweet, salted or plain"),
        ("Cold Coffee", 89, "Drinks", "Espresso, cream, ice"),
        ("Chocolate Brownie", 119, "Desserts", "Warm fudge brownie, vanilla scoop"),
        ("New York Cheesecake", 149, "Desserts", "Baked cheesecake, berry compote"),
    ]
    conn.executemany(
        "INSERT INTO food_items (name, price, category, description) VALUES (?, ?, ?, ?)",
        items,
    )
    conn.commit()
    conn.close()


# ---------- password helpers ----------

def hash_password(raw):
    return generate_password_hash(raw)


def verify_password(hashed, raw):
    return check_password_hash(hashed, raw)


# ---------- User ----------

def create_user(name, email, password, phone=None):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)",
        (name, email, hash_password(password), phone),
    )
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid


def get_user_by_email(email):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def update_user(user_id, name, phone, address):
    conn = get_db()
    conn.execute(
        "UPDATE users SET name = ?, phone = ?, address = ? WHERE id = ?",
        (name, phone, address, user_id),
    )
    conn.commit()
    conn.close()


# ---------- Food items ----------

def get_all_food_items(category=None):
    conn = get_db()
    if category and category != "All":
        rows = conn.execute(
            "SELECT * FROM food_items WHERE category = ? ORDER BY id", (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM food_items ORDER BY id").fetchall()
    conn.close()
    return rows


def get_food_item(item_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM food_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return row


# ---------- Cart ----------

def get_cart_items(user_id):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT cart.id AS cart_id, cart.quantity, food_items.*
        FROM cart JOIN food_items ON cart.item_id = food_items.id
        WHERE cart.user_id = ?
        ORDER BY cart.id
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def cart_count(user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) AS c FROM cart WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row["c"]


def add_to_cart(user_id, item_id):
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM cart WHERE user_id = ? AND item_id = ?", (user_id, item_id)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id = ?", (existing["id"],)
        )
    else:
        conn.execute(
            "INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, 1)",
            (user_id, item_id),
        )
    conn.commit()
    conn.close()


def update_cart_item(cart_id, user_id, action):
    conn = get_db()
    row = conn.execute("SELECT * FROM cart WHERE id = ?", (cart_id,)).fetchone()
    if not row or row["user_id"] != user_id:
        conn.close()
        return
    if action == "increase":
        conn.execute("UPDATE cart SET quantity = quantity + 1 WHERE id = ?", (cart_id,))
    elif action == "decrease":
        new_qty = row["quantity"] - 1
        if new_qty <= 0:
            conn.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
        else:
            conn.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_qty, cart_id))
    elif action == "remove":
        conn.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()


def clear_cart(user_id):
    conn = get_db()
    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ---------- Orders ----------

def create_order(user_id, total, name, address, phone, pincode, payment_method, cart_items):
    conn = get_db()
    cur = conn.execute(
        """
        INSERT INTO orders (user_id, total, date, status, name, address, phone, pincode, payment_method)
        VALUES (?, ?, ?, 'Placed', ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            total,
            datetime.utcnow().isoformat(),
            name,
            address,
            phone,
            pincode,
            payment_method,
        ),
    )
    order_id = cur.lastrowid
    for c in cart_items:
        conn.execute(
            "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, c["id"], c["quantity"], c["price"]),
        )
    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return order_id


def get_order(order_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    return row


def get_orders_for_user(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY date DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_order_items(order_id):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT order_items.*, food_items.name AS food_name
        FROM order_items JOIN food_items ON order_items.item_id = food_items.id
        WHERE order_id = ?
        """,
        (order_id,),
    ).fetchall()
    conn.close()
    return rows
