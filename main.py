from scripts.graphic.config import apply_appearance
from scripts.graphic.app import BudgetBuddyApp

if __name__ == "__main__":
    apply_appearance()
    app = BudgetBuddyApp()
    app.mainloop()
