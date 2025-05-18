# E-Banking App

A basic digital banking app with a GUI, built using Python and MySQL.

Developed during the third year of studies as part of the *Software Engineering* course, this project models the core logic of an e-banking system. It simulates real-world banking operations, inspired by existing apps, using Python classes to manage accounts, transactions, payments, savings, and currency exchange.

---

## Features

- **Account Management**: Manages user accounts, balances, and currency data.
- **Credit Cards**: Links and validates card information for payments.
- **Bills & Payments**: Supports bill tracking, payments, and transaction logging.
- **Savings Goals**: Tracks user-defined savings objectives.
- **Money Transfers**: Enables both domestic and foreign transfers between accounts.
- **Currency Exchange**: Allows buying/selling of foreign currencies using exchange rates.
- **Persistence Layer**: Simulates data retrieval and updates using mocked fetcher and etcher utilities.

---

## Technologies Used

- **Python 3.12**
- **OOP principles**
- **MySQL** (for persistent storage)
- **MVC-inspired architecture**

---

## Implementation Highlights

- **Database**: Designed in MySQL with normalized tables.
- **Connector**: `mysql-connector-python` used for database interactions.
- **GUI**: Built with `tkinter`.
- **Image Generation**: `Pillow` (PIL) used to generate custom credit card visuals.

---

## Project Structure

e-banking-app/
- │
- ├── card_templates/ *Blank templates for Visa, MasterCard, Dina cards*
- ├── classes/ *Core logic and entity classes (Account, Bill, etc.)*
- ├── gui/ *GUI components and widgets*
- ├── utils/ *Database connection + data fetching/writing utilities*
- └── main.py *Entry point for the application*

---

## How It Works

- After signing in, the user is presented with a dashboard displaying account and credit card details.
- If multiple accounts exist, the user can switch between them using left/right arrow buttons.
- A grid-based menu provides access to core services like:
  - Viewing and paying bills
  - Managing savings
  - Making transfers
  - Viewing past transactions
  - Checking and using exchange rates
- Each service opens in a separate pop-up window and commits changes directly to the MySQL database, with real-time UI refresh.
- Rigorous validation is in place to prevent logical errors (e.g., overspending) and incomplete form submissions.

---

## Quick Demonstration

![Demo](https://i.imgur.com/a4lFpoe.gif)

---

## Installation

### 1. Clone the Repository

git clone https://github.com/shugimilo/E-Banking.git
cd e-banking-app

### 2. (Recommended) Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Requirements
pip install -r requirements.txt

### 4. Import the Database
Import the provided .sql database dump into your local MySQL server (localhost). You can use MySQL Workbench, phpMyAdmin, or the CLI:
mysql -u your_username -p your_database_name < path/to/database_file.sql
**Note**: Ensure your database credentials in the app match your MySQL configuration.

### 5. Run the App
python main.py
