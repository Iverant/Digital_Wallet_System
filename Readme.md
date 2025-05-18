# 💳 Digital Wallet System with Fraud Detection (Flask Backend)

This is a backend system for a **Digital Wallet Platform** built using Python and Flask. It allows users to register, manage virtual funds, and transfer money between users. The system also includes **basic fraud detection**, **JWT-based authentication**, and **admin reporting APIs**.

---

## 🚀 Features

- ✅ Secure user authentication (JWT)
- 💰 Deposit, withdraw, and transfer funds
- 📜 Transaction history tracking
- 🕵️ Basic rule-based fraud detection
- 🧾 Admin APIs for reports and flagged transactions
- 🌐 Fully documented REST API (Postman)

---

## 🛠 Technologies Used

| Component        | Technology       |
|------------------|------------------|
| Backend Framework | Flask (Python)  |
| Database          | SQLite (via SQLAlchemy) |
| Authentication    | JWT (using Flask-JWT-Extended) |
| API Docs & Testing | Postman          |
| Security          | bcrypt (password hashing) |

---

## 📦 Project Structure

```

wallet-app/
│
├── app.py                  # Main entrypoint
├── models.py               # Database models
├── routes/
│ ├── auth.py               # Auth endpoints
│ └── wallet.py             # Wallet + admin routes
├── utils/
│ └── fraud.py              # Fraud detection logic
├── config.py               # App configuration
├── requirements.txt        # Dependencies
└── README.md               # This file

```

# Endpoints Overview

This backend API allows users to manage a virtual wallet: deposit, withdraw, transfer funds, and detect fraudulent activity.

---

## 🧍 User Authentication

### `POST /auth/register`
- Registers a new user with a username and password.

### `POST /auth/login`
- Logs in a user and returns a JWT token for authentication.

---

## 💸 Wallet Operations (Require JWT)

### `POST /wallet/deposit`
- Deposits virtual cash into the logged-in user's wallet.
- **Payload**: `{ "amount": 1000 }`

### `POST /wallet/withdraw`
- Withdraws virtual cash from the logged-in user's wallet.
- **Payload**: `{ "amount": 500 }`

### `POST /wallet/transfer`
- Transfers virtual cash from the logged-in user to another user.
- **Payload**: `{ "receiver": "username", "amount": 200 }`

### `GET /wallet/history`
- Retrieves the full transaction history of the logged-in user.

---

## 🛡️ Fraud Detection & Admin (Require JWT)

### `GET /admin/flagged`
- Returns all transactions that have been flagged as potentially fraudulent.

### `GET /admin/top-users`
- Returns the top users sorted by wallet balance or total transaction volume.

### `GET /admin/total-balances`
- Calculates and returns the sum of all users' wallet balances.

---

## 🔐 Note
- All wallet and admin routes require a valid JWT token in the **Authorization** header.
- Format: `Bearer <your_token>`