from datetime import datetime
from scripts.logic.database_connection import get_connection

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


def categories_depot() -> list:
    """Catégories réservées aux dépôts (espèces / chèque)."""
    return ["Espèces", "Chèque"]


def get_categorie_id(label: str) -> int:
    """Résout le label d'une catégorie en son id dans OperationCategory.
    Retourne 1 par défaut si non trouvé."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM OperationCategory WHERE label = %s", (label,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 1
    except Exception as e:
        print("Erreur résolution catégorie :", e)
        return 1


def types() -> list:
    return ["Tous", "Débit", "Crédit"]


def tris() -> list:
    return ["Date ↓", "Date ↑", "Montant ↓", "Montant ↑"]