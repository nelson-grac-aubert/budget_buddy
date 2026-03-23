# budget-buddy

A lightweight budget manager app made for La Plateforme_ IT school.

## Features

- User authentication : secure registration and login with bcrypt password hashing (salted + peppered), email format validation, and password strength enforcement  
- Dashboard : at-a-glance view of your current balance, monthly income, monthly expenses, and a balance-over-time curve showing the full history of your account  
- Deposit : add funds to your account with a description  
- Withdrawal : record cash withdrawals with a description and amount validation  
- Transfer : send money to another account by entering the recipient's account ID  
- Transaction history : full statement view listing all operations with date, category, type (credit/debit) and amount  
- Spending breakdown : pie chart of your top 5 expense categories with percentage and total per category  
- Notifications : in-app notification centre with a badge counter on the sidebar; toast popups appear after each operation  
- Account management : dedicated window to view and manage account settings
- Admin mode for an overview of all accounts.

## Dependencies
Our program uses MySQL and the Python library MySQL Connector.
For any help with MySQL, please consult the official docs : https://dev.mysql.com/doc/
1. Install MySQL
Follow the official installer: https://dev.mysql.com/downloads/installer/
Create a root user and set a password if prompted.
2. Install Python dependencies  
```pip install mysql-connector-python bcrypt customtkinter matplotlib```
3. Create the database user
Open a shell (cmd, PowerShell) and log into MySQL with your root account:  
```mysql -u root -p```  
Enter your password, then run:```CREATE USER 'budget_buddy_test'@'%' IDENTIFIED BY 'strong_password_budget_buddies';
GRANT ALL PRIVILEGES ON *.* TO 'budget_buddy_test'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;``` 
5. Run the app
```python main.py```
Or launch the .exe build find in releases

## Authors
- Cécilia Perana : Front-end
- Adrien Meinier : Transactions
- Nelson Grac-Aubert : Database
