import sys
from scripts.graphic.config import apply_appearance
from scripts.graphic.app import BudgetBuddyApp
from scripts.logic.initialize import initialize_all


if __name__ == "__main__":

    # Ensure the database, tables, and reference data exist before the UI
    # starts. This is a no-op on all subsequent launches once everything
    # is already in place.
    db_ready = initialize_all()

    if not db_ready:
        # MySQL is unreachable — show a plain-text error and exit cleanly
        # rather than letting the app open and crash later on the first query.
        print(
            "\n[FATAL] Cannot connect to MySQL.\n"
            "Please make sure the MySQL server is running and that the user\n"
            "'budget_buddy_test' exists with the correct password.\n"
            "See README.md for setup instructions."
        )
        sys.exit(1)

    apply_appearance()
    app = BudgetBuddyApp()
    app.mainloop()