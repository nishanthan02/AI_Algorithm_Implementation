import tkinter as tk
from tkinter import font as tkfont
import random
import math

# --- GAME STATE ---
board = [""] * 9
current_player = "X"
player_symbol = "X"
ai_symbol = "O"
mode = "single"
game_over = False

# --- NEON COLOR PALETTE ---
BG_DARK    = "#0a0a1a"
BG_MID     = "#12122a"
NEON_PINK  = "#ff2d78"
NEON_CYAN  = "#00f5ff"
NEON_YELLOW= "#fff700"
NEON_GREEN = "#39ff14"
NEON_ORANGE= "#ff6600"
CARD_BG    = "#1a1a35"
BTN_IDLE   = "#1e1e40"

root = tk.Tk()
root.title("🎰 CHAOS TIC TAC TOE 🎰")
root.geometry("480x700")
root.configure(bg=BG_DARK)
root.resizable(False, False)

# --- FONTS ---
try:
    title_font  = tkfont.Font(family="Impact", size=28, weight="bold")
    cell_font   = tkfont.Font(family="Impact", size=36, weight="bold")
    btn_font    = tkfont.Font(family="Courier", size=11, weight="bold")
    status_font = tkfont.Font(family="Courier", size=13, weight="bold")
    small_font  = tkfont.Font(family="Courier", size=9)
except:
    title_font  = tkfont.Font(size=22, weight="bold")
    cell_font   = tkfont.Font(size=32, weight="bold")
    btn_font    = tkfont.Font(size=10, weight="bold")
    status_font = tkfont.Font(size=12, weight="bold")
    small_font  = tkfont.Font(size=9)

# ── SCANLINE CANVAS BACKGROUND ──────────────────────────────────────────────
bg_canvas = tk.Canvas(root, width=480, height=700, bg=BG_DARK,
                      highlightthickness=0)
bg_canvas.place(x=0, y=0)

def draw_scanlines():
    bg_canvas.delete("scanline")
    for y in range(0, 700, 4):
        bg_canvas.create_line(0, y, 480, y, fill="#111128", tags="scanline")

draw_scanlines()

# ── GLOWING TITLE ────────────────────────────────────────────────────────────
title_canvas = tk.Canvas(root, width=480, height=70, bg=BG_DARK,
                         highlightthickness=0)
title_canvas.place(x=0, y=5)

def draw_title(color1=NEON_PINK, color2=NEON_CYAN):
    title_canvas.delete("all")
    # glow layers
    for offset, alpha in [(4,"#551133"),(2,"#aa2255"),(0,color1)]:
        title_canvas.create_text(240+offset, 36+offset,
            text="★ CHAOS TIC TAC TOE ★",
            font=title_font, fill=alpha, anchor="center")
    title_canvas.create_text(240, 36,
        text="★ CHAOS TIC TAC TOE ★",
        font=title_font, fill=color1, anchor="center")

draw_title()

# Title flicker animation
_title_colors = [NEON_PINK, NEON_CYAN, NEON_YELLOW, NEON_GREEN, NEON_ORANGE]
_tc_idx = [0]
def flicker_title():
    _tc_idx[0] = (_tc_idx[0] + 1) % len(_title_colors)
    draw_title(_title_colors[_tc_idx[0]])
    root.after(600 + random.randint(0, 400), flicker_title)
root.after(800, flicker_title)

# ── STATUS BAR ───────────────────────────────────────────────────────────────
status_frame = tk.Frame(root, bg=BG_MID, bd=0, relief="flat",
                        highlightbackground=NEON_CYAN, highlightthickness=2)
status_frame.place(x=20, y=78, width=440, height=42)

status_label = tk.Label(status_frame,
    text="🕹️  SELECT MODE  🕹️",
    font=status_font, bg=BG_MID, fg=NEON_YELLOW,
    wraplength=430)
status_label.pack(expand=True, fill="both", padx=6, pady=4)

# ── SCORE DISPLAY ────────────────────────────────────────────────────────────
score_frame = tk.Frame(root, bg=BG_DARK)
score_frame.place(x=20, y=128, width=440, height=38)

score_x_var = tk.StringVar(value="X: 0")
score_o_var = tk.StringVar(value="O: 0")
score_x = 0
score_o = 0

tk.Label(score_frame, textvariable=score_x_var,
         font=btn_font, bg=BG_DARK, fg=NEON_PINK, width=8).pack(side="left", padx=10)

tk.Label(score_frame, text="VS",
         font=btn_font, bg=BG_DARK, fg=NEON_YELLOW).pack(side="left", expand=True)

tk.Label(score_frame, textvariable=score_o_var,
         font=btn_font, bg=BG_DARK, fg=NEON_CYAN, width=8).pack(side="right", padx=10)

# ── GAME BOARD ───────────────────────────────────────────────────────────────
board_canvas = tk.Canvas(root, width=360, height=360, bg=CARD_BG,
                         highlightbackground=NEON_PINK, highlightthickness=3,
                         cursor="crosshair")
board_canvas.place(x=60, y=170)

CELL_SIZE = 120

def draw_board_grid():
    board_canvas.delete("grid")
    for i in [1, 2]:
        board_canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, 360,
            fill=NEON_CYAN, width=3, dash=(8,4), tags="grid")
        board_canvas.create_line(0, i*CELL_SIZE, 360, i*CELL_SIZE,
            fill=NEON_CYAN, width=3, dash=(8,4), tags="grid")

def draw_cell_symbols():
    board_canvas.delete("symbol")
    for idx, val in enumerate(board):
        if not val:
            continue
        r, c = divmod(idx, 3)
        cx = c * CELL_SIZE + CELL_SIZE // 2
        cy = r * CELL_SIZE + CELL_SIZE // 2
        color = NEON_PINK if val == "X" else NEON_CYAN
        symbol = "✕" if val == "X" else "◉"
        # glow
        board_canvas.create_text(cx+2, cy+2, text=symbol, font=cell_font,
            fill="#000033", tags="symbol")
        board_canvas.create_text(cx, cy, text=symbol, font=cell_font,
            fill=color, tags="symbol")

def get_cell(x, y):
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if 0 <= col < 3 and 0 <= row < 3:
        return row * 3 + col
    return None

draw_board_grid()

# ── WIN CONDITIONS ────────────────────────────────────────────────────────────
wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_winner(b, p):
    for combo in wins:
        if all(b[i] == p for i in combo):
            return combo
    return None

def is_draw():
    return "" not in board

def draw_win_line(combo):
    board_canvas.delete("winline")
    positions = []
    for idx in combo:
        r, c = divmod(idx, 3)
        positions.append((c * CELL_SIZE + CELL_SIZE // 2,
                          r * CELL_SIZE + CELL_SIZE // 2))
    x1, y1 = positions[0]
    x2, y2 = positions[2]
    
    # Draw the layered glowing line
    for offset in [4, 2, 0]:
        # FIXED: Replaced "#fff70033" with a standard dark yellow "#888800"
        line_color = NEON_YELLOW if offset == 0 else "#888800" 
        board_canvas.create_line(x1, y1, x2, y2,
            fill=line_color,
            width=6 - offset*1.5,
            capstyle="round", tags="winline")

# ── MINIMAX ───────────────────────────────────────────────────────────────────
def minimax(b, maximizing):
    if check_winner(b, ai_symbol):
        return 1
    if check_winner(b, player_symbol):
        return -1
    if "" not in b:
        return 0
    if maximizing:
        best = -999
        for i in range(9):
            if b[i] == "":
                b[i] = ai_symbol
                best = max(best, minimax(b, False))
                b[i] = ""
        return best
    else:
        best = 999
        for i in range(9):
            if b[i] == "":
                b[i] = player_symbol
                best = min(best, minimax(b, True))
                b[i] = ""
        return best

def best_move():
    best_score = -999
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = ai_symbol
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# ── CLICK HANDLER ─────────────────────────────────────────────────────────────
def on_board_click(event):
    global current_player, game_over
    if game_over:
        return
    idx = get_cell(event.x, event.y)
    if idx is None or board[idx] != "":
        return
    board[idx] = current_player
    draw_cell_symbols()
    combo = check_winner(board, current_player)
    if combo:
        draw_win_line(combo)
        funny_win(current_player)
        game_over = True
        return
    if is_draw():
        set_status("😐 DRAW! Both of you are equally bad!", NEON_YELLOW)
        game_over = True
        return
    if mode == "single":
        root.after(300, ai_turn)
    else:
        current_player = "O" if current_player == "X" else "X"
        emoji = "🩷" if current_player == "X" else "💠"
        set_status(f"{emoji} Player {current_player}'s turn — NO PRESSURE!", NEON_GREEN)

board_canvas.bind("<Button-1>", on_board_click)

# cursor hover glow
def on_hover(event):
    idx = get_cell(event.x, event.y)
    board_canvas.delete("hover")
    if idx is not None and board[idx] == "" and not game_over:
        r, c = divmod(idx, 3)
        x0, y0 = c*CELL_SIZE+6, r*CELL_SIZE+6
        x1, y1 = x0+CELL_SIZE-12, y0+CELL_SIZE-12
        board_canvas.create_rectangle(x0, y0, x1, y1,
            outline=NEON_YELLOW, width=2, dash=(4,3), tags="hover")

board_canvas.bind("<Motion>", on_hover)

# ── AI TURN ───────────────────────────────────────────────────────────────────
def ai_turn():
    global game_over
    move = best_move()
    if move is not None:
        board[move] = ai_symbol
        draw_cell_symbols()
        combo = check_winner(board, ai_symbol)
        if combo:
            draw_win_line(combo)
            set_status("🤖 AI goes BRRR! You got cooked!", NEON_CYAN)
            update_score(ai_symbol) # Fixed to update correct symbol score
            game_over = True
            return
        if is_draw():
            set_status("🤝 Draw! AI is being NICE today!", NEON_YELLOW)
            game_over = True
            return
        set_status("🎯 YOUR TURN. Don't embarrass yourself!", NEON_PINK)

# ── WIN / SCORE ────────────────────────────────────────────────────────────────
WIN_MSGS = [
    "🎉 {p} WINS! Opponent: touch grass!",
    "🔥 {p} is ON FIRE! GGs only!",
    "😂 {p} just rekt the battlefield!",
    "👑 ALL HAIL {p}, the TicTac KING!",
    "⚡ {p} speedran victory. EZ CLAP!",
    "🏆 {p} wins! Loser buys snacks!",
]

def funny_win(player):
    msg = random.choice(WIN_MSGS).format(p=player)
    color = NEON_PINK if player == "X" else NEON_CYAN
    set_status(msg, color)
    update_score(player)
    flash_board(color)

def update_score(winner):
    global score_x, score_o
    if winner == "X":
        score_x += 1
        score_x_var.set(f"✕ : {score_x}")
    else:
        score_o += 1
        score_o_var.set(f"◉ : {score_o}")

def flash_board(color, times=6):
    if times <= 0:
        board_canvas.configure(highlightbackground=NEON_PINK)
        return
    c = color if times % 2 == 0 else BG_MID
    board_canvas.configure(highlightbackground=c)
    root.after(120, lambda: flash_board(color, times-1))

def set_status(text, color=NEON_YELLOW):
    status_label.config(text=text, fg=color)

# ── RESET ──────────────────────────────────────────────────────────────────────
def reset():
    global board, current_player, game_over
    board = [""] * 9
    current_player = player_symbol
    game_over = False
    board_canvas.delete("symbol", "winline", "hover")
    draw_board_grid()
    set_status("🕹️  NEW ROUND — FIGHT!  🕹️", NEON_GREEN)
    board_canvas.configure(highlightbackground=NEON_PINK)

# ── MODE / SYMBOL BUTTONS ──────────────────────────────────────────────────────
ctrl_frame = tk.Frame(root, bg=BG_DARK)
ctrl_frame.place(x=20, y=545, width=440, height=90)

def neon_btn(parent, text, cmd, fg, row, col):
    btn = tk.Button(parent, text=text, command=cmd,
        font=btn_font, bg=BTN_IDLE, fg=fg,
        activebackground=fg, activeforeground=BG_DARK,
        relief="flat", cursor="hand2", bd=0,
        highlightthickness=2, highlightbackground=fg,
        padx=6, pady=5)
    btn.grid(row=row, column=col, padx=5, pady=4, sticky="ew")
    return btn

ctrl_frame.columnconfigure((0,1,2,3), weight=1)

def set_mode(m):
    global mode
    mode = m
    label = "🤖 vs AI" if m == "single" else "👬 2 Players"
    set_status(f"Mode: {label}. Pick your symbol!", NEON_CYAN)

def set_symbol(s):
    global player_symbol, ai_symbol
    player_symbol = s
    ai_symbol = "O" if s == "X" else "X"
    reset()
    set_status(f"You're {'✕' if s == 'X' else '◉'}! Let the chaos begin!", NEON_GREEN)

neon_btn(ctrl_frame, "🤖  AI MODE",   lambda: set_mode("single"), NEON_CYAN,   0, 0)
neon_btn(ctrl_frame, "👬  2P MODE",   lambda: set_mode("double"), NEON_GREEN,  0, 1)
neon_btn(ctrl_frame, "❌  PLAY X",    lambda: set_symbol("X"),    NEON_PINK,   0, 2)
neon_btn(ctrl_frame, "⭕  PLAY O",    lambda: set_symbol("O"),    NEON_ORANGE, 0, 3)

restart_btn = tk.Button(root, text="🔄  RESTART THE CHAOS",
    command=reset,
    font=tkfont.Font(family="Courier", size=13, weight="bold"),
    bg=NEON_YELLOW, fg=BG_DARK,
    activebackground=NEON_ORANGE, activeforeground=BG_DARK,
    relief="flat", cursor="hand2", bd=0, pady=8)
restart_btn.place(x=60, y=545+100-10, width=360, height=44)

# ── CORNER DECORATIONS ───────────────────────────────────────────────────────
def draw_corners():
    bg_canvas.delete("deco")
    size = 36
    for x, y, dx, dy in [(0,0,1,1),(479,0,-1,1),(0,699,1,-1),(479,699,-1,-1)]:
        for i, color in enumerate([NEON_PINK, NEON_CYAN, NEON_YELLOW]):
            off = i * 7
            bg_canvas.create_line(x, y, x+dx*(size-off), y, fill=color, width=2, tags="deco")
            bg_canvas.create_line(x, y, x, y+dy*(size-off), fill=color, width=2, tags="deco")

draw_corners()

root.mainloop()