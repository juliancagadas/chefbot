"""
gui.py

This file defines ChefBotGUI, a Tkinter window that wraps a ChefBot
instance in a simple chat interface.

Job of this class (single responsibility):
    - Draw the window, chat area, entry box, and buttons.
    - Turn button clicks / Enter key presses into calls to
      chefbot.process_message(...).
    - Display the conversation using the orange color theme.

Notice this class does NOT know anything about intents, recipes, or
NLP -- it only calls one method on ChefBot and displays the string it
gets back. That is the point of OOP separation: the GUI is just a
"front door", and all the thinking happens elsewhere.
"""

import tkinter as tk
from tkinter import font as tkfont

# ----------------------------------------------------------------------
# COLOR THEME (matches the orange, cooking-inspired palette)
# ----------------------------------------------------------------------
PRIMARY_ORANGE = "#F28C28"
DARK_ORANGE = "#D96B0B"
BACKGROUND = "#FFF8F0"
CARD_WHITE = "#FFFFFF"
TEXT_PRIMARY = "#2B2118"
TEXT_SECONDARY = "#7A6656"
USER_BUBBLE = "#F28C28"
BOT_BUBBLE = "#FFE4C7"


class ChefBotGUI:
    """A Tkinter chat window for talking to a ChefBot instance."""

    def __init__(self, root, chefbot):
        self.chefbot = chefbot
        self.root = root

        self.root.title("ChefBot 👨‍🍳")
        self.root.configure(bg=BACKGROUND)
        self.root.geometry("700x800")
        self.root.minsize(500, 600)

        self._build_header()
        self._build_chat_area()
        self._build_input_area()

        self._show_bot_message(
            "Yo! 👨‍🍳 What's cooking today? Need ingredients, a recipe, or just wanna talk food?"
        )

    # ------------------------------------------------------------------
    # UI CONSTRUCTION
    # ------------------------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self.root, bg=PRIMARY_ORANGE, height=64)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        tk.Label(
            header,
            text="👨‍🍳 ChefBot",
            bg=PRIMARY_ORANGE,
            fg="white",
            font=title_font,
        ).pack(side="left", padx=16)

        exit_button = tk.Button(
            header,
            text="Exit",
            command=self.root.destroy,
            bg=DARK_ORANGE,
            fg="white",
            activebackground=DARK_ORANGE,
            activeforeground="white",
            relief="flat",
            padx=10,
        )
        exit_button.pack(side="right", padx=16)

    def _build_chat_area(self):
        chat_frame = tk.Frame(self.root, bg=BACKGROUND)
        chat_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side="right", fill="y")

        self.chat_display = tk.Text(
            chat_frame,
            bg=CARD_WHITE,
            fg=TEXT_PRIMARY,
            wrap="word",
            state="disabled",
            font=("Helvetica", 11),
            padx=10,
            pady=10,
            relief="flat",
            yscrollcommand=scrollbar.set,
        )
        self.chat_display.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.chat_display.yview)

        # Text "tags" let us style specific chunks of text differently,
        # which is how we create the two different chat bubble colors.
        self.chat_display.tag_configure(
            "user", background=USER_BUBBLE, foreground="white",
            justify="right", spacing1=6, spacing3=6, lmargin1=80, rmargin=10,
        )
        self.chat_display.tag_configure(
            "bot", background=BOT_BUBBLE, foreground=TEXT_PRIMARY,
            justify="left", spacing1=6, spacing3=6, rmargin=80, lmargin1=10,
        )
        self.chat_display.tag_configure(
            "label", foreground=TEXT_SECONDARY, font=("Helvetica", 8, "italic"),
        )

    def _build_input_area(self):
        input_frame = tk.Frame(self.root, bg=BACKGROUND)
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            relief="flat",
            highlightthickness=1,
            highlightbackground=DARK_ORANGE,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()

        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self._on_send,
            bg=PRIMARY_ORANGE,
            fg="white",
            activebackground=DARK_ORANGE,
            activeforeground="white",
            relief="flat",
            padx=16,
        )
        send_button.pack(side="right")

    # ------------------------------------------------------------------
    # EVENT HANDLING
    # ------------------------------------------------------------------

    def _on_send(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, "end")
        self._show_user_message(user_text)

        reply = self.chefbot.process_message(user_text)
        self._show_bot_message(reply)

        if not self.chefbot.is_running:
            self.entry.config(state="disabled")

    # ------------------------------------------------------------------
    # DISPLAY HELPERS
    # ------------------------------------------------------------------

    def _show_user_message(self, text):
        self._append_message("You", text, "user")

    def _show_bot_message(self, text):
        self._append_message("ChefBot", text, "bot")

    def _append_message(self, sender, text, tag):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{sender}\n", "label")
        self.chat_display.insert("end", f"{text}\n\n", tag)
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
