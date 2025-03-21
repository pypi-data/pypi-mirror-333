# 📌 PyDBManager - SQL Server Database Manager  

![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  ![SQL Server](https://img.shields.io/badge/SQL%20Server-ODBC%20Driver%2017-red.svg)  ![MIT License](https://img.shields.io/badge/License-MIT-green.svg)  

Welcome to **PyDBManager** – a Python package for managing **SQL Server connections and queries** easily and efficiently! 🎯  

This guide will help you:
- ✅ Install PyDBManager
- ✅ Set up your `.env` file for credentials
- ✅ Perform SQL operations using Python
- ✅ Save query results
- ✅ Use caching & batch fetching

---

## **1. Install PyDBManager**  
Run the following command to install `PyDBManager`:
```bash
pip install pydbmanager
```
**If installation is successful, continue to the next step!**  

---

## **2. Create `.env` File to Store Database Credentials**  
To avoid hardcoding credentials, create a `.env` file in your project directory.

### **Steps**  
1. **Create a `.env` file** in your project root.  
2. **Add the following credentials** (update as needed):
    ```
    DB_SERVER=localhost
    DB_DATABASE=your_database_name
    DB_USERNAME=your_username
    DB_PASSWORD=your_password
    DB_DRIVER={ODBC Driver 17 for SQL Server}
    ```
3. **Ensure `.env` is ignored by Git** (Add `.env` to `.gitignore`).  
4. **Verify that `.env` loads correctly** (Next step).  

---

## **3. Verify `.env` File**  
Run this script to check if the values are loaded correctly:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\u2705 Database Configuration Loaded:")
print(f"SERVER: {os.getenv('DB_SERVER')}")
print(f"DATABASE: {os.getenv('DB_DATABASE')}")
print(f"USERNAME: {os.getenv('DB_USERNAME')}")
print(f"PASSWORD: {'*' * len(os.getenv('DB_PASSWORD')) if os.getenv('DB_PASSWORD') else 'Not Set'}")
print(f"DRIVER: {os.getenv('DB_DRIVER')}")
```
**Expected Output**
```
Database Configuration Loaded:
SERVER: localhost
DATABASE: testDB
USERNAME: your_username
PASSWORD: **********
DRIVER: {ODBC Driver 17 for SQL Server}
```

---

## **4. Connect to the Database**  
```python
from pydbmanager.connection import DatabaseConnection

# Initialize and test database connection
db = DatabaseConnection()
conn = db.create_connection()

if conn:
    print("\u2705 Connection Successful!")
    db.close_connection()
else:
    print("\u274c Connection Failed!")
```
**Expected Output**
```
Connection Successful!
```

---

## **5. Perform SQL Operations**  

### **🔹 Fetch All Users**  
```python
from pydbmanager.operations import DatabaseOperations

db_ops = DatabaseOperations()

# Fetch all users
df = db_ops.query_data("SELECT * FROM users", batch_size=5)
df
```
**Expected Output** → A **pandas DataFrame** displaying user data.

---

### **🔹 Insert a New Record**  
```python
insert_query = """
INSERT INTO users (name, email, age, gender, phone_number, address, city, country)
VALUES ('John Doe', 'john.doe@example.com', 29, 'Male', '123-456-7890', '123 Elm St', 'New York', 'USA')
"""
db_ops.execute_query(insert_query)
print("\u2705 User inserted successfully!")
```

---

### **🔹 Update a Record**  
```python
update_query = """
UPDATE users SET age = 30 WHERE email = 'john.doe@example.com'
"""
db_ops.execute_query(update_query)
print("\u2705 User updated successfully!")
```

---

### **🔹 Delete a Record**  
```python
delete_query = """
DELETE FROM users WHERE email = 'john.doe@example.com'
"""
db_ops.execute_query(delete_query)
print("\u2705 User deleted successfully!")
```

---

## **6. Saving Query Results**  

### **🔹 Save Data to CSV**  
```python
db_ops.save_results(df, "users_data.csv", "csv")
print("\u2705 Data saved to users_data.csv")
```
📁 **Check your project folder for `users_data.csv`**  

---

## **7. Using Caching & Batch Fetching**  

### **🔹 Query with Caching**  
```python
df_cached = db_ops.cached_query("SELECT * FROM users")
df_cached
```

### **🔹 Query with Batch Fetching**  
```python
df_batch = db_ops.query_data("SELECT * FROM users", batch_size= 10)
df_batch
```

---

### **🔹 Closing Connection**  
```python
db_ops.close()
print("\u2705 Database connection closed.")
```

---

## **✅ Congratulations! 🎉**  
You’ve successfully used **PyDBManager** for:  
- Connecting to SQL Server  
- Running SQL queries in Python  
- Fetching, inserting, updating & deleting data  
- Using caching & batch fetching  
- Saving results to a file  

---

## **🚀 Contributing & License**  
I welcome contributions! Feel free to submit issues and pull requests. 🛠️  

This project is **MIT Licensed** — you are free to modify and distribute it as needed. 🏆  

🔥 **Happy Coding!** 🚀  

