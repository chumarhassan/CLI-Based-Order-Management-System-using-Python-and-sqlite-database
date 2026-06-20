# 🧾 Customer Order Management System

A polished, Python-based CLI application for managing customers, products, and orders. Uses SQLite for persistence and pandas for reporting and analysis.

---

## ✨ Highlights
- Manage customers and products (CRUD)
- Create, update, and delete orders
- Generate CSV order reports with pandas
- Interactive menu-driven CLI for quick operations

## 🛠️ Tech Stack
- Python 3.8+
- SQLite (built-in)
- pandas
- datetime

## 🚀 Quickstart
1. Clone repo

```bash
git clone <repo-url>
cd <repo-folder>
```

2. Create virtual env & install

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Unix
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app

```bash
python main.py
```

The interactive menu will appear. Follow prompts to add customers, products, and orders.

---

## 📌 Features (User-facing)
- Add / Update / Delete customers
- Add / Update / Delete products
- Place, update, or delete orders linked to customers
- View lists: customers, products, orders
- Export orders to CSV (`orders_report.csv`)

## 🧭 Classes & Methods (Overview)
- DatabaseConnection: connect(), disconnect(), execute_query(), fetch_data()
- TableManager: create_tables(db_conn)
- Customer: add_customer(), update_customer(), delete_customer(), get_all_customers()
- Product: add_product(), update_product(), delete_product(), get_all_products()
- Order: add_order(), update_order(), delete_order(), generate_report(csv_path='orders_report.csv')

Refer to source files for full method signatures and docstrings.

---

## 🧾 Generating Reports
From the menu choose `Generate Report`. The app will create `orders_report.csv` in the working directory. Open it with Excel or any spreadsheet app.

Example: `pandas` CSV contains order id, customer, items, quantities, total, and timestamp.

---

## 💡 Usage Tips
- Seed sample data using seed script (if provided) to explore quickly.
- Run `python -m pdb main.py` to step through logic while debugging.
- Keep backups of the SQLite DB file (e.g., `data.db`).

---

## 🤝 Contributing
1. Fork the repo
2. Create a branch: `git checkout -b feat/awesome`
3. Run and test locally
4. Submit a PR with a clear description

---

## 📬 Questions
Open an issue in this repository for bugs or feature requests.

---

