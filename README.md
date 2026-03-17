# budget-buddy
A lightweight budget manager app made for La Plateforme_ IT school. Made by Adrien Meinier, Cécilia Perana and Nelson Grac-Aubert. 

## Dependancies

Our program uses MySQL and the Python Library MySQL Connector. 

Install MySQL following https://dev.mysql.com/downloads/installer/

In a MySQL Shell using the root user, create a user that will be used by our programm to manipulate the Budget Buddy database : 

```bash
CREATE USER 'budget_buddy_test'@'%' IDENTIFIED BY 'strong_password_budget_buddies';
GRANT ALL PRIVILEGES ON astérisque.astérisque TO 'budget_buddy_test'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
