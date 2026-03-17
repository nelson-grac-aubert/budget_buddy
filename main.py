from script.graphic.config import apply_appearance
from script.graphic.app import BudgetBuddyApp

if __name__ == "__main__":
    apply_appearance()
    app = BudgetBuddyApp()
    app.mainloop()