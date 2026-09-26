"""
main.py

This is the single entry point for the ChefBot project.

Run this file to start the app:
    python main.py            -> opens the graphical (Tkinter) chat window
    python main.py --cli      -> runs ChefBot in the terminal instead
"""

import sys

from chef_bot import ChefBot


def start_gui():
    import tkinter as tk
    from gui import ChefBotGUI

    root = tk.Tk()
    bot = ChefBot()
    ChefBotGUI(root, bot)
    root.mainloop()


def start_cli():
    ChefBot().run_cli()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        start_cli()
    else:
        start_gui()
