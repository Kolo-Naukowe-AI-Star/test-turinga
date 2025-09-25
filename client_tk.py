import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from test_turinga import Message

APP_NAME = "Klient Testu Turinga"

PRIMARY_COLOR = "#007ACC"
BG_COLOR = "#F5EEE5"
TEXT_BG = "#FFFFFF" 
TEXT_FG = "#333333"
INFO_COLOR = "#1100FF"

class Client:
    def __init__(self, host: str, port: int):
        self.master = tk.Tk()
        self.master.title(APP_NAME)
        self.master.configure(bg=BG_COLOR)

        header_frame = tk.Frame(self.master, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(5, 0))

        header_frame.grid_columnconfigure(0, weight=1)  # logo 1
        header_frame.grid_columnconfigure(1, weight=1)  # title
        header_frame.grid_columnconfigure(2, weight=1)  # logo 2

        aistar_image = Image.open("images/aistar_logo.png")
        aistar_image = aistar_image.resize((100, 100))
        self.aistar_photo = ImageTk.PhotoImage(aistar_image)
        aistar_label = tk.Label(header_frame, image=self.aistar_photo, bg=BG_COLOR)
        aistar_label.grid(row=0, column=0, sticky="w", padx=(10, 5))

        title_label = tk.Label(
            header_frame,
            text="Klient Testu Turinga",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        )
        title_label.grid(row=0, column=1)

        turing_image = Image.open("images/turing_logo.png")
        turing_image = turing_image.resize((100, 100))
        self.turing_photo = ImageTk.PhotoImage(turing_image)
        turing_label = tk.Label(header_frame, image=self.turing_photo, bg=BG_COLOR)
        turing_label.grid(row=0, column=2, sticky="e", padx=(5, 10))

        self.text_area = scrolledtext.ScrolledText(
            self.master,
            state="disabled",
            width=48,
            height=18,
            bg=TEXT_BG,
            fg=TEXT_FG,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1
        )
        self.text_area.pack(padx=10, pady=10)

        # coloring tags
        self.text_area.tag_config("correct", foreground="green", font=("Segoe UI", 10, "bold"))
        self.text_area.tag_config("wrong", foreground="red", font=("Segoe UI", 10, "bold"))
        self.text_area.tag_config("user", foreground=PRIMARY_COLOR)
        self.text_area.tag_config("partner", foreground="#444444")

        bottom_frame = tk.Frame(self.master, bg=BG_COLOR)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))

        self.entry = tk.Entry(bottom_frame, width=40, font=("Segoe UI", 10))
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            bottom_frame,
            text="Wyślij",
            command=self.send_message,
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground="#005A99",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=3,
            font=("Segoe UI", 10, "bold")
        )
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        # Turn indicator
        self.turn_label = tk.Label(
            bottom_frame,
            text="",
            bg=BG_COLOR,
            fg=PRIMARY_COLOR,
            font=("Segoe UI", 10, "italic")
        )
        self.turn_label.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 10))

        # Frame for decision buttons
        self.decision_frame = tk.Frame(self.master, bg=BG_COLOR)
        self.decision_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.running = True
        self.can_send = True
        self._update_turn_ui(enabled=True)
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_reset(self):
        self.client_socket.sendall(Message("RESET_SESSION").bytes)

        self.append_message("Restartowanie sesji...", tag="info")

        self.text_area.config(state="normal")
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state="disabled")

        for widget in self.decision_frame.winfo_children():
            widget.destroy()
        self.decision_frame.pack_forget() 

    def send_message(self, event: tk.Event | None = None) -> None:
        msg = self.entry.get()
        if msg and self.can_send:
            self.client_socket.sendall(Message(msg).bytes)
            self.entry.delete(0, tk.END)
            self.append_message("Ty: " + msg, tag="user")
            # Disable input if not your turn
            self.can_send = False
            self._update_turn_ui(enabled=False)

    def receive_messages(self) -> None:
        while self.running:
            try:
                msg = Message.read(self.client_socket)
                text = str(msg)

                # Handle optional turn-control messages
                if text.startswith("TURN:"):
                    if text == "TURN:YOU":
                        self.can_send = True
                        self._update_turn_ui(enabled=True)
                    elif text == "TURN:WAIT":
                        self.can_send = False
                        self._update_turn_ui(enabled=False)
                    continue
                # Handle decision message
                if text.startswith("DECISION:"):
                    self.append_message(text.replace("DECISION:", ""))

                    self.can_send = False
                    self._update_turn_ui(enabled=False)

                    self.show_decision_buttons()
                    continue

                # Choice coloring
                if text in ("Correct!", "Wrong!"):
                    if text == "Correct!":
                        self.append_message("Wynik: Poprawnie!", tag="correct")
                    else:
                        self.append_message("Wynik: Źle!", tag="wrong")
                    continue

                self.append_message("Partner: " + text, tag="partner")
            except StopIteration:
                pass

    def send_decision(self, decision: str):
        self.client_socket.sendall(Message(decision).bytes)
        self.append_message(f"Twój wybór: {decision}", tag="user")

        for widget in self.decision_frame.winfo_children():
            widget.destroy()

        reset_button = tk.Button(
            self.decision_frame,
            text="Zacznij od nowa",
            command=self.send_reset,
            width=15,
            bg="#FF6600",
            fg="white",
            relief="flat",
            activebackground="#CC5200",
            activeforeground="white",
            font=("Segoe UI", 10, "bold")
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def show_decision_buttons(self):
        self.decision_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        for widget in self.decision_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.decision_frame,
            text="Kto to był?",
            bg=BG_COLOR,
            fg=INFO_COLOR,
            font=("Segoe UI", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)

        human_button = tk.Button(
            self.decision_frame,
            text="Człowiek",
            command=lambda: self.send_decision("HUMAN"),
            width=10,
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            activebackground="#005A99",
            activeforeground="white",
            font=("Segoe UI", 10, "bold")
        )
        human_button.pack(side=tk.LEFT, padx=5)

        ai_button = tk.Button(
            self.decision_frame,
            text="AI",
            command=lambda: self.send_decision("AI"),
            width=10,
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            activebackground="#005A99",
            activeforeground="white",
            font=("Segoe UI", 10, "bold")
        )
        ai_button.pack(side=tk.LEFT, padx=5)
    def append_message(self, msg: str, tag: str | None = None) -> None:
        self.text_area.config(state="normal")
        if tag:
            self.text_area.insert(tk.END, msg + "\n", tag)
        else:
            self.text_area.insert(tk.END, msg + "\n")
        self.text_area.config(state="disabled")
        self.text_area.see(tk.END)

    def _update_turn_ui(self, *, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.entry.config(state=state)
        self.send_button.config(state=state)
        self.turn_label.config(
            text=("Twoja tura" if enabled else "Poczekaj na swoją turę")
        )

    def on_close(self) -> None:
        self.running = False
        try:
            self.client_socket.close()
        except Exception:
            pass
        self.master.destroy()

    def main(self) -> None:
        self.master.mainloop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host serwera"
    )
    parser.add_argument("--port", type=int, default=5000, help="Port serwera")
    args = parser.parse_args()

    app = Client(args.host, args.port)
    app.main()
