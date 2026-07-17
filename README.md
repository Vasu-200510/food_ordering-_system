# 🍔 Foodies - Online Food Ordering System

Foodies is a Flask-based web application that allows users to browse food items, manage a shopping cart, place orders, and view their order history. The project demonstrates user authentication, session management, cart functionality, and order processing using Python and Flask.

---

## 📌 Features

* User Registration and Login
* Secure Session Management
* Browse Food Menu by Category
* Add Items to Shopping Cart
* Update Cart Quantity
* Checkout and Place Orders
* Order Confirmation
* User Profile Management
* Order History
* Contact Page
* Flash Messages for User Feedback

---

## 🛠️ Technologies Used

* Python 3.x
* Flask
* HTML5
* CSS3
* Jinja2 Templates
* SQLite
* Werkzeug (Password Hashing)

---

## 📂 Project Structure

```text
Foodies/
│
├── app.py
├── models.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── menu.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   ├── profile.html
│   ├── edit_profile.html
│   └── contact.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── database/
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/foodies.git
cd foodies
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will start at:

```text
http://127.0.0.1:5000
```

---

## 📋 Requirements

Example `requirements.txt`

```text
Flask
Werkzeug
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 👤 User Workflow

1. Register a new account.
2. Log in to the application.
3. Browse the food menu.
4. Add food items to the cart.
5. Update cart quantities.
6. Proceed to checkout.
7. Enter delivery information.
8. Place the order.
9. View order confirmation.
10. Check previous orders from the profile page.

---

## 🔒 Security Features

* Password authentication
* Session-based login
* Protected routes using `login_required`
* User-specific cart and order history
* Flash messages for validation and feedback

---

## 📸 Screenshots

Add screenshots of the application here.

Example:

* Home Page
* Menu Page
* Cart
* Checkout
* Profile
* Order Confirmation

---

## 🌟 Future Enhancements

* Online payment integration (Stripe/Razorpay)
* Admin dashboard
* Food search
* Ratings and reviews
* Wishlist
* Order tracking
* Email notifications
* Responsive mobile design
* Coupons and discounts
* REST API support

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and modify it for educational and personal projects.

---

## 👨‍💻 Author

**Your Name**

* GitHub: https://github.com/your-username
* Email: [your-email@example.com](mailto:your-email@example.com)

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
