from datetime import datetime

#todo : a enlever quand on aura une vraie base de données, et remplacer les appels à ces fonctions par des imports depuis la base de données
def get_transactions(user_id=1):
    return [
        {"date": "14/12/2020", "description": "Courses Carrefour",        "categorie": "Courses",      "type": "Débit",  "montant": -52.30},
        {"date": "14/11/2020", "description": "Restaurant Le Bistrot",    "categorie": "Restaurants",  "type": "Débit",  "montant": -32.00},
        {"date": "01/10/2020", "description": "Loyer octobre",            "categorie": "Loyer",        "type": "Débit",  "montant": -750.00},
        {"date": "13/07/2020", "description": "Pharmacie",                "categorie": "Santé",        "type": "Débit",  "montant": -18.50},
        {"date": "16/12/2020", "description": "Paiement Netflix",         "categorie": "Abonnements",  "type": "Débit",  "montant": -13.99},
        {"date": "01/07/2020", "description": "Virement salaire juillet", "categorie": "Salaire",      "type": "Crédit", "montant":  1800.00},
        {"date": "16/04/2021", "description": "Virement salaire avril",   "categorie": "Salaire",      "type": "Crédit", "montant":  1800.00},
        {"date": "08/01/2021", "description": "Remboursement frais",      "categorie": "Santé",        "type": "Crédit", "montant":  45.00},
        {"date": "06/07/2020", "description": "Freelance mission",        "categorie": "Revenus",      "type": "Crédit", "montant":  320.00},
        {"date": "16/11/2020", "description": "Virement ami",             "categorie": "Loisirs",      "type": "Crédit", "montant":  20.00},
        {"date": "03/08/2020", "description": "Prime vacances",           "categorie": "Revenus",      "type": "Crédit", "montant":  150.00},
        {"date": "11/11/2020", "description": "Remboursement sécu.",      "categorie": "Santé",        "type": "Crédit", "montant":  6.94},
        {"date": "15/03/2021", "description": "Cinéma UGC",              "categorie": "Loisirs",      "type": "Débit",  "montant": -22.00},
        {"date": "20/02/2021", "description": "Essence Total",            "categorie": "Transport",    "type": "Débit",  "montant": -60.00},
        {"date": "05/01/2021", "description": "Abonnement Spotify",       "categorie": "Abonnements",  "type": "Débit",  "montant": -9.99},
    ]


def pie_color(categorie: str) -> str:
    return {
        "Loyer":       "#7c3aed",
        "Courses":     "#0d9488",
        "Restaurants": "#f59e0b",
        "Abonnements": "#3b82f6",
        "Transport":   "#ef4444",
        "Santé":       "#22c55e",
        "Loisirs":     "#ec4899",
        "Salaire":     "#6366f1",
        "Revenus":     "#14b8a6",
    }.get(categorie, "#888888")


def parse_date(s: str):
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except Exception:
        return datetime.min


def col(key: str) -> str:
    return {
        "header":    "#1a7a7a",
        "row_odd":   "#1e2a2a",
        "row_even":  "#162020",
        "bold":      "#0d3030",
        "debit":     "#ef4444",
        "credit":    "#22c55e",
        "head":      "#ffffff",
        "normal":    "#d1d5db",
        "gray":      "#9ca3af",
    }[key]


def categories() -> list:
    return ["Toutes", "Loyer", "Courses", "Restaurants", "Abonnements",
            "Transport", "Santé", "Loisirs", "Salaire", "Revenus"]


def types() -> list:
    return ["Tous", "Débit", "Crédit"]


def tris() -> list:
    return ["Date ↓", "Date ↑", "Montant ↓", "Montant ↑"]