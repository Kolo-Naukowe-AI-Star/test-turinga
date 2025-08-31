import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

from test_turinga.message import Message

APP_NAME = "Test Turinga Client"


class Client:
    def __init__(self, host: str, port: int):
        self.master = tk.Tk()
        self.master.title(APP_NAME)

        self.text_area = scrolledtext.ScrolledText(
            self.master, state="disabled", width=50, height=20
        )
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.master, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.master, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        # Turn indicator
        self.turn_label = tk.Label(self.master, text="")
        self.turn_label.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 10))

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.running = True
        self.can_send = True
        self._update_turn_ui(enabled=True)
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self, event: tk.Event | None = None) -> None:
        msg = self.entry.get()
        if msg and self.can_send:
            self.client_socket.sendall(Message(msg).bytes)
            self.entry.delete(0, tk.END)
            self.append_message("You: " + msg)
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
                self.append_message("Partner: " + text)
            except StopIteration:
                self.on_close()

    def append_message(self, msg: str) -> None:
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.config(state="disabled")
        self.text_area.see(tk.END)

    def _update_turn_ui(self, *, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.entry.config(state=state)
        self.send_button.config(state=state)
        self.turn_label.config(text=("Your turn" if enabled else "Wait for your turn"))

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
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    args = parser.parse_args()

    app = Client(args.host, args.port)
    app.main()
