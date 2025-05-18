# E-Banking App

Basic E-Banking App with GUI built in Python and MySQL
Made during the third year of studies, as part of the course of Software Engineering.
This project models the core logic of a digital banking application. It simulates real-world banking heavily based on existing apps and operations using Python classes to manage accounts, transactions, payments, and foreign exchange.

## Features

- **Account Management**: Handles user accounts, balances, and currency.
- **Credit Cards**: Links and validates card data for payments.
- **Bills & Payments**: Supports bill assignment, payment tracking, and transaction logging.
- **Savings Goals**: Tracks progress toward saving objectives.
- **Money Transfers**: Enables domestic and foreign transfers between accounts.
- **Currency Exchange**: Supports buying/selling foreign currency using exchange rates.
- **Persistence Layer**: Interacts with mocked fetcher and etcher utilities simulating data retrieval and updates.

## Technologies

- **Python 3**
- **OOP principles**
- **MySQL**
- **MVC-like approach**

## Implementation

- Database created in MySQL
- mysql-connector-python is used to connect the app with the database
- Tkinter is used for the GUI
- pillow (PIL) is used for credit card customization

## Structure

- `card_templates/`: Contains images of blank Visa, MasterCard and Dina cards, which fills out with user's information in a layout mirroring real-world cards.
- `classes/`: Contains classes that represent entities.
- `gui/`: Contains interactable widgets that show up on the screen.
- `utils/`: Contains the database class, along with the fetcher and etcher classes used for retrieving and storing data.
- `main.py`: The entry point of the application.

## Basic Explanation

After a successful sign in, the user is brought to the main menu, which shows useful information about their credit card/account. If the user has multiple bank accounts, they can navigate using the left/right arrow to switch between them.
Each bank account has a credit card and bills, payments, savings, exchanges and money transfers associated with it.
By interacting with the grid menu, the user can explore different services - viewing past payments, paying bills, creating, adding and withdrawing from savings etc.
If a service is interacted with, it will open as a pop-up window and store any changes directly in the database, refreshing the entire app instantaneously.

Implemented rigorous checking for logic errors (e.g. user wants increase saving by an amount exceeding current balance) and incomplete form sending.

## Quick Demonstration

![image](https://i.imgur.com/a4lFpoe.gif)

## Note

This project was built as part of a university assignment and showcases practical use of object-oriented design in simulating financial systems. It was completed before taking advanced software engineering courses. It reflects self-taught design choices and practical experimentation with object-oriented concepts.

---

