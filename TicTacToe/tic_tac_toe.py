import tkinter as tk
import pygame
import random

# ---------------- Music ----------------
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
music_on = True


def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.unpause()
        mute_button.config(text="🔊")
    else:
        pygame.mixer.music.pause()
        mute_button.config(text="🔇")


# ---------------- Window ----------------
root = tk.Tk()
root.title("Tic Tac Toe - Neon Arcade")
root.geometry("700x800")
root.resizable(False, False)

# ---------------- Styles ----------------
TITLE_FONT = ("Consolas", 32, "bold")
MENU_FONT = ("Consolas", 18, "bold")
DESC_FONT = ("Consolas", 16)
BUTTON_BG = "#111111"
BUTTON_FG = "#ffffff"
X_COLOR = "#00ffff"
O_COLOR = "#ff00ff"
RESULT_COLOR = "#ff3399"

board = [""] * 9
buttons = []
current_turn = "X"

# ---------------- Neon Background Animation ----------------
colors = ["#0d0d0d", "#1a0d1a", "#0d1a1a", "#1a001a", "#1a0d0d"]
color_index = 0


def animate_bg():
    global color_index
    root.configure(bg=colors[color_index])
    color_index = (color_index + 1) % len(colors)
    root.after(300, animate_bg)


animate_bg()


# ---------------- Helper Functions ----------------
def check_winner():
    combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in combos:
        if board[a] == board[b] == board[c] != "": return board[a]
    if "" not in board: return "Draw"
    return None


def update_button(i, player):
    color = X_COLOR if player == "X" else O_COLOR

    def pulse(count=0):
        if count < 6:
            buttons[i].config(fg=color if count % 2 == 0 else "#0d0d0d")
            buttons[i].after(100, lambda: pulse(count + 1))

    buttons[i].config(text=player, state="disabled")
    pulse()


# ---------------- Computer AI ----------------
def computer_move():
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner() == "O":
                update_button(i, "O")
                return
            board[i] = ""
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner() == "X":
                board[i] = "O"
                update_button(i, "O")
                return
            board[i] = ""
    if board[4] == "": board[4] = "O"; update_button(4, "O"); return
    for i in [0, 2, 6, 8]:
        if board[i] == "": board[i] = "O"; update_button(i, "O"); return
    for i in [1, 3, 5, 7]:
        if board[i] == "": board[i] = "O"; update_button(i, "O"); return


# ---------------- Make Move ----------------
def make_move(i, mode):
    global current_turn
    if board[i] == "":
        if mode == "Friend":
            board[i] = current_turn
            update_button(i, current_turn)
            current_turn = "O" if current_turn == "X" else "X"
        else:
            board[i] = "X"
            update_button(i, "X")
            winner = check_winner()
            if winner: end_game(winner); return
            computer_move()
    winner = check_winner()
    if winner: end_game(winner)


# ---------------- End Game ----------------
def end_game(winner):
    result = "Draw!" if winner == "Draw" else f"{winner} Wins!"
    result_label.config(text=result)
    for b in buttons: b.config(state="disabled")


# ---------------- Hover Effect ----------------
def add_hover(button, hover_bg, normal_bg, hover_fg, normal_fg):
    button.bind("<Enter>", lambda e: button.config(bg=hover_bg, fg=hover_fg))
    button.bind("<Leave>", lambda e: button.config(bg=normal_bg, fg=normal_fg))


# ---------------- Place Mute Button ----------------
def place_mute_button():
    global mute_button
    mute_button = tk.Button(root, text="🔊", font=("Arial", 28), bg=root["bg"], fg="#00ffff", bd=0, command=toggle_music)
    mute_button.place(x=620, y=20)


# ---------------- Welcome Page ----------------
def welcome_page():
    for w in root.winfo_children(): w.destroy()
    title = tk.Label(root, text="Welcome to Tic Tac Toe!", font=TITLE_FONT, fg="#00ffff", bg=root["bg"])
    title.pack(pady=30)
    desc = tk.Label(root, text="Neon Arcade Theme\nPlay vs Computer or Friend", font=DESC_FONT, fg="#ffffff",
                    bg=root["bg"])
    desc.pack(pady=20)
    info = tk.Label(root, text="Click Start to enter menu", font=("Consolas", 14, "italic"), fg="#00bfff",
                    bg=root["bg"])
    info.pack(pady=20)
    start_btn = tk.Button(root, text="Start Game", font=MENU_FONT, width=20, bg=BUTTON_BG, fg=BUTTON_FG,
                          command=open_menu)
    start_btn.pack(pady=40)
    add_hover(start_btn, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)
    place_mute_button()


# ---------------- Menu ----------------
def open_menu():
    for w in root.winfo_children(): w.destroy()
    menu_label = tk.Label(root, text="Choose an Option", font=TITLE_FONT, fg="#00ffff", bg=root["bg"])
    menu_label.pack(pady=40)

    btn1 = tk.Button(root, text="Play with Computer", font=MENU_FONT, width=25, bg=BUTTON_BG, fg=BUTTON_FG,
                     command=lambda: start_game("Computer"))
    btn1.pack(pady=15)
    add_hover(btn1, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)

    btn2 = tk.Button(root, text="Play with Friend", font=MENU_FONT, width=25, bg=BUTTON_BG, fg=BUTTON_FG,
                     command=lambda: start_game("Friend"))
    btn2.pack(pady=15)
    add_hover(btn2, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)

    btn3 = tk.Button(root, text="Exit", font=MENU_FONT, width=25, bg=BUTTON_BG, fg=BUTTON_FG, command=root.destroy)
    btn3.pack(pady=15)
    add_hover(btn3, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)
    place_mute_button()


# ---------------- Start Game ----------------
def start_game(mode):
    global board, buttons, current_turn
    current_turn = "X"
    board = [""] * 9
    buttons = []
    for w in root.winfo_children(): w.destroy()

    title = tk.Label(root, text=f"Tic Tac Toe - {mode}", font=TITLE_FONT, fg="#00ffff", bg=root["bg"])
    title.pack(pady=20)

    grid = tk.Frame(root, bg="#0d0d0d", highlightbackground="#ff00ff", highlightthickness=5)  # Neon glowing border
    grid.pack(pady=10)

    for i in range(9):
        b = tk.Button(grid, text="", font=("Consolas", 28, "bold"), width=5, height=2,
                      bg="#0d0d0d", fg="#0d0d0d", highlightbackground="#00ffff", highlightthickness=2,
                      command=lambda i=i: make_move(i, mode))
        b.grid(row=i // 3, column=i % 3, padx=8, pady=8)
        buttons.append(b)

    global result_label
    result_label = tk.Label(root, text="", font=("Consolas", 22, "bold"), fg=RESULT_COLOR, bg=root["bg"])
    result_label.pack(pady=20)

    restart_btn = tk.Button(root, text="Restart", font=MENU_FONT, width=20, bg=BUTTON_BG, fg=BUTTON_FG,
                            command=lambda: start_game(mode))
    restart_btn.pack(pady=10)
    add_hover(restart_btn, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)

    back_btn = tk.Button(root, text="Back to Menu", font=MENU_FONT, width=20, bg=BUTTON_BG, fg=BUTTON_FG,
                         command=open_menu)
    back_btn.pack(pady=10)
    add_hover(back_btn, "#00ffff", BUTTON_BG, "#0d0d0d", BUTTON_FG)

    place_mute_button()


# ---------------- Run ----------------
welcome_page()
root.mainloop()
