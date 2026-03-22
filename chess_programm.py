import chess
import chess.svg
from PIL import Image, ImageTk
import cairosvg
import io
import tkinter as tk
from tkinter import Canvas

# Chemin des images des pièces
piece_images = {
    'P': 'white_pawn.png',
    'N': 'white_knight.png',
    'B': 'white_bishop.png',
    'R': 'white_rook.png',
    'Q': 'white_queen.png',
    'K': 'white_king.png',
    'p': 'black_pawn.png',
    'n': 'black_knight.png',
    'b': 'black_bishop.png',
    'r': 'black_rook.png',
    'q': 'black_queen.png',
    'k': 'black_king.png'
}

def create_image_from_svg(svg_data):
    """ Convertit les données SVG en image PNG. """
    png_data = cairosvg.svg2png(bytestring=svg_data)
    image = Image.open(io.BytesIO(png_data))
    return image

def draw_board(canvas, board):
    """ Dessine l'échiquier et les pièces sur le canevas Tkinter. """
    board_svg = chess.svg.board(board=board, size=400)
    board_image = create_image_from_svg(board_svg.encode('utf-8'))
    canvas.image = ImageTk.PhotoImage(board_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def on_click(event, board, canvas):
    """ Gère le clic de souris pour déplacer les pièces. """
    global last_square
    col = event.x // 50
    row = 7 - (event.y // 50)
    square = chess.square(col, row)
    square_name = chess.square_name(square)

    if last_square:
        move = chess.Move.from_uci(f"{last_square}{square_name}")
        if move in board.legal_moves:
            board.push(move)
            last_square = ""
            draw_board(canvas, board)
        else:
            last_square = square_name
    else:
        last_square = square_name

def setup_board():
    """ Configure l'échiquier et l'interface graphique. """
    global last_square
    last_square = ""

    root = tk.Tk()
    root.title("Échiquier d'échecs")

    # Crée l'échiquier
    board = chess.Board()

    # Configure le canevas pour dessiner l'échiquier
    canvas = Canvas(root, width=400, height=400)
    canvas.pack()

    draw_board(canvas, board)

    # Associe l'événement de clic à la fonction de gestion des clics
    canvas.bind("<Button-1>", lambda event: on_click(event, board, canvas))

    root.mainloop()

# Exécute l'application
setup_board()



