from create_database import main
from logic.login_register import hash_password, check_password, validate_password

class User:
    def __init__(self, id, nom, prenom, email, balance):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.balance = balance

    @staticmethod
    def register(nom, prenom, email, password):
        if not validate_password(password):
            return "Mot de passe invalide"

        hashed = hash_password(password)
        conn = main()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (nom, prenom, email, password) VALUES (%s,%s,%s,%s)",
            (nom, prenom, email, hashed.decode())
        )
        conn.commit()
        conn.close()
        return "Utilisateur créé"

    @staticmethod
    def login(email, password):
        conn = main()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        data = cursor.fetchone()
        conn.close()

        if data and check_password(password, data["password"]):
            return User(data["id"], data["nom"], data["prenom"], data["email"], data["balance"])
        return None

    def update_balance(self, amount):
        self.balance += amount
        conn = main()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance=%s WHERE id=%s", (self.balance, self.id))
        conn.commit()
        conn.close()