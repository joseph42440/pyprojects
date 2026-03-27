import tkinter as tk
from PIL import Image, ImageTk
from playsound3 import playsound

BOARD_SIZE = 8

# Board setup (uppercase = white, lowercase = black)
INITIAL_BOARD = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"],
]

# Mapping pieces to filenames
PIECE_IMAGES = {
    "P": "icons/white_p.png",
    "R": "icons/white_r.png",
    "N": "icons/white_n.png",
    "B": "icons/white_b.png",
    "Q": "icons/white_q.png",
    "K": "icons/white_k.png",
    "p": "icons/black_p.png",
    "r": "icons/black_r.png",
    "n": "icons/black_n.png",
    "b": "icons/black_b.png",
    "q": "icons/black_q.png",
    "k": "icons/black_k.png",
}

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.board = [row[:] for row in INITIAL_BOARD]
        self.selected_r = None
        self.selected_c = None

        # Load images
        self.original_images = {}
        for piece, path in PIECE_IMAGES.items():
            img = Image.open(path).convert("RGBA")
            self.original_images[piece] = img

        self.images = {}  # will store resized ImageTk.PhotoImage

        # Event bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Configure>", self.on_resize)

        self.SQUARE_SIZE = 80  # initial
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1, y1 = c*self.SQUARE_SIZE, r*self.SQUARE_SIZE
                x2, y2 = x1+self.SQUARE_SIZE, y1+self.SQUARE_SIZE
                color = "#EEEED2" if (r+c)%2==0 else "#769656"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board[r][c]
                if piece:
                    if piece in self.images:
                        self.canvas.create_image(
                            x1+self.SQUARE_SIZE//2,
                            y1+self.SQUARE_SIZE//2,
                            image=self.images[piece]
                        )
                    else:
                        self.canvas.create_text(
                            x1+self.SQUARE_SIZE//2,
                            y1+self.SQUARE_SIZE//2,
                            text=piece,
                            font=("Arial", int(self.SQUARE_SIZE/2))
                        )

        # highlight selected square
        if self.selected_r is not None and self.selected_c is not None:
            self.canvas.create_rectangle(
                self.selected_c*self.SQUARE_SIZE, self.selected_r*self.SQUARE_SIZE,
                (self.selected_c+1)*self.SQUARE_SIZE, (self.selected_r+1)*self.SQUARE_SIZE,
                outline="red", width=3
            )

    def on_click(self, event):
        c = int(event.x // self.SQUARE_SIZE)
        r = int(event.y // self.SQUARE_SIZE)
        if not (0 <= r < 8 and 0 <= c < 8):
            return

        if self.selected_r is None or self.selected_c is None:
            if self.board[r][c] != "":
                self.selected_r = r
                self.selected_c = c
        else:
            fr, fc = self.selected_r, self.selected_c
            tr, tc = r, c
            if is_valid_move(self.board, fr, fc, tr, tc):
                if self.board[tr][tc] == "":
                    playsound("sfx/move.mp3", block=False)
                else:
                    playsound("sfx/capture.mp3", block=False)
                self.board[tr][tc] = self.board[fr][fc]
                self.board[fr][fc] = ""
            else:
                playsound("sfx/illegal.mp3", block=False)

            self.selected_r = None
            self.selected_c = None

        self.draw_board()

    def on_resize(self, event):
        # compute new square size
        self.SQUARE_SIZE = min(event.width, event.height) / BOARD_SIZE

        # resize images
        self.images.clear()
        for piece, img in self.original_images.items():
            resized = img.resize((int(self.SQUARE_SIZE-10), int(self.SQUARE_SIZE-10)), Image.Resampling.LANCZOS)
            self.images[piece] = ImageTk.PhotoImage(resized)

        self.draw_board()


# ---------------- MOVE LOGIC ---------------- #
def is_valid_move(board, fr, fc, tr, tc):
    """Allow all moves (replace with rules later)"""
    return True


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Diva Chess")
    root.geometry("640x640")
    app = ChessGUI(root)
    root.mainloop()