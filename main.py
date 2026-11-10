import tkinter as tk
from src.app import TetrisApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TetrisApp(root)
    root.mainloop()
