# E-Banking App

Basic E-Banking App with GUI built in Python and MySQL
Made during the third year of studies, as part of the course of Software Engineering.
This project models the core logic of a digital banking application. It simulates real-world banking heavily based on existing apps and operations using Python classes to manage accounts, transactions, payments, and foreign exchange.

## Features

- **Account Management**: Handles user accounts, balances, and currency.
- **Credit Cards**: Links and validates card data for payments.
- **Bills & Payments**: Supports bill assignment, payment tracking, and transaction logging.
- **Savings Goals**: Tracks progress toward saving objectives.
- **Money Transfers**: Enables domestic transfers between accounts.
- **Currency Exchange**: Supports buying/selling foreign currency using exchange rates.
- **Persistence Layer**: Interacts with mocked fetcher and etcher utilities simulating data retrieval and updates.

## Technologies

- **Python 3**
- **OOP principles**
- **Datetime handling**
- **Modular structure (classes for each entity)**

## Structure

- `account.py`: Core class representing user accounts and coordinating actions.
- `utils/fetcher.py`: Simulates data fetching from a database.
- `utils/etcher.py`: Simulates data modification/writing.
- `creditcard.py`, `bill.py`, `saving.py`, etc.: Data models for financial entities.

## Usage

This is a logic-layer module designed to be integrated into a broader application (e.g., with a frontend or database). Each class is self-contained and easily testable.

## Note

This project was built as part of a university assignment and showcases practical use of object-oriented design in simulating financial systems. It was completed before taking advanced software engineering courses. It reflects self-taught design choices and practical experimentation with object-oriented concepts.

---

