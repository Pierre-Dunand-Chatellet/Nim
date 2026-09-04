import tkinter as tk
from tkinter import font as tkfont
import random
import os
import sys

# ── Palette : Mode Lecture (Sépia - Doux pour les yeux) ─────────────────────
BG        = "#EADDCD"  # Parchemin très doux (anti-lumière bleue)
PANEL     = "#DCC7B0"  # Parchemin légèrement plus sombre
ACCENT    = "#A66E4E"  # Marron cuir / Terre de Sienne
GOLD      = "#C48B5D"  # Ocre doux
WHITE     = "#3A2E25"  # Marron expresso très foncé (pour la lisibilité du texte)
MUTED     = "#827265"  # Marron grisé (textes secondaires)
BTN_HOVER = "#8B583B"  # Cuir foncé au survol du bouton
GREEN     = "#6B845C"  # Vert mousse (Victoires / Bouton rejouer)


# ── Logique du jeu ──────────────────────────────────────────────────────────
def choix_ordinateur(nb_objet, difficulte):
    # Niveau 1 : Aléatoire, mais finit la partie s'il le peut
    if difficulte == 1:
        if nb_objet <= 3:
            return nb_objet
        return random.randint(1, 3)
    
    # Niveau 2 : Aléatoire au-dessus de 12, puis stratégique en dessous de 13
    elif difficulte == 2:
        if nb_objet < 13:
            reste = nb_objet % 4
            return random.randint(1, 3) if reste == 0 else reste
        return random.randint(1, 3)
    
    # Niveau 3 : Stratégie gagnante dès le début
    else:
        reste = nb_objet % 4
        return random.randint(1, 3) if reste == 0 else reste


# ── Interface graphique ─────────────────────────────────────────────────────
class NimApp(tk.Tk):
    def __init__(self):
        super().__init__()
        

        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "JDN.ico")

            self.iconbitmap(icon_path)
        except Exception as e:
            print("Erreur icône :", e)
            
        self.title("Jeu de Nim")
        self.configure(bg=BG)
        
        # Taille minimale et padding global pour l'écart des fenêtres
        self.minsize(650, 680)
        self.config(padx=30, pady=30)

        # Polices
        self.f_title = tkfont.Font(family="Georgia",  size=28, weight="bold")
        self.f_sub   = tkfont.Font(family="Georgia",  size=14, slant="italic")
        self.f_body  = tkfont.Font(family="Courier",  size=12)
        self.f_btn   = tkfont.Font(family="Courier",  size=12, weight="bold")
        self.f_count = tkfont.Font(family="Courier",  size=45, weight="bold")
        self.f_small = tkfont.Font(family="Courier",  size=10)

        self._build_menu()
        self._center(800, 720)

    # ── Utilitaires ─────────────────────────────────────────────────────────
    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()
        self.unbind("<Configure>")

    def _btn(self, parent, text, cmd, color=ACCENT, hover=BTN_HOVER):
        b = tk.Button(parent, text=text, command=cmd,
                      font=self.f_btn, bg=color, fg=BG,  
                      activebackground=hover, activeforeground=BG,
                      bd=0, padx=25, pady=12, cursor="hand2", relief="flat")
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    # ─────────────────────────────────────────────────────────────────────────
    # ÉCRAN 1 : MENU PRINCIPAL
    # ─────────────────────────────────────────────────────────────────────────
    def _build_menu(self):
        self._clear()
        self.resizable(True, True)

        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="JEU DE NIM", font=self.f_title,
                 bg=BG, fg=ACCENT).pack(pady=(0, 10))
        tk.Label(outer, text="Un duel tactique : celui qui prend le dernier objet gagne !",
                 font=self.f_sub, bg=BG, fg=WHITE, wraplength=550, justify="center").pack(pady=(0, 40))

        # Erreur corrigée ici (caractère parasite supprimé)
        self._btn(outer, "❯  Défier un ami (Local)",
                  lambda: self._start_game("pvp")).pack(fill="x", pady=10)
        self._btn(outer, "❯  Affronter l'ordinateur",
                  self._build_difficulty_menu).pack(fill="x", pady=10)

        tk.Label(outer, text="Configuration : 20 objets · 1 à 3 par tour",
                 font=self.f_small, bg=BG, fg=MUTED).pack(pady=(50, 0))

        self.bind("<Configure>", lambda e: outer.place(relx=0.5, rely=0.5, anchor="center"))

    # ─────────────────────────────────────────────────────────────────────────
    # ÉCRAN 2 : SELECTION DE LA DIFFICULTÉ
    # ─────────────────────────────────────────────────────────────────────────
    def _build_difficulty_menu(self):
        self._clear()

        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="CHOIX DU NIVEAU", font=self.f_title,
                 bg=BG, fg=GOLD).pack(pady=(0, 10))
        tk.Label(outer, text="À quel point votre adversaire doit-il être redoutable ?",
                 font=self.f_sub, bg=BG, fg=WHITE, wraplength=550, justify="center").pack(pady=(0, 35))

        self._btn(outer, "✦  Apprenti (Idéal pour s'entraîner)", 
                  lambda: self._start_game("pvc", 1), color=GREEN, hover="#546B44").pack(fill="x", pady=10)
        
        self._btn(outer, "❖  Stratège (Un défi équilibré)", 
                  lambda: self._start_game("pvc", 2), color=GOLD, hover="#A87343").pack(fill="x", pady=10)
        
        self._btn(outer, "➤  Imbattable (Esprit mathématique)", 
                  lambda: self._start_game("pvc", 3), color=ACCENT, hover=BTN_HOVER).pack(fill="x", pady=10)

        self._btn(outer, "↩  Retour au menu", self._build_menu,
                  color=MUTED, hover="#6A5A4E").pack(fill="x", pady=(35, 0))

        self.bind("<Configure>", lambda e: outer.place(relx=0.5, rely=0.5, anchor="center"))

    # ─────────────────────────────────────────────────────────────────────────
    # ÉCRAN DE JEU
    # ─────────────────────────────────────────────────────────────────────────
    def _start_game(self, mode, difficulte=None):
        self._clear()

        self.mode       = mode
        self.difficulte = difficulte
        self.nb_objet   = 20
        self.game_over  = False
        self.joueur     = 1  # Le Joueur 1 ouvre toujours la partie

        # Attribution aléatoire des rôles (Joueur 1 ou Joueur 2)
        if mode == "pvc":
            if random.choice([True, False]):
                self.humain     = 1
                self.ordinateur = 2
            else:
                self.humain     = 2
                self.ordinateur = 1
        else:
            self.ordinateur = None
            self.humain     = None

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)   
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)
        self.columnconfigure(0, weight=1)

        # ── En-tête ───────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=PANEL, pady=16)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(0, weight=1)
        tk.Label(hdr, text="JEU DE NIM", font=self.f_title,
                 bg=PANEL, fg=ACCENT).grid(row=0, column=0)
        
        if mode == "pvc":
            niveaux = {1: "Apprenti", 2: "Stratège", 3: "Imbattable"}
            info = f"Adversaire : {niveaux[self.difficulte]} (Joueur {self.ordinateur})   |   Vous : Joueur {self.humain}"
            tk.Label(hdr, text=info, font=self.f_small,
                     bg=PANEL, fg=WHITE).grid(row=1, column=0)
        else:
            tk.Label(hdr, text="Mode 2 joueurs en local", font=self.f_small,
                     bg=PANEL, fg=WHITE).grid(row=1, column=0)

        # ── Tour + compteur ───────────────────────────────────────────────────
        info_frame = tk.Frame(self, bg=BG)
        info_frame.grid(row=1, column=0, pady=(20, 0))
        self.lbl_tour  = tk.Label(info_frame, font=self.f_sub,  bg=BG, fg=GOLD)
        self.lbl_tour.pack()
        self.lbl_count = tk.Label(info_frame, font=self.f_count, bg=BG, fg=WHITE)
        self.lbl_count.pack()
        tk.Label(info_frame, text="objets restants sur la table", font=self.f_small,
                 bg=BG, fg=MUTED).pack()

        # ── Canvas responsive ─────────────────────────────────────────────────
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=10, pady=15)

        # ── Log / Journal de texte (Phrases d'ambiance intégrées) ─────────────
        if mode == "pvc":
            if self.humain == 1:
                msg_debut = "La partie commence ! Vous êtes le Joueur 1, c'est à vous d'ouvrir le bal."
            else:
                msg_debut = "La partie commence ! L'ordinateur est le Joueur 1, il prend la main en premier."
        else:
            msg_debut = "La partie commence. Joueur 1, à vous l'honneur !"

        self.lbl_log = tk.Label(self, text=msg_debut, font=self.f_body, bg=BG, fg=WHITE,
                                wraplength=650)
        self.lbl_log.grid(row=3, column=0, pady=(0, 10))

        # ── Boutons 1 / 2 / 3 ────────────────────────────────────────────────
        btn_frame_game = tk.Frame(self, bg=BG)
        btn_frame_game.grid(row=4, column=0, pady=10)
        tk.Label(btn_frame_game, text="Prendre :", font=self.f_body,
                 bg=BG, fg=WHITE).grid(row=0, column=0, padx=15)
        self.btns = []
        for k in (1, 2, 3):
            b = self._btn(btn_frame_game, f"{k}  objets" if k > 1 else f"{k}  objet", lambda v=k: self._human_play(v))
            b.grid(row=0, column=k, padx=8)
            self.btns.append(b)

        # ── Retour menu ───────────────────────────────────────────────────────
        self._btn(self, "↩  Quitter la partie", self._build_menu,
                  color=MUTED, hover="#6A5A4E").grid(row=5, column=0, pady=(10, 5))

        self.bind("<Configure>", lambda e: self.after_idle(self._draw_canvas))
        self._refresh()

        # Si l'ordinateur est le Joueur 1, il lance automatiquement son coup initial
        if mode == "pvc" and self.joueur == self.ordinateur:
            self.after(1200, self._computer_play)

    # ─────────────────────────────────────────────────────────────────────────
    # DESSIN DU CANVAS
    # ─────────────────────────────────────────────────────────────────────────
    def _draw_canvas(self):
        self.update_idletasks()
        c  = self.canvas
        n  = self.nb_objet
        cw = c.winfo_width()
        ch = c.winfo_height()

        if cw < 10 or ch < 10:
            return

        c.delete("all")

        pad_x  = 20
        bar_h  = 24
        bar_y  = 8
        usable = cw - 2 * pad_x

        # Barre de progression
        c.create_rectangle(pad_x, bar_y, pad_x + usable, bar_y + bar_h,
                           fill=PANEL, outline="")
        filled = int(usable * n / 20)
        if filled:
            c.create_rectangle(pad_x, bar_y, pad_x + filled, bar_y + bar_h,
                               fill=ACCENT, outline="")
        c.create_text(cw // 2, bar_y + bar_h // 2,
                      text=f"{n} / 20", fill=BG, font=self.f_small)

        # Grille de ronds
        cols      = 10
        rows      = 2
        gap       = 10
        grid_top  = bar_y + bar_h + 20
        grid_h    = ch - grid_top - 8

        r_by_w = (usable - (cols - 1) * gap) // (cols * 2)
        r_by_h = (grid_h - (rows - 1) * gap) // (rows * 2)
        r      = max(8, min(r_by_w, r_by_h, 28))

        grid_w      = cols * 2 * r + (cols - 1) * gap
        grid_real_h = rows * 2 * r + (rows - 1) * gap

        origin_x = pad_x + (usable    - grid_w)      // 2
        origin_y = grid_top + (grid_h - grid_real_h) // 2

        for i in range(20):
            col = i % cols
            row = i // cols
            cx = origin_x + col * (2 * r + gap) + r
            cy = origin_y + row * (2 * r + gap) + r
            color = ACCENT if i < n else PANEL
            c.create_oval(cx - r, cy - r, cx + r, cy + r,
                          fill=color, outline="")

    # ─────────────────────────────────────────────────────────────────────────
    # RAFRAÎCHISSEMENT
    # ─────────────────────────────────────────────────────────────────────────
    def _refresh(self):
        self.lbl_count.config(text=str(self.nb_objet))

        if not self.game_over:
            if self.mode == "pvc" and self.joueur == self.ordinateur:
                who = "L'ordinateur analyse la table..."
            elif self.mode == "pvc":
                who = "C'est votre tour, faites le bon choix !"
            else:
                who = f"À toi de jouer, Joueur {self.joueur} !"
            self.lbl_tour.config(text=who)

        self.after_idle(self._draw_canvas)

        is_human = (self.mode == "pvp") or \
                   (self.mode == "pvc" and self.joueur == self.humain)
        state = "normal" if (is_human and not self.game_over) else "disabled"
        for b in self.btns:
            b.config(state=state)

    # ─────────────────────────────────────────────────────────────────────────
    # COUPS
    # ─────────────────────────────────────────────────────────────────────────
    def _human_play(self, n):
        if n > self.nb_objet:
            self.lbl_log.config(
                text=f"Impossible ! Il ne reste que {self.nb_objet} objet(s).", fg=GOLD)
            return
        
        accord = "objet" if n == 1 else "objets"
        who = "Vous avez pris" if self.mode == "pvc" else f"Le Joueur {self.joueur} a pris"
        self.lbl_log.config(text=f"{who} {n} {accord}.", fg=WHITE)
        self._apply_move(n)

    def _computer_play(self):
        if self.game_over:
            return
        n = min(choix_ordinateur(self.nb_objet, self.difficulte), self.nb_objet)
        accord = "objet" if n == 1 else "objets"
        self.lbl_log.config(text=f"L'ordinateur a retiré {n} {accord}.", fg=WHITE)
        self._apply_move(n)

    def _apply_move(self, n):
        self.nb_objet -= n
        if self.nb_objet == 0:
            self._refresh()
            self._end_game()
            return
        self.joueur = 2 if self.joueur == 1 else 1
        self._refresh()
        if self.mode == "pvc" and self.joueur == self.ordinateur:
            self.after(900, self._computer_play)

    # ─────────────────────────────────────────────────────────────────────────
    # FIN DE PARTIE
    # ─────────────────────────────────────────────────────────────────────────
    def _end_game(self):
        self.game_over = True

        if self.mode == "pvp":
            msg = f"✦ Victoire éclatante du Joueur {self.joueur} ! ✦"
            btn_text = "❯  Match retour !"
        elif self.joueur == self.humain:
            msg = "✦ Félicitations, vous avez battu l'ordinateur ! ✦"
            btn_text = "❯  Rejouez contre lui"
        else:
            msg = "Dommage... L'ordinateur a été plus malin cette fois."
            btn_text = "❯  Prendre ma revanche"

        self.lbl_tour.config(text="Partie terminée", fg=MUTED)
        self.lbl_log.config(
            text=msg, fg=WHITE,
            font=tkfont.Font(family="Courier", size=14, weight="bold"))

        for b in self.btns:
            b.config(state="disabled")

        self._btn(self, btn_text,
                  lambda: self._start_game(self.mode, self.difficulte),
                  color=GREEN, hover="#546B44").grid(row=6, column=0, pady=(10, 0))


if __name__ == "__main__":
    app = NimApp()
    app.mainloop()